# Sci-Evo-LabTrace 技术报告

## 1. 数据集简介

Sci-Evo-LabTrace 是面向 Sci-Evo（科学演化数据）方向的数据集，聚焦蛋白设计、酶工程与合成生物学中的科研闭环过程。数据集目标不是记录静态知识问答，而是把真实科研论文中的探索过程整理成可机器读取、可训练、可评测的科学智能体轨迹。

本项目以从头设计人工荧光素酶为种子案例，并扩展到机器学习组合文库设计、定向进化复盘、LLM 辅助工业抗体耐受性优化、酵母分泌信号工程、抗体/肽 binder 设计、蛋白语言模型、主动学习、贝叶斯优化、机器人实验和代谢/酶再工程等子方向。每条 case 都覆盖初始目标定义、关键决策、工具或实验、观测结果、迭代逻辑与最终指标确认。

## 2. 数据集设计目标

本数据集服务于三类 AI4S 能力：

1. 科研过程理解：模型能够理解一个科研目标如何被拆成多步实验与计算决策。
2. 科研决策学习：模型能够在给定研究状态、观察结果或失败信息时预测下一步行动。
3. 科学证据追溯：每个关键字段都应能回溯到原始论文页面、段落、图、表或 MinerU 解析块。

## 3. 数据结构

每条样本对应一个完整科研链路，字段包括：

- `case_id`：稳定样本编号。
- `source`：论文或原始资料来源、许可状态、MinerU 解析产物路径。
- `initial_request`：科研目标、输入信息、用户意图和量化目标。
- `agent_trajectory`：逐步科研轨迹，包括思考、行动、工具、参数、观察、结果类型和证据。
- `success_verification`：最终验证方法、指标和结论。
- `quality`：人工/自动标注等级、证据覆盖率和许可复核状态。

Schema 文件位于 `schemas/scievo_case.schema.json`。处理后的 JSONL 文件位于 `data/processed/scievo_gold.jsonl`。

## 4. MinerU 使用方式

本项目使用 MinerU API 作为科学文献解析工具链的核心组件。本仓库内公开 4 条开放论文 case 的脱敏结构化解析产物：

- `mineru_artifacts/SELT-PROT-0002/full.md`
- `mineru_artifacts/SELT-PROT-0003/full.md`
- `mineru_artifacts/SELT-PROT-0004/full.md`
- `mineru_artifacts/SELT-PROT-0005/full.md`
- 对应 `content_list.json`、`content_list_v2.json` 和 `layout.json`。

开放版本已移除通讯作者联系信息，并不包含可能携带大段内嵌图片载荷的 `model.json` 原始模型输出。需要完整复现时，可从 `source_papers/` 中的开放许可 PDF 重新运行解析流程。

`SELT-PROT-0001` 是外部 seed case；数据集中保留结构化字段和页面级证据指针，但不声明仓库内 MinerU artifact 路径。

标准流程如下：

1. 将每篇 PDF 上传至 MinerU API 或使用 MinerU 开源项目离线解析。
2. 获取 Markdown、content list JSON、图片、表格和公式等结构化结果。
3. 把抽取出的 Sci-Evo 字段与 MinerU 输出中的页面、段落、图表块建立映射。
4. 在最终数据集中通过 `evidence` 字段保留 `source_doc`、`page`、`locator` 和 `mineru_block_id`。

本仓库提供 `scripts/mineru_parse.py`，用于调用 MinerU API 批量解析 PDF。该脚本从环境变量 `MINERU_API_TOKEN` 或本地 `mineru-api-token.txt` 读取 token，不会把 token 写入输出文件。

## 5. 数据构建流程

本项目最小完整流程：

```bash
python3 scripts/build_dataset.py
python3 scripts/validate_dataset.py data/processed/scievo_gold.jsonl
python3 scripts/build_eval_tasks.py
python3 scripts/make_quality_report.py
```

后续扩展流程：

1. 收集开放许可论文或允许复用的原始 PDF。
2. 使用 MinerU 生成结构化解析产物。
3. 从论文叙事中抽取科研演化链路。
4. 通过 schema validator 检查字段完整性。
5. 通过人工复核确认关键指标、工具、参数、失败/修正链路和证据链接。

