#!/usr/bin/env python3
"""sample-taylor-sim-s5-improvement-selfcheck.py：圖 S5 自我檢查。
從 sample-taylor-sim-s5-improvement.csv 比較舊版與新版。
中心化均方根誤差以 s_r = 1 用餘弦定理重算。
E'^2 = s_r^2 + s_m^2 - 2 * s_r * s_m * R。只需 Python 標準函式庫。
用法：python3 sample-taylor-sim-s5-improvement-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。圖說的紅、綠與箭頭是畫法，CSV 沒有顏色欄。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-taylor-sim-s5-improvement.csv"
COLS = ["version", "std", "corr"]
RESULTS = []
SR = 1.0
TOL = 1e-12

# 模擬記載（寫死）。標準差與相關取自 sim_facts，並對過 CSV。
OLD_STD, OLD_CORR, OLD_E = 1.35, 0.6, 1.0965856099730655
NEW_STD, NEW_CORR, NEW_E = 1.05, 0.88, 0.5044799302251775

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
    chk("第一行是表頭", first.startswith("version,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
chk("欄位", list(rows[0].keys()) == COLS)
chk("2 列且順序是舊版、新版", len(rows) == 2 and [r["version"] for r in rows] == ["舊版", "新版"])
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
old, new = rows[0], rows[1]
chk("舊版標準差 1.35、相關 0.6", near(float(old["std"]), OLD_STD) and near(float(old["corr"]), OLD_CORR))
chk("新版標準差 1.05、相關 0.88", near(float(new["std"]), NEW_STD) and near(float(new["corr"]), NEW_CORR))
old_e = crmse(SR, float(old["std"]), float(old["corr"]))
new_e = crmse(SR, float(new["std"]), float(new["corr"]))
chk("舊版與新版的中心化均方根誤差", near(old_e, OLD_E) and near(new_e, NEW_E), (old_e, new_e))
chk("新版的中心化均方根誤差較小", new_e < old_e)
chk(
    "新版標準差更靠近 1，相關也較高",
    abs(float(new["std"]) - 1.0) < abs(float(old["std"]) - 1.0) and float(new["corr"]) > float(old["corr"]),
)
done()
