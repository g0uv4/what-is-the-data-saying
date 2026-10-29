#!/usr/bin/env python3
"""sample-piper-sim-s5-ratio-only-selfcheck.py：圖 S5 自我檢查。
從 sample-piper-sim-s5-ratio-only.csv 核對濃度差 10 倍的兩瓶水離子合計，
以及用同一套當量重算出的派柏圖位置。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-piper-sim-s5-ratio-only-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-piper-sim-s5-ratio-only.csv"
COLS = [
    "sample",
    "Ca_mg_per_L", "Mg_mg_per_L", "Na_mg_per_L", "K_mg_per_L",
    "HCO3_mg_per_L", "SO4_mg_per_L", "Cl_mg_per_L",
    "sum_mg_per_L",
]
IONS = ["Ca", "Mg", "Na", "K", "HCO3", "SO4", "Cl"]
MG = [k + "_mg_per_L" for k in IONS]
EW = {"Ca": 20.039, "Mg": 12.1525, "Na": 22.99, "K": 39.098, "HCO3": 61.017, "SO4": 48.03, "Cl": 35.453}
RESULTS = []

A_MG = (60.0, 10.0, 8.0, 1.5, 220.0, 15.0, 10.0)
SUM_A = 324.5
SUM_B = 3245.0
CAMG = 90.80876511662076
SO4CL = 14.15189465377601
TOL = 1e-12

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def unchecked():
    skip("點的大小代表濃度", "CSV 沒有點大小欄；課程稿說要比濃度另加點大小或並排長條")

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def end():
    unchecked()
    done()

def piper_mg(mg):
    m = {k: mg[i] / EW[k] for i, k in enumerate(IONS)}
    cat = m["Ca"] + m["Mg"] + m["Na"] + m["K"]
    an = m["HCO3"] + m["SO4"] + m["Cl"]
    return 100.0 * (m["Ca"] + m["Mg"]) / cat, 100.0 * (m["SO4"] + m["Cl"]) / an

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("sample,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("2 列", len(rows) == 2, len(rows))
if not cols_ok or len(rows) != 2:
    end()
empty = any(any((r[c] or "").strip() == "" for c in COLS) for r in rows)
chk("沒有空值", not empty)
if empty:
    end()
names = [r["sample"] for r in rows]
chk("樣本名是甲、乙", names == ["甲", "乙"], names)
a, b = rows
amg = [float(a[c]) for c in MG]
bmg = [float(b[c]) for c in MG]
chk("甲的毫克", all(near(x, y) for x, y in zip(amg, A_MG)), amg)
chk("乙是甲的 10 倍", all(near(x, 10.0 * y) for x, y in zip(bmg, amg)), bmg)
suma = sum(amg)
sumb = sum(bmg)
chk("甲離子合計 324.5", near(suma, SUM_A) and near(float(a["sum_mg_per_L"]), SUM_A), (suma, a["sum_mg_per_L"]))
chk("乙離子合計 3245", near(sumb, SUM_B) and near(float(b["sum_mg_per_L"]), SUM_B), (sumb, b["sum_mg_per_L"]))
chk("合計也是 10 倍", near(sumb, 10.0 * suma))
ca, sa = piper_mg(amg)
cb, sb = piper_mg(bmg)
chk("甲菱形點鈣＋鎂 90.80876511662076", near(ca, CAMG), ca)
chk("甲菱形點硫酸根＋氯 14.15189465377601", near(sa, SO4CL), sa)
chk("乙與甲同一點", near(ca, cb) and near(sa, sb), (cb, sb))
end()
