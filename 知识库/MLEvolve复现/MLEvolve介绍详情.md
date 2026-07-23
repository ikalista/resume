mlebench的特点是什么？
1. 任务多样，有机器学习，有nlp，有图像
2. 数据集偏小
3. 榜单上的所有人都是在做agent层的优化（模型选用gemini/claude opus 4.6等），没有人做模型

我理解的，对嘉银有用的算法的特点是什么？
1. 任务单一，只有机器学习，不大需要考虑nlp和图像（可以纳入考虑）
2. 数据集中等偏大，100万行上千列起步


我们的目标是什么？

mlebench + MLEvolve复现结论：
MLEvolve: https://github.com/InternScience/MLEvolve
我们感谢AIDE和ML-Master对MLE中MCTS开发的贡献，以及InternAgent 1.5对智能记忆机制发展的贡献。我们衷心感谢所有团队对社区的开源贡献。
https://github.com/sjtu-sai-agents/ML-Master
https://github.com/InternScience/InternAgent?tab=readme-ov-file

这是一套

MLEvolve的架构是怎么样的？
**MLEvolve 的“显式数据结构”更像一棵带虚根的搜索树；但它的“信息依赖结构”更像一个 DAG。**
原因是：每个 `SearchNode` 只有一个 `parent`，实现上是树；但 `fusion` 和 `aggregation` 会读取**其他分支**的历史/优秀节点来生成新节点，所以如果把“参考了谁”也画成边，那就是一个**无环有向图**而不是纯树。这个判断是基于代码结构做出的推断：`SearchNode` 只有单父指针；`fusion` 节点仍然挂在一个 `source_node` 下面，但它会把别的 branch 的 top 节点当参考；`aggregation` 更是从多个 branch 的代表解综合出一个新的 `fusion_draft` 分支。([GitHub][1])

---

## 一、它到底在干什么

MLEvolve 不是“让 LLM 一次性写一份 Kaggle 代码”，而是一个**闭环的自动 ML 工程系统**：
**任务描述 → 规划 → 代码生成 → 执行 → 解析指标/校验 → 回传搜索树 → 再规划/改进/调试/融合**。项目页和 README 都把它描述成：基于 progressive MCGS、multi-agent collaboration、experience-driven memory 的长期优化循环，而不是单次试错。([internscience.github.io][2])

它的核心创新，仓库自己总结成三块：

1. **Multi-Mode Planning & Code Generation**：有 base / memory-enhanced planning，以及 single-pass / stepwise / diff patch 三种代码生成路径。([GitHub][3])
2. **Experience-Driven Memory**：每个节点的 plan、code、metric、success/failure 都会入全局记忆；检索是 BM25 + 向量检索 + RRF 融合。([GitHub][3])
3. **Progressive MCGS with Cross-Branch Fusion**：不是只在一条链上改，而是多分支并行搜索，后期做 explore/exploit 切换，并在停滞时做 branch fusion / aggregation。([GitHub][3])

---

## 二、模块级架构

从 repo 目录看，最关键的是这几层：

* `run.py`：总调度器，负责启动搜索、并行执行、保存结果。([GitHub][4])
* `engine/`：搜索核心，包括
  `agent_search.py`、`node_selection.py`、`search_node.py`、`evaluation.py`、`execution.py`、`executor.py`、`solution_manager.py`。([GitHub][5])
* `agents/`：真正“出主意”的 agent，包括
  `draft_agent`、`improve_agent`、`debug_agent`、`evolution_agent`、`fusion_agent`、`aggregation_agent`、`code_review_agent`、`result_parse_agent`。([GitHub][6])
* `agents/planner/`：规划器，含 base planner 和 memory-enhanced two-stage planner。([GitHub][7])
* `agents/coder/`：代码生成器，支持单次生成、stepwise 分步生成、diff patch。([GitHub][8])
* `agents/memory/`：全局记忆和混合检索。([GitHub][9])

你可以把它理解成：

```text
run.py
  └── AgentSearch
        ├── node_selection      # 选哪个节点继续扩展
        ├── agent dispatcher    # draft / improve / debug / evolution / fusion / aggregation
        ├── code_review
        ├── executor            # 真跑代码
        ├── result_parse        # 从输出里解析 metric / buggy / validity
        ├── execution.validate  # submission 是否存在、0分异常等
        ├── evaluation          # reward / backprop / 终止判断
        ├── solution_manager    # best solution / top-k candidates
        └── global_memory       # 记忆检索，反哺 planner / debug
```

