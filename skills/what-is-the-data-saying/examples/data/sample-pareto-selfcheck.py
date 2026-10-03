#!/usr/bin/env python3
"""sample-pareto-selfcheck.py：檢查虛構樣本資料 sample-pareto-fictional.csv（數字未核）。

用法：在本資料夾執行  python3 sample-pareto-selfcheck.py
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。

資料範圍（含兩端）：8 個原因類別（第 1 列到第 8 列），件數合計 340。
這份資料與課程稿的模擬圖 S1、S2、S6、S7、S8 用同一組件數（虛構，數字未核）。
"""
import csv
from pathlib import Path

CSV_NAME = "sample-pareto-fictional.csv"          # 指定檔名，不用 glob
path = Path(__file__).resolve().parent / CSV_NAME

with open(path, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

# ---- 1. 形狀：兩欄資料（類別、件數）加一欄標示「虛構」的備註欄 ---------------------
assert list(rows[0].keys()) == ["category", "count", "data_status"]
assert len(rows) == 8
assert all(r["data_status"] == "虛構資料，數字未核" for r in rows)
cats = [r["category"] for r in rows]
cnt = [int(r["count"]) for r in rows]
assert len(set(cats)) == 8                       # 8 個類別沒有重複
assert all(c > 0 for c in cnt)
total = sum(cnt)
assert total == 340

# ---- 2. 排序：前 7 個具名類別由大到小，「其他」固定放最右 ---------------------------
assert cats[-1] == "其他"
assert cnt[:7] == sorted(cnt[:7], reverse=True)
# 「其他」(8) 剛好也是最小的一項，所以這份資料看不出「其他比別人大仍放最右」；
# 那種情況請看課程稿圖 S3（另一份虛構資料）。
assert cnt[-1] == min(cnt)

# ---- 3. 累計百分比（用整數乘除算，四捨五入到小數 1 位） ------------------------------
cum, run = [], 0
for c in cnt:
    run += c
    cum.append(run)
pct = [round(100 * x / total, 1) for x in cum]
assert cum == [118, 204, 256, 287, 309, 323, 332, 340]
assert pct == [34.7, 60.0, 75.3, 84.4, 90.9, 95.0, 97.6, 100.0]
assert pct[-1] == 100.0

# ---- 4. 第一次達到 80% ----------------------------------------------------------------
# 從第 1 項往右數，累計百分比第一次大於或等於 80% 的是第 4 項（84.4%）。
# 「4 個」包含越過 80% 的那一項本身：前 3 項只有 75.3%，還沒到。
first = next(i + 1 for i, x in enumerate(cum) if 100 * x >= 80 * total)
assert first == 4
assert pct[first - 2] == 75.3 and pct[first - 1] == 84.4
# 前 4 項占 8 個類別的 4/8 = 50%（不是 20%）；累計 84.4%。
assert first / len(cnt) == 0.5

# ---- 5. 累計點與 80% 線的位置（只適用這 8 個累計點） ---------------------------------
above = [p for p in pct if p > 80]
below = [p for p in pct if p < 80]
equal = [p for p in pct if p == 80]
# 8 個累計點中：高於 80% 的有 5 個（第 4 到第 8 項），低於 80% 的有 3 個（第 1 到第 3 項），
# 沒有剛好等於 80% 的。5 + 3 = 8。
assert (len(above), len(below), len(equal)) == (5, 3, 0)
assert len(above) + len(below) + len(equal) == 8
# 「全部」只在指定區間成立：第 4 到第 8 項的累計點全部高於 80%；第 1 到第 3 項的累計點全部低於 80%。
assert all(p > 80 for p in pct[3:8])
assert all(p < 80 for p in pct[0:3])
# 不能說「全部累計點都高於 80%」：第 1 到第 3 項就不是。
assert not all(p > 80 for p in pct)

# ---- 6. 單項占比與 20% 的比較（8 個類別中的 2 個） ------------------------------------
share = [100 * c / total for c in cnt]
big = [i + 1 for i, s in enumerate(share) if s > 20]
# 單項占全部超過 20% 的只有第 1 項（34.7%）和第 2 項（25.3%），共 2 個類別；
# 第 3 項 52 件是 15.3%，已經低於 20%。
assert big == [1, 2]
assert round(share[0], 1) == 34.7 and round(share[1], 1) == 25.3 and round(share[2], 1) == 15.3

# ---- 7. 最小的 3 項（第 6 到第 8 項）合計 -------------------------------------------
small3 = sum(cnt[5:8])
# 文件缺漏 14 + 受潮 9 + 其他 8 = 31 件，占 340 件的 9.1%（不是 5%）。
assert small3 == 31
assert round(100 * small3 / total, 1) == 9.1
# 它們和累計曲線的關係：前 5 項累計 90.9%，最小的 3 項合計 9.1%，兩者相加 = 100.0%。
assert pct[4] == 90.9 and round(100 * small3 / total, 1) + pct[4] == 100.0

# ---- 8. 累計曲線其實是 Lorenz 曲線（由大到小排的版本） --------------------------------
# 由小到大排時，最小的 4 項是數量短少 22、文件缺漏 14、受潮 9、其他 8，合計 53 件，
# 占 340 件的 15.6%；剩下最大的 4 項占 84.4%（就是上面第 4 項的累計值）。兩者相加 = 100.0%。
asc = sorted(cnt)
low4 = sum(asc[:4])
assert asc[:4] == [8, 9, 14, 22] and low4 == 53
assert round(100 * low4 / total, 1) == 15.6
assert round(100 * low4 / total, 1) + pct[3] == 100.0

# ---- 9. 加權版（件數 × 假設單件損失，元，虛構）---------------------------------------
unit = [20, 150, 40, 30, 300, 10, 500, 50]
loss = [c * u for c, u in zip(cnt, unit)]
assert loss == [2360, 12900, 2080, 930, 6600, 140, 4500, 400]
assert sum(loss) == 29910
# 依損失排（「其他」固定放最右）：尺寸超差、數量短少、受潮、外觀刮傷、包裝破損、標示錯誤、文件缺漏，最後其他。
order = sorted(range(7), key=lambda i: -loss[i]) + [7]
assert [cats[i] for i in order] == ["尺寸超差", "數量短少", "受潮", "外觀刮傷", "包裝破損", "標示錯誤", "文件缺漏", "其他"]
lv = [loss[i] for i in order]
lc, run = [], 0
for v in lv:
    run += v
    lc.append(round(100 * run / sum(loss), 1))
# 依損失排，前 3 項（尺寸超差 12,900＋數量短少 6,600＋受潮 4,500＝24,000 元）累計 80.2%，
# 第 3 項就第一次越過 80%（前 2 項只有 65.2%）。
assert lc[:3] == [43.1, 65.2, 80.2]
assert sum(lv[:3]) == 24000
# 外觀刮傷件數第 1，但損失只排第 4（2,360 元，占 7.9%）。
assert cats[order[3]] == "外觀刮傷" and round(100 * 2360 / 29910, 1) == 7.9

print("全部檢查通過：8 列、合計 340、第 4 項首次達 80%、8 個累計點中 5 個高於 80% 且 3 個低於 80%。")
