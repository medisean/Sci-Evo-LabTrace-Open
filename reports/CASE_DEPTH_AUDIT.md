# Gold Case 深度审计

## 总体结论

本数据集包含 25 条 gold case、169 个科研轨迹步骤和 363 条自动生成评测任务。主题集中在 AI/ML 驱动的蛋白与酶工程，边界清晰，适合以“高质量科研演化轨迹”而不是“大而散的论文抽取集”作为数据集定位。

25 条 gold case 均已绑定来源证据。仓库包含 4 篇开放许可论文的 PDF 与结构化解析产物，便于复核来源、页面和字段；外部 seed case 和扩展 case 保留结构化字段、DOI/URL/PDF 指针与许可状态。

## Case 1：从头设计人工荧光素酶

- Case ID：`SELT-PROT-0001`
- 子方向：从头蛋白设计、酶工程、生物发光、合成生物学
- 轨迹深度：7 步
- 核心闭环：scaffold 生成 → 活性位点安装 → 序列优化 → 大肠杆菌筛选 → 新底物扩展 → 位点饱和突变 → 哺乳动物细胞验证
- 质量亮点：干实验与湿实验交替清晰，最终指标包含分子量、热稳定性、催化效率和底物特异性。
- 主要风险：作为外部 seed case，后续可替换为许可更清晰、来源材料更完整的开放案例；结构化字段已保留证据指针。

## Case 2：机器学习辅助组合文库设计

- Case ID：`SELT-PROT-0002`
- 子方向：机器学习文库设计、酶工程、生物催化
- 轨迹深度：5 步
- 核心闭环：结构引导位点选择 → MODIFY 文库设计 → 双反应实验筛选 → 命中体排序 → 分子动力学机制解释
- 质量亮点：体现了模型如何平衡 fitness 与 diversity，并通过实验筛选验证文库质量。
- 主要风险：应持续核对论文版本、PDF 页面和 evidence 页码的一致性。

## Case 3：定向进化复盘与 ensemble-based 再设计

- Case ID：`SELT-PROT-0003`
- 子方向：定向进化、结构生物学、计算蛋白设计
- 轨迹深度：5 步
- 核心闭环：进化轨迹审计 → 室温晶体结构测量 → 构象机制推断 → 结构引导突变再设计 → ensemble 模型比较
- 质量亮点：直接记录从实验进化中抽取机制，再反馈到计算设计的过程。
- 主要风险：部分字段保留英文科学原文；这是为了保留论文语义和术语精度。

## Case 4：Pro-PRIME 工业抗碱 VHH 抗体优化

- Case ID：`SELT-PROT-0004`
- 子方向：蛋白语言模型、抗体工程、工业生物制造、极端环境耐受性
- 轨迹深度：6 步
- 核心闭环：工业目标定义 → Pro-PRIME 零样本单点突变筛选 → 45 个单点突变湿实验验证 → 基于单点数据微调模型并设计 20 个多点突变 → epistasis 与 MD 机制分析 → 动态结合容量和工业纯化循环验证
- 质量亮点：这是本数据集中代表性的“AI 设计 - 实验反馈 - 模型微调 - 工业验证”闭环；最终指标包括 65 个突变体、67.7% 抗碱提升、10.02 C Tm 提升、zero-shot 多点预测失败对照和生产线验证。
- 主要风险：eLife 存在 reviewed preprint 与正式文章版本差异，后续维护时应同步 DOI 与页面证据。

## Case 5：alpha-factor 分泌信号工程

- Case ID：`SELT-PROT-0005`
- 子方向：定向进化、酵母分泌、信号肽设计、酶生产
- 轨迹深度：6 步
- 核心闭环：alpha9H2 与 native leader 基准比较 → 13 个单点突变 bottom-up 扫描 → 组合突变与 1600 克隆重组筛选 → top-down 回退简化 → 跨氧化还原酶和水解酶泛化验证 → 86/87 位点 CSM 目标特异调优规则
- 质量亮点：补足了定向进化与工程优化中的轨迹拆解、组合 epistasis、跨目标泛化和可复用规则。
- 主要风险：与 AI/ML 强相关性弱于其他 case，适合作为 directed-evolution baseline。

## 覆盖的子方向

- 从头蛋白/酶设计：`SELT-PROT-0001`
- ML-guided combinatorial library design：`SELT-PROT-0002`
- Directed evolution trajectory audit + ensemble redesign：`SELT-PROT-0003`
- Protein language model + wet-lab feedback + industrial validation：`SELT-PROT-0004`
- Signal peptide / secretion engineering via bottom-up and top-down evolution analysis：`SELT-PROT-0005`
- AI-powered protein engineering strategy synthesis：`SELT-PROT-0006`
- De novo binder and peptide/protein design：`SELT-PROT-0007`、`SELT-PROT-0013`、`SELT-PROT-0023`
- Foundation/protein language model sequence generation and optimization：`SELT-PROT-0008`、`SELT-PROT-0012`、`SELT-PROT-0022`
- Robotic or active-learning protein engineering loops：`SELT-PROT-0009`、`SELT-PROT-0010`
- Antibody design, inverse folding and complex modeling：`SELT-PROT-0011`、`SELT-PROT-0014`、`SELT-PROT-0024`
- Designer enzyme evolution and mechanism-guided re-engineering：`SELT-PROT-0015`、`SELT-PROT-0017`、`SELT-PROT-0021`
- Metabolic engineering, genome-scale design and targeted degradation：`SELT-PROT-0016`、`SELT-PROT-0018`、`SELT-PROT-0019`、`SELT-PROT-0020`、`SELT-PROT-0025`

## 扩展 Case 审计口径

`SELT-PROT-0006` 到 `SELT-PROT-0025` 每条均采用 7 步 Sci-Evo 轨迹：问题定义、输入与约束装配、模型或设计策略、候选优先级排序、实验或基准验证、失败/缺口与机制解释、泛化复用。这个结构可以保证扩展样本不是论文摘要，而是带有决策状态、行动、观察和证据指针的科研过程数据。

扩展 case 的主要价值是扩大同主题覆盖面，让数据集从少量深描样本变成可训练、可评测的科研轨迹集合。主要风险是部分来源尚未在仓库内附带本地 PDF 与 MinerU 页级 artifact，因此这些 case 在 `source.license_status` 中保留复核状态，并避免写入未经逐页确认的精确数值。

## 扩展建议

后续扩展时，建议继续沿同主题增加高证据密度的 gold case，而不是跨到过多无关领域。推荐方向：

- 蛋白语言模型生成 functional protein sequences。
- Bayesian optimization + robotic experiments 的蛋白工程。
- 抗体 CDR inverse folding 设计。
- AI 辅助工业酶耐受性优化。
- de novo peptide/protein binder 设计。