这就是它的主架构。([GitHub][10])

---

## 三、主循环是怎么跑的

`run.py` 里实际上是一个两阶段调度：

### 1）Phase 1：先生成若干个初始 draft

配置里默认 `initial_drafts: 3`，总步数默认 `steps: 500`。`run.py` 先从虚根连续生成几份 draft，但**先不执行**，只是拿到代码，目的是增加初始多样性。([GitHub][11])

### 2）Phase 2：并行执行 + 持续扩展

随后它把这些 pending draft 丢进线程池执行，并继续根据已有节点结果不断提交新的 `step_task`。并行度由 `Interpreter.max_parallel_run` 决定，默认可由 `agent.search.parallel_search_num` 控制；执行是通过**子进程**跑 Python 代码，不用 fork 的 multiprocessing，以避免 CUDA 问题。([GitHub][12])

这意味着它不是“串行试一个再试下一个”，而是：

```text
先造多个初始候选
    ↓
并行执行
    ↓
谁先跑完就把结果喂回搜索器
    ↓
搜索器决定下一步扩哪个节点
    ↓
继续并行
```

这就是它能做“budget 内持续优化”的基础。([GitHub][12])

---

## 四、核心对象：SearchNode

`SearchNode` 是整个系统最重要的数据结构。它里面同时装了：

* 代码和 plan
* 执行结果（stdout/stderr、异常、耗时）
* 评估结果（metric、is_buggy、is_valid、analysis）
* 搜索元数据（`stage`、`visits`、`total_reward`、`is_terminal`、`local_best_node`、`continue_improve`、`branch_id` 等）([GitHub][1])

它允许的 `stage` 有：

* `root`
* `draft`
* `fusion_draft`
* `improve`
* `debug`
* `evolution`
* `fusion` ([GitHub][1])

这几个 stage 非常关键，因为 MLEvolve 其实就是在不同 stage 之间切换。

```mermaid
stateDiagram-v2
    
    root --> draft: 初始生成
    root --> fusion_draft: aggregation触发
    
    
```

---

## 五、AgentSearch：谁决定下一步干嘛

`AgentSearch` 是搜索总控。它初始化时会：

* 建一个 `virtual_root`
* 维护所有 branch 的节点列表
* 维护 successful nodes、top candidates、best node
* 判断 metric 是 maximize 还是 minimize
* 按配置决定是否开启 global memory。([GitHub][10])

它的 `_run_single_step()` 里有非常清楚的**动作分派逻辑**：

* **如果当前是 root**：继续 `draft`；如果 root 的常规 draft 数达到上限，就尝试 `aggregation_agent`。
* **如果父节点 buggy / invalid**：走 `debug_agent`。
* **如果父节点没 bug**：

  * 分支停滞时，根据时间和概率，选 `fusion_agent` 或 `evolution_agent`；
  * 否则正常 `improve_agent`。
* 生成代码后还会经过 `code_review_agent`，然后执行、解析结果、校验、更新 best solution。([GitHub][10])

所以你可以把它看成一个**状态机 + 搜索控制器**。

---

## 六、搜索策略：它怎么选节点

### 1）基础仍然是 UCT

`node_selection.py` 里写得很明确：核心选择器是 UCT。`SearchNode.uct_value()` 也是标准
`Q + c * sqrt(ln(N) / n)`。([GitHub][13])

### 2）但 exploration constant 不是固定的

它有 `_piecewise_decay()` 和 `_compute_exploration_constant()`：前期探索强，后期衰减到较低值。配置里默认 `exploration_constant: 1.414`，下界 `0.5`，相位比例 `[0.3, 0.7]`。([GitHub][13])

### 3）还有 time-aware 的 soft switch

`select_with_soft_switch()` 不只靠 UCT。它会根据已经消耗的时间，在“探索模式”和“Top-K exploitation 模式”之间切换；后期更多从全局 top-k 里按 rank 加权抽节点，再继续扩。配置里默认 `explore_switch_start: 0.5`、`explore_switch_end: 0.7`、`min_exploration_weight: 0.2`。([GitHub][13])

