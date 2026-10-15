#!/usr/bin/env python3
"""sample-seasonal-decomp-sim-s1-anatomy-selfcheck.py：圖 S1 自我檢查。
從 sample-seasonal-decomp-sim-s1-anatomy.csv 獨立重算（自寫最大絕對值、頭尾空值、加法還原），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-seasonal-decomp-sim-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-seasonal-decomp-sim-s1-anatomy.csv"
COLS = ["year_frac", "observed", "trend", "seasonal", "resid"]
RESULTS = []

# 圖說預期值（寫死；對齊模擬記載，四捨五入）
EXPECT_N = 120
RESID_ABSMAX = 4.4
SEASONAL_ABSMAX = 9.8
TREND_NAN_EACH_END = 6

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

def nan_run(xs, from_start=True):
    n = 0
    seq = xs if from_start else reversed(xs)
    for x in seq:
        if x is None:
            n += 1
        else:
            break
    return n

def r1(x):
    return round(float(x) + 1e-12, 1)

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
obs, tr, se, re = col(rows, "observed"), col(rows, "trend"), col(rows, "seasonal"), col(rows, "resid")
chk("期間 2015–2024 月資料", rows[0]["year_frac"] == "2015.0" and rows[-1]["year_frac"] == "2024.9167")
chk("殘差最大絕對值", r1(max(abs(x) for x in nonempty(re))) == RESID_ABSMAX)
chk("季節最大絕對值", r1(max(abs(x) for x in nonempty(se))) == SEASONAL_ABSMAX)
chk("趨勢頭尾各缺 6 筆", nan_run(tr, True) == TREND_NAN_EACH_END and nan_run(tr, False) == TREND_NAN_EACH_END)
mx = 0.0
n_add = 0
for a, b, c, d in zip(obs, tr, se, re):
    if None in (b, c, d):
        continue
    n_add += 1
    mx = max(mx, abs(a - (b + c + d)))
chk("有值處 observed＝trend＋seasonal＋resid", n_add == EXPECT_N - 2 * TREND_NAN_EACH_END and mx < 5e-4)
done()
