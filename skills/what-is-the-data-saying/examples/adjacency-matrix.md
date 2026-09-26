# Pattern: adjacency-matrix

> **圖種**：鄰接矩陣（Adjacency matrix）
> **來源（納茲教圖）**：`teach-viz/2026-09-18-am-adjacency.md`

## When

- 問「節點×節點有無邊／權重，重排後看團」
- 形狀：邊表或方陣

## Recommend

- **主選**：鄰接矩陣
- **備選**：直覺圖 → 力導向／弧線

## Avoid

- 不重排；與相關熱力混淆（兩軸同一組節點、格子是邊 ≠ 矩陣熱圖的任意兩類別軸，見 `matrix-heatmap.md`）

## Produce checklist

- [ ] 排序最關鍵
- [ ] 圖注寫排序依據與有向方向

鄰居 pattern：`matrix-heatmap.md`（一般色階矩陣／相關矩陣；鄰接矩陣不算其變體）、`force-network.md`、`arc-diagram.md`、`chord-matrix.md`。
