## 主流VLA框架横向调研与真机复现（2025年11月-至今）

**背景**：VLA 方向迭代极快，各框架在动作生成范式（离散 token / Diffusion / Flow Matching）与世界模型设计上差异显著；作为算法背景、机器人硬件资源有限的转型者，先选定一个社区活跃、设计收敛的通用框架作为落地支点，再全力投入仿真训练与真机实采，是最优先级的路径选择。

**任务**：掌握 LeRobot 框架并跑通各项入门任务；对 InternVLA、π 系列、ACT 等主流方案进行架构拆解与横向对比；完成阶段性仿真复现，并推进 InternVLA-A1 在 RoboTwin 与双臂真机链路上的 sim2real 复现。

**行动**：
- 系统拆解 ACT/Openvla、π0/π0.5/π0.6/π-fast、InternVLA（M1/A1），归纳三类技术路线（动作离散化 / 扩散与 Flow Matching / 世界模型联合优化），梳理各主流数据集在语言泛化、双臂协同与真机迁移中的适用边界
- 完成 ACT on Cube Transfer、π0 on LIBERO-Spatial、smolvla on pushT 的训练与推理复现
- 完成 InternVLA-A1 on RoboTwin 环境搭建与前向推理联调，当前进入调参与批量评测阶段

**结果**：
- ACT on Cube Transfer：成功率约 60%（官方约 80%），瓶颈定位至最终 handover，已进入定向调参
- π0 on LIBERO-Spatial（n=30 episodes）：平均成功率 61%，简单任务 70%+，长链路任务 45%-55%
- InternVLA-A1 on RoboTwin：环境已通，待训练流程调通后进入双臂真机联调
