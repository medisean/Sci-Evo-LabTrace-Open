# Sci-Evo-LabTrace

Sci-Evo-LabTrace 是面向 AI4S 科学智能体的科学演化数据集。本项目聚焦蛋白设计、酶工程与合成生物学中的真实科研闭环：目标提出、计算设计、湿实验验证、失败/差距分析、迭代优化与最终指标确认。

本项目聚焦 Sci-Evo 科研演化数据方向。它不是静态科学问答数据，而是把真实论文和实验叙事整理成可训练、可评测、可追溯的科研过程轨迹。

本仓面向希望参考、复用或扩展 Sci-Evo 科研轨迹数据的人开放，包含数据集、相关代码、开放论文 PDF、脱敏后的 MinerU 结构化解析产物、技术文档和质量报告。

## 数据集链接

- OpenDataLab：https://opendatalab.com/medimedi/Sci-Evo-LabTrace
- GitHub：https://github.com/medisean/Sci-Evo-LabTrace-Open

## 内容结构

- `data/processed/scievo_gold.jsonl`：整理后的 Sci-Evo gold case。
- `data/processed/scievo_eval_tasks.jsonl`：由 gold case 自动生成的评测任务。
- `data/processed/vetted_open_access_sources.jsonl`：开放来源候选论文筛选队列。
- `data/raw/candidate_papers.jsonl`：开放论文候选元数据。
- `data/curated/cases/`：人工整理的 gold case 源文件。
- `source_papers/`：4 篇开放许可论文 PDF。
- `mineru_artifacts/`：4 篇开放论文对应的脱敏 MinerU Markdown、content list 和 layout 产物。
- `schemas/scievo_case.schema.json`：case 字段定义。
- `scripts/build_dataset.py`：构建主 JSONL 数据集。
- `scripts/validate_dataset.py`：校验必填字段与轨迹一致性。
- `scripts/build_eval_tasks.py`：从轨迹数据生成评测任务。
- `scripts/collect_openalex_candidates.py`：收集开放论文候选元数据。
- `scripts/vet_candidate_sources.py`：按许可信息筛选开放论文候选。
- `docs/TECHNICAL_REPORT.md`：技术报告。
- `docs/ANNOTATION_GUIDELINES.md`：标注规范。
- `docs/DATASET_CARD.md`：数据集卡片。
- `reports/QUALITY_REPORT.md`：数据质量报告。
- `reports/BASELINE_RESULTS.md`：结构化评测任务 baseline 结果表。
- `reports/CASE_DEPTH_AUDIT.md`：逐 case 深度审计。
- `reports/MINERU_RUN_REPORT.md`：MinerU 运行报告。

## 数据单元

每条 case 表示一条完整科研链路：

1. 初始科研需求与可量化目标。
2. 多步科研轨迹，包括干实验、湿实验、工具选择、参数、观察结果和迭代逻辑。
3. 成功验证，包括验证方法、关键指标和最终结论。
4. 证据链接，回溯到原始文档页面、段落、图、表或 MinerU 解析块。

## 构建与检查

```bash
python3 scripts/build_dataset.py
python3 scripts/validate_dataset.py data/processed/scievo_gold.jsonl
python3 scripts/build_eval_tasks.py
python3 scripts/vet_candidate_sources.py
python3 scripts/make_quality_report.py
python3 scripts/run_baselines.py
```

本数据集包含 25 条 gold case、169 个科研轨迹步骤和 363 条自动生成评测任务。

## MinerU 使用

25 条 gold case 均已完成结构化标注，并在 `source.license_status` 中记录来源许可状态。仓库包含 4 篇开放许可论文的 PDF 与脱敏后的 MinerU 结构化产物，包括 Markdown、content list JSON 和 layout JSON；其余扩展 case 保留 DOI、来源 URL、PDF 指针或文献级证据，并显式标注是否需要进一步许可复核。`SELT-PROT-0001` 是外部 seed case，仓库保留结构化标注和证据指针，第三方原文再分发前需单独复核许可。

本地重新解析命令：

```bash
python3 scripts/mineru_parse.py source_papers/SELT-PROT-0002.pdf source_papers/SELT-PROT-0003.pdf source_papers/SELT-PROT-0004.pdf source_papers/SELT-PROT-0005.pdf --output-dir mineru_artifacts
```

## 扩展流程

你可以把本仓当作一个模板，用同样的方法整理自己的 Sci-Evo 科研轨迹数据。最小可复用闭环是：确定主题、收集来源、解析文档、整理 case、生成数据集、校验质量。推荐流程如下。

1. 先确定一个边界清晰的科研主题。

   例如蛋白设计、催化剂优化、材料发现、药物发现或实验自动化。主题越聚焦，后续 case 之间越容易形成可比较的科研轨迹，而不是松散的论文集合。

2. 收集候选论文或项目材料。

   如果要从开放论文开始，可以使用 `scripts/collect_openalex_candidates.py` 收集开放获取论文元数据：

   ```bash
   python3 scripts/collect_openalex_candidates.py --limit 25
   ```

   该脚本只保存题名、DOI、开放获取状态、许可信息和 OA 链接，不下载全文。你也可以手动把候选来源整理成 `data/raw/candidate_papers.jsonl`。

