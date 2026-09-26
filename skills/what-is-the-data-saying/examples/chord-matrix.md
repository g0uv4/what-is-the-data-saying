# Pattern: chord-matrix

> **圖種**：弦圖（Chord diagram）
> **來源（納茲教圖）**：`teach-viz/2026-08-30-am-chord-draft.md`

## When

- 問「一組實體兩兩互流／交換多少」
- 形狀：方陣或來源/去向/非負值

## Recommend

- **主選**：弦圖
- **備選**：多階段過程 → 桑基；階層 → 旭日／冰柱

## Avoid

- 拿弦圖畫階層；弱邊全畫
- 要讀每一格強度而非交換帶 → 同一方陣改畫矩陣熱圖（`matrix-heatmap.md`）或鄰接矩陣（`adjacency-matrix.md`）

## Produce checklist

- [ ] 節點序減少交叉；裁弱邊
- [ ] 分步敘事

鄰居 pattern：`matrix-heatmap.md`、`adjacency-matrix.md`、`sankey-flow.md`。