为支持后续扩展，仓库提供 `scripts/collect_openalex_candidates.py`，用于收集开放获取论文的候选元数据；该脚本只保存题名、DOI、开放获取状态、许可信息和 OA 链接，不下载全文。评测任务由 `scripts/build_eval_tasks.py` 从 gold case 自动生成。

仓库同时提供 `scripts/run_baselines.py`，用于在结构化评测任务上生成可复现 baseline 结果。当前 baseline 只评估 `phase/action/tool` 等头字段，不替代完整科学答案的语义评测。

## 6. 质量控制

本项目的质量控制分为四层：

- Schema 完整性：所有样本必须通过 `scripts/validate_dataset.py`。
- 证据覆盖：每个轨迹步骤必须至少有一个来源证据。
- 科学一致性：关键指标、工具名、实验结果不得脱离原文证据。
- 许可合规：每个来源记录 `license_status`，公开发布前必须完成许可复核。

此外，仓库提供了多个质量控制文件或自动检查：

- `scripts/vet_candidate_sources.py`：把 OpenAlex 候选元数据转换为“可安全本地处理 / 需人工复核 / 暂缓处理”的来源队列，避免在许可不清晰时直接抓取全文。
- `scripts/run_baselines.py`：生成 next-step 与 gap-reasoning 任务的字段级 baseline 结果表。
- `docs/ANNOTATION_GUIDELINES.md`：定义 gold case 标注口径、证据规范与质量分级。
- `reports/CASE_DEPTH_AUDIT.md`：逐条审计现有 gold case 的深度、闭环结构和风险。

## 7. 应用场景

数据集可用于：

- 科学智能体轨迹学习。
- 科研工具调用决策训练。
- 实验失败分析与下一步方案生成。
- 蛋白设计/酶工程领域的 AI4S 推理评测。
- 从论文到结构化科研知识库的自动化抽取任务。

## 8. 项目版本说明

版本 `0.1.0` 是完整底座版本，包含：

- 25 条 gold case（其中 13 条来自明确 CC-BY 来源，4 条附带本地 PDF 与 MinerU 解析产物，其余扩展 case 保留 DOI/PDF 来源指针和许可复核状态）。
- 169 个科研轨迹步骤和 363 条自动生成评测任务。
- 1 套 Sci-Evo case schema。
- 1 个构建脚本。
- 1 个验证脚本。
- 1 个质量报告生成脚本。
- 1 个评测任务生成脚本。
- 1 个 baseline 评测脚本。
- 1 个开放论文候选收集脚本。
- 1 个开放来源许可筛选脚本。
- 1 份标注规范。
- 1 份 gold case 深度审计报告。
- README、技术报告和数据集卡片。

## 9. 质量维度对应

- 数据价值与任务契合度：聚焦 Sci-Evo，而不是静态 QA；每条样本记录真实科研演化链路。
- 数据质量：要求 schema 校验、逐步证据、最终验证字段和人工 gold 标注。
- 工程完整度：提供数据构建、校验、评测任务生成、质量报告和完整性检查。
- MinerU 使用深度：保留脱敏 Markdown、content list、layout 等本地解析产物，并把样本字段映射回页面与块级证据。
- 可扩展与可复核性：通过开放来源候选收集、许可筛选队列和多 case 构建路径支持后续规模化扩展。

## 10. 后续维护建议

本项目已经具备基础完整度，并且 4 条开放论文 case 已补齐本地 MinerU 解析记录；其余扩展 case 已保留来源指针、许可状态与结构化 evidence。后续维护优先顺序是：

1. 对新增开放论文使用 `scripts/mineru_parse.py` 补齐 MinerU 解析产物。
2. 从 `reports/VETTED_SOURCE_QUEUE.md` 继续扩展更多 `permitted_for_local_processing` 的开放论文。
3. 重新生成数据集、评测任务和质量报告。
4. 定期核对 DOI、许可状态和 evidence 页码。
