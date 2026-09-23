# Pattern: population-pyramid

> **圖種**：人口金字塔（Population pyramid／age-sex pyramid）
> **來源（納茲教圖）**：`teach-viz/2026-09-22-pm-pyramid.md`（正式專題）
> **亦稱**：年齡性別金字塔、age structure pyramid；工具常以 Split Bars＋Mirror 建置

## When

- 問「某群體在各年齡層怎麼分布、整體是擴張／穩定／收縮、兩側是否失衡」
- 形狀：可排序年齡組 × 雙側對照（典型男／女，或本籍／外籍等）× 人數或占比
- 敘事重點是**輪廓形態**與特定年齡帶突起／缺口，不是單一長條精準競賽

## Recommend

- **主選**：人口金字塔（左右對開水平條；常見男左女右；橫軸對稱同尺）
  - 跨地／跨國比較優先**占比**；強調母體規模用絕對人數
  - 兩城／兩年對照 → 小多圖並列（同尺），勿硬疊一圖
- **備選**：只要單側排序比大小 → 水平長條；多側對照 → facets；年齡組成歷年演變 → 堆疊面積／時間序列（非單年金字塔）

## Avoid

- 只有總人口、無年齡分組
- 把**龍捲風／蝴蝶圖**（敏感度／正負因子）當成人口金字塔
- 左右軸自動縮放不同 max → 某一側「看起來比較大」
- 對照群體 >2 硬塞雙側；非二元性別框架勿硬套傳統左右語意
- 指望精讀同年齡層細微差額卻類別極多、標籤打架 → 改表或單側條

## Produce checklist

- [ ] 故事句含：擴張／穩定／收縮輪廓或青年膨脹／高齡壺形（不是「讀出某組精確人」為主）
- [ ] 資料：age_group（可排序、間距盡量一致）+ 左／右側度量；長表（age, sex, count）或寬表（age, male, female）
- [ ] 左右橫軸**共用同一 max**；單位（人／千人／％）與年齡組距寫清
- [ ] 標年份／地理範圍；關鍵缺口／隆起加註；示範數標「數字未核」
- [ ] 工具誠實：Datawrapper Split Bars＋Mirror Bars；Flourish Population Pyramid；Vega／amCharts／Tableau；Observable D3 本輪可能 429
- [ ] 自檢：左右對調或改單側條後若問題變成「同年齡差額」→ 改表／點距；若問扶養比長期走勢 → 時間序列，勿單年金字塔硬答

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `population-pyramid-long.csv` — 長表（age_group, sex, count）
- `population-pyramid-wide.csv` — 寬表（age_group, male, female）

## 參考連結（可點；教圖已核狀態）

- https://datavizcatalogue.com/methods/population_pyramid.html
- https://datavizproject.com/data-type/population-pyramid/
- https://en.wikipedia.org/wiki/Population_pyramid
- https://www.datawrapper.de/academy/how-to-create-a-population-pyramid
- https://www.datawrapper.de/charts/population-pyramid
- https://help.flourish.studio/article/88-how-to-make-a-population-pyramid
- https://www.populationpyramid.net/japan/2023/
- https://vega.github.io/vega/examples/population-pyramid/
- https://www.amcharts.com/demos/population-pyramid/
- https://population.un.org/wpp/

圖檔與截圖留在教圖／skill-pack（`/workspace/skill-packs/2026-09-22-pm-pyramid/images/`，約 19 張），本 repo **不複製**大圖；對帳見 `ATTRIBUTION.md`。
