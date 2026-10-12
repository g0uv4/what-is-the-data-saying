#!/usr/bin/env python3
"""sample-seasonal-subseries-sim-s5-no-season-selfcheck.py：圖 S5 自我檢查。
從 sample-seasonal-subseries-sim-s5-no-season.csv 獨立重算（自寫各月平均高低差），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-seasonal-subseries-sim-s5-no-season-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "虛構資料，數字未核"
FN = "sample-seasonal-subseries-sim-s5-no-season.csv"
RESULTS = []

MEANS_RANGE_NOISE = 6.5
MEANS_RANGE_SEASON = 10.7

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

def means_range(grid):
    means = [mean([row[j] for row in grid]) for j in range(len(grid[0]))]
    return max(means) - min(means)

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
chk("純雜訊高低差", r1(means_range(season_matrix(rows, "noise_only"))) == MEANS_RANGE_NOISE)
chk("有季節高低差", r1(means_range(season_matrix(rows, "with_season"))) == MEANS_RANGE_SEASON)
done()
