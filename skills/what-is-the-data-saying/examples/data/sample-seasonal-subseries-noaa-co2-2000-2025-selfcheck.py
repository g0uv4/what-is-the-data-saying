#!/usr/bin/env python3
"""sample-seasonal-subseries-noaa-co2-2000-2025-selfcheck.py：海洋暨大氣總署資料（圖 R15、R16）自我檢查。
從 sample-seasonal-subseries-noaa-co2-2000-2025.csv 獨立重算（自寫平均，以及一次、二次趨勢的正規方程最小平方），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-seasonal-subseries-noaa-co2-2000-2025-selfcheck.py   全部通過時結束碼為 0。真實資料。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "真實資料"
FN = "sample-seasonal-subseries-noaa-co2-2000-2025.csv"
RESULTS = []

# 圖說預期值（寫死；只含原先要比對的數字）
EXPECT_MEAN_SLOPE = 2.29
EXPECT_MONTH_MEANS = [0.25, 0.88, 1.49, 2.71, 3.15, 2.37, 0.44, -1.83, -3.35, -3.34, -2.01, -0.77]
EXPECT_RANGE = 6.51

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

def month_matrix(rows, col):
    years = sorted({r["year"] for r in rows}, key=float)
    nmonth = max(int(r["month"]) for r in rows)
    index = {y: i for i, y in enumerate(years)}
    M = [[0.0] * nmonth for _ in years]
    for r in rows:
        M[index[r["year"]]][int(r["month"]) - 1] = float(r[col])
    return M

def column(M, j):
    return [row[j] for row in M]

def solve(A, b):
    # 高斯消去、部分選主元，解正規方程 A c = b
    n = len(b)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[pivot] = M[pivot], M[col]
        div = M[col][col]
        for c in range(col, n + 1):
            M[col][c] /= div
        for r in range(n):
            if r == col:
                continue
            factor = M[r][col]
            if factor == 0.0:
                continue
            for c in range(col, n + 1):
                M[r][c] -= factor * M[col][c]
    return [M[i][n] for i in range(n)]

def polyfit(y, deg):
    # x = 0..n−1 的 deg 次最小平方。x 先減平均再組正規方程，避免二次項量級差太大。
    # 回傳 (x̄, [c0, c1, ...])，擬合值 = Σ ck (x−x̄)^k；c1 是對原始 x 的斜率。
    n = len(y)
    xbar = (n - 1) / 2.0
    u = [i - xbar for i in range(n)]
    cols = deg + 1
    psum = [0.0] * (2 * deg + 1)
    psum[0] = float(n)
    for ui in u:
        p = 1.0
        for k in range(1, 2 * deg + 1):
            p *= ui
            psum[k] += p
    rhs = [0.0] * cols
    for yi, ui in zip(y, u):
        p = 1.0
        rhs[0] += yi
        for k in range(1, cols):
            p *= ui
            rhs[k] += yi * p
    A = [[psum[i + j] for j in range(cols)] for i in range(cols)]
    return xbar, solve(A, rhs)

def slope(y):
    _xbar, coef = polyfit(y, 1)
    return coef[1]

def fitted(y, deg):
    n = len(y)
    xbar, coef = polyfit(y, deg)
    out = []
    for i in range(n):
        u = i - xbar
        s = 0.0
        p = 1.0
        for c in coef:
            s += c * p
            p *= u
        out.append(s)
    return out

def argmax(xs):
    best = 0
    for i in range(1, len(xs)):
        if xs[i] > xs[best]:
            best = i
    return best

def argmin(xs):
    best = 0
    for i in range(1, len(xs)):
        if xs[i] < xs[best]:
            best = i
    return best

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
Y = month_matrix(rows, "average_ppm")
chk("26 年 × 12 月", len(Y) == 26 and len(Y[0]) == 12)
slopes = [slope(column(Y, j)) for j in range(12)]
chk("原始格內平均斜率 2.29", round(mean(slopes), 2) == EXPECT_MEAN_SLOPE)

flat = [v for row in Y for v in row]
fit = fitted(flat, 2)
resid = [flat[i] - fit[i] for i in range(len(flat))]
n_year, n_month = len(Y), len(Y[0])
mm = [mean([resid[i * n_month + j] for i in range(n_year)]) for j in range(n_month)]
chk("扣二次趨勢後各月平均", [round(x, 2) for x in mm] == EXPECT_MONTH_MEANS)
chk("5 月最高、9 月最低、差 6.51", argmax(mm) + 1 == 5 and argmin(mm) + 1 == 9 and round(max(mm) - min(mm), 2) == EXPECT_RANGE)

may = round(mean([row[4] - mean(row) for row in Y]), 2)
sep = round(mean([row[8] - mean(row) for row in Y]), 2)
chk("對照：減當年平均 5 月 +2.87、9 月 −2.88", may == 2.87 and sep == -2.88, (may, sep))
done()
