# Pattern: radar-profile

> **圖種**：雷達圖（Radar chart）
> **來源（納茲教圖）**：`teach-viz/2026-09-14-pm-radar.md`

## When

- 問「少數對象多度量剖面」
- 形狀：對象 × 多可比度量

## Recommend

- **主選**：雷達（系列 ≤2～3）
- **備選**：多特徵 → 平行座標；精準比 → 分組長條

## Avoid

- 面積當總分；軸不可比；與圓形長條／玫瑰混淆；與螺旋圖混淆（螺旋是時間序列捲成多圈，見 `spiral-plot.md`）

## Produce checklist

- [ ] 同尺；半透明填色
- [ ] 自檢換軸序結論是否仍穩

鄰居 pattern：`circular-bar.md`、`spiral-plot.md`、`parallel-coordinates.md`。
