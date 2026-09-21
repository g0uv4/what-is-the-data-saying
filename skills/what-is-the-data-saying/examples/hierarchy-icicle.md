# Pattern: hierarchy-icicle

## When

- 問「結構怎麼切、往下鑽、預算／組織／科目樹佔比」
- 形狀：階層（parent–child 或 path）+ 數值

## Recommend

- **主選**：**icicle／partition**（標籤可讀、適合報表下鑽）
- **備選**：sunburst（緊湊總覽）；treemap（葉節點面積比較）
- **對帳**：旁掛 table（節點路徑 + 金額）

## Avoid

- 把深階層压成單一 pie
- 無加總閉合的樹（子項加總 ≠ 父項）不先清洗

## Produce checklist

- [ ] 驗證階層加總
- [ ] 互動：click 下鑽或 breadcrumb
- [ ] 靜態輸出：限制深度或只展示 top 層 + 重點枝
- [ ] zh-TW 節點名；單位一致
