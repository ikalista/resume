# ai_customer_complaint_v2 - Design Spec

> Human-readable design narrative for the second iteration of the AI 客诉专项立项简报. This version refactors page 2 into an explicit dual-chain flow diagram and folds staffing into per-node ownership chips. Machine-readable runtime contract lives in `spec_lock.md`; on divergence `spec_lock.md` wins.

## I. Project Information

| Item | Value |
| ---- | ----- |
| **Project Name** | ai_customer_complaint_v2 |
| **Canvas Format** | PPT 16:9 (1280x720) |
| **Page Count** | 2 pages |
| **Design Style** | Top Consulting + technology management briefing |
| **Target Audience** | 张总、业务负责人、AI 与客诉专项团队 |
| **Use Case** | AI 客诉专项立项 / 资源投入 / 节奏汇报（v2 强调流程图化拆解与横向比较） |
| **Created Date** | 2026-05-09 |

---

## II. Canvas Specification

| Property | Value |
| -------- | ----- |
| **Format** | PPT 16:9 |
| **Dimensions** | 1280x720 |
| **viewBox** | `0 0 1280 720` |
| **Margins** | left/right 44px, top 34px, bottom 28px |
| **Content Area** | 1192x610 |

---

## III. Visual Theme

### Theme Style

- **Style**: Top Consulting
- **Theme**: Light theme
- **Tone**: stable, technical, conclusion-first; visually flow-chart heavy on page 2

### Color Scheme

| Role | HEX | Purpose |
| ---- | --- | ------- |
| **Background** | `#F7F9FC` | Page background |
| **Secondary bg** | `#FFFFFF` | Cards, table surfaces, flow nodes |
| **Primary** | `#1E3A5F` | Title bar, conclusion box, structural lines |
| **Accent** | `#00A6A6` | 链路一（业务知识）节点强调色 |
| **Secondary accent** | `#4A90A4` | 链路二（大模型挖掘）节点强调色 |
| **Pale accent** | `#E8F7F7` | 链路一通道底色 |
| **Pale primary** | `#EAF0F6` | 链路二通道底色 |
| **Pale warning** | `#FFF4ED` | 短接路线 / 横向比较高亮底 |
| **Body text** | `#172033` | Main text |
| **Secondary text** | `#667085` | Captions, owner chips, table metadata |
| **Tertiary text** | `#98A2B3` | Footer |
| **Border/divider** | `#D9E2EC` | Card borders, divider lines |
| **Success** | `#1F8A70` | 闭环 / 反哺成功状态 |
| **Warning** | `#D04A02` | 短接路线箭头 / 风险信号 |

### Gradient Scheme

Single restrained top rule per page from `#1E3A5F` to `#00A6A6`, 4px height. No decorative gradient orbs — this deck is structure-driven, not atmosphere-driven.

```xml
<linearGradient id="topRule" x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" stop-color="#1E3A5F"/>
  <stop offset="100%" stop-color="#00A6A6"/>
</linearGradient>
```

---

## IV. Typography System

### Font Plan

**Typography direction**: modern CJK sans, dense consulting briefing. Single-family weight contrast (Bold 700 / SemiBold 600 / Regular 400) carries hierarchy.

| Role | Chinese | English | Fallback tail |
| ---- | ------- | ------- | ------------- |
| **Title** | `"Microsoft YaHei", "PingFang SC"` | Arial | sans-serif |
| **Body** | `"Microsoft YaHei", "PingFang SC"` | Arial | sans-serif |
| **Emphasis** | `"Microsoft YaHei", "PingFang SC"` | Arial | sans-serif |
| **Code** | — | Consolas, `"Courier New"` | monospace |

**Per-role font stacks**

- Title: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- Body: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- Emphasis: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- Code: `Consolas, "Courier New", monospace`

### Font Size Hierarchy

**Baseline**: Body font size = 18px (dense briefing).

| Purpose | Size | Weight |
| ------- | ---- | ------ |
| Page title | 32-36px | Bold |
| Takeaway sentence | 18-20px | Bold (white on primary bar) |
| Section heading | 18-20px | Bold |
| Flow node title | 15-16px | Bold |
| Body content | 14-16px | Regular / SemiBold |
| Owner chip / annotation | 11-12px | SemiBold |
| Footer | 10-11px | Regular |

> Page-1 keeps the original 36/24/18 ramp. Page-2 compresses node-internal text to 14-16px because two parallel chains must coexist on one canvas without overflow.

---

## V. Layout Principles

### Page Structure

