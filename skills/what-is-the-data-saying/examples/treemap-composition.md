# Pattern: treemap-composition

> **圖種**：矩形樹狀圖（Treemap）
> **來源（納茲教圖）**：`teach-viz/2026-09-06-am-treemap.md`

## When

- 問「誰屬於誰、哪一枝最大、葉很多要鋪滿」
- 形狀：樹 + 葉非負可加總度量

## Recommend

- **主選**：矩形樹狀圖
- **備選**：深度軸可讀 → 冰柱；交叉表 → 馬賽克

## Avoid

- 與馬賽克混淆；精準比面積卻不給旁表

## Produce checklist

- [ ] 葉面積∝值；父≈子和
- [ ] 色可編第二維並說明
