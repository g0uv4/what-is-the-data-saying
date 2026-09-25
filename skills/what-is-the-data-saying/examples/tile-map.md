# Pattern: tile-map

> **圖種**：圖塊地圖（Tile map）
> **來源（納茲教圖）**：`teach-viz/2026-09-25-pm-tilemap.md`（首次正式主課；與同日上午等值區域圖分開）
> **亦稱**：格子地圖、statebins（R 套件；Wilke 稱 cartogram heatmap）、tile grid map／grid map（NPR 等新聞編輯室用語）、hexagon map（Datawrapper 底圖名稱）
> **核心**：**每個區域一格、每格一樣大**（方塊或六角），大致照地理相對方位排列，再依數值或類別上色；拿掉等值區域圖「面積大就搶眼」的偏誤。代價是**形狀與鄰接關係失真**，讀者要靠格內縮寫辨認區域

## When

- 問「各州／邦／縣在某比率或類別上怎麼分布」，而且**每區同等重要**（一區一票、一區一政策），不想讓地廣人稀的大區搶走注意力
- 形狀：每區一列 + 區域代碼 + 已正規化指標（比率、人均、通過率）或少數類別狀態；另需一張「區域 → 格座標（row／col）」對照表或現成底圖
- 區域數適中、讀者認得縮寫與大致方位（美國 50+1 州、瑞士各邦、一國各縣）；重點是「幾區屬於哪一類、相鄰區是否同色」，不是「哪塊陸地最大」

## Recommend

- **主選**：圖塊地圖（等大圖塊，一區一格）
  - **方塊圖塊**：橫豎好掃讀、好放縮寫；鄰接較難完整保留
  - **六角圖塊**：多兩個邊，較能保留真實鄰接；掃讀略不直覺（NPR 專文談取捨）
  - **色階**：單向高低 → 順序色；相對全國平均／目標 → 發散色；少數類別 → 質性色；分 4–6 級較好辨認；參考 ColorBrewer
  - **延伸**：geofacet——每格放一張小圖（例如折線），版面仍模擬地理；屬小多圖延伸，不是本課主圖
- **加權變體（另一種圖，勿與主課混寫）**：格數代表人口或選舉人票，大州佔多格——Datawrapper「USA » States: electoral college (hexagons)」底圖、Datawrapper 部落格的 grid cartogram（一格＝固定人數）、Wikipedia Cartogram 條目的鑲嵌式面積變形地圖（mosaic cartogram；例如每個六角＝25 萬人）、Pitch Interactive Tilegrams（依資料比例縮放）。它們的邏輯是「面積∝數量」，屬於**面積變形地圖**家族 → 見 `cartogram-geo.md`
- **備選（何時改用哪一種）**：
  - 要真實邊界、海岸線，或土地面積本身就是故事 → **等值區域圖**（`choropleth-map.md`）
  - 要讓面積反映人口／選票總量 → **面積變形地圖**（`cartogram-geo.md`）或上面的加權變體
  - 點事件疏密 → **點密度地圖**（`dot-density-map.md`）；非行政區的點聚合六角格 → **六角分箱**（`hexbin-density.md`）
  - 點位總量規模 → **比例符號地圖**（bubble map）
  - 只比少數幾區的精確高下 → 排序長條／`lollipop-rank.md`

## Avoid

- **把一區一格與加權變體寫成同一種**：Datawrapper electoral college hexagons、grid cartogram、Wikipedia 鑲嵌式面積變形地圖、Tilegrams 都是「格數＝數量」，不是等大圖塊
- **把色塊面積加總讀成人口或土地**：每格等大，面積不代表任何量 → 標題或圖例寫明「每格＝一個區域，大小不代表人口」
- 用總量（人口、件數）上色：面積已經拉平，更該讓顏色承載可比的比率
- 與**六角分箱（hexbin）**混：hexbin 是把點資料聚到網格，格子沒有區名；R Graph Gallery 那頁標題寫「hexbin map」，實作其實是一州一格的圖塊地圖
- 與**矩陣熱力圖**混：圖塊地圖的排法必須讓讀者看得出國家或地區的大致輪廓
- 區域太多、讀者不熟方位時硬畫 → 會變成認不出的色塊拼圖
- 沒有縮寫標籤、沒說明半區／飛地等特殊格（瑞士半邦是經典例）
- 引用 Wikipedia `Tile_map` 條目當定義（那是電玩 tile 畫面）；FiveThirtyEight 舊文〈How to make a state grid map〉已失效，不引用
- 編造 X 教學原帖：本輪 X 查無可用教學原帖

## Produce checklist

