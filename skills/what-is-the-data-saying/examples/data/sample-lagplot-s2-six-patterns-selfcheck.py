#!/usr/bin/env python3
"""sample-lagplot-s2-six-patterns-selfcheck.py：圖 S2 自我檢查。
從 sample-lagplot-s2-six-patterns.csv 獨立重算（自寫滯後 k 皮爾森相關與自相關），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-lagplot-s2-six-patterns-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "虛構資料，數字未核"
FN = "sample-lagplot-s2-six-patterns.csv"
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

def near(a, b):
    return abs(round(a, 3) - b) < 0.0006

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

# 名稱裡的減號是 U+2212，與圖說相同
PANELS = [
    ("white_noise", "白噪音（無結構）", 0.008),
    ("ar_pos_0p9", "強正自相關（係數 0.9）", 0.763),
    ("ar_neg", "負自相關（係數 −0.7）", -0.705),
    ("period12", "週期 12（正弦＋雜訊）", 0.81),
    ("trend_noise", "線性趨勢＋白噪音", 0.755),
    ("random_walk", "隨機漫步（未差分）", 0.985),
]

rows = read_rows(FN)
for key, name, want in PANELS:
    y = col(rows, key)
    chk(name + " 滯後 1 相關", near(lagr(y, 1), want), round(lagr(y, 1), 3))
done()
