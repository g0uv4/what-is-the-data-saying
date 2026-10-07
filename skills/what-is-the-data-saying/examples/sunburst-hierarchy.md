# Pattern: sunburst-hierarchy

> **圖種**：旭日圖（Sunburst）
> **來源（納茲教圖）**：`teach-viz/2026-08-31-pm-sunburst-draft.md`

## When

- 問「階層組成總覽、一圈一層」
- 形狀：path／父子 + 非負值

## Recommend

- **主選**：旭日圖
- **備選**：好標字／深層 → 冰柱；帶呼叫堆疊的效能剖面 → 火焰圖 `flame-graph.md`（非組成）；鋪滿矩形 → treemap

## Avoid

- 無階層硬畫；父子加總不合；與南丁格爾玫瑰混淆
- 與 Circos 混淆：本圖同心環＝階層深度、沒有連線層；Circos 同心環＝同一位置的多層訊號＋對位連線（`circos.md`）

## Produce checklist

- [ ] 層順序＝圈順序；父角寬＝子加總
- [ ] 小塊靠 hover／下鑽

鄰居 pattern：`hierarchy-icicle.md`、`treemap-composition.md`、`flame-graph.md`、`circos.md`（同心環意義不同：多軌訊號，不是階層）。
