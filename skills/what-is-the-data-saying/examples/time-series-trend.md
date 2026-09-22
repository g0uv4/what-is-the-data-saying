# Pattern: time-series-trend

> **圖種**：折線圖（Line chart）
> **來源（納茲教圖）**：`（通用；對照 teach-viz 溪流／凹凸／坡度等時間教圖）`

## When

- 問「怎麼變、事件前後」
- 形狀：時間 + 數值（+ 少許系列）

## Recommend

- **主選**：折線圖（≤3 系列）
- **備選**：多實體 → 小多圖；組成河（河流圖）→ `streamgraph-composition.md`；兩期 only → `slope-two-period.md`

## Avoid

- 單圖重疊 20+ 線
- 用每日長條塞滿密日資料

## Produce checklist

- [ ] 時間軸解析度與故事一致
- [ ] 系列過多改小多圖或篩選
- [ ] 標事件註記（若有）
- [ ] 單位／來源 zh-TW
