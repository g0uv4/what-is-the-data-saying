# Pattern: force-network

> **圖種**：力導向網路圖（Force-directed graph）
> **來源（專案維護者整理）**：`teach-viz/2026-09-17-pm-force.md`

## When

- 問「誰連誰、團與橋」
- 形狀：節點 + 邊

## Recommend

- **主選**：力導向
- **備選**：稠密成毛球、要每條邊可辨識或邊依類型分塊 → BioFabric（`biofabric.md`）；讀全名 → 弧線；規則比較 → 蜂巢；矩陣團 → 鄰接矩陣；階層葉連線 → HEB

## Avoid

- 佈局當地理；全量毛球硬上

## Produce checklist

- [ ] 先過濾規模
- [ ] 圖注：位置由演算法決定；只標樞紐

鄰居 pattern：`biofabric.md`（節點＝水平列、邊＝垂直欄的正交織物，專梳毛球）、`arc-diagram.md`、`adjacency-matrix.md`、`chord-matrix.md`。