- **Header area**: 34-90px — gradient top rule, page title, conclusion takeaway bar
- **Content area**: 90-660px — page-specific structural visualization
- **Footer area**: 660-720px — page number, project tag, ownership / reference note

### Layout Pattern Library

| Pattern | Used in |
| ------- | ------- |
| **Pipeline with stages** (5-stage horizontal pipeline, output artifact per stage) | Page 01 |
| **Dual swimlane process flow** (two horizontal chains with shared merge node + bottom phase ribbon) | Page 02 |
| **Asymmetric split** (chain area + phase ribbon) | Page 02 |

### Spacing Specification

| Element | Current Project |
| ------- | --------------- |
| Safe margin from canvas edge | 44px |
| Content block gap | 24-32px |
| Icon-text gap | 8-12px |
| Flow node padding | 10-14px |
| Flow node corner radius | 8px |
| Lane vertical gap | 18-24px |

---

## VI. Icon Usage Specification

### Source

- **Built-in icon library**: `chunk-filled` (single library — no mixing)
- **Usage method**: SVG placeholder `<use data-icon="chunk-filled/icon-name" .../>`; finalize_svg embeds at post-process.

### Recommended Icon List

| Purpose | Icon Path | Page |
| ------- | --------- | ---- |
| 电话 / 数据源 | `chunk-filled/phone` | Slide 01 |
| 大模型能力 | `chunk-filled/bolt` | Slide 01 / 02 |
| 行为识别 | `chunk-filled/target` | Slide 01 |
| 客群分类 | `chunk-filled/users` | Slide 01 |
| 处置策略 | `chunk-filled/shield-check` | Slide 01 |
| 数据闭环 / 反哺 | `chunk-filled/arrows-rotate-clockwise` | Slide 01 / 02 |
| 专家知识输入 | `chunk-filled/lightbulb` | Slide 02 |
| 用户行为洞察 | `chunk-filled/chart-line` | Slide 02 |
| 分群下钻 / 同质化挖掘 | `chunk-filled/magnifying-glass` | Slide 02 |
| 大模型直接分群（短接） | `chunk-filled/wand-with-sparkles` | Slide 02 |
| 聚类条线起点 | `chunk-filled/share-nodes` | Slide 02 |
| 聚类行为洞察 | `chunk-filled/layers` | Slide 02 |
| 横向比较与发现 | `chunk-filled/arrows-left-right` | Slide 02 |
| 阶段时钟 | `chunk-filled/clock` | Slide 02 |
| 责任人 | `chunk-filled/circle-user` | Slide 02 |

---

## VII. Visualization Reference List

```
Catalog read: 70 templates / 10 categories

Per-page selection:
  P01 pipeline_with_stages | summary-quote: "Pick for 3-5 stage horizontal pipeline where each stage = title + 1-line description + output artifact, connected by directional arrows."
  P02 process_flow         | summary-quote: "Pick for 3-8 sequential steps connected by simple arrows. Skip if cyclical (use cycle_diagram) or stages produce named outputs (use pipeline_with_stages)."

Runners-up considered:
  chevron_process | rejected for P01: P01 stages produce named outputs (pipeline_with_stages is more specific).
  snake_flow      | rejected for P02: dual-lane parallel chains, not one long winding journey.
  hub_spoke       | rejected for P02: P02 has two linear chains plus a merge, no single radial hub.
```

| Visualization Type | Reference Template | Used In |
| ------------------ | ------------------ | ------- |
| pipeline_with_stages | `templates/charts/pipeline_with_stages.svg` | Slide 01 |
| process_flow | `templates/charts/process_flow.svg` | Slide 02 (adapted into dual-lane swimlane) |

> Slide 02 adapts `process_flow` twice (one chain per lane) plus a custom merge arrow into the shared "分群下钻分析 / 横向比较" zone. The bottom 4-stage phase ribbon is a free design element.

---

## VIII. Image Resource List

No external images. All visuals are native SVG (shapes, text, built-in icon placeholders). The `architecture diagram` JPG is reference material only (lives in `sources/`), not embedded in the deck.

---

## IX. Content Outline

### Part 1: AI 专项价值与方法路径

#### Slide 01 - AI 专项价值与方法路径