- [ ] 故事句含：幾區屬於哪一類／哪些相鄰區同色，而且「每區同等權重」是刻意選擇
- [ ] 表：每區恰一列、區域代碼完整（對照表或底圖裡的每區都有值，缺值另標）；指標已正規化，單位寫進標題
- [ ] 格座標：每區恰一格；(row, col) 不重複；外形好認、真實鄰居盡量相鄰、東西南北大致正確
- [ ] 方塊 vs 六角二選一（好讀好標 vs 鄰接較完整）
- [ ] 色階：順序／發散（中心值寫明）／質性；圖例必備；缺值灰或斜線＋「無資料」
- [ ] 格內放縮寫、對比足夠；標題或註記寫「每格一區、格子等大」；特殊格（半區、飛地）另註
- [ ] 若其實要「格數＝人口／選舉人票」→ 改做加權變體，並檢查各區格數加總＝總數（例如選舉人票總數），圖例寫「1 格＝N」
- [ ] 必要時旁附一張小的真實邊界等值區域圖做地理對照
- [ ] 工具誠實（只寫教圖證實的）：R `statebins`（美國州等大方塊）、`geofacet`（格內小圖）、R Graph Gallery 美國州六角；Datawrapper「Switzerland › Cantons (square)」、各州等大的「U.S. hexagons」底圖（加權版是 electoral college hexagons）；Python／Plotly（Medium 教學的方塊／六角模板）；Tableau（欄／列座標＋方塊標記）；D3（Bill Mill grid choropleth、d3kit-gridmap）；Flourish 有 grid maps 說明文。Observable `@d3/statebins`、`@d3/tile-map` 本輪 429、CDC COVE hex-map 403，未核內容
- [ ] 示範數字標「數字未核」
- [ ] 自檢：讀者會不會把「一大片同色」讀成「很多人」？圖是不是其實在畫格數＝數量（那是加權變體，找 `cartogram-geo.md`）？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-tilemap.csv` — state + row + col + value_pct；美國西部 9 州排成 3×3 等大方塊（每州一格、row／col 不重複），用 `value_pct` 上色。示範讀法：WA（62）、CO（58）偏高，WY（30）最低；MT、WY 雖然土地大，在圖上和其他州一樣只佔一格

## 參考連結（可點；皆出自素材包 sources.txt）

- https://clauswilke.com/dataviz/geospatial-data.html （Figure 15.16 州級等大方塊；並對照真實面積 choropleth 與 cartogram）
- https://blog.apps.npr.org/2015/05/11/hex-tile-maps.html （NPR：方塊 vs 六角 tile grid，為何改用等大格子）
- https://www.datawrapper.de/blog/tilemap-of-swiss-cantons （瑞士邦方塊圖塊地圖）
- https://www.datawrapper.de/blog/how-to-visualize-the-us-election-2020-with-datawrapper （U.S. hexagons 等大底圖；electoral college hexagons 是選票加權變體）
- https://www.datawrapper.de/maps （地圖總覽；原美國州六角底圖頁已轉址至此）
- https://www.datawrapper.de/blog/cartograms （grid cartogram＝加權變體，對照用）
- https://en.wikipedia.org/wiki/Cartogram （鑲嵌式面積變形地圖＝加權變體）
- https://pitchinteractiveinc.github.io/tilegrams/ （Tilegrams：依資料比例縮放＝加權變體）
- https://github.com/hrbrmstr/statebins
- https://cran.r-project.org/package=statebins
- https://cran.r-project.org/web/packages/geofacet/vignettes/geofacet.html
- https://r-graph-gallery.com/328-hexbin-map-of-the-usa.html （標題寫 hexbin，實為一州一格六角）
- https://billmill.org/d3_grid_choropleth.html
- https://github.com/kristw/d3kit-gridmap
- https://medium.com/data-science-collective/easy-tile-grid-maps-with-python-and-plotly-85d9d6ba05cc
- https://tamasszabo.org/blog/usa-tile-map/ （Tableau 做法，第三方）
- https://flourish.studio/blog/grid-maps-explained/
- https://flourish.studio/visualisations/maps/ （地圖總覽，未專講圖塊地圖）
- https://www.data-to-viz.com/graph/map.html （地圖家族總覽；無獨立 tile map 項目）
- https://colorbrewer2.org/
- 查核限制（未核內容）：https://observablehq.com/@d3/statebins 、https://observablehq.com/@d3/tile-map （429）；https://www.cdc.gov/cove/data-visualization-types/hex-map.html （403）

X 教學原帖：本輪查無（不編造）。

鄰居 pattern：`choropleth-map.md`（真實面積填色；本圖解其大面積低人口偏誤）、`cartogram-geo.md`（面積∝數量；加權六角／方塊變體歸這裡）、`hexbin-density.md`（點聚合，非行政區）、`dot-density-map.md`、`matrix-heatmap.md`、`small-multiples.md`（geofacet 延伸）。

圖檔留在教圖／skill-pack（`/workspace/skill-packs/2026-09-25-pm-tilemap/images/`，稿內嵌 24 張），本 repo **不複製**大圖。可當圖塊地圖範例對照的是 wilke-statebins、dw-swiss-tilemap、dw-swiss-chart、npr-square-tiles、npr-hex-tiles、statebins-*、rgg-usa-hex-*、medium-square、tableau-usa-tile；加權變體對照看 wiki-canada-hex、wiki-germany-hex、dw-cartogram-types。**不要**把 dw-election-hex（文章封面插圖，只有局部六角標記）、medium-hex（一般地理等值區域圖封面）、dw-swiss-compare（疫情圖表拼貼）當圖塊地圖範例引用。對帳見 `ATTRIBUTION.md`。
