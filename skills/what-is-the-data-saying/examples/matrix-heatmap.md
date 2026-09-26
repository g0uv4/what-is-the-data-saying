# Pattern: matrix-heatmap

> **圖種**：矩陣熱圖（Heatmap／Heat map／matrix heatmap）
> **來源（納茲教圖）**：`teach-viz/2026-09-26-am-heatmap.md`（方法教學；經已審 skill pack 升級原本的通用版）
> **亦稱**：熱力圖、色階矩陣
> **核心**：**兩個類別（或有序）軸交叉成矩陣，每一格用顏色表示該組合的數值強度**。先看熱區與冷區，精確值靠圖例或格內標註

## When

- 問「哪些列 × 欄的組合特別高／特別低」「多類別 × 多指標誰相對強」「變數兩兩相關結構」「週期規律（例如星期 × 小時）」
- 形狀：已經是、或可樞紐成「列 × 欄 → 一個數值」的矩陣；長格式 `row_category, col_category, value` 或寬表都可以
- 列欄數量適中；列欄極多時要先篩選或分群，不然只剩一片雜訊

## Recommend

- **主選**：矩陣熱圖（色塊格子）
  - **標註熱圖**：格子少時格內直接寫數字
  - **分群熱圖／clustermap**：依相似度重排列與欄，邊緣加樹狀圖；只有在「要看誰跟誰相似」時才重排
  - **相關矩陣／correlogram**：兩軸是同一組變數；Wilke 示範色塊與色圓兩種寫法；配發散色階（−1 到 +1，中點 0）
  - **時間 × 類別矩陣**（星期 × 小時等）：仍是本圖種；若排成日曆版面（週 × 星期、按月份排）就是日曆熱力圖，不算本圖種
- **色階**：單純高低 → 循序色階；有中點（相關係數、相對平均）→ 發散色階；避免彩虹色，優先 Viridis 類感知均勻色階（參考 ColorBrewer、Datawrapper 色階文）
- **備選（何時改用哪一種）**：
  - 要精確比較少數幾個值 → 排序長條／`lollipop-rank.md`
  - 每日一值、要看日曆上哪幾天忙 → **日曆熱力圖**（`calendar-heatmap.md`）
  - 兩軸是同一組網路節點、格子是邊（有無連結／權重）→ **鄰接矩陣**（`adjacency-matrix.md`）
  - 方陣其實是「成對交換／流量」→ **弦圖**（`chord-matrix.md`）
  - 地理分布 → 等值區域圖（`choropleth-map.md`）或圖塊地圖（`tile-map.md`）
  - 兩個連續變數的點事件密度 → 六角分箱（`hexbin-density.md`）／等高線（`contour-density.md`）
  - 要用面積表達占比 → 馬賽克（`mosaic-crosstab.md`）／馬里梅可（`marimekko-chart.md`）
  - 變數兩兩的原始點關係 → 散點（`correlation-scatter.md`）
  - 長時間序列＋穩定週期、要看季節對齊 → 螺旋圖（`spiral-plot.md`；螺旋熱圖的格子嵌在螺旋弧段上，不是本圖種）

## Avoid

- **各欄尺度差很大卻沒正規化**：大數值欄會主導整張圖的顏色 → 先依欄或依列正規化（並在圖注寫明）
- **缺失值塗成零**：缺值用獨立樣式（灰、斜線）並寫進圖例
- **彩虹色盤**：亮度不單調、讀者會看出假邊界；改 Viridis 類或 ColorBrewer 循序／發散色階
- **有固定順序的軸被重排**：時間、等級要保持原順序；只有要看相似度才分群重排
- **與日曆熱力圖混**：日曆版面（週 × 星期）是另一個 pattern；本圖是任意兩個類別軸
- **與鄰接矩陣混**：鄰接矩陣兩軸是同一組節點、格子是邊，而且排序是分析核心；把它當一般相關熱圖畫、又不重排節點，看不出群
- **與弦圖混**：弦圖把同樣的方陣畫成圓周上的帶，重點是交換量；本圖重點是格子強度
- **拿不對的圖當範例**：相關矩陣色塊範例用 Wilke 的 forensic glass 相關矩陣（`wilke-forensic1.png`），不要用 `wilke-correlations.png`（那是相關係數散點示意，不是熱圖）
- **套件寫錯**：R 的 `levelplot` 屬 **lattice**，不是 ggplot2（ggplot2 用 `geom_tile`）
- 列欄極多又不篩選、不分群；格子多還硬塞數字

## Produce checklist

