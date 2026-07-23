# fuxi_auto_research - Design Spec

> Human-readable design narrative - rationale, audience, style, color choices, content outline. Read once by downstream roles for context.
>
> Machine-readable execution contract: `spec_lock.md` (color / typography / icon / image short form). Executor re-reads `spec_lock.md` before every SVG page to resist context-compression drift. Keep both in sync; on divergence, `spec_lock.md` wins.

## I. Project Information

| Item | Value |
| ---- | ----- |
| **Project Name** | fuxi_auto_research |
| **Canvas Format** | PPT 16:9 (1280x720) |
| **Page Count** | 2 pages |
| **Design Style** | B) General Consulting + 科技咨询风 / 数据驱动 / 轻量深色科技感 |
| **Target Audience** | 业务管理者、风控 / 催收策略负责人、数据科学团队、产品技术负责人 |
| **Use Case** | 内部汇报或方案展示：说明伏羲 Auto-Research 的技术机制与外诉 T30 场景业务价值 |
| **Created Date** | 2026-06-17 |

---

## II. Canvas Specification

| Property | Value |
| -------- | ----- |
| **Format** | PPT 16:9 |
| **Dimensions** | 1280x720 |
| **viewBox** | `0 0 1280 720` |
| **Margins** | left/right 48px, top 42px, bottom 34px |
| **Content Area** | 1184x620 |

---

## III. Visual Theme

### Theme Style

- **Style**: General Consulting + data-driven technology briefing
- **Theme**: Light theme with deep tech accents
- **Tone**: professional, analytical, confident, implementation-oriented

### Color Scheme

| Role | HEX | Purpose |
| ---- | --- | ------- |
| **Background** | `#F7FAFC` | Page background |
| **Secondary bg** | `#FFFFFF` | Panels and chart surfaces |
| **Primary** | `#1565C0` | Technology blue, main section anchors |
| **Deep primary** | `#0B1F33` | Titles and dark emphasis blocks |
| **Accent** | `#00A884` | Improvement, optimization, positive action |
| **Risk** | `#E55353` | External complaint risk |
| **Body text** | `#0B1F33` | Main text |
| **Secondary text** | `#6B7280` | Captions and annotations |
| **Border/divider** | `#D8E1EA` | Dividers, chart grid, panel borders |
| **Soft blue** | `#E8F2FF` | Light blue fills |
| **Soft green** | `#E8F8F2` | Light green fills |
| **Soft red** | `#FDECEC` | Light risk fills |

### Gradient Scheme

```xml
<linearGradient id="titleGradient" x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" stop-color="#1565C0"/>
  <stop offset="100%" stop-color="#00A884"/>
</linearGradient>
```

---

## IV. Typography System

### Font Plan

**Typography direction**: PPT-safe CJK sans, stable and clear.

| Role | Chinese | English | Fallback tail |
| ---- | ------- | ------- | ------------- |
| **Title** | `"Microsoft YaHei", "PingFang SC"` | Arial | sans-serif |
| **Body** | `"Microsoft YaHei", "PingFang SC"` | Arial | sans-serif |
| **Emphasis** | `"Microsoft YaHei", "PingFang SC"` | Arial | sans-serif |
| **Code** | - | `Consolas, "Courier New"` | monospace |

**Per-role font stacks**:

- Title: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- Body: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- Emphasis: `"Microsoft YaHei", "PingFang SC", Arial, sans-serif`
- Code: `Consolas, "Courier New", monospace`

### Font Size Hierarchy

**Baseline**: Body font size = 18px.

| Purpose | Size | Weight |
| ------- | ---- | ------ |
| Page title | 36px | Bold |
| Subtitle | 24px | SemiBold |
| Body content | 18px | Regular |
| Annotation / caption | 14px | Regular |
| Hero number | 52px | Bold |
| Micro label | 12px | SemiBold |

---

## V. Layout Principles

### Page Structure

- **Header area**: 42-112px, title + short conclusion subtitle.
- **Content area**: 112-650px, one primary visual per page, supported by concise interpretation.
- **Footer area**: 650-700px, source / scenario / page number.

### Layout Pattern Library

| Pattern | Use in this deck |
| ------- | ---------------- |
| **Asymmetric split** | Slide 01: screenshot evidence dominates, mechanism narrative sits beside it |
| **Process flow** | Slide 01: model nodes advance toward metric targets |
| **Dumbbell / before-after comparison** | Slide 02: traditional vs new cycle time across stages |
| **KPI callouts** | Slide 02: 14 days to 12 days, feature/model phases 50% compression |

### Spacing Specification

| Element | Current Project |
| ------- | --------------- |
| Safe margin from canvas edge | 48px |
| Content block gap | 28px |
| Card gap | 20px |
| Card padding | 22px |
| Card border radius | 8px |
| Icon-text gap | 10px |

---

## VI. Icon Usage Specification

### Source

- **Built-in icon library**: `phosphor-duotone`
- **Usage method**: SVG placeholder `<use data-icon="phosphor-duotone/icon-name" .../>`

