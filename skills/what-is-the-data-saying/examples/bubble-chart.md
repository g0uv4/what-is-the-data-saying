# Pattern: bubble-chart

> **圖種**：氣泡圖（Bubble chart／Bubble plot）
> **來源（納茲教圖）**：`teach-viz/2026-09-24-am-bubble.md`（正式專題；比例符號地圖／bubble map 僅當鄰居）
> **亦稱**：氣泡散點圖
> **核心**：笛卡兒 X／Y 上每個實體一個圓；圓的**面積**＝第三數值（**非**半徑／直徑）；顏色可選；眼睛先讀散點關係，大小只宜粗比量級

## When

- 問「兩個數值變數的關聯」，同時要交代第三個連續量級（人口、營收、樣本數、市值…）
- 形狀：entity + x + y + size（非負）；可選 category 上色；實體數適中（約數十～一百多）
- 讀者接受「大小只能粗比」，版面備 **size 圖例**（數位圖另加懸停）

## Recommend

- **主選**：氣泡圖（靜態截面最常見；動態時間軸／標註離群／互動 tooltip 皆屬同家族）
  - X／Y＝關聯最強的兩維；size＝「一併交代、無須精讀」的第三維
  - 必須**面積映射**；半透明＋大氣泡在下／小在上緩重疊；只標少數離群或重點實體
- **備選**：只要兩變數 → **散點**；第三變數要精準排名 → **長條／棒棒糖／表**；地理分布 → **比例符號地圖（bubble map）**；多期同一實體軌跡 → **連結散點**；點過密 → hexbin／等高線

## Avoid

- 與**比例符號地圖／bubble map**混（圓在地理經緯 ≠ 笛卡兒數值軸）
- 與普通散點混（無第三 size 卻硬加裝飾大小）
- 與連結散點混（多期折線軌跡 ≠ 單截面一實體一圓）
- 與圓堆／Treemap 混（階層面積占比，**無** X／Y 關聯軸）
- 與六角分箱／等高線混（密度聚合 ≠ 每實體可辨氣泡）
- 把數值映到**半徑／直徑**（直徑×2 → 面積×4，嚴重扭曲）
- 宣稱 Datawrapper「有獨立 Bubble 按鈕」——實際是 **Scatter Plot 綁 size**；勿寫成一鍵產品
- 虛構 data-to-viz caveat/bubble、RAWGraphs make-a-bubble-chart、Datawrapper bubble 部落格（本輪 **404**）；Observable `@d3/bubble-chart` 本輪可能 **429**；X 無可用教學原帖（勿編造）

## Produce checklist

- [ ] 故事句含：X×Y 關聯＋第三量級粗比（不是「從大小精讀排名」或「地理哪裡大」）
- [ ] 資料：entity + x + y + size（非負；負值須先轉換並圖脚揭露）；可選 region／category；示範數標「數字未核」
- [ ] **面積映射**（工具若只給半徑 → 先開根號或勾 scale-by-area）；必備 size 圖例（≥2～3 參考圓）
- [ ] 防重疊：透明度、圖層順序；標籤只給少數離群／重點
- [ ] 工具誠實：Catalogue／Dataviz Project／data-to-viz graph/bubble／Wikipedia／Wilke／D3／R／Python Gallery／Plotly／Gapminder／Flourish 模板有路徑；**Datawrapper＝Scatter 綁 size，無獨立 Bubble**；caveat/bubble、RAWGraphs 教學、DW bubble 部落格＝**404**；Observable 可能 **429**；X＝找不到
- [ ] 自檢：拿掉 size 只留散點，主故事是否仍成立？讀者會不會把直徑當數值？會不會誤讀成 bubble map？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-bubble.csv` — entity + x_gdp_pc + y_life_exp + size_pop_m + region（Gapminder 風格示意）

## 參考連結（可點；教圖已核狀態）

- https://datavizcatalogue.com/methods/bubble_chart.html
- https://datavizproject.com/data-type/bubble-chart/
- https://www.data-to-viz.com/graph/bubble.html （`caveat/bubble`＝404）
- https://en.wikipedia.org/wiki/Bubble_chart
- https://clauswilke.com/dataviz/visualizing-associations.html
- https://d3-graph-gallery.com/bubble.html
- https://r-graph-gallery.com/bubble-chart.html
- https://python-graph-gallery.com/bubble-plot/
- https://plotly.com/python/bubble-charts/
- https://www.gapminder.org/tools/
- https://app.flourish.studio/@flourish/bubble-chart
- https://www.datawrapper.de/charts/scatter-plot （Scatter 綁 size；無獨立 Bubble；bubble 部落格＝404）
- https://rawgraphs.io/learning/make-a-bubble-chart/ （本輪 404）
- https://observablehq.com/@d3/bubble-chart （本輪可能 429）

鄰居 pattern：`correlation-scatter.md`、`connected-scatter.md`、`dot-density-map.md`（地理鄰居另見 heuristics 比例符號地圖列）。

圖檔與截圖留在教圖／skill-pack（`/workspace/skill-packs/2026-09-24-am-bubble/images/`，稿內嵌約 24 張），本 repo **不複製**大圖；對帳見 `ATTRIBUTION.md`。
