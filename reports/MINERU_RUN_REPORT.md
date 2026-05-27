# MinerU 运行报告

## 概要

- 输入文件：`SELT-PROT-0002.pdf`、`SELT-PROT-0003.pdf`、`SELT-PROT-0004.pdf`、`SELT-PROT-0005.pdf`
- API 模式：MinerU batch API
- 模型版本：`vlm`
- 公式解析：已开启
- 表格解析：已开启
- 最终状态：`done`
- 原始运行输出目录：`data/interim/mineru/`
- 仓库内归一化目录：`mineru_artifacts/`（包含开放许可论文 case）

## 本地生成产物

通用批处理产物：

- `batch_create_response.json`
- `batch_status.json`
- `downloads/*.zip`
- `extracted*/full.md`
- `extracted*/*_content_list.json`
- `extracted*/*_content_list_v2.json`
- `extracted*/layout.json`
- `extracted*/*_model.json`（本地复现产物，开放版本不包含）
- `extracted*/images/`

原始运行记录中的逐 case 归一化产物：

- `SELT-PROT-0002/full.md`
- `SELT-PROT-0002/content_list.json`
- `SELT-PROT-0002/content_list_v2.json`
- `SELT-PROT-0002/layout.json`
- `SELT-PROT-0003/full.md`
- `SELT-PROT-0003/content_list.json`
- `SELT-PROT-0003/content_list_v2.json`
- `SELT-PROT-0003/layout.json`
- `SELT-PROT-0004/full.md`
- `SELT-PROT-0004/content_list.json`
- `SELT-PROT-0004/content_list_v2.json`
- `SELT-PROT-0004/layout.json`
- `SELT-PROT-0005/full.md`
- `SELT-PROT-0005/content_list.json`
- `SELT-PROT-0005/content_list_v2.json`
- `SELT-PROT-0005/layout.json`

仓库内提供的开放论文归一化产物：

- `mineru_artifacts/SELT-PROT-0002/full.md`
- `mineru_artifacts/SELT-PROT-0002/content_list.json`
- `mineru_artifacts/SELT-PROT-0002/content_list_v2.json`
- `mineru_artifacts/SELT-PROT-0002/layout.json`
- `mineru_artifacts/SELT-PROT-0003/full.md`
- `mineru_artifacts/SELT-PROT-0003/content_list.json`
- `mineru_artifacts/SELT-PROT-0003/content_list_v2.json`
- `mineru_artifacts/SELT-PROT-0003/layout.json`
- `mineru_artifacts/SELT-PROT-0004/full.md`
- `mineru_artifacts/SELT-PROT-0004/content_list.json`
- `mineru_artifacts/SELT-PROT-0004/content_list_v2.json`
- `mineru_artifacts/SELT-PROT-0004/layout.json`
- `mineru_artifacts/SELT-PROT-0005/full.md`
- `mineru_artifacts/SELT-PROT-0005/content_list.json`
- `mineru_artifacts/SELT-PROT-0005/content_list_v2.json`
- `mineru_artifacts/SELT-PROT-0005/layout.json`

## 用途说明

MinerU 输出用于三类工作：

1. 将论文 PDF 转换为可检索 Markdown 和 content list，便于定位科研目标、实验步骤和关键指标。
2. 为 `evidence` 字段提供页面、段落、图表和方法位置依据。
3. 支撑人工复核，避免只根据摘要生成 Sci-Evo 轨迹。

## 公开发布说明

仓库包含 4 篇开放许可论文的 PDF 与脱敏 MinerU 结构化解析产物，便于复核 evidence 字段和原文之间的对应关系。开放版本已移除通讯作者联系信息，并不包含下载 zip、图片目录、原始模型输出或本地凭据；外部 seed case 只保留结构化字段和证据指针。
