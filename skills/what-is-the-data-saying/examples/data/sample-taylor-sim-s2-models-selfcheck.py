#!/usr/bin/env python3
"""sample-taylor-sim-s2-models-selfcheck.py：圖 S2 自我檢查。
從 sample-taylor-sim-s2-models.csv 用餘弦定理重算六個模型的中心化均方根誤差。
E'^2 = s_r^2 + s_m^2 - 2 * s_r * s_m * R，s_r = 1。只需 Python 標準函式庫。
用法：python3 sample-taylor-sim-s2-models-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-taylor-sim-s2-models.csv"
COLS = ["model", "std", "corr", "marker"]
RESULTS = []
SR = 1.0
TOL = 1e-12

# 模擬記載（寫死）。標準差、相關取自 sim_facts，並對過 CSV。形狀記號是 CSV 原文。
# 中心化均方根誤差是 math.sqrt 的 repr，不是四捨五入。A 的值與 sim_facts 的 crmse_A_approx 相同。
EXPECT = [
    ("A", 1.0, 0.92, "o", 0.3999999999999999),
    ("B", 0.85, 0.88, "s", 0.4759201613716317),
    ("C", 1.15, 0.9, "^", 0.5024937810560445),
    ("D", 1.55, 0.7, "D", 1.110180165558726),
    ("E", 0.95, 0.45, "v", 1.023474474522936),
    ("F", 1.3, 0.65, "P", 1.0),
]

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def crmse(sr, sm, r):
    return math.sqrt(sr * sr + sm * sm - 2.0 * sr * sm * r)

def near(got, exp):
    return abs(got - exp) <= TOL

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("model,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
chk("欄位", list(rows[0].keys()) == COLS)
chk("6 列且順序是 A 到 F", len(rows) == 6 and [r["model"] for r in rows] == [e[0] for e in EXPECT])
empty = False
vals_ok = True
marks_ok = True
errs = []
for r, e in zip(rows, EXPECT):
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
    if not (near(float(r["std"]), e[1]) and near(float(r["corr"]), e[2])):
        vals_ok = False
    if r["marker"] != e[3]:
        marks_ok = False
    errs.append(crmse(SR, float(r["std"]), float(r["corr"])))
chk("沒有空值", not empty)
chk("六個模型的標準差與相關", vals_ok)
chk("形狀記號 o s ^ D v P", marks_ok, [r["marker"] for r in rows])
err_ok = all(near(got, e[4]) for got, e in zip(errs, EXPECT))
chk("六個中心化均方根誤差", err_ok, errs)
chk("模型 A 的中心化均方根誤差", near(errs[0], 0.3999999999999999), errs[0])
chk("模型 A 的中心化均方根誤差最小", errs[0] < min(errs[1:]))
done()
