#!/usr/bin/env python3
"""sample-piper-sim-s2-conversion-selfcheck.py：圖 S2 自我檢查。
從 sample-piper-sim-s2-conversion.csv 核對毫克換毫當量、質量比例與當量比例、
陽陰離子總量與電荷平衡。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-piper-sim-s2-conversion-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
比例由存檔的毫克與毫當量重算。課程稿四捨五入的 11.7、20.0、80.6、71.9、73.3、81.1、37.06、38.25、−1.58 不是這一檔的原列。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-piper-sim-s2-conversion.csv"
COLS = ["ion", "mg_per_L", "equivalent_weight", "meq_per_L"]
IONS = ["Ca", "Mg", "Na", "K", "HCO3", "SO4", "Cl"]
RESULTS = []

STORED = {
    "Ca": (60.0, 20.039, 2.99416),
    "Mg": (90.0, 12.1525, 7.40588),
    "Na": (600.0, 22.99, 26.0983),
    "K": (22.0, 39.098, 0.562689),
    "HCO3": (250.0, 61.017, 4.09722),
    "SO4": (150.0, 48.03, 3.12305),
    "Cl": (1100.0, 35.453, 31.027),
}
CAT_MG = 772.0
AN_MG = 1500.0
CAT_MEQ = 37.061029
AN_MEQ = 38.24727
NAK_MEQ = 26.660988999999997
IB = -1.5751796491911236
MG_MASS = 11.658031088082902
MG_EQ = 19.98293139675102
NAK_MASS = 80.56994818652849
NAK_EQ = 71.93807004117451
CA_MASS = 7.772020725388601
CA_EQ = 8.078998562074464
HCO3_MASS = 16.666666666666668
HCO3_EQ = 10.712450849433175
SO4_MASS = 10.0
SO4_EQ = 8.165419388102732
CL_MASS = 73.33333333333333
CL_EQ = 81.1221297624641
MEQ_TOL = 1e-5
TOL = 1e-12

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def unchecked():
    skip("當量重寫成 20.04、12.15、39.10、61.02、35.45", "存檔是 20.039、12.1525、39.098、61.017、35.453；鈉 22.99、硫酸根 48.03 與記載相同")
    skip("鎂質量 11.7%、當量 20.0%；鈉＋鉀 80.6→71.9；氯 73.3→81.1", "由存檔重算是 11.658031088082902、19.98293139675102、80.56994818652849、71.93807004117451、73.33333333333333、81.1221297624641")
    skip("陽離子 37.06、陰離子 38.25 毫當量每公升，電荷差 −1.58%", "存檔加總是 37.061029 與 38.24727，電荷差 −1.5751796491911236")

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
    chk("第一行是表頭", first.startswith("ion,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("7 列", len(rows) == 7, len(rows))
if not cols_ok or len(rows) != 7:
    end()
empty = any(any((r[c] or "").strip() == "" for c in COLS) for r in rows)
chk("沒有空值", not empty)
if empty:
    end()
names = [r["ion"] for r in rows]
chk("離子順序是鈣鎂鈉鉀碳酸氫根硫酸根氯", names == IONS, names)
got = {}
ok_stored = True
ok_div = True
max_div = 0.0
for r in rows:
    ion = r["ion"]
    mg, ew, meq = float(r["mg_per_L"]), float(r["equivalent_weight"]), float(r["meq_per_L"])
    exp = STORED[ion]
    if not (near(mg, exp[0]) and near(ew, exp[1]) and near(meq, exp[2])):
        ok_stored = False
    recom = mg / ew
    max_div = max(max_div, abs(recom - meq))
    if abs(recom - meq) > MEQ_TOL:
        ok_div = False
    got[ion] = (mg, ew, meq)
chk("存檔的毫克、當量重、毫當量", ok_stored, {k: got[k] for k in IONS})
chk("毫當量＝毫克÷當量重（存檔四捨五入）", ok_div, max_div)
chk("當量重 40.078／2 與 24.305／2、96.06／2", near(got["Ca"][1], 40.078 / 2) and near(got["Mg"][1], 24.305 / 2) and near(got["SO4"][1], 96.06 / 2))
cat_mg = got["Ca"][0] + got["Mg"][0] + got["Na"][0] + got["K"][0]
an_mg = got["HCO3"][0] + got["SO4"][0] + got["Cl"][0]
cat_meq = got["Ca"][2] + got["Mg"][2] + got["Na"][2] + got["K"][2]
an_meq = got["HCO3"][2] + got["SO4"][2] + got["Cl"][2]
nak_meq = got["Na"][2] + got["K"][2]
chk("陽離子毫克合計 772", near(cat_mg, CAT_MG), cat_mg)
chk("陰離子毫克合計 1500", near(an_mg, AN_MG), an_mg)
chk("陽離子毫當量合計 37.061029", near(cat_meq, CAT_MEQ), cat_meq)
chk("陰離子毫當量合計 38.24727", near(an_meq, AN_MEQ), an_meq)
chk("鈉＋鉀毫當量 26.660988999999997", near(nak_meq, NAK_MEQ), nak_meq)
ib = 100.0 * (cat_meq - an_meq) / (cat_meq + an_meq)
chk("電荷差 −1.5751796491911236%", near(ib, IB), ib)
chk("鎂質量比例 11.658031088082902%", near(100.0 * got["Mg"][0] / cat_mg, MG_MASS))
chk("鎂當量比例 19.98293139675102%", near(100.0 * got["Mg"][2] / cat_meq, MG_EQ))
chk("鈉＋鉀質量比例 80.56994818652849%", near(100.0 * (got["Na"][0] + got["K"][0]) / cat_mg, NAK_MASS))
chk("鈉＋鉀當量比例 71.93807004117451%", near(100.0 * nak_meq / cat_meq, NAK_EQ))
chk("鈣質量與當量比例", near(100.0 * got["Ca"][0] / cat_mg, CA_MASS) and near(100.0 * got["Ca"][2] / cat_meq, CA_EQ))
chk("碳酸氫根質量與當量比例", near(100.0 * got["HCO3"][0] / an_mg, HCO3_MASS) and near(100.0 * got["HCO3"][2] / an_meq, HCO3_EQ))
chk("硫酸根質量 10%、當量 8.165419388102732%", near(100.0 * got["SO4"][0] / an_mg, SO4_MASS) and near(100.0 * got["SO4"][2] / an_meq, SO4_EQ))
chk("氯質量比例 73.33333333333333%", near(100.0 * got["Cl"][0] / an_mg, CL_MASS))
chk("氯當量比例 81.1221297624641%", near(100.0 * got["Cl"][2] / an_meq, CL_EQ))
end()
