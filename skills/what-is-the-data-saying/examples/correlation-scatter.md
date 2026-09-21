# Pattern: correlation-scatter

## When

- 問「是否相關、誰是離群」
- 形狀：兩個數值欄；可選分組色／點大小

## Recommend

- **主選**：scatter（可加 LOESS／線性參考線）
- **備選**：hexbin／density（點極多時）；分組小 multiples

## Avoid

- 把無序類別編碼成線段相連
- 相關當因果的標題語氣

## Produce checklist

- [ ] 兩軸單位清楚；必要時 log
- [ ] 標離群點名稱（若有 id）
- [ ] 說明樣本數與期間
- [ ] 相關敘述用「相關／伴隨」，避免「導致」（除非有因果設計）
