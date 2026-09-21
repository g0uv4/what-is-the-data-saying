# Pattern: categorical-comparison

## When

- 問「誰大／誰小／排名」
- 形狀：1 個類別欄 + 1 個數值欄（可先聚合）
- 類別約 ≤15；更多則 top-N +「其他」或改 table

## Recommend

- **主選**：sorted horizontal bar（長中文標籤）或 vertical bar（短標籤）
- **備選**：table + 條件格式（對帳／精確值）
- **少用**：pie（僅 ≤4 塊且敘事需要）

## Avoid

- 未排序的類別軸
- 3D、爆炸型圓餅
- 把時間當一般類別卻用 bar 塞滿每日（改 line）

## Produce checklist

- [ ] 按數值排序（除非有固有順序）
- [ ] 軸標與單位 zh-TW
- [ ] 標資料期間與來源
- [ ] 類別 >12 時做 top-N 策略並在圖註說明
