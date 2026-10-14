#!/usr/bin/env python3
"""sample-splom-sim-s2-corr-upper-selfcheck.py：圖 S2 自我檢查。
從 sample-splom-sim-s2-corr-upper.csv 獨立重算四欄兩兩皮爾森相關。
只需 Python 標準函式庫。
用法：python3 sample-splom-sim-s2-corr-upper-selfcheck.py   全部通過時結束碼為 0。
底層是公有領域鳶尾花四個數值欄，不是虛構亂數；課程稿圖說仍標未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-splom-sim-s2-corr-upper.csv"
COLS = ["萼片長", "萼片寬", "花瓣長", "花瓣寬"]
RESULTS = []

EXPECT_N = 150
PETAL_R = 0.962865431402796
TOL = 1e-12

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def read_rows(fn):
    path = os.path.join(HERE, fn)
    chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
    with open(path, encoding="utf-8", newline="") as fh:
        first = fh.readline()
        chk("第一行是表頭", first.startswith("萼片長,"))
        fh.seek(0)
        rows = list(csv.DictReader(fh))
    chk("欄位", list(rows[0].keys()) == COLS)
    chk("150 列", len(rows) == EXPECT_N)
    return rows

def nums(row):
    return [float((row[c] or "").strip()) for c in COLS]

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
chk("首列是 5.1, 3.5, 1.4, 0.2", nums(rows[0]) == [5.1, 3.5, 1.4, 0.2])
chk("末列是 5.9, 3.0, 5.1, 1.8", nums(rows[-1]) == [5.9, 3.0, 5.1, 1.8])
data = {c: [float(r[c]) for r in rows] for c in COLS}
best = None
petal = pearson(data["花瓣長"], data["花瓣寬"])
for i, a in enumerate(COLS):
    for b in COLS[i + 1:]:
        r = pearson(data[a], data[b])
        if best is None or abs(r) > abs(best[0]):
            best = (r, a, b)
chk("花瓣長與花瓣寬皮爾森相關", near(petal, PETAL_R), petal)
chk("非對角絕對值最大的一對就是花瓣長寬", best[1:] == ("花瓣長", "花瓣寬") and near(best[0], PETAL_R), best)
done()
