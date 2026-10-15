#!/usr/bin/env python3
"""sample-seasonal-decomp-sim-s5-outlier-selfcheck.py：圖 S5 自我檢查。
從 sample-seasonal-decomp-sim-s5-outlier.csv 獨立重算（離群位置、該點殘差、趨勢相對 100＋0.5×序號的鼓起），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-seasonal-decomp-sim-s5-outlier-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-seasonal-decomp-sim-s5-outlier.csv"
COLS = ["year_frac", "observed", "classical_trend", "stl_trend", "classical_resid", "stl_resid"]
RESULTS = []

# 圖說預期值（寫死；對齊模擬記載，四捨五入）
EXPECT_N = 120
OUTLIER_INDEX = 62
CLASSICAL_RESID_AT_OUTLIER = 51.0
STL_RESID_AT_OUTLIER = 61.6
CLASSICAL_TREND_BUMP_MAX = 5.4
STL_TREND_BUMP_MAX = 1.1
# 產生過程（模擬記載）：水準 100、每月 +0.5。趨勢鼓起＝該欄減去 100＋0.5×序號（0 起算）。
TRUE_LEVEL = 100.0
TRUE_SLOPE = 0.5

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

def r1(x):
    return round(float(x) + 1e-12, 1)

def bump_max(trend):
    mx = None
    for i, v in enumerate(trend):
        if v is None:
            continue
        d = v - (TRUE_LEVEL + TRUE_SLOPE * i)
        if mx is None or d > mx:
            mx = d
    return mx

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
chk("期間 2015–2024 月資料", rows[0]["year_frac"] == "2015.0" and rows[-1]["year_frac"] == "2024.9167")
obs = col(rows, "observed")
ct, st = col(rows, "classical_trend"), col(rows, "stl_trend")
cr, sr = col(rows, "classical_resid"), col(rows, "stl_resid")
idx = max(range(len(obs)), key=lambda i: obs[i])
chk("離群值序號 62", idx == OUTLIER_INDEX)
chk("古典殘差在離群點", r1(cr[idx]) == CLASSICAL_RESID_AT_OUTLIER)
chk("STL 殘差在離群點", r1(sr[idx]) == STL_RESID_AT_OUTLIER)
chk("古典趨勢鼓起最多", r1(bump_max(ct)) == CLASSICAL_TREND_BUMP_MAX)
chk("穩健 STL 趨勢鼓起最多", r1(bump_max(st)) == STL_TREND_BUMP_MAX)
done()
