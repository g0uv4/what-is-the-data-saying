# Pattern: correlation-scatter

> **圖種**：散點圖（Scatter plot）
> **來源（納茲教圖）**：`（通用；過密見 hexbin／contour 教圖）`

## When

- 問「是否相關、離群、分群」
- 形狀：數值 × 數值

## Recommend

- **主選**：散點（可加趨勢／分組色）
- **備選**：點很密 → `hexbin-density.md`／`contour-density.md`；雙序列演化 → `connected-scatter.md`

## Avoid

- 用折線連接無序類別
- 雙軸硬疊兩個不同單位卻不說明

## Produce checklist

- [ ] 軸標單位清楚
- [ ] 離群點是否標註或截尾說明
- [ ] 分組色有圖例
