## canvas
- viewBox: 0 0 1280 720
- format: PPT 16:9

## colors
- bg: #F7F9FC
- secondary_bg: #FFFFFF
- primary: #1E3A5F
- accent: #00A6A6
- secondary_accent: #4A90A4
- pale_accent: #E8F7F7
- pale_primary: #EAF0F6
- pale_warning: #FFF4ED
- accent_highlight: #7FE3E3
- text: #172033
- text_secondary: #667085
- text_tertiary: #98A2B3
- border: #D9E2EC
- success: #1F8A70
- warning: #D04A02

## typography
- font_family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif
- code_family: Consolas, "Courier New", monospace
- body: 18
- title: 36
- subtitle: 22
- node_title: 16
- node_body: 14
- annotation: 12
- footer: 11

## icons
- library: chunk-filled
- inventory: phone, bolt, target, users, shield-check, arrows-rotate-clockwise, lightbulb, chart-line, magnifying-glass, wand-with-sparkles, share-nodes, layers, arrows-left-right, clock, circle-user

## page_rhythm
- P01: dense
- P02: dense

## page_charts
- P01: pipeline_with_stages
- P02: process_flow

## forbidden
- Mixing icon libraries
- rgba()
- `<style>`, `class`, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<script>`, `<iframe>`, `<symbol>`+`<use>`
- `<g opacity>` (set opacity on each child element individually)
- HTML named entities in text; XML reserved chars must be escaped as `&amp; &lt; &gt; &quot; &apos;`
