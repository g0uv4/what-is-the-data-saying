#!/usr/bin/env python3
"""sample-splom-sim-s1-anatomy-selfcheck.py：圖 S1 自我檢查。
從 sample-splom-sim-s1-anatomy.csv 獨立重算三對皮爾森相關，與模擬記載比對。
只需 Python 標準函式庫。
用法：python3 sample-splom-sim-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-splom-sim-s1-anatomy.csv"
COLS = ["變數甲", "變數乙", "變數丙"]
RESULTS = []

# 模擬記載（寫死）。甲乙相關取自 sim_facts；甲丙、乙丙由本腳本同一套皮爾森算法對 CSV 重算後寫死。
EXPECT_N = 80
CORR_AB = 0.7124228200726517
CORR_AC = -0.0559115140907558
CORR_BC = 0.0763799869580054
TOL = 1e-12

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def read_rows(fn):
    path = os.path.join(HERE, fn)
    chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
    with open(path, encoding="utf-8", newline="") as fh:
        first = fh.readline()
        chk("第一行是表頭", first.startswith("變數甲,"))
        fh.seek(0)
        rows = list(csv.DictReader(fh))
    chk("欄位", list(rows[0].keys()) == COLS)
    chk("80 列", len(rows) == EXPECT_N)
    return rows

def col(rows, name):
    out = []
    for r in rows:
        v = (r[name] or "").strip()
        if v == "":
            return None
        out.append(float(v))
    return out

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
a, b, c = col(rows, "變數甲"), col(rows, "變數乙"), col(rows, "變數丙")
chk("三欄都沒有空值", a is not None and b is not None and c is not None)
r_ab, r_ac, r_bc = pearson(a, b), pearson(a, c), pearson(b, c)
chk("甲與乙皮爾森相關", near(r_ab, CORR_AB), r_ab)
chk("甲與丙皮爾森相關", near(r_ac, CORR_AC), r_ac)
chk("乙與丙皮爾森相關", near(r_bc, CORR_BC), r_bc)
chk("三對裡甲乙絕對值最大", abs(r_ab) > abs(r_ac) and abs(r_ab) > abs(r_bc))
done()
