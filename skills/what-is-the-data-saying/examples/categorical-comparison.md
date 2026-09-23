# Pattern: categorical-comparison

> **圖種**：長條圖（Bar chart）
> **來源（納茲教圖）**：`（通用；對照 teach-viz 長條相關教圖）`

## When

- 問「誰大／誰小／排名」
- 形狀：1 個類別欄 + 1 個數值欄（可先聚合）
- 類別約 ≤15；更多則 top-N +「其他」、改 table、或見 `circular-bar.md`

## Recommend

- **主選**：排序水平長條（長中文標籤）或垂直長條（短標籤）
- **備選**：高值齊頭要減墨水 → `lollipop-rank.md`；表格 + 條件格式（對帳）
- **少用**：圓餅（僅 ≤4 塊且敘事需要）

## Avoid

- 未排序的類別軸
- 3D、爆炸型圓餅
- 把密時間序列當類別長條

## Produce checklist

- [ ] 按數值排序（除非固有順序）
- [ ] 軸標與單位 zh-TW
- [ ] 標資料期間與來源
- [ ] 類別 >12 時做 top-N 並在圖註說明
