- 项目地址：[Issues · InternScience/MLEvolve](https://github.com/InternScience/MLEvolve)
- 论文地址：[AutoMLGen: Navigating Fine-Grained Optimization for Coding Agents](https://arxiv.org/html/2510.08511v1)

整体流程：

1. 流程与 prompt（已写入 README）
代码怎么走（一次 run）：
入口 run.py：加载 config、任务描述、cold-start；prep_agent_workspace；建 Journal、AgentSearch、Interpreter。
Phase 1：按 initial_drafts 次数，只生成不执行 → draft_agent 拼 prompt（任务 + data preview + 可选 memory），用 LLM generate() 得到 plan+code，节点先不执行。
Phase 2：线程池里先执行这些 draft，再循环 step_task(上一个节点) 直到步数用完。每一步：
node_selection：按 UCT 从 root 往下选要扩展的节点（探索系数随步数衰减）。
Agent 分支（_run_single_step）：
root 且未满 draft 数 → draft_agent
root 且 draft 已满 → aggregation_agent（多分支经验汇总）
当前节点是 bug → debug_agent
当前节点正常但停滞 → evolution_agent 或 fusion_agent
当前节点正常且未停滞 → improve_agent
生成代码后走 code_review_agent，再执行、result_parse_agent 解析指标/是否 bug，然后 journal.append、save_run。
用到的 prompt 来源：
指标方向：result_parse_agent 里一次 prompt（任务描述 → lower_is_better + 理由）。
Draft：draft_agent = 任务 + 说明（格式、防泄漏、环境、coldstart）+ 可选 memory；stepwise 会再经过 planner + coder（如 diff_coder）。
Improve / evolution / fusion：各自 agent = 任务 + 当前方案(plan/code/输出) + 分支历史或参考方案 + 通用 instructions。
Debug：debug_agent = 任务 + 出错代码 + 执行输出 + analysis + instructions。
Code review：code_review_agent = validation 模板 + impl guideline。
公共模块：agents/prompts/（shared、impl_guideline、environment、validation_template_prompts 等）。
