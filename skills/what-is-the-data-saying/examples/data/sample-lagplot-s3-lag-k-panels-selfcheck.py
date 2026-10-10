#!/usr/bin/env python3
"""sample-lagplot-s3-lag-k-panels-selfcheck.py：圖 S3 自我檢查。
從 sample-lagplot-s3-lag-k-panels.csv 獨立重算（自寫滯後 k 皮爾森相關與自相關），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-lagplot-s3-lag-k-panels-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "虛構資料，數字未核"
FN = "sample-lagplot-s3-lag-k-panels.csv"
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
    return pearson(x[:-k], x[k:])

def acf(x, k):
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

# 滯後：皮爾森相關、自相關
PANELS = [
    (1, 0.794, 0.787),
    (2, 0.461, 0.454),
    (3, -0.004, -0.004),
    (6, -0.929, -0.901),
    (9, 0.002, 0.002),
    (12, 0.928, 0.862),
]

rows = read_rows(FN)
y = col(rows, "y")
for k, want_p, want_a in PANELS:
    chk(f"滯後 {k} 相關", near(lagr(y, k), want_p), round(lagr(y, k), 3))
    chk(f"滯後 {k} 自相關", near(acf(y, k), want_a), round(acf(y, k), 3))
done()
