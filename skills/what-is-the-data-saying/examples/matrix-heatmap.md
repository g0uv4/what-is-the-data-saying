# Pattern: matrix-heatmap

## When

- 問「哪一格特別高／低」
- 形狀：兩個類別維度 + 一數值（或相關矩陣）

## Recommend

- **主選**：heatmap（連續色盲友善色階，如 viridis／藍–白–紅 發散）
- **備選**：sorted clustered heatmap；精確值用 table 並存

## Avoid

- 彩虹無序色階表達數量
- 類別極多又不聚合（先 roll-up）

## Produce checklist

- [ ] 發散資料用中性中點（0 或平均）
- [ ] 色階圖例有單位
- [ ] 軸標可讀（必要時縮寫 + 全名表）
