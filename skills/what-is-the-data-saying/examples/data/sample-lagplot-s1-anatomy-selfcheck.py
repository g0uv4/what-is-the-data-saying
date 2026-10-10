#!/usr/bin/env python3
"""sample-lagplot-s1-anatomy-selfcheck.py：圖 S1 自我檢查。
從 sample-lagplot-s1-anatomy.csv 獨立重算（自寫滯後 k 皮爾森相關與自相關），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-lagplot-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "虛構資料，數字未核"
FN = "sample-lagplot-s1-anatomy.csv"
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def read_rows(fn):
    path = os.path.join(HERE, fn)
    with open(path, encoding="utf-8", newline="") as fh:
        first = fh.readline()
        chk("第一行標示虛構資料", first.startswith("# " + STATUS))
        rows = list(csv.DictReader(fh))
    chk("每列 data_status 正確", all(r["data_status"] == STATUS for r in rows))
    chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
    return rows

def col(rows, k):
    return [float(r[k]) for r in rows if r[k] != ""]

def mean(xs):
    return sum(xs) / len(xs)

def pearson(a, b):
    n = len(a)
    ma, mb = mean(a), mean(b)
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    da = math.sqrt(sum((v - ma) ** 2 for v in a))
    db = math.sqrt(sum((v - mb) ** 2 for v in b))
    return num / (da * db)

def lagr(x, k):
    # 只用 n−k 對 (y_t, y_{t+k})，兩欄各自的平均與標準差
    return pearson(x[:-k], x[k:])

def acf(x, k):
    # r(k)＝c(k)/c(0)，用全序列平均、分子分母的 /n 相消
    mu = mean(x)
    xc = [v - mu for v in x]
    num = sum(xc[t] * xc[t + k] for t in range(len(x) - k))
    den = sum(v * v for v in xc)
    return num / den

def near(a, b):
    return abs(round(a, 3) - b) < 0.0006

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
y = col(rows, "y")
chk("120 點", len(y) == 120)
chk("滯後 1 相關", near(lagr(y, 1), 0.722), round(lagr(y, 1), 3))
chk("自相關 r(1)", near(acf(y, 1), 0.711), round(acf(y, 1), 3))
done()
