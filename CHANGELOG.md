# Changelog

## 0.3.10 — 螺旋圖 pattern

- Add `examples/spiral-plot.md` from Nazh teach-viz `2026-09-26-pm-spiral.md` (approved skill pack; 方法教學); primary name **螺旋圖**（Spiral plot／Time series spiral；climate spiral 變體）. No spiral／periodic-time-series example existed before → new pattern.
- Core lesson: time on an Archimedean spiral, one turn = one period (centre earlier, outer newer), same angle = same point in the cycle; track encodings bar／condegram, line／area, spiral heatmap, horizon; climate spiral needs baseline period + units. Pitfalls: undefined turn／direction ("one turn = one month" misreading), dense turns, outer-arc distortion, unstable periods.
- Neighbours cross-linked: `time-series-trend.md`, `calendar-heatmap.md`, `matrix-heatmap.md`, `circular-bar.md`, `radar-profile.md` (plus streamgraph／gantt mentioned).
- Heuristics / how-to / data-shape checks. Tool honesty: R spiralize, D3 community (tomshanley d3-spiral-heatmap, Condegram gist), Hawkins Climate Visuals, NASA SVS 5190; no dedicated pages on data-to-viz／Flourish／R・Python Graph Gallery. Dataviz Project 403 and spiralize COVID app timeout noted; Carlis & Konstan DOI 10.1145/288392.288399; NASA stills attributed to SVS 5383／5057 (not 5190). Two X explainer posts (one flagged for the "one turn = one month" error); no coding tutorial post (none invented).
- Fictional demo CSV `examples/data/sample-spiral.csv`（2017–2024 monthly bike rentals, 96 rows, anomalous 2020 turn；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 47 → 48.

## 0.3.9 — 矩陣熱圖 pattern 升級

- Upgrade `examples/matrix-heatmap.md` from Nazh teach-viz `2026-09-26-am-heatmap.md` (approved skill pack); primary name **矩陣熱圖**（Heatmap；熱力圖／色階矩陣）. A generic example already existed → upgrade in place; pattern count stays 47.
- Core lesson: two categorical／ordered axes → matrix, colour = value strength; variants annotated heatmap, clustermap (reorder + dendrogram), correlation matrix (Wilke tiles／circles), time × category. Normalise by column／row when scales differ; sequential vs diverging (midpoint) scales, avoid rainbow (Viridis／ColorBrewer); missing ≠ zero; keep fixed axis order unless clustering.
- Calendar heatmap and adjacency matrix are neighbours only (not variants); cross-links added in `calendar-heatmap.md`, `adjacency-matrix.md`, `chord-matrix.md`.
- Heuristics / how-to / data-shape checks. Tool honesty: ggplot2 `geom_tile`, lattice `levelplot` (not ggplot), base `heatmap()`, Seaborn heatmap／clustermap, Plotly, D3 Graph Gallery, Flourish Heatmaps, Highcharts; Datawrapper heatmap pages 404, Flourish how-to 404, Observable 429, D3 heatmap2_basic 404 noted. One X teaching post (clcoding). Correlation-matrix image = wilke-forensic1 (not wilke-correlations).
- Fictional demo CSV `examples/data/sample-heatmap.csv`（12 categories × 7 channels, long format；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied.

## 0.3.8 — 圖塊地圖 pattern

- Add `examples/tile-map.md` from Nazh teach-viz `2026-09-25-pm-tilemap.md` (approved skill pack); primary name **圖塊地圖**（Tile map；statebins／tile grid map／格子地圖）. No dedicated example existed before (repo only had `hexbin-density.md` and `cartogram-geo.md`) → new pattern.
- Core lesson: one region = one tile, all tiles equal size; fixes choropleth large-area-low-population bias at the cost of shape／adjacency distortion. Weighted variants (Datawrapper electoral college hexagons, grid cartogram, Wikipedia mosaic cartogram, Tilegrams; tiles = population／votes) written separately and routed to `cartogram-geo.md`; cross-links with `choropleth-map.md` and `cartogram-geo.md`.
- Heuristics / how-to / data-shape checks (one tile per region, unique row/col, complete region codes, weighted tile counts sum to total). Tool honesty: statebins／geofacet／R Graph Gallery, Datawrapper square cantons + U.S. hexagons, Plotly, Tableau, D3; Observable 429 and CDC COVE 403 noted; no X teaching post this round (none invented). Cover／collage images (dw-election-hex, medium-hex, dw-swiss-compare) not cited as tile-map examples.
- Fictional demo CSV `examples/data/sample-tilemap.csv`（state+row+col+value_pct；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 46 → 47.

## 0.3.7 — 等值區域圖 pattern

- Add `examples/choropleth-map.md` from Nazh teach-viz `2026-09-25-am-choropleth.md` (approved skill pack); primary name **等值區域圖**（Choropleth map；分級設色圖／等值區劃圖）. No dedicated example existed before (only heuristics mentions) → new pattern.
- Core rules: normalize first (rate／per capita／per area) — never fill by totals; totals → 比例符號地圖. Separate from cartogram／比例符號／點密度／流向地圖 with when-to-switch; cross-links with `dot-density-map.md` and `cartogram-geo.md`. Classing (分位數／等距／自然斷點), sequential vs diverging, large-area-low-population bias, missing-value styling.
- Heuristics / how-to / data-shape checks (denominator present, geo codes match boundary file, missing regions ≠ 0). Tool honesty: Flourish = Projection map template; Observable old `@d3/choropleth` deprecated → `@d3/choropleth/2`; 4 verified X teaching posts.
- Fictional demo CSV `examples/data/sample-choropleth.csv`（region+population+cases+rate_per_100k；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 45 → 46.

