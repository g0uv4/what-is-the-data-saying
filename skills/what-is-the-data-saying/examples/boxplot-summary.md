# Pattern: boxplot-summary

> **圖種**：箱形圖（Box plot／Box-and-whisker plot）
> **來源（納茲教圖）**：`teach-viz/2026-09-23-pm-boxplot.md`（正式專題；雨雲／小提琴僅當鄰居）
> **亦稱**：盒鬚圖、箱線圖；工具常寫 Boxplot
> **核心**：五數摘要＋（可選）離群——箱＝IQR、中線＝中位數、鬚＝規則內非離群範圍、點＝離群；拿手**並排比多組分布**

## When

- 問「多組同單位數值的分布中心、離散、偏斜與離群，要在有限版面並排比較」
- 形狀：連續／可排序數值（+ 類別組別）；組數約數個至數十；重點是摘要不是每個點
- EDA 先掃中位數／IQR／離群，再決定要不要升小提琴／雨雲

## Recommend

- **主選**：箱形圖（垂直或水平；多組並排最常見；長標籤／多組 → 水平）
  - 鬚規則寫清（常見 1.5×IQR 圍籬內最遠觀測；或 min–max）
  - 可選：平均菱形／十字（≠ 中位數）、可變寬度（反映 n）、缺口（粗示中位不確定性）、箱上疊 jitter
- **備選**：要密度／雙峰 → **小提琴**；雲＋雨＋傘 → **雨雲**；要每個點 → **蜂群**；單組細形狀 → 直方／密度；多組密度漂移 → 山脊；類別單值 → 長條／棒棒糖

## Avoid

- 硬把**小提琴**（密度形狀）、**雨雲**（複合）、**蜂群**（每點）叫成「就是箱形」
- 雙峰／多峰卻只給純箱形（data-to-viz 核心陷阱；需時疊 jitter 或改鄰居）
- n 很小、組間 n 差很大卻不標 n、不疊點 → 易誤判「哪組比較好」
- 類別只有**單一彙總值**卻畫箱（應長條／棒棒糖）
- 把中線當平均值；鬚規則不寫；離群直接刪而不查
- 宣稱 Datawrapper「有原生箱形」——**無**；勿寫成一鍵產品

## Produce checklist

- [ ] 故事句含：多組分布摘要（中位／IQR／離群）（不是「讀出每個點」或「完整密度」）
- [ ] 資料：value（+ group）；同單位；缺值處理寫進圖脚
- [ ] 鬚規則、是否標平均、各組 n= 寫清；示範數標「數字未核」
- [ ] 無固有序可依中位數／IQR 排序；長標籤用水平
- [ ] 工具誠實：Catalogue／Dataviz Project／Wikipedia／Wilke／D3／R／Python Gallery／RAWGraphs／Plotly 有路徑；Flourish Help 深鏈本輪可能改版轉首頁；**Datawrapper 無原生箱形**；data-to-viz `graph/boxplot` 本輪 **404**（caveat 可用）；Observable @d3/box-plot 本輪可能 **429**
- [ ] 自檢：讀者會不會把中線當平均？純箱形是否藏了雙峰？離群是查因還是硬刪？

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `sample-boxplot.csv` — group + value（三組數值示意）

## 參考連結（可點；教圖已核狀態）

- https://datavizcatalogue.com/methods/box_plot.html
- https://datavizcatalogue.com/blog/box-plot-variations/
- https://datavizproject.com/data-type/box-plot/
- https://www.data-to-viz.com/caveat/boxplot.html （caveat；`graph/boxplot`＝404）
- https://en.wikipedia.org/wiki/Box_plot
- https://clauswilke.com/dataviz/boxplots-violins.html
- https://d3-graph-gallery.com/boxplot.html
- https://r-graph-gallery.com/boxplot.html
- https://python-graph-gallery.com/boxplot/
- https://rawgraphs.io/learning/how-to-make-a-boxplot/
- https://plotly.com/python/box-plots/
- https://help.flourish.studio/article/128-how-to-make-a-boxplot （深鏈可能改版）
- https://www.datawrapper.de/charts （無原生 box-plot 產品頁）

鄰居 pattern：`violin-distribution.md`、`raincloud-combo.md`、`beeswarm-points.md`。

圖檔與截圖留在教圖／skill-pack（`/workspace/skill-packs/2026-09-23-pm-boxplot/images/`，稿內嵌約 24 張），本 repo **不複製**大圖；對帳見 `ATTRIBUTION.md`。
