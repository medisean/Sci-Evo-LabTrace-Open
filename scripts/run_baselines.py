#!/usr/bin/env python3
"""Run simple reproducible baselines for Sci-Evo evaluation tasks."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "data" / "processed" / "scievo_eval_tasks.jsonl"
OUT_JSON = ROOT / "data" / "processed" / "baseline_results.json"
OUT_MD = ROOT / "reports" / "BASELINE_RESULTS.md"


def load_tasks(path: Path) -> list[dict]:
    tasks = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    return tasks


def tool_name(value: object) -> str:
    if isinstance(value, dict):
        return str(value.get("name", ""))
    return str(value or "")


def step_index(task: dict) -> int | None:
    parts = task["task_id"].split("-")
    if task["task_type"] == "success_metric_extraction":
        return None
    try:
        return int(parts[-1])
    except ValueError:
        return None


def answer_fields(task: dict) -> dict:
    answer = task["answer"]
    if task["task_type"] == "next_step_decision":
        return {
            "phase": answer.get("phase", ""),
            "action": answer.get("action", ""),
            "tool": tool_name(answer.get("tool", "")),
        }
    if task["task_type"] == "gap_to_decision_reasoning":
        return {
            "phase": answer.get("decision", ""),
            "action": answer.get("action", ""),
            "tool": tool_name(answer.get("tool", "")),
        }
    return {}


def most_common(counter: Counter[str]) -> str:
    if not counter:
        return ""
    return counter.most_common(1)[0][0]


def leave_one_case_counters(tasks: list[dict], key_fn: Callable[[dict], object] | None = None) -> dict[str, dict[object, dict[str, Counter[str]]]]:
    all_counts: dict[object, dict[str, Counter[str]]] = defaultdict(lambda: defaultdict(Counter))
    by_case: dict[str, dict[object, dict[str, Counter[str]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(Counter)))
    for task in tasks:
        if task["task_type"] == "success_metric_extraction":
            continue
        key = key_fn(task) if key_fn else "global"
        fields = answer_fields(task)
        for field, value in fields.items():
            all_counts[key][field][value] += 1
            by_case[task["case_id"]][key][field][value] += 1

    result: dict[str, dict[object, dict[str, Counter[str]]]] = {}
    for task in tasks:
        case_id = task["case_id"]
        if case_id in result:
            continue
        result[case_id] = {}
        for key, field_counts in all_counts.items():
            result[case_id][key] = {}
            for field, counter in field_counts.items():
                adjusted = counter.copy()
                for value, count in by_case[case_id].get(key, {}).get(field, {}).items():
                    adjusted[value] -= count
                    if adjusted[value] <= 0:
                        del adjusted[value]
                result[case_id][key][field] = adjusted
    return result


def predict_majority(task: dict, counters: dict[str, dict[object, dict[str, Counter[str]]]]) -> dict:
    case_counters = counters[task["case_id"]]["global"]
    return {field: most_common(counter) for field, counter in case_counters.items()}


def predict_step_prior(task: dict, counters: dict[str, dict[object, dict[str, Counter[str]]]]) -> dict:
    idx = step_index(task)
    case_counters = counters[task["case_id"]].get(idx, {})
    return {field: most_common(counter) for field, counter in case_counters.items()}


def predict_last_step_copy(task: dict) -> dict:
    if task["task_type"] != "next_step_decision":
        return {}
    previous = task.get("input", {}).get("previous_steps", [])
    if not previous:
        return {}
    last = previous[-1]
    return {
        "phase": last.get("phase", ""),
        "action": last.get("action", ""),
        "tool": tool_name(last.get("tool", "")),
    }


def evaluate(tasks: list[dict], name: str, predictor: Callable[[dict], dict], task_type: str) -> dict:
    selected = [task for task in tasks if task["task_type"] == task_type]
    totals = Counter()
    correct = Counter()
    all_three = 0
    answered = 0
    for task in selected:
        gold = answer_fields(task)
        pred = predictor(task)
        if not pred:
            continue
        answered += 1
        matched_all = True
        for field in ["phase", "action", "tool"]:
            totals[field] += 1
            if pred.get(field, "") == gold.get(field, ""):
                correct[field] += 1
            else:
                matched_all = False
        if matched_all:
            all_three += 1
    return {
        "baseline": name,
        "task_type": task_type,
        "task_count": len(selected),
        "answered_count": answered,
        "phase_accuracy": round(correct["phase"] / totals["phase"], 4) if totals["phase"] else None,
        "action_accuracy": round(correct["action"] / totals["action"], 4) if totals["action"] else None,
        "tool_accuracy": round(correct["tool"] / totals["tool"], 4) if totals["tool"] else None,
        "all_three_accuracy": round(all_three / answered, 4) if answered else None,
    }


def pct(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value * 100:.1f}%"


def write_report(results: list[dict], tasks: list[dict]) -> None:
    task_counts = Counter(task["task_type"] for task in tasks)
    lines = [
        "# Baseline 结果表",
        "",
        "本报告记录 Sci-Evo 结构化评测任务上的轻量可复现 baseline。baseline 刻意保持简单，用于帮助理解任务难度和字段分布，不代表模型级性能。",
        "",
        "## 数据集",
        "",
        f"- 评测任务总数：{len(tasks)}",
        f"- `next_step_decision`: {task_counts['next_step_decision']}",
        f"- `gap_to_decision_reasoning`: {task_counts['gap_to_decision_reasoning']}",
        f"- `success_metric_extraction`: {task_counts['success_metric_extraction']}",
        "",
        "## Baseline 定义",
        "",
        "- `majority_prior_loco`：leave-one-case-out 的全局多数类先验，只预测 phase、action 和 tool。",
        "- `step_index_prior_loco`：leave-one-case-out 的 step-index 条件多数类先验，只预测 phase、action 和 tool。",
        "- `last_step_copy`：复制上一轨迹步骤，仅适用于带历史上下文的 next-step 任务。",
        "",
        "## 字段级结构化准确率",
        "",
        "下表只评估结构化头字段 `phase/action/tool`，不评估 `parameters` 与 `observation` 的完整生成质量；完整答案仍需要模型生成或人工/LLM 语义评测。",
        "",
        "| Baseline | 任务类型 | 已回答/总数 | Phase | Action | Tool | 三字段全对 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in results:
        lines.append(
            "| {baseline} | `{task_type}` | {answered_count}/{task_count} | {phase} | {action} | {tool} | {all_three} |".format(
                baseline=row["baseline"],
                task_type=row["task_type"],
                answered_count=row["answered_count"],
                task_count=row["task_count"],
                phase=pct(row["phase_accuracy"]),
                action=pct(row["action_accuracy"]),
                tool=pct(row["tool_accuracy"]),
                all_three=pct(row["all_three_accuracy"]),
            )
        )
    lines.extend(
        [
            "",
            "## Success Metric Extraction",
            "",
            "`success_metric_extraction` 是开放式结构化抽取任务，需要抽取验证方法、成功指标和最终结论。可靠评分应结合字段匹配、数值核对与语义评估；本报告只记录任务数量，不编造脆弱的字符串匹配分数。",
            "",
            "## 结果解读",
            "",
            "`step_index_prior_loco` 明显强于全局多数类先验，说明当前扩展 gold case 使用了稳定的 Sci-Evo 决策骨架。它只能预测结构化头字段，不能生成科学参数、观测结果或证据解释。真正有能力的模型应利用科研目标、历史观察、工具上下文和 evidence 指针，在完整答案质量上超过这些弱基线。",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    tasks = load_tasks(TASKS)
    majority_counters = leave_one_case_counters(tasks)
    step_counters = leave_one_case_counters(tasks, key_fn=step_index)
    results = []
    for task_type in ["next_step_decision", "gap_to_decision_reasoning"]:
        results.append(
            evaluate(
                tasks,
                "majority_prior_loco",
                lambda task: predict_majority(task, majority_counters),
                task_type,
            )
        )
        results.append(
            evaluate(
                tasks,
                "step_index_prior_loco",
                lambda task: predict_step_prior(task, step_counters),
                task_type,
            )
        )
    results.append(evaluate(tasks, "last_step_copy", predict_last_step_copy, "next_step_decision"))
    OUT_JSON.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(results, tasks)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