3. 筛选来源许可和可用性。

   运行来源筛选脚本：

   ```bash
   python3 scripts/vet_candidate_sources.py
   ```

   筛选结果会写入 `data/processed/vetted_open_access_sources.jsonl` 和 `reports/VETTED_SOURCE_QUEUE.md`。优先选择许可清晰、PDF 可获取、论文中包含明确“目标 - 方法 - 观察 - 迭代 - 验证”链路的材料。

4. 保存原始 PDF 和结构化解析产物。

   将允许复用的 PDF 放到类似 `source_papers/` 的目录。然后用 MinerU 或其它 PDF 解析工具生成 Markdown、content list、layout 等结构化产物。例如：

   ```bash
   python3 scripts/mineru_parse.py source_papers/YOUR-PAPER.pdf --output-dir data/interim/mineru
   ```

   如果你不用 MinerU，也可以替换为其它解析器；关键是后续 `evidence` 字段必须能回到原始文档的页码、段落、图表或结构化块。

5. 人工整理 gold case。

   参考 `data/curated/cases/SELT-PROT-0004.json` 这类较完整的样例，新增自己的 case 文件。若你正在快速扩展一个主题，也可以参考 `SELT-PROT-0006` 到 `SELT-PROT-0025` 的写法：先保留 DOI、来源链接、许可状态和文献级 evidence，再把论文中的目标、约束、模型策略、候选排序、验证、失败解释和复用结论整理成连续步骤。每条 case 至少要包含：

   - `initial_request`：科研目标、输入信息、用户意图和量化目标。
   - `agent_trajectory`：多步科研轨迹，每一步包含 thought、action、tool、parameters、observation 和 evidence。
   - `success_verification`：最终验证方法、指标和结论。
   - `quality`：标注等级、证据覆盖率和许可复核状态。

   标注时不要只摘摘要；要把论文里的科研决策拆成轨迹步骤。一个好步骤通常回答三个问题：当时已经知道什么、还缺什么、为什么下一步要这样做。建议先复制一个已有 case，替换 `case_id`、`source`、`initial_request` 和 `agent_trajectory`，再逐步补齐 evidence 与验证指标。为了减少事实性错误，若尚未完成逐页核对，不要编造精确数值；可以先使用 `reported_in_source`、章节/图表级 locator 或 DOI 级指针，并把复核状态写入 `quality.notes` 或 `source.license_status`。

6. 生成数据集、评测任务和质量报告。

   ```bash
   python3 scripts/build_dataset.py
   python3 scripts/validate_dataset.py data/processed/scievo_gold.jsonl
   python3 scripts/build_eval_tasks.py
   python3 scripts/make_quality_report.py
   ```

   `build_dataset.py` 会把 seed case 和 `data/curated/cases/*.json` 合并成 JSONL；`validate_dataset.py` 检查字段完整性；`build_eval_tasks.py` 会自动生成 next-step decision、gap-to-decision reasoning 和 success-metric extraction 等评测任务。生成文件默认写到 `data/processed/`，质量报告写到 `reports/QUALITY_REPORT.md`。

7. 做人工复核。

   对外开放前建议逐条检查：

   - 每一步 trajectory 是否真的有 evidence 支撑。
   - 指标数值是否与原文一致。
   - `source.license_status` 是否清楚。
   - PDF、图片、表格和解析产物是否允许公开。
   - README、数据卡和质量报告是否能让别人复现你的整理流程。

   对外发布时，建议同时提供 `docs/DATASET_CARD.md`、`docs/ANNOTATION_GUIDELINES.md` 和 `reports/QUALITY_REPORT.md`，方便其他人理解数据边界和质量标准。

   如果你要维护自己的分支，建议保留本仓的目录约定：原始来源放在 `source_papers/` 或等价目录，人工 case 放在 `data/curated/cases/`，脚本生成物放在 `data/processed/`，复核说明放在 `reports/`。这样后续新增 case 时只需要重复“新增来源 -> 新增 case JSON -> 运行构建脚本 -> 校验报告”的循环。

## 项目规模

- 数据构建与校验流程已就绪，本项目生成 25 条 gold case、169 个科研轨迹步骤和 363 条评测任务。
- 已记录 MinerU API 使用过程；4 条开放论文 case 在本仓附带 MinerU 结构化产物，seed case 与扩展 case 保留结构化标注和证据指针。
- 当前包含 13 条明确 CC-BY 来源 case；其余扩展 case 保留 DOI/PDF 来源指针，并在数据中标出许可复核状态。
- 技术报告、数据集卡片、质量报告和 MinerU 报告均已准备。
- 已补充逐 case 深度审计与标注规范，用于说明 gold case 的质量控制口径。
- 本仓库聚焦数据集、代码、论文数据和复核材料。

## 许可说明

原创标注、文档和代码以 CC-BY-4.0 开放。第三方论文 PDF 与解析产物遵循原论文许可；本仓只公开许可明确的开放论文材料。详见 `OPEN_SOURCE_MANIFEST.md` 与 `NOTICE.md`。
