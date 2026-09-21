# Data shape checks

Run these before recommending a chart. Output a short diagnosis, not a essay.

## Roles

Assign each column one primary role:

| Role | Signals |
|------|---------|
| time | date, datetime, year, month, 期別, 年月 |
| category | 名稱, id, 部門, 產品, region (unordered) |
| ordered-category | 評等, 年齡層, Likert, 階段 |
| numeric | 金額, 數量, %, 指數 |
| hierarchy | parent/child, path, 科目樹, org levels |
| geo | 縣市, 郵遞區號, lat/lon |
| id | opaque key (usually not plotted alone) |

## Structure probes

1. **Grain**: one row = ? (日／人／訂單／科目／…)。Grain 不清就先問或推斷並標「假設」。
2. **Cardinality**: distinct count per category. >12–15 類別比大小 → 考慮 top-N + other、或改 table／small multiples。
3. **Nulls / zeros**: 缺值比例；0 是真實還是空白。
4. **Units**: 混用千元／元／%？統一後再畫。
5. **Duplicates**: 同 key 多列 → 需聚合規則（sum/mean/last）。
6. **Outliers**: 是否該用 log、截尾、或獨立標註。
7. **Wide vs long**: 寬表（每年一欄）常需 melt 成長表再畫 line/bar。

## Question type → next file

| Question | Go to |
|----------|-------|
| 誰大誰小 | chart-heuristics → bar / table |
| 怎麼變 | line / area |
| 是否相關 | scatter / heat |
| 佔多少 | stacked bar / treemap / icicle（階層） |
| 結構／下鑽 | icicle / sunburst / partition |
| 很多同類比較 | small multiples |

## Minimum viable sample

Prefer: header + ≥5–20 rows + 單位說明. Screenshot-only → recommend + ask for machine-readable extract.
