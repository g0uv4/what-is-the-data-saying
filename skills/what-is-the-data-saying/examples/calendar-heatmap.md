# Pattern: calendar-heatmap

> **圖種**：日曆熱力圖（Calendar heatmap）
> **來源（納茲教圖）**：`teach-viz/2026-09-19-pm-calendar.md`

## When

- 問「哪幾天忙、哪段連打」
- 形狀：可聚成每日一值

## Recommend

- **主選**：日曆熱力圖（週×星期）
- **備選**：連續趨勢 → 折線

## Avoid

- 與鄰接矩陣／類別熱力混淆；時區不標
- 任意兩個類別軸（例如星期 × 小時、商品 × 通路）不排日曆版面 → 那是矩陣熱圖（`matrix-heatmap.md`）

## Produce checklist

- [ ] 聚合每日一值
- [ ] 圖注：週起始、時區、零 vs 無資料

鄰居 pattern：`matrix-heatmap.md`（任意兩個類別軸的色階矩陣；日曆版面才歸本檔）、`time-series-trend.md`。
