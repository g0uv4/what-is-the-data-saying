#!/usr/bin/env python3
"""sample-seasonal-decomp-sim-s2-add-vs-mult-selfcheck.py：圖 S2 自我檢查。
從 sample-seasonal-decomp-sim-s2-add-vs-mult.csv 獨立重算（自寫母體標準差；去掉空值後前 24／後 24 筆），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-seasonal-decomp-sim-s2-add-vs-mult-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-seasonal-decomp-sim-s2-add-vs-mult.csv"
COLS = ["year_frac", "observed", "add_resid", "mult_resid"]
RESULTS = []

# 圖說預期值（寫死；對齊模擬記載，四捨五入到小數第二位）
EXPECT_N = 120
ADD_SD_FIRST2Y_LAST2Y = [14.47, 15.98]
MULT_SD_FIRST2Y_LAST2Y = [0.02, 0.01]

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def read_rows(fn):
    path = os.path.join(HERE, fn)
    chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
    with open(path, encoding="utf-8", newline="") as fh:
        first = fh.readline()
        chk("第一行是表頭", first.startswith("year_frac,"))
        fh.seek(0)
        rows = list(csv.DictReader(fh))
    chk("欄位", list(rows[0].keys()) == COLS)
    chk("120 列", len(rows) == EXPECT_N)
    return rows

def parse(v):
    v = (v or "").strip()
    if v == "":
        return None
    return float(v)

def col(rows, name):
    return [parse(r[name]) for r in rows]

def nonempty(xs):
    return [x for x in xs if x is not None]

def mean(xs):
    return math.fsum(xs) / len(xs)

def sd(xs):
    # 母體標準差（除以 n）
    m = mean(xs)
    return math.sqrt(math.fsum((x - m) ** 2 for x in xs) / len(xs))

def r2(x):
    return round(float(x) + 1e-12, 2)

def spread(xs):
    y = nonempty(xs)
    return [r2(sd(y[:24])), r2(sd(y[-24:]))]

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
chk("期間 2015–2024 月資料", rows[0]["year_frac"] == "2015.0" and rows[-1]["year_frac"] == "2024.9167")
add, mult = col(rows, "add_resid"), col(rows, "mult_resid")
chk("加法殘差頭尾約兩年標準差", spread(add) == ADD_SD_FIRST2Y_LAST2Y)
chk("乘法殘差頭尾約兩年標準差", spread(mult) == MULT_SD_FIRST2Y_LAST2Y)
done()
