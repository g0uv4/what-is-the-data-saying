# Pattern: ridgeline-density

> **圖種**：山脊圖（Ridgeline plot）
> **來源（專案維護者整理）**：`teach-viz/2026-09-08-pm-ridgeline.md`

## When

- 問「很多組密度外形如何漂移」
- 形狀：同一數值 + 很多組

## Recommend

- **主選**：山脊圖（勿用 joyplot 當正式名）
- **備選**：少組 → 雨雲／小提琴

## Avoid

- 無軸專輯封面當分析圖；與地平線圖（[`horizon-chart.md`](horizon-chart.md)；摺疊色帶看相對基準的漲跌強度，不是看形狀）混淆

## Produce checklist

- [ ] 同尺密度；有刻度與標籤
- [ ] 組順序有故事

鄰居 pattern：`qq-plot.md`（要檢查形狀像不像某個參考分布、或兩批像不像同一種分布時的分位數診斷）、`boxplot-summary.md`；`horizon-chart.md`（地平線圖：一條序列一列、相對基準切色帶疊回矮條；看漲跌強度，不是密度形狀）。