- [ ] 故事句含：哪些列 × 欄組合最熱／最冷，或哪一群變數彼此相關
- [ ] 表：樞紐成列 × 欄 → 一個值（長格式 `row, col, value` 或寬表）；每個組合恰一列，重複鍵先定聚合規則
- [ ] 尺度：各欄（或各列）尺度差很大 → 先正規化，圖注寫「依欄／依列正規化」
- [ ] 色階：循序（單向高低）或發散（中點寫明，例如相關係數 0）；Viridis 類或 ColorBrewer；不用彩虹
- [ ] 缺值：獨立樣式＋圖例「無資料」，不當 0
- [ ] 排序：固定順序（時間、等級）保持原序；要看相似才分群重排（clustermap／樹狀圖），圖注寫排序依據
- [ ] 標註：格子少 → 格內數字；格子多 → 圖例＋懸停提示
- [ ] 工具誠實（只寫素材包證實的）：R（ggplot2 `geom_tile`、lattice `levelplot`、基本 `heatmap()`）；Python（Seaborn `heatmap`／`clustermap`、Plotly）；D3（D3 Graph Gallery）；Flourish Heatmaps（數值與類別版面）；Highcharts。Datawrapper 本輪查無熱圖產品專頁、熱圖部落格文 404，不宣稱原生支援
- [ ] 示範數字標「數字未核」
- [ ] 自檢：這其實是日曆版面（→ 日曆熱力圖）、節點 × 節點的邊（→ 鄰接矩陣）、成對流量（→ 弦圖）嗎？讀者需要精確比較少數值嗎（→ 長條）？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-heatmap.csv` — 長格式 `category, channel, sales_index`；12 個商品大類 × 7 個通路（84 格）的銷售指數。示範讀法：樞紐成 12 列 × 7 欄後用循序色階上色；最熱是文具 × 電商平台A（98）、母嬰 × 門市（96）、家電小物 × 外送平台（94），最冷是乳品 × 電商平台B（9）、日用品 × 門市（10）。七個通路都是同一指數尺度，不必再依欄正規化；通路與商品無固定順序，可依總和排序或分群重排

## 參考連結（可點；皆出自素材包 sources.txt）

- https://datavizcatalogue.com/methods/heatmap.html （定義與構造圖解）
- https://datavizproject.com/data-type/heat-map/
- https://www.data-to-viz.com/graph/heatmap.html
- https://en.wikipedia.org/wiki/Heat_map （歷史例、灰階 vs 彩虹 vs Viridis 色階對照）
- https://clauswilke.com/dataviz/visualizing-associations.html （相關矩陣：色塊與色圓；forensic glass 例）
- https://colorbrewer2.org/
- https://blog.datawrapper.de/which-color-scale-to-use-in-data-vis/ （循序 vs 發散色階怎麼選）
- https://flourish.studio/visualisations/heatmaps/ （Flourish Heatmaps：數值與類別版面）
- https://app.flourish.studio/@flourish/heatmap （Flourish 熱圖範本）
- https://d3-graph-gallery.com/heatmap.html
- https://www.d3-graph-gallery.com/graph/heatmap_basic.html
- https://www.d3-graph-gallery.com/graph/heatmap_style.html
- https://r-graph-gallery.com/heatmap.html （基本 `heatmap()`、ggplot2 `geom_tile`、lattice `levelplot`）
- https://r-graph-gallery.com/283-the-hourly-heatmap.html （時間 × 類別矩陣例）
- https://python-graph-gallery.com/heatmap/
- https://python-graph-gallery.com/91-customize-seaborn-heatmap/ （格內標註）
- https://python-graph-gallery.com/404-dendrogram-with-heat-map/ （分群熱圖＋樹狀圖）
- https://seaborn.pydata.org/generated/seaborn.heatmap.html
- https://seaborn.pydata.org/examples/structured_heatmap.html
- https://seaborn.pydata.org/generated/seaborn.clustermap.html
- https://plotly.com/python/heatmaps/
- https://www.highcharts.com/docs/chart-and-series-types/heatmap
- X 教學原帖（本輪唯一可用）：https://x.com/clcoding/status/2099864539659710972
- 查核限制（未核內容、不列連結）：Datawrapper 無熱圖產品專頁、熱圖部落格文 404；Flourish 熱圖操作教學頁 404；Observable `@d3/heatmap` 429；D3 Graph Gallery `heatmap2_basic` 404

鄰居 pattern：`calendar-heatmap.md`（日曆版面的每日一值；不算本圖種）、`adjacency-matrix.md`（節點 × 節點的邊，排序是核心；不算本圖種）、`chord-matrix.md`（同樣方陣畫成交換帶）、`correlation-scatter.md`（兩變數原始點）、`mosaic-crosstab.md`、`marimekko-chart.md`（面積編碼占比）、`hexbin-density.md`、`contour-density.md`（點資料密度）、`choropleth-map.md`、`tile-map.md`（地理）、`spiral-plot.md`（週期時間序列捲成螺旋）。

圖檔留在教圖／skill-pack（`/workspace/skill-packs/2026-09-26-am-heatmap/images/`，稿內嵌 24 張），本 repo **不複製**大圖。可當範例對照的是 catalogue-anatomy、wiki-heatmap、d3-basic、d3-style、rgg-215-1、rgg-283（時間 × 類別）、pygg-91-annotate（標註熱圖）、pygg-404-cluster、seaborn-cm1、seaborn-structured（分群熱圖）、wilke-forensic1／wilke-forensic2（相關矩陣色塊／色圓）、flourish-numeric、flourish-categorical、flourish-101（Flourish 熱圖編輯介面截圖：左預覽、右設定面板）；色階對照看 wiki-greyscale、wiki-rainbow-viridis、wiki-viridis。相關矩陣**不要**引用 wilke-correlations（散點示意，不是熱圖，也未收進本包）。對帳見 `ATTRIBUTION.md`。
