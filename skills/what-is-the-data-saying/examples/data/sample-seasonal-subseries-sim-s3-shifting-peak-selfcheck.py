#!/usr/bin/env python3
"""sample-seasonal-subseries-sim-s3-shifting-peak-selfcheck.py：圖 S3 自我檢查。
從 sample-seasonal-subseries-sim-s3-shifting-peak.csv 獨立重算（自寫線性最小平方斜率與各月平均），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-seasonal-subseries-sim-s3-shifting-peak-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "虛構資料，數字未核"
FN = "sample-seasonal-subseries-sim-s3-shifting-peak.csv"
RESULTS = []

JUL_SLOPE = -1.5
SEP_SLOPE = 2.0
PEAK_FIRST3 = 8
PEAK_LAST3 = 9

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

def polyfit(xs, ys, deg):
    # 正規方程最小平方。係數由高次到常數；deg 1 直線、deg 2 二次。
    xs = list(xs)
    m = deg + 1
    sp = [0.0] * (2 * deg + 1)
    for x in xs:
        p = 1.0
        for k in range(2 * deg + 1):
            sp[k] += p
            p *= x
    rhs = [0.0] * m
    for x, y in zip(xs, ys):
        p = 1.0
        xp = [0.0] * m
        for k in range(m):
            xp[k] = p
            p *= x
        for i in range(m):
            rhs[i] += y * xp[deg - i]
    aug = [[sp[(deg - i) + (deg - j)] for j in range(m)] + [rhs[i]] for i in range(m)]
    for col in range(m):
        pivot = max(range(col, m), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        div = aug[col][col]
        for j in range(col, m + 1):
            aug[col][j] /= div
        for r in range(m):
            if r == col:
                continue
            factor = aug[r][col]
            for j in range(col, m + 1):
                aug[r][j] -= factor * aug[col][j]
    return [aug[i][m] for i in range(m)]

def slope(values):
    return polyfit(range(len(values)), values, 1)[0]

def season_matrix(rows, col, season_key="month"):
    years = sorted({r["year"] for r in rows}, key=float)
    n_season = max(int(r[season_key]) for r in rows)
    index = {y: i for i, y in enumerate(years)}
    grid = [[0.0] * n_season for _ in years]
    for r in rows:
        grid[index[r["year"]]][int(r[season_key]) - 1] = float(r[col])
    return grid

def col_means(grid):
    width = len(grid[0])
    return [mean([row[j] for row in grid]) for j in range(width)]

def argmax(xs):
    best = 0
    for i, v in enumerate(xs):
        if v > xs[best]:
            best = i
    return best

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
grid = season_matrix(rows, "value")
chk("7 月斜率", r1(slope([row[6] for row in grid])) == JUL_SLOPE)
chk("9 月斜率", r1(slope([row[8] for row in grid])) == SEP_SLOPE)
chk("前後 3 年高峰", argmax(col_means(grid[:3])) + 1 == PEAK_FIRST3 and argmax(col_means(grid[-3:])) + 1 == PEAK_LAST3)
done()
