# Pattern: lollipop-rank

> **圖種**：棒棒糖圖（Lollipop chart／Lollipop plot）
> **來源（納茲教圖）**：`teach-viz/2026-09-23-am-lollipop.md`（正式專題；啞鈴課僅列鄰居）
> **核心**：一類別一數值；自基線（常是 0）拉細莖，末端一點；眼睛讀點落點（與莖長）

## When

- 問「多個類別各自一個同單位數值誰高誰低／排名」——要比長條更減墨水、減高值齊頭時的莫列紋
- 形狀：類別 + 單一數值；類別名長 → 水平；約十～數十類
- 基線可以是 0、目標或平均（須寫清語意）

## Recommend

- **主選**：棒棒糖圖（單點＋自基線細莖；無固有序就依數值排序；可灰底＋少數強調色）
- **備選**：要面積感或讀者不熟點圖 → **長條**；同一類別兩端差 → **啞鈴**；未排序且無天然序 → 長條常更好讀

## Avoid

- 同一列塞兩個點＋互連卻叫棒棒糖（那是**啞鈴**；Flourish 等公開作標題含 lollipop 時以視覺為準）
- 硬加誤差棒／多值當單莖；分布／離群 → 蜂群／雨雲／小提琴
- 多期連續趨勢 → 折線／凹凸／連接散點
- 宣稱 Datawrapper「有原生 Lollipop」——實際近路是 Dot Plot；雙端差走 Range Plot
- 圓點過大讓人對齊外緣而非圓心

## Produce checklist

- [ ] 故事句含：相對基線的高低／排名（不是兩條件差距）
- [ ] 資料：category + value（同單位）；無天然序 → 依數值排序
- [ ] 寫清基線語意（0／目標／平均）；長標籤用水平
- [ ] 點等大為主；少數強調色、其餘灰；示範數標「數字未核」
- [ ] 工具誠實：D3／R／Python Graph Gallery 有專頁；Flourish Help 有作法；Datawrapper → Dot Plot（單點）或長條，Range Plot＝啞鈴；Catalogue／Wikipedia Lollipop 專條本輪 404；Observable 可能 429
- [ ] 自檢：拔掉莖只留點敘事是否仍成立；外觀會不會被讀成啞鈴或誤差棒

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `lollipop-categories.csv` — 類別 + 單一數值（頻道淨增示意）

## 參考連結（可點；教圖已核狀態）

- https://datavizproject.com/data-type/lollipop-chart/
- https://www.data-to-viz.com/graph/lollipop.html
- https://d3-graph-gallery.com/lollipop.html
- https://r-graph-gallery.com/lollipop-plot.html
- https://python-graph-gallery.com/lollipop-plot/
- https://help.flourish.studio/article/130-how-to-make-a-lollipop-chart
- https://www.datawrapper.de/charts/dot-plot
- https://academy.datawrapper.de/article/384-how-to-create-a-dot-plot
- https://en.wikipedia.org/wiki/Dot_plot_(statistics) （相近；Lollipop_chart 專條＝404）

圖檔與截圖留在教圖／skill-pack（`/workspace/skill-packs/2026-09-23-am-lollipop/images/`，稿內嵌約 24 張），本 repo **不複製**大圖；對帳見 `ATTRIBUTION.md`。
