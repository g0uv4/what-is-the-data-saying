# Chart-type heuristics

One primary recommendation + 1–2 alternates. Prefer the simplest chart that answers the question.

## Decision table

| If the main job is… | Prefer | Avoid / caution |
|---------------------|--------|-----------------|
| Look up exact values, audit, legal annex | **table** (+ conditional format) | Decorative charts that hide numbers |
| Compare magnitudes across categories | **bar** (horizontal if labels long) | Pie with >5 slices; 3D bar |
| Rank / top-N | **sorted bar** | Unsorted categorical axis |
| Trend over time (few series) | **line** | Bar for dense daily series (unless discrete periods) |
| Trend, many entities | **small multiples** (same scale) | Single chart with 20+ overlapping lines |
| Part-to-whole, few parts | **stacked bar** or **100% stacked** | Pie unless ≤4 parts and brand requires it |
| Part-to-whole, hierarchy | **icicle** / **sunburst** / **treemap** | Flat pie of leaf nodes only |
| Relationship of two numerics | **scatter** | Line (unless ordered by a third variable) |
| Correlation / matrix intensity | **heatmap** | Scatter matrix when N is huge (sample first) |
| Distribution | **histogram** / **violin** / **box** | Bar of every raw point |
| Flow A→B | **sankey** / **alluvial** | Sankey with cycles unless tool supports |
| Geographic rate | **choropleth** (normalized) | Raw counts on unequal regions without note |

## Shape → chart shortcuts

- **time + 1 numeric + ≤3 series** → line  
- **category + 1 numeric** → bar  
- **category + time + numeric** → line facets or grouped bar (few periods)  
- **2 numerics** → scatter  
- **category × category + numeric** → heatmap  
- **path / parent-child + numeric** → icicle (detail labels) or sunburst (compact overview)  
- **many parallel series, same grain** → small multiples  

## Encoding rules (short)

- Position > length > angle > area > color hue for quantity.
- One numeric encoding per primary question.
- Dual axis: only if user insists; label both scales; prefer index/normalize or dual panel.
- Stacked absolute: good for total + rough composition; bad for comparing middle segments → prefer grouped or 100% stacked + absolute table.

## Output medium

| Medium | Bias |
|--------|------|
| 投影片／PDF | Fewer series, larger type, static png/svg |
| 互動 dashboard | Hover detail, filter, drill (icicle/sunburst) |
| 內部對帳 | Table first |
| 對外敘事 | One clear chart + one sentence takeaway |

## Library hints (non-binding)

- Python: plotly (interactive), matplotlib/seaborn (static), altair (grammar)
- JS: Observable Plot / d3, echarts
- No-code: Flourish, spreadsheet pivot + chart

Pick what the repo already uses when inside a codebase.
