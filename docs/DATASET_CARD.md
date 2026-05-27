# 数据集卡片：Sci-Evo-LabTrace

## 数据类型

Sci-Evo 科学演化数据。

## 覆盖领域

蛋白设计、酶工程、合成生物学、生物催化、生物发光、抗体工程、蛋白语言模型、工业生物制造和酵母分泌工程。

## 预期用途

- 训练 AI4S 智能体理解真实科研轨迹。
- 评测模型在科研过程中的下一步决策能力。
- 研究计算设计、湿实验验证和优化循环中的工具调用推理。
- 构建可追溯的科研过程知识库。

## 数据格式

JSON Lines。每一行是一条完整科学演化 case。

## 数据集页面

- OpenDataLab：https://opendatalab.com/medimedi/Sci-Evo-LabTrace
- GitHub：https://github.com/medisean/Sci-Evo-LabTrace-Open

## 标注等级

本数据集包含 25 条 gold curated case、169 个科研轨迹步骤和 363 条自动生成评测任务，并可继续扩展 silver 自动抽取样本。

## 来源与溯源

外部 seed case 来自项目初始结构化 JSON；新增 case 来自开放获取论文和候选来源队列，并在数据中记录来源、许可状态和证据字段。仓库包含 4 篇开放论文 PDF 和脱敏 MinerU 结构化解析产物；其余扩展 case 保留 DOI、来源 URL、PDF 指针或文献级 evidence，便于继续复核。

## 质量信号

- 必须通过 schema 校验。
- 每个轨迹步骤必须具备证据指针。
- 显式记录 `curation_level`。
- 显式记录来源许可状态与是否需要许可复核。
- 提供评测任务和完整性检查。

## 局限性

本项目已经具备可复用的基础完整度。部分扩展 case 仍是文献级 evidence 与许可状态记录，后续可继续沿 `reports/VETTED_SOURCE_QUEUE.md` 为更多 case 补齐 MinerU 本地解析产物、页级 evidence 和人工数值核对。

## 扩展入口

- 来源筛选队列：`reports/VETTED_SOURCE_QUEUE.md`
- 质量报告：`reports/QUALITY_REPORT.md`
- 标注规范：`docs/ANNOTATION_GUIDELINES.md`
- 深度审计：`reports/CASE_DEPTH_AUDIT.md`
- 下一步安全操作：只下载许可信息明确允许本地处理的 PDF，并通过 MinerU 解析后再人工复核成 gold case。
