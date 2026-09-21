# Pattern: contour-density

> **圖種**：等高線圖（Contour plot）
> **來源（納茲教圖）**：`teach-viz/2026-09-19-am-contour.md`

## When

- 問「兩連續軸上密度峰與鞍」
- 形狀：兩數值、點夠多

## Recommend

- **主選**：等高線／填充等高
- **備選**：hexbin；點少 → 散點

## Avoid

- 帶寬亂調造假山脊；外推區當實測

## Produce checklist

- [ ] 寫清 Z＝密度或第三變數
- [ ] 對照不同帶寬／層數
