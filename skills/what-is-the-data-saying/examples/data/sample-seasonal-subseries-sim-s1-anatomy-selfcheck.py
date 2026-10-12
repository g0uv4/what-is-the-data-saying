#!/usr/bin/env python3
"""sample-seasonal-subseries-sim-s1-anatomy-selfcheck.py：圖 S1 自我檢查。
從 sample-seasonal-subseries-sim-s1-anatomy.csv 獨立重算（自寫各月平均），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-seasonal-subseries-sim-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "虛構資料，數字未核"
FN = "sample-seasonal-subseries-sim-s1-anatomy.csv"
RESULTS = []

# 圖說預期值（寫死；只含原先要比對的數字）
EXPECT_N = 72
EXPECT_MONTH_MEANS = [203.3, 225.7, 257.7, 325.7, 380.9, 422.7, 447.4, 423.3, 391.7, 317.1, 260.1, 215.4]
EXPECT_PEAK_MONTH = 7
EXPECT_LOW_MONTH = 1

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
M = month_matrix(rows, "value")
chk("72 點", len(M) * len(M[0]) == EXPECT_N)
mm = [mean(column(M, j)) for j in range(len(M[0]))]
chk("各月平均", [r1(x) for x in mm] == EXPECT_MONTH_MEANS)
chk("7 月最高、1 月最低", argmax(mm) + 1 == EXPECT_PEAK_MONTH and argmin(mm) + 1 == EXPECT_LOW_MONTH)
done()
