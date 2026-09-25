# Pattern: dot-density-map

> **圖種**：點密度圖（Dot density map／Dot distribution map）
> **來源（納茲教圖）**：`teach-viz/2026-09-21-pm-dotdensity.md`
> **亦稱**：點描圖、地理脈絡下的 dot map／point map

## When

- 問「計數在地圖上哪裡密、哪裡空」——人口、案件、設備、會員等**可數總量**的空間分布與叢集
- 想避開分區著色圖「大行政區視覺權重過高」；又不想把總量壓成單一大氣泡
- 多類別等大著色點（同尺寸、不同色）看區域組成
- 一對一：真實經緯度事件／設施落點（讀位置，不讀單點規模）

## Recommend

- **主選**：點密度圖
  - **一對多**：一點＝固定單位（Dot Value），在多邊形內演算法灑點
  - **一對一**：一點＝一筆真實座標
- **備選**：比率／人均 → **等值區域圖（choropleth）**（`choropleth-map.md`）；少數具名城市比規模 → **比例符號地圖**；起迄流向 → **流量地圖**；非地理兩軸＋第三 size → `bubble-chart.md`（笛卡兒氣泡，≠ bubble map）；非地理兩軸密度 → hexbin／等高線（勿當地圖）

## Avoid

- 把比率／成長率當主軸仍畫點密度
- 點尺寸隨數值縮放（那是比例符號／氣泡地圖）
- 圖例漏標「1 點＝？單位」
- 把 Datawrapper／Flourish 標記圖／Size-by 氣泡**假裝**成原生一對多多邊形灑點
- 把演算法灑點讀成真實門牌；把 John Snow 式歷史疾病點混成一對多行政區配置
- 跨大緯度比密度卻不交代投影／等積限制

## Produce checklist

- [ ] 故事句含：疏密／叢集（不是單點變大變小）
- [ ] 先選一對多或一對一；欄位契約對得上（多邊形+計數+Dot Value，或 lat/lon）
- [ ] 圖例必寫「1 點＝N 單位」；點等大；必要時標統計期間與「數字未核」
- [ ] 校準 Dot Value／點徑：最密不糊成色塊、最疏仍看得出相對差
- [ ] 工具誠實：一對多 → ArcGIS Pro Dot Density／Atlas／QGIS；一對一 → Datawrapper Symbol map（勿 Size by）或 Flourish Marker／Projection Points
- [ ] 自檢：隱藏點後若只靠填色就夠 → 該用 choropleth（`choropleth-map.md`）；點少且大小不一 → 實際是比例符號

## 虛構 demo 資料

見 `examples/data/`（**虛構示意，數字未核**）：

- `dot-density-one-to-many.csv` — 縣市人口灑點構想
- `dot-density-one-to-one.csv` — 設施／事件落點

## 參考連結（可點；教圖已核狀態）

- https://datavizcatalogue.com/methods/dot_map.html （`dot_density_map.html`＝404）
- https://datavizproject.com/data-type/dot-density-map/
- https://en.wikipedia.org/wiki/Dot_distribution_map
- https://pro.arcgis.com/en/pro-app/latest/help/mapping/layer-properties/dot-density.htm
- https://atlas.co/create/dot-density-maps/
- https://www.visualizing.org/dot-density-map

圖檔與截圖留在教圖／skill-pack，本 repo **不複製**大圖；對帳見 `ATTRIBUTION.md`。
