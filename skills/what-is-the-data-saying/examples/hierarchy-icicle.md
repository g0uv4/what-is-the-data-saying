# Pattern: hierarchy-icicle

> **圖種**：冰柱圖（Icicle diagram）
> **來源（納茲教圖）**：`teach-viz/2026-09-01-am-icicle-draft.md`

## When

- 問「結構怎麼切、往下鑽、預算／組織／科目樹佔比」
- 形狀：階層（parent–child 或 path）+ 非負數值
- 要好標文字、層偏深

## Recommend

- **主選**：**冰柱圖（icicle）**／partition 直角版
- **備選**：旭日（緊湊總覽）；矩形樹狀（葉面積）；圓堆；Voronoi 樹狀
- **對帳**：旁掛表格（路徑 + 金額）

## Avoid

- 深階層压成單一圓餅
- 子加總 ≠ 父卻不洗資料
- 有向流量改畫冰柱（應桑基）
- 假設 Flourish 有原生冰柱（多數 Hierarchy 模板沒有）

## Produce checklist

- [ ] 驗證階層加總（父＝子 sum）
- [ ] 層順序＝深度軸順序
- [ ] 互動：下鑽／breadcrumb；靜態限制深度
- [ ] zh-TW 節點名；單位一致
- [ ] 故事句先寫清「隸屬組成」不是流量
