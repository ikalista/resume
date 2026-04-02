## 企业级 RAG 系统与 LLM 微调（第2-3年）

**背景**：公司400+员工存在财务、人力、helpdesk等多业务线智能问答需求，系统冷启动仅80篇文档，文档格式杂乱（Word/PPT/PDF/Excel/扫描件），高频计算类问题（个税、薪资核算）大模型直接回答准确率仅23%。

**任务**：主导整体架构设计与场景化模型微调，覆盖文档预处理、召回优化、LLM微调全链路。

**行动**：
- 设计不chunk架构，搭建多格式文档预处理管线（python-docx/python-pptx/pdfplumber/QwenVL，兼用markitdown），将Word、PPT、PDF、Excel统一转成Markdown+LaTeX标准中间文件，附带来源、更新时间等元数据JSON；复杂PPT整页送入QwenVL生成结构化Markdown，扫描件PDF用QwenVL OCR；单卡A10吞吐约200篇/小时
- 构建BM25/Embedding/关键词多路召回重排机制，建立召回评测集
- 针对个税、薪资核算与入职流程高频计算任务，用DeepSeek结合正则表达式生成思维链数据集，基于LLaMA-Factory SFT微调，再用verl框架做GRPO强化学习优化

**结果**：
- 1@Pass从45%提升至64%（+19pp），3@Pass从45%提升至71%（+26pp），ROUGE从0.34提升至0.58
- 个税/薪资类问题准确率从 23% 提升至 80%
- 预处理管线沉淀为通用组件，支撑后续需求文档助手扩展至上万篇文档
