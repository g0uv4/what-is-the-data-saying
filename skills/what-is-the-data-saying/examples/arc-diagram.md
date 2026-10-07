# Pattern: arc-diagram

> **圖種**：弧線圖（Arc diagram）
> **來源（納茲教圖）**：`teach-viz/2026-09-17-am-arc.md`

## When

- 問「關係邊 + 較好標節點名」
- 形狀：邊表；節點可一維排序

## Recommend

- **主選**：弧線圖
- **備選**：長刻度參考軸上的位置對位＋沿軸多層訊號 → Circos（`circos.md`，圓形版面）；邊多到弧線交疊、要每條邊一欄並依類型分塊 → BioFabric（`biofabric.md`）；探索 → 力導向；重排看塊 → 鄰接矩陣

## Avoid

- 節點順序亂排；與弦圖／桑基混淆；與 BioFabric 混淆（本圖節點在單一軸、邊是弧線；BioFabric 節點各占一列、邊一律垂直）

## Produce checklist

- [ ] 排序最關鍵；優化序 vs 亂序對照
- [ ] 圖注寫排序依據

鄰居 pattern：`circos.md`（圓形刻度軸＋多軌；本圖是直線版面的拓撲）、`biofabric.md`、`force-network.md`、`adjacency-matrix.md`。
