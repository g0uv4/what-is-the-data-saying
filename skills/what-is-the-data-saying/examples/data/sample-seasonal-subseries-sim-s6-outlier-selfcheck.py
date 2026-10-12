#!/usr/bin/env python3
"""sample-seasonal-subseries-sim-s6-outlier-selfcheck.py：圖 S6 自我檢查。
從 sample-seasonal-subseries-sim-s6-outlier.csv 獨立重算（自寫平均與中位數），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-seasonal-subseries-sim-s6-outlier-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "虛構資料，數字未核"
FN = "sample-seasonal-subseries-sim-s6-outlier.csv"
RESULTS = []

OUTLIER_VALUE = 43.1
MAR_MEAN_WITH = 68.8
MAR_MEAN_WITHOUT = 72.4
MAR_MEDIAN_WITH = 72.8

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def read_rows(fn):
    path = os.path.join(HERE, fn)
    with open(path, encoding="utf-8", newline="") as fh:
        first = fh.readline()
        chk("第一行標示資料性質", first.startswith("# " + STATUS.split("，")[0]))
        rows = list(csv.DictReader(fh))
    chk("每列 data_status 正確", all(r["data_status"] == STATUS for r in rows))
    chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
    return rows

def mean(xs):
    return math.fsum(xs) / len(xs)

def median(xs):
    s = sorted(xs)
    n = len(s)
    mid = n // 2
    if n % 2:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2.0

def r1(x):
    return round(float(x) + 1e-12, 1)

def season_matrix(rows, col, season_key="month"):
    years = sorted({r["year"] for r in rows}, key=float)
    n_season = max(int(r[season_key]) for r in rows)
    index = {y: i for i, y in enumerate(years)}
    grid = [[0.0] * n_season for _ in years]
    for r in rows:
        grid[index[r["year"]]][int(r[season_key]) - 1] = float(r[col])
    return grid

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
grid = season_matrix(rows, "value")
march = [row[2] for row in grid]
march_without = march[:4] + march[5:]
chk("怪值 2021 年 3 月", r1(grid[4][2]) == OUTLIER_VALUE)
chk("3 月平均含與不含", r1(mean(march)) == MAR_MEAN_WITH and r1(mean(march_without)) == MAR_MEAN_WITHOUT)
chk("3 月中位數", r1(median(march)) == MAR_MEDIAN_WITH)
done()