### 4）Top-K 还带 branch diversity

`get_top_k_nodes_global()` 会限制同一个 branch 最多入选多少个节点，避免 exploitation 时只盯着一个分支。([GitHub][13])

这就是它所谓 **progressive MCGS** 的“search”味道：
不是简单 DFS/BFS，也不是死板 MCTS，而是**UCT + 时间开关 + top-k exploitation + branch diversity**。([GitHub][3])

---

## 七、生成层：它不是一种 coder，而是三种 mode

### 1）single-pass

最基础的 `plan_and_code_query`，一次吐 plan + code。([GitHub][8])

### 2）stepwise

`draft_agent` 可以调用 `stepwise_plan_and_code_query`，而 `AgentSearch` 初始化里把 `use_stepwise_generation=True`。也就是初始草稿默认偏向**分步生成**。([GitHub][14])

### 3）diff patch

`improve_agent` 明确支持 `use_diff_mode`，配置里默认也是 `True`；也就是后续改进优先走 SEARCH/REPLACE 风格的局部补丁，不行再退回 full rewrite。([GitHub][15])

所以它不是“从头重写一百次”，而更像：

```text
初始阶段：先分步搭几条完整 pipeline
中期阶段：围绕已有成功分支局部改
后期停滞：要么参考分支历史 evolution，要么跨分支 fusion
```

---

## 八、planner 是怎么参与的

`agents/planner` 里分两种：

* `base_planner`：把修改目标约束成几个模块：
  `data_processing_and_feature_engineering`、`model_design`、`training_evaluation`。输出结构化 JSON 计划。([GitHub][16])
* `planner_with_memory`：两阶段规划

  1. 先生成自由文本 initial plan
  2. 再检索相似成功/失败记录，把 plan refine 成结构化 JSON。([GitHub][17])

这个设计很聪明：
先让模型“发散想法”，再用记忆把它“收束到结构化模块修改”，避免 LLM 一上来就被 schema 束缚死。

---

## 九、memory 是怎么接进来的

### 存什么

README 说每个节点会记录 **plan / code / metrics / success-failure labels**。`MemRecord` 里也能看到最小记录包括 `description`、`method`、`label` 等。([GitHub][3])

### 怎么检索

`HybridRetriever` 明确是：

* BM25 keyword retrieval
* 向量检索（FAISS）
* 然后用 RRF 做融合。([GitHub][18])

### 怎么用

* `planner_with_memory` 会先取相似成功和失败记录，再 refine plan。([GitHub][17])
* `debug_agent` 会取相似错误的历史修复经验，拼到调试提示里。([GitHub][19])
* `draft_agent` 也会把 root 下已有尝试整理成 Memory，要求新方案必须有新意。([GitHub][14])

所以它的 memory 不是“聊天记忆”，而是**在线增长的 experiment memory**。

---

## 十、执行、校验、回传奖励

### 执行

`Interpreter` 把每个候选代码写成独立子进程运行，并自动隔离 submission 文件名、模型 checkpoint 文件名，避免并行冲突。([GitHub][20])

### 结果解析

`result_parse_agent` 先判断 metric 方向是 maximize 还是 minimize。([GitHub][21])

### 执行后校验

`execution.validate_executed_node()` 会检查：

* 有没有生成 submission
* maximize 指标却打出 0.0 时，直接视作“根本性失败”，标成 buggy。([GitHub][22])

### 奖励与回传

`evaluation.py` 里：

* buggy 或没 metric 通常给负奖励
* 超过全局 best 会额外奖励
* debug 成功也会奖励
* 若连续改进失败超阈值，会把节点设为 terminal
* 否则继续 improve 链。([GitHub][23])

这一步把“代码执行结果”转成“搜索树上的信用分配”。

---

## 十一、fusion / evolution / aggregation 的区别

这是 MLEvolve 最容易混的地方。

### 1）improve

围绕**当前成功节点**做常规精修。通常是同分支局部改良。([GitHub][15])

### 2）evolution

不是只看当前节点，而是看**当前 branch 的演化轨迹**。如果轨迹太短，就退回普通 improve。([GitHub][24])

### 3）fusion

