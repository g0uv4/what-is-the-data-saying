# Pattern: choropleth-map

> **圖種**：等值區域圖（Choropleth map）
> **來源（納茲教圖）**：`teach-viz/2026-09-25-am-choropleth.md`（首次正式主課；先前地理課只涵蓋 cartogram／bubble map／flow map／點密度）
> **亦稱**：分級設色圖、等值區劃圖；媒體偶稱「熱力地圖」（≠ 連續密度場，勿混）
> **核心**：行政區／統計區多邊形依**已正規化**指標（比率、每人、每十萬人、每面積密度）填色；邊界與面積維持真實，數值只靠**顏色深淺**。總量不要拿來填色——總量改用**比例符號地圖**

## When

- 問「某比率／密度／人均指標在各區怎麼分布、哪裡偏高偏低、有沒有連片群聚、南北或城鄉差異」
- 形狀：每區一列 + 區域代碼（能對上邊界檔）+ 已正規化指標（或分子＋分母欄可算比率）
- 區域數適中、讀者認得外框；重點是**空間型態**，不是精確前三名排行

## Recommend

- **主選**：等值區域圖
  - **連續色階（unclassed）**：看細緻漸層；較難數「第幾級」
  - **分級色階（classed／binned）**：簡報講高／中／低；圖例寫明分級法——**分位數**（每級區數相同，易放大小差距）、**等距**（每級數值寬相同，偏態時多區擠同一級）、**自然斷點**（Jenks，依資料群聚切）；常見 3–7 級，勿無說明逕切 5 級
  - **色階**：單向高低 → **順序（sequential）**；有中心值（0、全國平均、目標）→ **發散（diverging）**；類別名目 → 質性色（勿套漸層）；參考 ColorBrewer，顧色盲友善
  - 進階：**雙變數（bivariate）**二維色盤，僅概念；確有兩指標關係要講才用
- **備選（何時改用哪一種）**：
  - 要讀**總量規模**（人口數、案件數、總營收）→ **比例符號地圖**（bubble map；圓心在點位、面積∝總量）
  - 要讓**面積＝資料量**、化解大區小區偏誤 → **面積變形地圖**（`cartogram-geo.md`；或方格／statebins）
  - 要看**可數計數的疏密／叢集** → **點密度地圖**（`dot-density-map.md`；等大點、1 點＝N）
  - 要看**起迄流向** → **流向地圖**（flow map）
  - 要精準比少數區 → 排序長條／`lollipop-rank.md` 或表；並列附上最穩

## Avoid

- **直接用總量填色**（人口、件數、總營收）：大區／人多的區自然偏深 → 先正規化，或改比例符號地圖
- **大面積、低人口的視覺偏誤**：地廣人稀區奪走注意力、小而人多的都會區看不見（choropleth illusion）→ 註明「色＝比率，面積＝土地」；必要時並列 cartogram 或排序長條
- 與**面積變形地圖**混（本圖不扭曲面積）；與**比例符號地圖**混（本圖整區填色，不畫點上圓）；與**點密度地圖**混（本圖不撒點）；與**流向地圖**混（本圖無方向）；與 hexbin／等高線或矩陣熱力混（本圖依既有地理邊界）
- 分級不交代方法；發散色卻沒有有意義的中心值；類別資料用漸層
- 缺值區塗成零色或最淺色（缺值 ≠ 0）→ 灰色或斜線網底並在圖例標「無資料」
- 邊界檔年份與統計年份不一致（區劃調整未對齊）
- 寫成 Flourish 有獨立「Choropleth」範本——Maps 產品頁的 Choropleth 卡片實際連到 **Projection map** 範本
- 引用 Observable 舊筆記 `@d3/choropleth`（2023 年 5 月已停用）→ 用新版 **`@d3/choropleth/2`**（本輪網頁可能 429）

## Produce checklist

