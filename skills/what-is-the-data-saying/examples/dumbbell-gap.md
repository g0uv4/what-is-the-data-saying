# Pattern: dumbbell-gap

> **圖種**：啞鈴圖（Dumbbell chart）
> **來源（專案維護者整理）**：`teach-viz/2026-09-07-pm-dumbbell.md`

## When

- 問「同一批類別兩個數值差多少、誰差最大」
- 形狀：類別 + 兩個同單位數值

## Recommend

- **主選**：啞鈴圖（Datawrapper **Range Plot**）
- **備選**：兩期軌跡／名次感 → 坡度圖；只要相對 0 的單值 → 棒棒糖

## Avoid

- 畫成坡度圖雙垂直軸卻說在比每列差距
- 兩端單位不同
- 多期連續趨勢硬塞成啞鈴

## Produce checklist

- [ ] 兩點 + 連線；按差距或某一端排序
- [ ] 兩端分色／形狀；圖例寫死語意與單位
- [ ] 精準對帳仍以表為準

鄰居 pattern：`forest-plot.md`（多項研究的估計加信賴區間與合併菱形；啞鈴圖只有兩點，沒有區間與權重）。