从**其他分支**里拿 top 节点作为参考，当前节点是 `source_node`，参考节点是 `target_node`。新节点仍然 `parent=source_node`，stage=`fusion`。([GitHub][25])

### 4）aggregation

这是更“重”的操作：不是在某个已有节点上继续改，而是把多个分支的 best solution / trajectory 整理成 `Branch Experiences`，然后在 **virtual_root 下创建一个全新的 `fusion_draft` 分支**。([GitHub][26])

你可以这样理解：

* `improve`：我把自己改好一点
* `evolution`：我参考自己这条支路过去怎么变强
* `fusion`：我借别的支路的长处改我自己
* `aggregation`：我直接从多条支路的经验里重新开一个新方向

---

## 十二、它的“DAG”到底长什么样

### 1）如果只看 `parent` 指针

那就是一棵树：

```text
virtual_root
├── draft(branch 1)
│   ├── improve
│   │   ├── improve
│   │   └── fusion
│   └── debug
├── draft(branch 2)
│   ├── improve
│   └── evolution
└── fusion_draft(branch 3)
    └── improve
```

这点是代码级事实，因为 `SearchNode` 只有一个 `parent`。([GitHub][1])

### 2）如果把“参考关系”也画出来

那就变成 DAG：

```text
branch1.nodeA  ───────────────┐
                              │  (reference edge)
branch2.nodeB  ──reference────┼──> fusion node on branch1
                              │
branch3.best   ───────────────┘

branch1.best ─┐
branch2.best ─┼──> aggregation -> new fusion_draft under root
branch4.best ─┘
```

因为：

* `fusion` 会从别的 branch 取 top nodes 当参考，但生成的新节点还挂在 `source_node` 下。([GitHub][25])
* `aggregation` 会读取多个 branch representative 的 `Branch Experiences`，再在 root 下开新分支。([GitHub][26])

所以我建议你用两个视角看它：

### 视角 A：执行树

用于保存节点、算 UCT、回传 reward。
这是实现层真正的数据结构。([GitHub][1])

### 视角 B：信息 DAG

用于表示“这个节点的想法/方案依赖了哪些历史节点”。
这是更贴近论文/README 里“graph search”措辞的理解。([GitHub][3])

---

## 十三、我给你画一个更完整的 MLEvolve DAG

```text
[Task Description]
        |
        v
[Cold-start Guidance] ----+
        |                 |
        v                 v
   [AgentSearch / Virtual Root] <-----------------------------+
        |                                                     |
        | select_with_soft_switch                             |
        v                                                     |
  +-----+--------------------+                                |
  |                          |                                |
  v                          v                                |
[draft_agent]           [aggregation_agent]                   |
  |                          |                                |
  | new branch               | new fusion_draft branch        |
  v                          v                                |
[Draft Node b1]         [Fusion_Draft Node bk]                |
  |                          |                                |
  | code_review              | code_review                    |
  v                          v                                |
[Executor / Subprocess Run]  [Executor / Subprocess Run]      |
  |                          |                                |
  v                          v                                |
[result_parse + validate]    [result_parse + validate]        |
  |                          |                                |
  +-----------+--------------+                                |
              |                                               |
              v                                               |
     [evaluation / reward / backprop]                         |
              |                                               |
      +-------+-------------------------+                     |
      |                                 |                     |
      v                                 v                     |
[buggy? -> debug_agent]      [good? -> improve/evolution/fusion]
      |                                 |
      |                                 +--> improve_agent ------+
      |                                 |                        |
      |                                 +--> evolution_agent ----+
      |                                 |                        |
      |                                 +--> fusion_agent -------+
      |                                                          |
      +------------------------> new SearchNode -----------------+
                                     |
                                     v
                             [register branch/node]
                                     |
                                     v
                           [global_memory update/retrieval]
                                     |
                                     +---- planner_with_memory
                                     +---- debug guidance
                                     +---- future draft novelty
```

这个图里，**实线父子边**是树边，**fusion/aggregation 的“参考”边**我没有单独画箭头，但它们确实在 prompt 里读了别的分支节点。([GitHub][10])

---

## 十四、它为什么不是普通 MCTS

严格说它不是教科书式 MCTS，而是更工程化的 **MCGS / MCTS-like graph search**：

