#!/usr/bin/env python3
"""sample-piper-sim-s3-groups-selfcheck.py：圖 S3 自我檢查。
從 sample-piper-sim-s3-groups.csv 核對四群各 4 瓶、菱形點與電荷平衡。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-piper-sim-s3-groups-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
電荷差絕對值最大是 4.04275，不是記載的 ±4.04%。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-piper-sim-s3-groups.csv"
COLS = [
    "group", "sample",
    "Ca_mg_per_L", "Mg_mg_per_L", "Na_mg_per_L", "K_mg_per_L",
    "HCO3_mg_per_L", "SO4_mg_per_L", "Cl_mg_per_L",
    "Ca_pct", "Mg_pct", "NaK_pct", "HCO3_pct", "SO4_pct", "Cl_pct",
    "ion_balance_pct",
]
MG = ["Ca_mg_per_L", "Mg_mg_per_L", "Na_mg_per_L", "K_mg_per_L", "HCO3_mg_per_L", "SO4_mg_per_L", "Cl_mg_per_L"]
PCT = ["Ca_pct", "Mg_pct", "NaK_pct", "HCO3_pct", "SO4_pct", "Cl_pct"]
EW = {"Ca": 20.039, "Mg": 12.1525, "Na": 22.99, "K": 39.098, "HCO3": 61.017, "SO4": 48.03, "Cl": 35.453}
GROUPS = ["山區補注井", "深層地下水", "沿海井", "石膏地層井"]
RESULTS = []

# 存檔：Ca+Mg、SO4+Cl、ion_balance_pct
DIAMOND = {
    "山區補注井1": (90.8087, 14.1519, 0.0411614),
    "山區補注井2": (88.4756, 17.16627, 0.75621),
    "山區補注井3": (92.768, 14.55958, -0.43371),
    "山區補注井4": (86.091, 18.06122, 4.04275),
    "深層地下水1": (10.87231, 12.49592, -1.96471),
    "深層地下水2": (17.41426, 15.47852, -2.68722),
    "深層地下水3": (6.97113, 12.56876, -2.05792),
    "深層地下水4": (13.3021, 14.29432, -1.14045),
    "沿海井1": (28.0619, 89.28752, -1.57516),
    "沿海井2": (27.28174, 88.09156, -3.78506),
    "沿海井3": (26.86258, 91.3611, -0.78324),
    "沿海井4": (28.49847, 88.77937, -1.27181),
    "石膏地層井1": (92.8457, 85.77253, -2.63581),
    "石膏地層井2": (93.1596, 84.81478, -3.75675),
    "石膏地層井3": (92.6063, 85.92341, -2.11643),
    "石膏地層井4": (92.8326, 86.41991, -2.3573),
}
IB_MAX = 4.04275
S2_MG = (60.0, 90.0, 600.0, 22.0, 250.0, 150.0, 1100.0)
PCT_TOL = 5e-4
IB_TOL = 1e-5
TOL = 1e-9

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def unchecked():
    skip("四群電荷差都在 ±4.04% 內", "存檔絕對值最大是 4.04275（山區補注井4）；4.04 是記載的兩位小數")
    skip("菱形點寫成一位小數 90.8／14.2 等", "頁上用存檔加總；sim_facts 的一位小數是記載")

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def end():
    unchecked()
    done()

def piper(r):
    ca = float(r["Ca_mg_per_L"]) / EW["Ca"]
    mg = float(r["Mg_mg_per_L"]) / EW["Mg"]
    na = float(r["Na_mg_per_L"]) / EW["Na"]
    k = float(r["K_mg_per_L"]) / EW["K"]
    h = float(r["HCO3_mg_per_L"]) / EW["HCO3"]
    so = float(r["SO4_mg_per_L"]) / EW["SO4"]
    cl = float(r["Cl_mg_per_L"]) / EW["Cl"]
    cat = ca + mg + na + k
    an = h + so + cl
    return 100.0 * (ca + mg) / cat, 100.0 * (so + cl) / an, 100.0 * (cat - an) / (cat + an)

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("group,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("16 列", len(rows) == 16, len(rows))
if not cols_ok or len(rows) != 16:
    end()
empty = any(any((r[c] or "").strip() == "" for c in COLS) for r in rows)
chk("沒有空值", not empty)
if empty:
    end()
from collections import Counter
cnt = Counter(r["group"] for r in rows)
chk("四群各 4 瓶", all(cnt[g] == 4 for g in GROUPS) and set(cnt) == set(GROUPS), dict(cnt))
names = [r["sample"] for r in rows]
chk("樣本名與記載相同", names == list(DIAMOND), names)
ibs = [float(r["ion_balance_pct"]) for r in rows]
absmax = max(abs(x) for x in ibs)
chk("電荷差絕對值最大是 4.04275", near(absmax, IB_MAX), absmax)
chk("每一列 |ion_balance_pct| ≤ 4.04275", all(abs(x) <= IB_MAX + 1e-12 for x in ibs))
chk("有一列超過 4.04", any(abs(x) > 4.04 for x in ibs), max(ibs))
ok_d = True
ok_re = True
max_camg = max_so4cl = max_ib = 0.0
for r in rows:
    camg = float(r["Ca_pct"]) + float(r["Mg_pct"])
    so4cl = float(r["SO4_pct"]) + float(r["Cl_pct"])
    ib = float(r["ion_balance_pct"])
    exp = DIAMOND[r["sample"]]
    if not (near(camg, exp[0], 1e-8) and near(so4cl, exp[1], 1e-8) and near(ib, exp[2], 1e-12)):
        ok_d = False
    rc, rs, rb = piper(r)
    max_camg = max(max_camg, abs(rc - camg))
    max_so4cl = max(max_so4cl, abs(rs - so4cl))
    max_ib = max(max_ib, abs(rb - ib))
    if abs(rc - camg) > PCT_TOL or abs(rs - so4cl) > PCT_TOL or abs(rb - ib) > IB_TOL:
        ok_re = False
    catp = float(r["Ca_pct"]) + float(r["Mg_pct"]) + float(r["NaK_pct"])
    anp = float(r["HCO3_pct"]) + float(r["SO4_pct"]) + float(r["Cl_pct"])
    if abs(catp - 100.0) > 2e-4 or abs(anp - 100.0) > 2e-4:
        ok_d = False
chk("存檔菱形點與電荷差", ok_d)
chk("用圖 S2 當量重從毫克重算百分比", ok_re, (max_camg, max_so4cl, max_ib))
w1 = [r for r in rows if r["sample"] == "沿海井1"][0]
chk(
    "沿海井1 的毫克與圖 S2 同一瓶",
    all(near(float(w1[c]), v) for c, v in zip(MG, S2_MG)),
    [float(w1[c]) for c in MG],
)
end()
