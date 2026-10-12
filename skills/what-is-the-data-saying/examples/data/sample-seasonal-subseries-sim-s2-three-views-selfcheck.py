#!/usr/bin/env python3
"""sample-seasonal-subseries-sim-s2-three-views-selfcheck.py：圖 S2 自我檢查。
從 sample-seasonal-subseries-sim-s2-three-views.csv 獨立重算（自寫一次趨勢的正規方程最小平方），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-seasonal-subseries-sim-s2-three-views-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "虛構資料，數字未核"
FN = "sample-seasonal-subseries-sim-s2-three-views.csv"
RESULTS = []

# 圖說預期值（寫死；只含原先要比對的數字）
EXPECT_SLOPES = [-0.9, 1.4, -0.9, -0.3, 1.8, 13.9, 15.2, 15.9, 0.7, 0.3, -3.2, -0.8]
EXPECT_SUMMER_SLOPE = 15.0

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
    # x = 0..n−1 的 deg 次最小平方。x 先減平均再組正規方程。
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

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
M = month_matrix(rows, "value")
slopes = [slope(column(M, j)) for j in range(12)]
chk("格內斜率", [r1(s) for s in slopes] == EXPECT_SLOPES)
chk("夏季平均斜率", r1(mean(slopes[5:8])) == EXPECT_SUMMER_SLOPE)
done()
