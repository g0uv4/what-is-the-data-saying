#!/usr/bin/env python3
"""sample-seasonal-decomp-sim-s4-no-season-selfcheck.py：圖 S4 自我檢查。
從 sample-seasonal-decomp-sim-s4-no-season.csv 獨立重算（自寫季節最大絕對值與殘差母體標準差），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-seasonal-decomp-sim-s4-no-season-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-seasonal-decomp-sim-s4-no-season.csv"
COLS = ["year_frac", "observed", "seasonal", "resid"]
RESULTS = []

# 圖說預期值（寫死；對齊模擬記載，四捨五入到小數第二位）
EXPECT_N = 120
SEASONAL_ABSMAX = 1.29
RESID_SD = 2.64

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

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
chk("期間 2015–2024 月資料", rows[0]["year_frac"] == "2015.0" and rows[-1]["year_frac"] == "2024.9167")
se, re = col(rows, "seasonal"), col(rows, "resid")
chk("季節最大絕對值", r2(max(abs(x) for x in nonempty(se))) == SEASONAL_ABSMAX)
chk("殘差標準差", r2(sd(nonempty(re))) == RESID_SD)
done()
