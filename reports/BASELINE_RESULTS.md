# Baseline 结果表

本报告记录 Sci-Evo 结构化评测任务上的轻量可复现 baseline。baseline 刻意保持简单，用于帮助理解任务难度和字段分布，不代表模型级性能。

## 数据集

- 评测任务总数：363
- `next_step_decision`: 169
- `gap_to_decision_reasoning`: 169
- `success_metric_extraction`: 25

## Baseline 定义

- `majority_prior_loco`：leave-one-case-out 的全局多数类先验，只预测 phase、action 和 tool。
- `step_index_prior_loco`：leave-one-case-out 的 step-index 条件多数类先验，只预测 phase、action 和 tool。
- `last_step_copy`：复制上一轨迹步骤，仅适用于带历史上下文的 next-step 任务。

## 字段级结构化准确率

下表只评估结构化头字段 `phase/action/tool`，不评估 `parameters` 与 `observation` 的完整生成质量；完整答案仍需要模型生成或人工/LLM 语义评测。

| Baseline | 任务类型 | 已回答/总数 | Phase | Action | Tool | 三字段全对 |
|---|---:|---:|---:|---:|---:|---:|
| majority_prior_loco | `next_step_decision` | 169/169 | 11.8% | 39.1% | 11.8% | 0.0% |
| step_index_prior_loco | `next_step_decision` | 169/169 | 82.8% | 84.0% | 82.8% | 82.8% |
| majority_prior_loco | `gap_to_decision_reasoning` | 169/169 | 11.8% | 39.1% | 11.8% | 0.0% |
| step_index_prior_loco | `gap_to_decision_reasoning` | 169/169 | 82.8% | 84.0% | 82.8% | 82.8% |
| last_step_copy | `next_step_decision` | 144/169 | 0.0% | 4.9% | 0.0% | 0.0% |

## Success Metric Extraction

`success_metric_extraction` 是开放式结构化抽取任务，需要抽取验证方法、成功指标和最终结论。可靠评分应结合字段匹配、数值核对与语义评估；本报告只记录任务数量，不编造脆弱的字符串匹配分数。

## 结果解读

`step_index_prior_loco` 明显强于全局多数类先验，说明当前扩展 gold case 使用了稳定的 Sci-Evo 决策骨架。它只能预测结构化头字段，不能生成科学参数、观测结果或证据解释。真正有能力的模型应利用科研目标、历史观察、工具上下文和 evidence 指针，在完整答案质量上超过这些弱基线。
