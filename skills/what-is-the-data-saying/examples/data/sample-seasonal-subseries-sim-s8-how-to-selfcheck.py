#!/usr/bin/env python3
"""sample-seasonal-subseries-sim-s8-how-to-selfcheck.py：圖 S8 自我檢查。
從 sample-seasonal-subseries-sim-s8-how-to.csv 獨立重算（自寫各季平均），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-seasonal-subseries-sim-s8-how-to-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "虛構資料，數字未核"
FN = "sample-seasonal-subseries-sim-s8-how-to.csv"
RESULTS = []

VALUES = [
    [42, 55, 61, 47],
    [45, 59, 66, 49],
    [47, 62, 70, 52],
]
QUARTER_MEANS = [44.7, 58.7, 65.7, 49.3]

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
grid = season_matrix(rows, "value", "quarter")
got_values = [[int(v) for v in row] for row in grid]
got_means = [r1(mean([row[j] for row in grid])) for j in range(len(grid[0]))]
chk("原值", got_values == VALUES)
chk("季平均", got_means == QUARTER_MEANS)
done()
