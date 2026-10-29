#!/usr/bin/env python3
"""sample-piper-sim-s4-mixing-selfcheck.py：圖 S4 自我檢查。
從 sample-piper-sim-s4-mixing.csv 核對淡水與海水按體積比例混合，以及菱形點。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-piper-sim-s4-mixing-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
1% 的菱形點是 46.3542／69.3683，不是記載的 46.4／69.4。5% 是 28.0013／91.3253，不是 28.0／91.3。
典型海水毫克值未核。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-piper-sim-s4-mixing.csv"
COLS = [
    "seawater_fraction",
    "Ca_mg_per_L", "Mg_mg_per_L", "Na_mg_per_L", "K_mg_per_L",
    "HCO3_mg_per_L", "SO4_mg_per_L", "Cl_mg_per_L",
    "CaMg_pct", "SO4Cl_pct",
]
IONS = ["Ca", "Mg", "Na", "K", "HCO3", "SO4", "Cl"]
MG = [k + "_mg_per_L" for k in IONS]
EW = {"Ca": 20.039, "Mg": 12.1525, "Na": 22.99, "K": 39.098, "HCO3": 61.017, "SO4": 48.03, "Cl": 35.453}
RESULTS = []

FRACS = [0.0, 0.002, 0.005, 0.01, 0.02, 0.05, 0.2, 1.0]
DIAMOND = {
    0.0: (87.2211, 18.0733),
    0.002: (71.1921, 38.6017),
    0.005: (57.7652, 55.3874),
    0.01: (46.3542, 69.3683),
    0.02: (36.5369, 81.1933),
    0.05: (28.0013, 91.3253),
    0.2: (22.5562, 97.7175),
    1.0: (20.9308, 99.615),
}
PATH_1 = 0.624088883285574
PATH_5 = 0.8963526203369079
FRESH_MG = (50.0, 10.0, 10.0, 2.0, 180.0, 15.0, 12.0)
SEA_MG = (412.0, 1290.0, 10770.0, 399.0, 142.0, 2710.0, 19350.0)
PCT_TOL = 5e-4
MIX_TOL = 1e-9
TOL = 1e-12

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def unchecked():
    skip("1% 寫成鈣＋鎂 46.4、硫酸根＋氯 69.4", "存檔是 46.3542 與 69.3683")
    skip("5% 寫成 28.0／91.3", "存檔是 28.0013 與 91.3253")
    skip("典型海水毫克值", "課程稿標未核；這一檔末列是 412、1290、10770、399、142、2710、19350，不當實測")

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
    chk("第一行是表頭", first.startswith("seawater_fraction,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("8 列", len(rows) == 8, len(rows))
if not cols_ok or len(rows) != 8:
    end()
empty = any(any((r[c] or "").strip() == "" for c in COLS) for r in rows)
chk("沒有空值", not empty)
if empty:
    end()
fracs = [float(r["seawater_fraction"]) for r in rows]
chk("海水比例 0、0.2%、0.5%、1%、2%、5%、20%、100%", all(near(a, b) for a, b in zip(fracs, FRACS)), fracs)
fresh = [float(rows[0][c]) for c in MG]
sea = [float(rows[-1][c]) for c in MG]
chk("淡水毫克", all(near(a, b) for a, b in zip(fresh, FRESH_MG)), fresh)
chk("海水毫克（示範值）", all(near(a, b) for a, b in zip(sea, SEA_MG)), sea)
ok_mix = True
ok_d = True
ok_re = True
max_re = 0.0
for r, f in zip(rows, fracs):
    mg = [float(r[c]) for c in MG]
    pred = [(1.0 - f) * a + f * b for a, b in zip(fresh, sea)]
    if any(abs(g - p) > MIX_TOL for g, p in zip(mg, pred)):
        ok_mix = False
    camg, so4cl = float(r["CaMg_pct"]), float(r["SO4Cl_pct"])
    exp = DIAMOND[f]
    if not (near(camg, exp[0]) and near(so4cl, exp[1])):
        ok_d = False
    rc, rs = piper_mg(mg)
    max_re = max(max_re, abs(rc - camg), abs(rs - so4cl))
    if abs(rc - camg) > PCT_TOL or abs(rs - so4cl) > PCT_TOL:
        ok_re = False
chk("濃度按體積比例線性相加", ok_mix)
chk("存檔菱形點", ok_d)
chk("用圖 S2 當量重從毫克重算菱形點", ok_re, max_re)
r1 = rows[3]
r5 = rows[5]
chk(
    "1% 鈣＋鎂 46.3542、硫酸根＋氯 69.3683",
    near(float(r1["CaMg_pct"]), 46.3542) and near(float(r1["SO4Cl_pct"]), 69.3683),
    (r1["CaMg_pct"], r1["SO4Cl_pct"]),
)
chk(
    "5% 鈣＋鎂 28.0013、硫酸根＋氯 91.3253",
    near(float(r5["CaMg_pct"]), 28.0013) and near(float(r5["SO4Cl_pct"]), 91.3253),
    (r5["CaMg_pct"], r5["SO4Cl_pct"]),
)
fc, fs = DIAMOND[0.0]
sc, ss = DIAMOND[1.0]
c1, s1 = DIAMOND[0.01]
c5, s5 = DIAMOND[0.05]
dt = math.hypot(sc - fc, ss - fs)
p1 = math.hypot(c1 - fc, s1 - fs) / dt
p5 = math.hypot(c5 - fc, s5 - fs) / dt
chk("1% 沿菱形連線走到 0.624088883285574", near(p1, PATH_1), p1)
chk("5% 沿菱形連線走到 0.8963526203369079", near(p5, PATH_5), p5)
chk("1% 已走過一半以上、約六成", p1 > 0.5 and 0.60 < p1 < 0.65)
end()
