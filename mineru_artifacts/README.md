# MinerU Artifacts

本目录包含 4 篇开放许可论文的脱敏 MinerU 结构化解析产物，用于复核 evidence 字段与原文之间的对应关系。

为降低开放平台审核风险，解析产物中的通讯作者邮箱、correspondence 字段等作者联系信息已脱敏；`model.json` 这类可能携带大段内嵌图片载荷的原始模型输出不进入开放版本。需要复现完整解析时，可使用 `scripts/mineru_parse.py` 从 `source_papers/` 中的开放许可 PDF 重新生成。

每个 case 子目录包含：

- `full.md`: MinerU 转换后的 Markdown 文本。
- `content_list.json`: 页面与块级内容列表。
- `content_list_v2.json`: 结构化内容列表 v2。
- `layout.json`: 页面布局信息。

不包含下载 zip、图片目录、原始模型输出或本地凭据。
