【角色设定】
- 你是一线互联网金融公司的首席架构师（Chief Architect），精通计算广告、强化学习（RL）及大规模分布式系统。

【任务背景】
- 目标设计：基于Agent的RTA（Real-Time API）智能投放系统
- 业务场景：金融信贷投放，有限日预算下最大化高价值用户获取量（总ROI最大化）
- 当前数据：eCPM 40±3，最终获客成本约10%；业内标杆（如360）约8%，存在2pp优化空间
- 核心提升点：
  1. **热点争夺让步（流量性价比）**：在流量竞争激烈且主流出价过高时，主动规避高热度资源，差异化竞争，预算集中投向高性价比流量。获客成本，是金融RTA最大杠杆
  2. **pApproval（风控通过率）**：进件后风控不通过=白花
  3. **pApply（进件率）**：减少"点击不进件"的无效流量，提升漏斗转化

【核心需求】
- 参考以上的论文，校验现在的内容是否有太大的偏离的地方
- 提到我们公司的内部数据，和业内的差距，即存在优化空间
- 输出/修正一份结构化系统架构设计思路（无需画图，文本层级清晰）
- 专业度高，主要受众为技术总监/算法专家（Top 30%的专业人士）
- 忽略基础科普，直入核心设计，不要太多的层级，最多分2-3大段，段内不要有太多的层级
- 输出格式为markdown代码块，相较于当前的版本，如非必要，不要做太大的结构上及内容上的修改，进行微调
- 我需要你在意的是业务架构，不要出现任何技术词汇（如redis，数据库等），算法名字和数学名称除外

【当前的版本】
# Enterprise RTA Bidding Architecture for Financial Credit (v5.0 - USCB Aligned)

## 1. 约束规划与影子出价模型 (Constrained Optimization & Shadow Bidding)
基于USCB论文的Theorem 2.1，我们将业务诉求抽象为带约束的线性规划（LP）问题，以此推导最优出价公式。

