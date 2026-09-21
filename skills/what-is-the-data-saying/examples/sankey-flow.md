# Pattern: sankey-flow

> **圖種**：桑基圖（Sankey diagram）
> **來源（納茲教圖）**：`teach-viz/2026-08-31-am-sankey-draft.md`

## When

- 問「從哪裡流到哪裡、流量多大」
- 形狀：來源、去向、非負數值

## Recommend

- **主選**：桑基圖
- **備選**：有序階段重分組 → 沖積；成對矩陣交換 → 弦圖；階層隸屬 → 冰柱／旭日

## Avoid

- 把階層組成畫成桑基
- 同名節點跨層未加後綴
- 弱邊全畫

## Produce checklist

- [ ] 長表三欄：來源／去向／值
- [ ] 帶寬=流量；裁弱邊
- [ ] hover 高亮路徑
