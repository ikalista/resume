MLEvolve介绍
基于MCTS的结合探索与利用的，并带着知识库作为全局记忆的，一个自动机器学习框架
动作空间及状态机如下

`root`, `draft`, `fusion_draft`, `improve`, `debug`, `evolution`, `fusion`

```mermaid
flowchart LR
    START([开始]) --> ROOT[root初始化]
  
    ROOT -->|初始生成| DRAFT[draft]
    ROOT -->|aggregation触发| FUSION_DRAFT[fusion_draft]
  
    DRAFT -->|生成代码+执行| DRAFT_EVAL{draft执行结果}
    FUSION_DRAFT -->|生成代码+执行| FUSION_DRAFT_EVAL{fusion_draft执行结果}
  
    DRAFT_EVAL -->|成功| IMPROVE[improve]
    DRAFT_EVAL -->|失败/buggy| DEBUG[debug]
  
    FUSION_DRAFT_EVAL -->|成功| IMPROVE
    FUSION_DRAFT_EVAL -->|失败| DEBUG
  
    DEBUG -->|检索经验+修复代码| DEBUG_EVAL{debug执行结果}
    DEBUG_EVAL -->|修复成功| IMPROVE
    DEBUG_EVAL -->|修复失败| DEBUG
    DEBUG_EVAL -->|超过重试上限| TERMINAL1([终止])
  
    IMPROVE -->|常规改进| IMPROVE_EVAL{improve执行结果}
    IMPROVE_EVAL -->|成功且未停滞| IMPROVE
    IMPROVE_EVAL -->|成功但分支停滞| EVOLUTION[evolution]
    IMPROVE_EVAL -->|成功且跨分支可期| FUSION[fusion]
    IMPROVE_EVAL -->|新代码有bug| DEBUG
    IMPROVE_EVAL -->|连续失败超阈值| TERMINAL2([终止])
  
    EVOLUTION -->|分析分支历史+生成代码| EVOLUTION_EVAL{evolution执行结果}
    EVOLUTION_EVAL -->|成功| IMPROVE
    EVOLUTION_EVAL -->|失败| DEBUG
  
    FUSION -->|参考其他分支top节点+生成代码| FUSION_EVAL{fusion执行结果}
    FUSION_EVAL -->|成功| IMPROVE
    FUSION_EVAL -->|失败| DEBUG
```

复现成果：
在lite数据集上，用minimax实现了奖牌率67%，并进行了记忆模块的消融，发现奖牌率下降至了33%，说明记忆模块非常重要。

复现发现的问题：

1. 大家都在用很强的大模型，如果要打榜，harness相同的情况下，minimax比gemini pro overall落后了10%个点。使用gemini会有网络/费用等问题。需要权衡费用和模型的选型。
2. 官方规定一个任务耗时24h，取3次误差。资源要求约等于1/4个A100，意味着A100全占我也只能起4并发。而lite任务有22个*3 / 4 = 16.5天，全部数据集要求高达 80 * 3 / 4 = 60天。这几乎不可承受。因此需要权衡下一步是继续打榜/部分打榜，还是转向落地。

未来需要考虑的功能：

1. 人在回路，需要切入该框架，让人可以干预这个MCTS/轨迹