* **原始对偶规划 (Primal-Dual Formulation)**
    * **核心目标 (Objective)**: 最大化每日放款总LTV（$\sum v_i x_i$），其中 $v_i$ 为预估单次曝光的金融生命周期价值。
    * **硬性约束 (Hard Constraint)**: 每日消耗 $\le$ 设定预算 $B$。
    * **柔性KPI约束 (Soft Constraints - mapping to Paper's CR/NCR)**:
        * **CR (Cost-Related)**: **进件成本 (CPA)**。约束形式：$\frac{\sum Cost}{\sum Apply} \le K_{CPA}$。
        * **NCR (Non-Cost-Related)**: **授信通过率 (Credit Approval Rate)**。这是RTA的核心风控防线。约束形式：$\frac{\sum Approval}{\sum Apply} \ge K_{Rate}$。此处论文中的 $\mathbb{p}_{ij}$ 对应流量的“风控分/通过概率”。

* **最优参数化出价 (Parametric Bidding Function)**
    Agent不直接输出价格，而是针对当前时间片输出一组拉格朗日乘子参数 $\vec{w}_t$，由推理引擎执行以下公式：
    $$b_i^* = w_{0,t} \cdot v_i - w_{cpa,t} \cdot (c_i - K_{CPA} \cdot pApply_i) + w_{risk,t} \cdot (pApproval_i - K_{Rate} \cdot pApply_i)$$
    * **逻辑修正**:
        * $w_{0,t}$: 流量价值的激进程度（Base Bid Base）。
        * $w_{cpa,t}$: 对成本超支的惩罚力度。当CPA超标时，Agent增大此参数，迫使出价降低。
        * $w_{risk,t}$: **风控防御系数**。当大盘授信率低于 $K_{Rate}$ 时，Agent提升此参数，对于 $pApproval$ 低的劣质流量，出价会被迅速拉负（直接拒量）。

## 2. 强化学习参数调优策略 (RL-Based Parameter Tuning)
利用论文Theorem 3.1证明的“递归优化”性质，Agent只需学习针对“剩余预算和剩余KPI缺口”的最优静态参数，无需预测全天序列。

* **状态空间 (State Space $S_t$)**
    * **资源维度**: 预算消耗进度（Budget Consumption Rate）、剩余时间占比。
    * **绩效维度**: 当前进件CPA与目标值的偏离度（Gap to KPI）。
    * **风控维度**: **实时授信通过率 (Real-time Approval Rate)**。这是状态空间中最关键的金融信号，直接反映当前流量池的资产质量。

* **策略与回报 (Policy & Reward Shaping)**
    * **Action**: 输出向量 $\vec{w}_t = [w_0, w_{cpa}, w_{risk}]$ 的调整步长。
    * **Reward Function ($G$)**: 严格对齐论文公式 Eq.(17)。
        $$G = \min(\frac{Realized\_LTV}{Optimal\_LTV}, 1.0) - \sum \lambda_j \cdot \text{Penalty}(Constraint\_Violation_j)$$
    * **Critic设计**: 预测在当前状态 $S_t$ 下，维持动作 $\vec{w}_t$ 至当日结束时，最终的“全天达成率”和“违约惩罚”。这种设计避免了复杂的时序差分学习，加速收敛。

## 3. 信号修正与全链路估值 (Signal Correction & Full-Link Estimation)
解决金融场景下“放款（Drawdown）”滞后带来的Reward计算有偏问题，确保USCB算法能获得准实时的反馈信号。

* **T0发标率无偏估计 (Unbiased Estimation via T0 Issuance)**
    * **业务痛点**: 真实的放款（LTV的确认）存在T+1甚至T+7的延迟，直接使用当日已放款数据计算Reward会导致严重的低估，误导Agent降价。
    * **分层估算逻辑**:
        1.  **积压与处理节奏**: 指订单由于流程积压或资方处理节奏不同，存在一部分当日内完成放款（T0已放单），另一部分则进入跨小时或跨天处理，放款数据较晚回流。
        2.  **T0发标率 ($\alpha$)**: 实时统计当前时间窗内，已成功放款的订单占当期进件的比例，作为观测窗口。
        3.  **全局预估**: 利用已观察到的T0放款金额与T0发标率，对总放款进行无偏估计。
            $$\hat{V}_{total} \approx \frac{V_{T0\_Observed}}{\hat{\alpha}_{T0}} \cdot \beta_{correction}$$
    * **作用**: Agent的Reward计算依赖 $\hat{V}_{total}$ 而非仅依赖已观察到的 $V_{T0}$，防止因放款数据回传延迟导致的策略震荡。

* **延迟梯度的回放修正 (Off-Policy Replay with Corrections)**
    * **在线阶段**: 使用上述"预估全量价值"进行实时的RL推断和参数更新。
    * **离线/近线阶段**: 当T+1真实授信和放款数据回流后，修正Replay Buffer中的 $(S_t, A_t, R_t)$。
    * **修正动作**: 将 $R_t$ 中的预估值替换为真实值（True Label），供Actor网络进行Off-policy更新。这确保了长期来看，模型能准确捕捉"高进件但低通过"的劣质流量特征，并体现在 $w_{risk}$ 的调整策略中。

## 4. 模型矩阵与估值体系 (Model Stack & Valuation)
定义RTA链路中各模型的职责边界与调用时序。业务漏斗：**曝光 → 点击 → 进件 → 授用信风控 → 放款**。

* **前置快筛层 (Pre-Screening)**
    * **Pre-Risk Model**: 端到端预估"曝光→最终借款"概率，目标是**高精度而非高召回**。
        * *调用时机*: RTA请求进入时，最先调用。
        * *决策逻辑*: 仅对极端分做快速决策——接近0分直接阻断（不参竞），接近1分提升出价竞争力（抢量）；中间分进入完整估值流程。
        * *建模目标*: 最终借款（1=放款，0=未放款），综合了进件意愿与风控通过两重因素。

* **漏斗估值模型 (Funnel Valuation Stack)**
    用于计算 $v_i = pCTR \times pApply \times pApproval \times LTV$。
    * **pCTR**: 点击率（曝光→点击）。可自建或使用媒体侧回传。
    * **pApply**: 进件率（点击→进件）。建模目标：**借款意愿**，高分用户是"想借钱"的用户。
    * **pApproval**: 授信通过率（进件→放款）。建模目标：**风险水平**，高分用户是"能还钱"的好用户。
    * **LTV**: 放款用户生命周期价值。简化公式：$LTV = \text{息费收益} - \text{资金成本} - \text{运营成本}$。

* **策略模型 (RL Policy)**
    * **Actor**: 输出参数向量 $\vec{w}_t = [w_0, w_{cpa}, w_{risk}]$ 的调整步长。
    * **Critic**: 预测当前状态下维持 $\vec{w}_t$ 至日终的全天达成率，用于评估动作优劣。
    
【你做的修改】：