## 0.3.6 — 馬里梅可圖 pattern

- Add `examples/marimekko-chart.md` from Nazh teach-viz `2026-09-24-pm-marimekko.md` (approved skill pack); primary name **馬里梅可圖**（Marimekko／Mekko；變寬堆疊長條）.
- Fold mix-ups vs 馬賽克（獨立性）／等寬堆疊／Treemap／Variwide＋軸模式（百分比 vs 絕對值）into `chart-heuristics.md` + how-to / data-shape checks (zh-TW); tool honesty: Datawrapper **無**原生 Marimekko；data-to-viz mosaic 404；Tableau 可能 403；Observable 可能 429；X 無可用教學原帖.
- Fictional demo CSV `examples/data/sample-marimekko.csv`（segment+product+value；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 44 → 45.

## 0.3.5 — 氣泡圖 pattern

- Add `examples/bubble-chart.md` from Nazh teach-viz `2026-09-24-am-bubble.md` (approved skill pack); primary name **氣泡圖**（Bubble chart／Bubble plot；氣泡散點圖）.
- Fold mix-ups vs bubble map／散點／連結散點／圓堆／Treemap／hexbin／等高線＋**面積≠半徑** into `chart-heuristics.md` + how-to / data-shape checks (zh-TW); tool honesty: Datawrapper＝Scatter 綁 size（無獨立 Bubble）；data-to-viz caveat/bubble、RAWGraphs、DW bubble 部落格 404；Observable 可能 429；X 無可用教學原帖.
- Fictional demo CSV `examples/data/sample-bubble.csv`（entity+x+y+size+region；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 43 → 44.

## 0.3.4 — 箱形圖 pattern

- Add `examples/boxplot-summary.md` from Nazh teach-viz `2026-09-23-pm-boxplot.md` (approved skill pack); primary name **箱形圖**（Box plot／Box-and-whisker；盒鬚圖）.
- Fold mix-ups vs 小提琴／雨雲／蜂群／直方／長條／誤差棒 into `chart-heuristics.md` + how-to / data-shape checks (zh-TW); tool honesty: Datawrapper **無**原生箱形；data-to-viz graph/boxplot 404；Observable 可能 429.
- Fictional demo CSV `examples/data/sample-boxplot.csv`（group+value；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count 42 → 43.

## 0.3.3 — 人口金字塔 + 棒棒糖圖 patterns

- Add `examples/population-pyramid.md` from Nazh teach-viz `2026-09-22-pm-pyramid.md` (approved skill pack); primary name **人口金字塔**（age-sex／population pyramid）.
- Add `examples/lollipop-rank.md` from Nazh teach-viz `2026-09-23-am-lollipop.md` (approved skill pack); primary name **棒棒糖圖**（lollipop；單點＋基線細莖，勿與啞鈴混）.
- Fold mix-ups vs 長條／龍捲風／啞鈴／點圖／誤差棒 into `chart-heuristics.md` + how-to / data-shape checks (zh-TW).
- Fictional demo CSVs under `examples/data/`（金字塔長／寬表；棒棒糖類別單值；數字未核）.
- ATTRIBUTION cites final teach-viz + pack paths; images cited, not copied. Pattern count 40 → 42.

## 0.3.2 — 河流圖 pattern（正式專題）

- Upgrade `examples/streamgraph-composition.md` from draft to Nazh teach-viz `2026-09-22-am-streamgraph.md` (approved skill pack); primary name **河流圖**（亦稱溪流圖／ThemeRiver）.
- Fold mix-ups vs stacked area / ThemeRiver / ridgeline / alluvial / investment「河道」into `chart-heuristics.md` + how-to / data-shape checks (zh-TW).
- Fictional demo CSVs under `examples/data/`（長／寬表；數字未核）.
- ATTRIBUTION cites final teach-viz + pack path; images cited, not copied. Pattern count unchanged (40).

## 0.3.1 — 點密度圖 pattern

- Add `examples/dot-density-map.md` from Nazh teach-viz `2026-09-21-pm-dotdensity.md` (approved skill pack).
- Fold 點密度圖 heuristics / how-to / mix-ups into `chart-heuristics.md` and `how-to-produce.md` (zh-TW).
- Fictional demo CSVs under `examples/data/` (one-to-many / one-to-one; 數字未核).
- ATTRIBUTION + pattern count 39 → 40. Images cited, not copied.


## 0.3.0 — public launch

- Bilingual README (English lead + zh-TW) with install, demo, and conversion hooks.
- `COMMERCIAL.md` for B2B use cases (earnings decks, ops dashboards, research digests).
- Copy-paste `demos/` pack: icicle, funnel, waterfall, dumbbell, slope.
- Sharper `SKILL.md` frontmatter for first-time Grok Build users.
- Chart-request Issue template. MIT + Nazh ATTRIBUTION unchanged.
