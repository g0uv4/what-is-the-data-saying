# Demo 1 — Inventory hierarchy → icicle

A warehouse tree that people squash into one pie. The skill should refuse the pie and recommend **冰柱圖**.

## Paste this

```
這份庫存該怎麼畫？給台灣營運週會看。數字示意、未核。

我們要回答：庫存金額卡在哪一層、往下鑽時哪個倉／品類最重。不要圓餅。

| 通路 | 倉別 | 品類 | SKU | 庫存金額_千元 |
|------|------|------|-----|----------------|
| 電商 | 北倉 | 保健 | VIT-C-500 | 4200 |
| 電商 | 北倉 | 保健 | OMEGA-3 | 1800 |
| 電商 | 北倉 | 零食 | NUT-MIX | 900 |
| 電商 | 南倉 | 保健 | VIT-C-500 | 1100 |
| 電商 | 南倉 | 零食 | RICE-CRACKER | 2400 |
| 門市 | 中區DC | 保健 | VIT-D | 700 |
| 門市 | 中區DC | 家清 | SOAP-12 | 3100 |
| 門市 | 中區DC | 家清 | BLEACH | 1600 |

請依「資料在說什麼」格式：推薦 / 備選 / 避免 / 讀者／輸出 / pattern。
先講適不適合，再口述怎麼做（不必先寫程式）。
```

## You should hear

- **推薦：冰柱圖（icicle / partition）** — 通路→倉→品類→SKU 是隸屬組成，要好標中文與往下鑽。
- **備選：** 旭日（一頁總覽）、矩形樹狀（只比葉面積）。
- **避免：** 單一圓餅；把流向畫成桑基；父≠子加總卻不洗資料。
- Mentions `examples/hierarchy-icicle.md`.
- Story sentence about 隸屬／佔比, not flow.
- Units 千元, 未核, zh-TW labels.

## Why it wows

Most “chart choosers” say treemap or pie. Icicle is the teach-viz pick when labels and depth matter — and this table is exactly that shape.
