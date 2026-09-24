# Pattern: marimekko-chart

> **圖種**：馬里梅可圖（Marimekko chart／Mekko chart）
> **來源（納茲教圖）**：`teach-viz/2026-09-24-pm-marimekko.md`（正式專題；馬賽克圖僅當鄰居）
> **亦稱**：變寬堆疊長條圖、二維堆疊柱狀圖；商業軟體常寫 Mekko／Marimekko
> **核心**：欄寬＝外層區隔佔整體比重；欄內色帶高度＝區隔內組成；色塊面積＝該組合對整體的貢獻。主線是商用「變寬堆疊」，**不是**統計列聯／獨立性檢定的馬賽克圖

## When

- 問「哪個市場／區隔最大」，同時要拆「每個區隔裡誰佔多少」
- 形狀：外層類別 + 內層組成 + 可加總度量（營業額、出貨量、人數…）；外層約 3–8 欄、內層約 3–7 色
- 讀者要一眼看「市場結構全景」：寬度＝規模、高度＝區內占比（或絕對值軸下的絕對堆疊）

## Recommend

- **主選**：馬里梅可圖／Mekko（百分比軸最常見；絕對值／單位軸＝Bar Mekko；橫向＝Bar Marimekko）
  - 百分比軸：每欄總高固定 100%，欄寬＝區隔總量占比
  - 絕對值軸：縱軸為單位數值，欄高亦隨總量變；仍用欄寬編碼區隔規模
  - 色塊直接標籤優於遠端圖例；標題寫清「寬度＝……；高度＝……」
- **備選**：只要區隔總量 → **長條**；只要區內占比、規模同等重要 → **等寬 100% 堆疊長條**；嚴格樹狀階層 → **Treemap／冰柱／旭日**；要檢定兩類別獨立性 → **馬賽克圖**（`mosaic-crosstab.md`）

## Avoid

- 與**馬賽克圖（Mosaic plot）**混成同一圖種——幾何家族相近，但教學主線不同：馬賽克＝列聯表／獨立性殘差；本圖＝商用區隔規模 × 區內組成。Catalogue／Wikipedia／Qlik 常把名稱綁在一起，**本 pattern 拆開寫**
- 與**等寬堆疊／100% 堆疊長條**混（欄寬固定 ≠ 欄寬帶資訊）
- 與 **Treemap** 混（階層面積嵌套，無「外層類別沿軸、寬度＝邊際占比」敘事）
- 與桑基／平行集合混（有向流量／連帶路徑 ≠ 平面色塊分割）
- 與 Highcharts **Variwide** 直接等同（常為單系列變寬，未必含雙維組成）
- 外層或內層類別過多、細長色帶難讀卻不合併「其他」
- 要精確比較「不同欄中同一顏色」的色塊高度（面積＋未對齊基線弱於分組長條／表）
- 宣稱 Datawrapper「有原生 Marimekko」——**無**；僅有部落格手動示範。勿寫成一鍵產品
- 虛構 X 教學原帖（本輪**找不到**）；勿假裝 data-to-viz mosaic 專頁可用（本輪 **404**）；Tableau 教學可能 **403**；Observable mosaic 可能 **429**

## Produce checklist

- [ ] 故事句含：區隔誰大＋區內怎麼拆（不是「獨立性殘差」或「等寬堆疊就夠」）
- [ ] 資料：segment + product（或外層×內層）+ value（非負可加總）；先算每欄總量與欄內占比；示範數標「數字未核」
- [ ] 軸模式選清：百分比軸 vs 絕對值軸；欄寬語意寫在圖上
- [ ] 外層／內層排序統一（常依總量大→小）；極小組成合併「其他」；色序全圖一致
- [ ] 欄寬占比加總 ≈ 100%；百分比軸下每欄內部占比加總＝100%
- [ ] 標註：大色塊可直標 %／值；細帶改圖例或 hover
- [ ] 工具誠實：Flourish／think-cell／Qlik／Domo／Mekko Graphics／AnyChart 有原生路徑；Excel 無原生（常見＝堆疊面積＋累積寬度，見 Deckary）；**Datawrapper 無原生**（僅手動拼湊文）；Tableau 需手動算欄寬（本輪抓文可能 403）；data-to-viz mosaic＝**404**；Semiotic 舊例可能 **404**；Observable `@d3/mosaic-plot` 可能 **429**；X＝找不到教學原帖
- [ ] 自檢：抽掉寬度變化只留等寬堆疊，主故事還成立嗎？讀者會不會跟馬賽克獨立性搞混？類別是否過多？會不會把面積當唯一精準尺？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-marimekko.csv` — segment + product + value（四區 × 三品類示意）

## 參考連結（可點；教圖已核狀態）

- https://datavizcatalogue.com/methods/marimekko_chart.html （內文「Also known as Mosaic」→ 本課拆開）
- https://datavizproject.com/data-type/marimekko-chart/
- https://en.wikipedia.org/wiki/Marimekko_chart
- https://en.wikipedia.org/wiki/Mosaic_plot （鄰居對照，非本圖主線）
- https://clauswilke.com/dataviz/nested-proportions.html （嵌套占比／馬賽克對照）
- https://flourish.studio/visualisations/marimekko-charts/
- https://helpcenter.flourish.studio/hc/en-us/articles/8761553749007-Marimekko-charts-an-overview
- https://app.flourish.studio/@flourish/marimekko
- https://www.think-cell.com/en/resources/manual/mekko
- https://help.qlik.com/en-US/sense/May2026/Subsystems/Hub/Content/Sense_Hub/Visualizations/Mekko-Chart/mekko-chart.htm
- https://www.domo.com/learn/charts/marimekko-chart
- https://www.mekkographics.com/
- https://www.mekkographics.com/global-cloud-data-centers/
- https://docs.anychart.com/Basic_Charts/Marimekko_Chart
- https://deckary.com/blog/marimekko-chart-excel （Excel 無原生）
- https://blog.datawrapper.de/ukraine-war-wheat-shortage/ （手動拼湊；**非**原生 Marimekko）
- https://www.highcharts.com/docs/chart-and-series-types/variwide-chart （鄰居 Variwide）
- https://www.tableau.com/blog/how-build-marimekko-chart-tableau-58153 （本輪可能 403）
- https://www.data-to-viz.com/graph/mosaic.html （本輪 404）
- https://observablehq.com/@d3/mosaic-plot （本輪可能 429）

鄰居 pattern：`mosaic-crosstab.md`、`treemap-composition.md`、`sankey-flow.md`、`alluvial-stages.md`。

圖檔與截圖留在教圖／skill-pack（`/workspace/skill-packs/2026-09-24-pm-marimekko/images/`，稿內嵌約 23 張），本 repo **不複製**大圖；對帳見 `ATTRIBUTION.md`。
