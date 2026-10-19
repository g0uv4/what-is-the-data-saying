#!/usr/bin/env python3
"""sample-splom-sim-s4-too-many-vs-heatmap-selfcheck.py：圖 S4 自我檢查。
從 sample-splom-sim-s4-too-many-vs-heatmap.csv 獨立重算七變數非對角皮爾森相關的最大絕對值。
只需 Python 標準函式庫。
用法：python3 sample-splom-sim-s4-too-many-vs-heatmap-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-splom-sim-s4-too-many-vs-heatmap.csv"
COLS = ["甲", "乙", "丙", "丁", "戊", "己", "庚"]
RESULTS = []

EXPECT_N = 100
MAX_ABS_OFFDIAG = 0.8067857797701805
TOL = 1e-12

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def read_rows(fn):
    path = os.path.join(HERE, fn)
    chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
    with open(path, encoding="utf-8", newline="") as fh:
        first = fh.readline()
        chk("第一行是表頭", first.startswith("甲,"))
        fh.seek(0)
        rows = list(csv.DictReader(fh))
    chk("七個欄位", list(rows[0].keys()) == COLS)
    chk("100 列", len(rows) == EXPECT_N)
    return rows

def pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy)

def near(got, exp):
    return abs(got - exp) <= TOL

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
data = {}
empty = False
for c in COLS:
    xs = []
    for r in rows:
        v = (r[c] or "").strip()
        if v == "":
            empty = True
            break
        xs.append(float(v))
    data[c] = xs
chk("七欄都沒有空值", not empty)
best = None
n_off = 0
for i, a in enumerate(COLS):
    for b in COLS[i + 1:]:
        n_off += 1
        r = pearson(data[a], data[b])
        if best is None or abs(r) > abs(best[0]):
            best = (r, a, b)
chk("非對角共 21 對", n_off == 21)
chk("非對角最大絕對相關", near(abs(best[0]), MAX_ABS_OFFDIAG), best[0])
chk("最大的一對是丙與戊且為正", best[1:] == ("丙", "戊") and best[0] > 0)
done()
