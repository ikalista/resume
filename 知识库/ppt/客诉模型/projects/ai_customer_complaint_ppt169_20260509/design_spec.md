# ai_customer_complaint - Design Spec

## I. Project Information

| Item | Value |
| ---- | ----- |
| **Project Name** | ai_customer_complaint |
| **Canvas Format** | PPT 16:9 (1280x720) |
| **Page Count** | 2 pages |
| **Design Style** | Top Consulting + technology management briefing |
| **Target Audience** | 张总、业务负责人、AI 与客诉专项团队 |
| **Use Case** | AI 客诉专项立项 / 资源投入 / 执行安排汇报 |
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
- **Tone**: stable, technical, management-oriented, conclusion-first

### Color Scheme

| Role | HEX | Purpose |
| ---- | --- | ------- |
| **Background** | `#F7F9FC` | Page background |
| **Secondary bg** | `#FFFFFF` | Panels and table surfaces |
| **Primary** | `#1E3A5F` | Header, conclusion bar, key structures |
| **Accent** | `#00A6A6` | AI capability highlights |
| **Secondary accent** | `#4A90A4` | Supporting flow nodes |
| **Body text** | `#172033` | Main text |
| **Secondary text** | `#667085` | Captions and table metadata |
| **Tertiary text** | `#98A2B3` | Footer |
| **Border/divider** | `#D9E2EC` | Dividers and table lines |
| **Success** | `#1F8A70` | Positive closed-loop / completion |
| **Warning** | `#D04A02` | Risk / intervention signals |

### Gradient Scheme

Use a restrained top rule from `#1E3A5F` to `#00A6A6` on every page. No decorative gradient orbs.

---

## IV. Typography System

### Font Plan

**Typography direction**: modern CJK sans, dense consulting report.

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

**Baseline**: Body font size = 18px.

| Purpose | Size | Weight |
| ------- | ---- | ------ |
| Page title | 36px | Bold |
| Takeaway sentence | 20px | Bold |
| Section heading | 18-22px | Bold |
| Body content | 18px | Regular |
| Dense table body | 14-16px | Regular / Semibold |
| Annotation / caption | 13-15px | Regular |
| Footer | 11-12px | Regular |

---

## V. Layout Principles

### Page Structure

- **Header area**: 44px top margin, conclusion-first title, short subtitle, thin gradient top bar.
- **Content area**: 90px to 650px; use structured flow / table visualization.
- **Footer area**: page number, source note, confidentiality-style project footer.

### Layout Pattern Library

| Pattern | Suitable Scenarios |
| ------- | ----------------- |
| **Pipeline with stages** | Page 01, AI value and method path |
| **Project schedule table** | Page 02, work / owner / input plan |
| **Asymmetric split** | Side insight panel + main visualization |
| **Dense consulting table** | Responsibility and staffing |

### Spacing Specification

| Element | Current Project |
| ------- | --------------- |
| Safe margin from canvas edge | 44px |
| Content block gap | 24-32px |
| Icon-text gap | 10-14px |
| Card gap | 18-24px |
| Card padding | 18-24px |
| Card border radius | 8px |

---

## VI. Icon Usage Specification

### Source

- **Built-in icon library**: `chunk-filled`
- **Usage method**: SVG placeholder `<use data-icon="chunk-filled/icon-name" .../>`

### Recommended Icon List

| Purpose | Icon Path | Page |
| ------- | --------- | ---- |
| 电话数据 | `chunk-filled/phone` | Slide 01 |
| 大模型能力 | `chunk-filled/bolt` | Slide 01 |
| 行为识别 | `chunk-filled/target` | Slide 01 |
| 客群分类 | `chunk-filled/users` | Slide 01 |
| 处置策略 | `chunk-filled/shield-check` | Slide 01 |
| 数据闭环 | `chunk-filled/arrows-rotate-clockwise` | Slide 01 |
| 任务拆解 | `chunk-filled/route` | Slide 02 |
| 标签数据 | `chunk-filled/tag` | Slide 02 |
| 架构与分析 | `chunk-filled/database` | Slide 02 |
| 项目统筹 | `chunk-filled/circle-user` | Slide 02 |
| 指标跟踪 | `chunk-filled/chart-bar` | Slide 02 |
| 阶段节奏 | `chunk-filled/clock` | Slide 02 |