* 节点不是动作状态，而是“候选 solution program”
* expansion 不是离散动作枚举，而是调用不同 agent 生成新代码
* rollout 不是模拟器 rollout，而是真执行训练/推理脚本
* reward 来自 leaderboard-like metric
* 除了树回传，还叠加了 top-k exploitation、branch stagnation、memory retrieval、cross-branch fusion。([GitHub][3])

所以它更像：

**“把程序搜索、实验管理、经验记忆、MCTS 式 credit assignment 融成一个统一框架”**

---

## 十五、最值得你注意的设计点

我觉得这个仓库最有味道的是 4 个点：

### 1）root 不是只出一个 draft，而是先造多个

这让初始多样性更高。([GitHub][12])

### 2）后期不是还在盲探索，而是切到 Top-K exploitation

这很像比赛场景：前期广撒网，后期围绕强解深挖。([GitHub][13])

### 3）fusion 和 aggregation 分成两种

一个是“借鉴别人改自己”，一个是“综合多支路重新开枝”。这个分得很工程。([GitHub][25])

### 4）memory 不是外挂，而是嵌进 planner/debug/draft

这让它不是纯搜索，而是**越跑越有任务内经验**。([GitHub][17])

---

## 十六、一句话总结

**MLEvolve 的实现骨架是一棵“可并行扩展的搜索树”，而它真正的算法思想是一个“由多分支实验、跨分支信息融合、经验记忆检索共同驱动的结果导向 DAG 搜索系统”。**
如果你站在代码实现层看，它是 tree；如果你站在“方案依赖关系”和“知识流动”层看，它就是 DAG。([GitHub][1])

下一条如果你愿意，我可以继续给你画一版**“按文件名对应的调用链图”**，直接精确到 `run.py -> AgentSearch.step -> node_selection -> improve_agent -> planner -> coder -> executor -> evaluation` 这种粒度。

[1]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/engine/search_node.py "raw.githubusercontent.com"
[2]: https://internscience.github.io/MLEvolve/ "MLEvolve | #1 on MLE-bench in 12 Hours"
[3]: https://github.com/InternScience/MLEvolve/blob/main/README.md "MLEvolve/README.md at main · InternScience/MLEvolve · GitHub"
[4]: https://github.com/InternScience/MLEvolve "GitHub - InternScience/MLEvolve: MLEvolve is an open-source autonomous system for end-to-end machine learning algorithm design and optimization powered by progressive search and experience-driven memory. · GitHub"
[5]: https://github.com/InternScience/MLEvolve/tree/main/engine "MLEvolve/engine at main · InternScience/MLEvolve · GitHub"
[6]: https://github.com/InternScience/MLEvolve/tree/main/agents "MLEvolve/agents at main · InternScience/MLEvolve · GitHub"
[7]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/agents/planner/__init__.py "raw.githubusercontent.com"
[8]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/agents/coder/__init__.py "raw.githubusercontent.com"
[9]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/agents/memory/global_memory.py "raw.githubusercontent.com"
[10]: https://github.com/InternScience/MLEvolve/raw/main/engine/agent_search.py "raw.githubusercontent.com"
[11]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/config/config.yaml "raw.githubusercontent.com"
[12]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/run.py "raw.githubusercontent.com"
[13]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/engine/node_selection.py "raw.githubusercontent.com"
[14]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/agents/draft_agent.py "raw.githubusercontent.com"
[15]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/agents/improve_agent.py "raw.githubusercontent.com"
[16]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/agents/planner/base_planner.py "raw.githubusercontent.com"
[17]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/agents/planner/planner_with_memory.py "raw.githubusercontent.com"
[18]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/agents/memory/retriever.py "raw.githubusercontent.com"
[19]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/agents/debug_agent.py "raw.githubusercontent.com"
[20]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/engine/executor.py "raw.githubusercontent.com"
[21]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/agents/result_parse_agent.py "raw.githubusercontent.com"
[22]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/engine/execution.py "raw.githubusercontent.com"
[23]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/engine/evaluation.py "raw.githubusercontent.com"
[24]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/agents/evolution_agent.py "raw.githubusercontent.com"
[25]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/agents/fusion_agent.py "raw.githubusercontent.com"
[26]: https://raw.githubusercontent.com/InternScience/MLEvolve/main/agents/aggregation_agent.py "raw.githubusercontent.com"