### Recommended Icon List

| Purpose | Icon Path | Page |
| ------- | --------- | ---- |
| Model tree search | `phosphor-duotone/tree-structure` | Slide 01 |
| Target metric | `phosphor-duotone/target` | Slide 01 |
| Data set | `phosphor-duotone/database` | Slide 01 |
| AUC / PR trend | `phosphor-duotone/chart-line-up` | Slide 01 |
| Real-time call prediction | `phosphor-duotone/phone-call` | Slide 02 |
| Risk people | `phosphor-duotone/shield-warning` | Slide 02 |
| Cost / subsidy | `phosphor-duotone/currency-cny` | Slide 02 |
| Efficiency lift | `phosphor-duotone/trend-up` | Slide 02 |

---

## VII. Visualization Reference List

**Read-audit**:

```
Catalog read: 70 templates / 10 categories

Per-page selection:
  P01 process_flow | summary-quote: "Pick for 3-8 sequential steps connected by simple arrows."
  P02 dumbbell_chart | summary-quote: "Pick for before-vs-after or two-state difference across 5-10 items."

Runners-up considered:
  pipeline_with_stages | rejected for P01: the model search has node exploration and metric feedback, not fixed artifacts per pipeline stage.
  numbered_steps | rejected for P02: the business workflow has action branches and an efficiency comparison, not only 3-6 numbered steps.
  kpi_cards | rejected for P02: useful for callouts, but the core message is before-vs-after time compression across stages.
```

| Visualization Type | Reference Template | Used In |
| ------------------ | ------------------ | ------- |
| process_flow | `templates/charts/process_flow.svg` | Slide 01 |
| dumbbell_chart | `templates/charts/dumbbell_chart.svg` | Slide 02 |

---

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Status | Generation Description |
| -------- | ---------- | ----- | ------- | ---- | ------ | ---------------------- |
| 伏羲-autoresearch截图.png | 1870x1026 | 1.82 | Evidence image for Auto-Research tree search UI; no-crop screenshot | Diagram | Existing | User-provided screenshot, used on Slide 01 |

---

## IX. Content Outline

### Part 1: Technology Engine

#### Slide 01 - 伏羲 Auto-Research：以目标指标驱动的模型树搜索

- **Layout**: Asymmetric split, left screenshot evidence, right mechanism explanation and metric target rail.
- **Visualization**: process_flow.
- **Title**: 伏羲 Auto-Research：以目标指标驱动的模型树搜索
- **Subtitle**: 固定数据集上自动探索模型节点，围绕 AUC / PR 等目标持续逼近更优解。
- **Content**:
  - 确定数据集：统一样本、标签、特征口径。
  - 模型节点搜索：每个 node 是一组模型 / 特征 / 参数方案。
  - 目标函数优化：围绕 AUC、PR 等指标自动比较、淘汰、推进。
  - Bottom takeaway: 把“人工试模型”变成“系统性搜索最优模型路径”。

### Part 2: Business Value

#### Slide 02 - 外诉 T30 场景：更快建模，更精细处置

- **Layout**: Top business closed loop, bottom before-after efficiency comparison.
- **Visualization**: dumbbell_chart.
- **Title**: 外诉 T30 场景：更快建模，更精细处置
- **Subtitle**: 通话后实时预测外诉风险，高风险补钱降外诉，低风险降本控成本。
- **Content**:
  - 业务闭环：通话后实时预测 -> 识别外诉风险 -> 高风险补钱 / 强化安抚 -> 低风险标准处置 -> 降低外诉率。
  - 传统周期：数据准备 10 天 + 特征工程 2 天 + 模型工程 2 天 = 14 天。
  - 新周期：数据准备 10 天 + 特征工程 1 天 + 模型工程 1 天 = 12 天。
  - 重点结论：整体节省 2 天，特征与模型阶段均压缩 50%。

---

## X. Speaker Notes Requirements

One speaker note file per page, saved to `notes/`:

- **Filename**: match SVG name, e.g. `01_auto_research_tree.md`, `02_t30_business_value.md`
- **Content**: formal and concise executive briefing script.
- **Total duration**: around 3 minutes.
- **Purpose**: inform and persuade.

---

## XI. Technical Constraints Reminder

### SVG Generation Must Follow:

1. viewBox: `0 0 1280 720`
2. Background uses `<rect>` elements
3. Text wrapping uses `<tspan>`; `<foreignObject>` forbidden
4. Transparency uses `fill-opacity` / `stroke-opacity`; `rgba()` forbidden
5. Forbidden: `mask`, `<style>`, `class`, `foreignObject`
6. Forbidden: `textPath`, `animate*`, `script`
7. XML reserved characters in text must be escaped
8. `marker-end` allowed only with marker definitions in `<defs>`

### PPT Compatibility Rules:

- `<g opacity="...">` forbidden; set opacity on each child element individually
- Inline styles only; external CSS and `@font-face` forbidden
