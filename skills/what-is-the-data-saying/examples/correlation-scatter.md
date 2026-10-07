# Pattern: correlation-scatter

> **圖種**：散點圖（Scatter plot）
> **來源（專案維護者整理）**：`（通用；過密見 hexbin／contour 教圖）`

## When

- 問「是否相關、離群、分群」
- 形狀：數值 × 數值

## Recommend

- **主選**：散點（可加趨勢／分組色）
- **備選**：＋第三量級 → `bubble-chart.md`；點很密 → `hexbin-density.md`／`contour-density.md`；雙序列演化 → `connected-scatter.md`

## Avoid

- 用折線連接無序類別
- 雙軸硬疊兩個不同單位卻不說明
- 無第三連續量級卻硬加點大小裝飾（有第三 size → 氣泡圖，見 `bubble-chart.md`）

## Produce checklist

- [ ] 軸標單位清楚
- [ ] 離群點是否標註或截尾說明
- [ ] 分組色有圖例

鄰居 pattern：`volcano-plot.md`（兩軸語意固定：效應量 × 顯著性，不是任選兩欄）、`ma-plot.md`（兩軸固定為平均表現 A × 對數倍數 M）、`qq-plot.md`（兩軸是對齊同一累積比例的分位數）、`bland-altman.md`（兩欄是同一批樣本的配對量測：相關高不等於一致，要看差值對平均）、`locuszoom.md`（軸固定為區間位置對 −log10(p)，不是任選兩欄）、`pp-plot.md`（軸固定為兩個 0 到 1 的累積機率）、`karyotype-ideogram.md`（染色體形態與帶型，不是任選兩欄）、`contour-density.md`、`hexbin-density.md`、`bubble-chart.md`、`connected-scatter.md`；`forest-plot.md`（效應量加信賴區間的多列比較，一軸只是列的順序，不是兩個變數的關係）。