- [ ] 故事句含：哪裡比率高／低、有無群聚（不是「哪區總量最大」→ 那要比例符號地圖或長條）
- [ ] 指標已正規化（比率／每人／每十萬人／每面積）；分母欄存在且非零；單位寫進標題與圖例
- [ ] 區域代碼與邊界檔同一套編碼、同一年份；join 後檢查未匹配區與缺值
- [ ] 連續 vs 分級；分級時寫出方法（分位數／等距／自然斷點）與級距
- [ ] 色階：順序 vs 發散（中心值寫明）；ColorBrewer／Datawrapper 色階文；色盲友善
- [ ] 缺值：灰／斜線＋圖例「無資料」；標題寫年份與地理層級
- [ ] 只標少數要點名的區或極端值；精確數靠 hover 或附表；示範數標「數字未核」
- [ ] 工具誠實：Datawrapper Choropleth map（Academy 有專文）；Flourish＝**Projection map** 範本；D3（d3-graph-gallery 含 hover 例；Observable 新版 `@d3/choropleth/2`）、R、Python（GeoPandas）、Plotly
- [ ] 自檢：讀者會不會把「顏色深」讀成「人數多」？大面積低人口區是否誤導？會不會被看成 bubble map 或 cartogram？隱藏填色改撒點才說得清 → 該用點密度地圖

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-choropleth.csv` — region + region_code + population + cases + rate_per_100k；示範「用 `rate_per_100k` 上色，不用 `cases` 總量」（北區件數最多，但比率最高的是東區）

## 參考連結（可點；教圖已核狀態）

- https://datavizcatalogue.com/methods/choropleth.html
- https://datavizproject.com/data-type/choropleth-map/ （轉址至 `choropleth-map-2/`）
- https://www.data-to-viz.com/graph/choropleth.html
- https://www.data-to-viz.com/graph/map.html （地圖家族總覽）
- https://en.wikipedia.org/wiki/Choropleth_map （正規化、分級、色階、雙變數）
- https://clauswilke.com/dataviz/geospatial-data.html （人口密度／所得分箱 vs cartogram 對照）
- https://blog.datawrapper.de/choroplethmaps/
- https://blog.datawrapper.de/which-color-scale-to-use-in-data-vis/
- https://www.datawrapper.de/maps
- https://www.datawrapper.de/academy/what-to-consider-when-creating-choropleth-maps
- https://www.datawrapper.de/academy/category/choropleth-maps
- https://colorbrewer2.org/
- https://flourish.studio/visualisations/maps/
- https://app.flourish.studio/@flourish/projection-map
- https://d3-graph-gallery.com/choropleth.html
- https://www.d3-graph-gallery.com/graph/choropleth_basic.html
- https://d3-graph-gallery.com/graph/choropleth_hover_effect.html
- https://r-graph-gallery.com/choropleth-map.html
- https://python-graph-gallery.com/choropleth-map/
- https://plotly.com/python/choropleth-maps/
- https://observablehq.com/@d3/choropleth/2 （新版；舊 `@d3/choropleth` 已停用；本輪網頁可能 429）

X 教學原帖（Liora 已逐則核對帳號與內文）：

- https://x.com/Africa_DataHub/status/2097233483903160540 — 免費課：Mapshaper＋Datawrapper＋Flourish 做 choropleth
- https://x.com/World_Data_A/status/2099152833253638574 — choropleth illusion（大面積視覺偏誤）
- https://x.com/tableaupublic/status/2100593181209297136 — Highlight／Heat／Density／Choropleth 辨異
- https://x.com/JoachimSchork/status/2101027736395378725 — 雙變數等值區域圖（Python 套件 bivario）

鄰居 pattern：`dot-density-map.md`、`cartogram-geo.md`、`bubble-chart.md`（笛卡兒氣泡，≠ bubble map）、`hexbin-density.md`、`matrix-heatmap.md`。

圖檔與截圖留在教圖／skill-pack（`/workspace/skill-packs/2026-09-25-am-choropleth/images/`，稿內嵌 24 張），本 repo **不複製**大圖；對帳見 `ATTRIBUTION.md`。