- **Layout**: Top consulting header + dark conclusion bar + 5-stage horizontal pipeline + bottom value mapping
- **Title**: AI 专项要形成"识别—分类—策略—反馈"的业务闭环，而不是单点模型实验
- **Takeaway**: 同时压降外诉、优化退费、沉淀专家经验 — 形成可复用的客诉处置机制
- **Visualization**: pipeline_with_stages
- **Content**:
  - **电话（数据源）**：通话文本、12378 拨打、工单、短信触达、退费与投诉结果
  - **大模型（专家经验嵌入）**：自顶向下规则归类 + 自底向上文本聚类并行
  - **行为识别**：投诉倾向、外溢风险、诉求强度、沟通方式
  - **客群分类**：专业性维度（小白 / 豆包人 / 专业型）× 诉求维度（强硬 / 协商 / 软弱），保留"等待挖掘"维度
  - **处置策略**：分流建议、外呼话术、退费力度、拒绝方式、跟进周期；结果反哺模型
- **底部价值映射**：压降外诉 · 优化退费 · 沉淀经验 — 闭环箭头回到大模型节点

### Part 2: 任务拆解与资源安排

#### Slide 02 - 双链路任务拆解（流程图化）

- **Layout**: Top consulting header + 双 swimlane 平行流程 + 共享汇合区（横向比较与发现）+ 底部 4 阶段节奏 ribbon
- **Title**: 业务知识链路 + 大模型自动挖掘链路并行推进，由横向比较收口
- **Takeaway**: 两条洞察链路并行跑，陶可晗负责横向比较把两路结论对齐成统一客群体系
- **Visualization**: process_flow (×2 lanes adapted to dual-swimlane)
- **链路一 · 基于业务知识的洞察**（lane 上半，accent 色 `#00A6A6`）
  - **大模型 + 专家知识**（李怡静）：客诉分类、风险信号、退费经验、坐席话术 → 标签定义 + 提示词
  - **用户行为洞察**（李怡静）：诉求 / 情绪 / 沟通方式 / 反复进线 / 退费预期 → 客户级行为画像
  - **基于专家知识的分客群洞察**（李怡静）：专业性 × 诉求 × 风险维度切分客群
  - **大模型直接分客群洞察**（李怡静）：⚡ 短接路线 — 不受专家框架约束，模型直接给分群判断
  - **分群下钻分析**（汇合点）：每类客群 → Top 诉求 / 典型话术 / 风险触发 / 退费敏感度 / 处置策略
- **链路二 · 基于大模型的自动化挖掘**（lane 下半，secondary_accent 色 `#4A90A4`）
  - **大模型 + embedding + 聚类算法**（殷文天）：全量通话向量化 → 自然簇
  - **聚类行为洞察**（殷文天）：同簇通话词频 + 关键句 + 大模型总结
  - **同质化信息挖掘**（殷文天）：每簇输出"为什么相似 / 风险点 / 处置方式"
- **横向比较与发现**（陶可晗）：把链路一分群 / 链路二聚类簇 / 其他团队洞察对齐 — 例如"大模型认为的豆包人 vs 专家规则定义的豆包人有何不同"，发现纳入新维度，反哺专家框架
- **底部 4 阶段节奏**（icon: clock）：
  - 阶段 1 — 输入与跑通：专家知识入库 + 行为信号定义 + 聚类链路打通
  - 阶段 2 — 横向对齐：专家分群 / 大模型分群 / 聚类簇三方对齐，发现新维度
  - 阶段 3 — 重点客群下钻：Top 诉求 / 话术 / 风险 / 处置建议输出
  - 阶段 4 — 工具化落地：工单高亮 / 坐席辅助 / AI 首通回访 / 周复盘
- **底注**（一行）：4 人各 0.5 人力 · 整体代码架构：李嘉辉 · 聚类条线：殷文天 · 行为与分群洞察：李怡静 · 横向比较与发现：陶可晗

---

## X. Speaker Notes Requirements

- 单一 `notes/total.md`，按 `# 01_xxx` `# 02_xxx` 拆分到 `notes/` 子文件
- 风格：结论先行的中文口播，每页 ~80-110 秒，不要 meta 标签
- 重点：第二页要把"为什么需要短接路线 / 横向比较的价值"讲清楚

---

## XI. Technical Constraints Reminder

1. viewBox: `0 0 1280 720`
2. Background: `<rect>`，不用 image 填充
3. Text wrapping: `<tspan>`；禁用 `<foreignObject>`
4. Transparency: `fill-opacity` / `stroke-opacity`；禁用 `rgba()`
5. Forbidden: `mask`, `<style>`, `class`, `textPath`, `animate*`, `script`
6. Group opacity 禁用，逐元素设 `opacity`
7. Icons via `<use data-icon="chunk-filled/...">` 占位符，post-process 时由 finalize 嵌入
8. 文本中文字符直接写 Unicode；XML 保留字 `& < > " '` 必须转义