---

## VII. Visualization Reference List

Catalog read: 70 templates / 10 categories

Per-page selection:
  P01 pipeline_with_stages | summary-quote: "Pick for 3-5 stage horizontal pipeline where each stage = title + 1-line description + output artifact, connected by directional arrows."
  P02 project_schedule_table | summary-quote: "Pick for table-style task tracker (task / owner / status / timeline)."

Runners-up considered:
  process_flow | rejected for P01: Page 01 stages have named outputs and a closed business loop, so pipeline_with_stages is more specific.
  chevron_process | rejected for P01: The flow is method plus output artifacts, not just phase methodology blocks.
  team_roster | rejected for P02: The page needs work ownership and staffing intensity, not profile cards.

| Visualization Type | Reference Template | Used In |
| ------------------ | ------------------ | ------- |
| pipeline_with_stages | `templates/charts/pipeline_with_stages.svg` | Slide 01 |
| project_schedule_table | `templates/charts/project_schedule_table.svg` | Slide 02 |

---

## VIII. Image Resource List

No external images. Slides are built with native SVG shapes, text, and built-in icons.

---

## IX. Content Outline

### Part 1: AI专项价值与方法路径

#### Slide 01 - AI专项价值与方法路径

- **Layout**: Top consulting header + dark takeaway bar + 5-stage pipeline + bottom value mapping.
- **Title**: AI专项要形成“识别—分类—策略—反馈”的业务闭环，而不是单点模型实验
- **Takeaway**: 目标是同时压降外诉、优化退费、沉淀专家经验。
- **Visualization**: pipeline_with_stages
- **Content**:
  - 电话：通话文本、12378 拨打、工单、短信、退费与投诉结果。
  - 大模型：专家经验嵌入，自顶向下规则和自底向上聚类并行。
  - 行为识别：投诉倾向、外溢风险、诉求强度、沟通方式。
  - 客群分类：专业性维度与诉求态度维度双轴打标，保留等待挖掘维度。
  - 处置策略：分流、外呼话术、退费力度、拒绝方式、跟进周期，并将结果反哺模型。

### Part 2: 任务拆解与资源安排

#### Slide 02 - 任务拆解与资源安排

- **Layout**: Top consulting header + dark takeaway bar + left two-path task decomposition + right staffing table + bottom four-stage rhythm.
- **Title**: 4人各0.5人力即可启动专项，但必须把专家下钻与模型探索并行推进
- **Takeaway**: 先用两条路径跑出统一标签体系，再小流量验证并工具化。
- **Visualization**: project_schedule_table
- **Content**:
  - 路径一：专家知识驱动，下钻客诉类型、风险信号、退费策略矩阵、话术与干预节点。
  - 路径二：大模型与文本聚类，自底向上发现通话主题、行为模式和新维度。
  - 人力：李嘉辉 Leader；殷文天 架构及聚类探索；李怡静 广义文本标签；陶可晗 架构及标签数据分析；每人 0.5。
  - 阶段：分类框架与聚类、两路对齐与评测集、小流量验证、工具化落地。

---

## X. Speaker Notes Requirements

One `notes/total.md` file, then split to per-page notes. Notes should be concise spoken Chinese, conclusion-first, without meta labels.

---

## XI. Technical Constraints Reminder

1. viewBox: `0 0 1280 720`
2. Background uses `<rect>` elements.
3. Text wrapping uses `<tspan>`; `<foreignObject>` is forbidden.
4. Transparency uses `fill-opacity` / `stroke-opacity`; `rgba()` is forbidden.
5. Forbidden: `mask`, `<style>`, `class`, `textPath`, `animate*`, `script`.
6. PPT compatibility: no group opacity; icons use built-in `<use data-icon="...">` placeholders and are embedded during finalization.
