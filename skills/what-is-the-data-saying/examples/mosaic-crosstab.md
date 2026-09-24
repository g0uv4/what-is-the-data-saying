# Pattern: mosaic-crosstab

> **圖種**：馬賽克圖（Mosaic plot）
> **來源（納茲教圖）**：`teach-viz/2026-09-03-am-mosaic.md`
> **核心**：列聯表的聯合／條件／邊際比例；常搭配獨立性殘差著色。商用「變寬堆疊／市場地圖」請改走 `marimekko-chart.md`

## When

- 問「交叉表邊際／條件／聯合比例」或「兩類別是否偏離獨立」
- 形狀：≥2 類別 + 計數

## Recommend

- **主選**：馬賽克圖（統計列聯／獨立性主線）
- **備選**：多維頻率帶 → 平行集合；商用區隔規模 × 區內組成 → `marimekko-chart.md`

## Avoid

- 「馬賽克」被讀成打碼；獨立≠面積一樣
- 與商用 **Marimekko／Mekko（變寬堆疊）** 混成同一課——名稱常被 Catalogue／Wikipedia 綁在一起，但主線不同 → `marimekko-chart.md`

## Produce checklist

- [ ] 欄寬=邊際、格高=條件、面積=聯合
- [ ] 標題寫全名；若著色殘差，圖例說明獨立性語意
