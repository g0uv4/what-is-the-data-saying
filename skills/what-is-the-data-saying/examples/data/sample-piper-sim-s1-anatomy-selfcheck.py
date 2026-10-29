#!/usr/bin/env python3
"""sample-piper-sim-s1-anatomy-selfcheck.py：圖 S1 自我檢查。
從 sample-piper-sim-s1-anatomy.csv 核對一瓶示範水的毫當量百分比，
以及菱形點鈣＋鎂、硫酸根＋氯。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-piper-sim-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-piper-sim-s1-anatomy.csv"
COLS = ["Ca_pct", "Mg_pct", "NaK_pct", "HCO3_pct", "SO4_pct", "Cl_pct"]
RESULTS = []

CA, MG, NAK = 55.0, 25.0, 20.0
HCO3, SO4, CL = 65.0, 20.0, 15.0
CAMG, SO4CL = 80.0, 35.0
TOL = 1e-12

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def unchecked():
    skip("這些百分比的單位寫在欄位裡", "CSV 只有比例，沒有毫克或毫當量欄；課程稿把這一列當毫當量百分比")

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def end():
    unchecked()
    done()

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("Ca_pct,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("1 列", len(rows) == 1, len(rows))
if not cols_ok or len(rows) != 1:
    end()
r = rows[0]
empty = any((r[c] or "").strip() == "" for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
vals = {c: float(r[c]) for c in COLS}
chk(
    "陽離子百分比是鈣 55、鎂 25、鈉＋鉀 20",
    near(vals["Ca_pct"], CA) and near(vals["Mg_pct"], MG) and near(vals["NaK_pct"], NAK),
    (vals["Ca_pct"], vals["Mg_pct"], vals["NaK_pct"]),
)
chk(
    "陰離子百分比是碳酸氫根 65、硫酸根 20、氯 15",
    near(vals["HCO3_pct"], HCO3) and near(vals["SO4_pct"], SO4) and near(vals["Cl_pct"], CL),
    (vals["HCO3_pct"], vals["SO4_pct"], vals["Cl_pct"]),
)
cat = vals["Ca_pct"] + vals["Mg_pct"] + vals["NaK_pct"]
an = vals["HCO3_pct"] + vals["SO4_pct"] + vals["Cl_pct"]
chk("陽離子加總 100", near(cat, 100.0), cat)
chk("陰離子加總 100", near(an, 100.0), an)
camg = vals["Ca_pct"] + vals["Mg_pct"]
so4cl = vals["SO4_pct"] + vals["Cl_pct"]
chk("菱形點鈣＋鎂 80", near(camg, CAMG), camg)
chk("菱形點硫酸根＋氯 35", near(so4cl, SO4CL), so4cl)
end()
