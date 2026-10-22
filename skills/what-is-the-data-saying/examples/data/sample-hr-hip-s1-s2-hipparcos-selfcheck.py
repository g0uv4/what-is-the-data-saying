#!/usr/bin/env python3
"""sample-hr-hip-s1-s2-hipparcos-selfcheck.py：圖 S1、S2 自我檢查。
從 sample-hr-hip-s1-s2-hipparcos.csv 核對同一份依巴谷樣本。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-hr-hip-s1-s2-hipparcos-selfcheck.py   全部通過時結束碼為 0。
依巴谷公開資料，不是模擬。17,746 列、視差相對誤差、絕對星等公式、最亮最暗、視星等範圍、白矮星框從 CSV 重算。
絕對星等在檔裡收到三位小數，公式容差 0.002。太陽符號與下載截斷不在表裡，印 NOT CHECKED。
這份約 60 萬位元組，檔案上限用 100 萬，不用 25 萬。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-hr-hip-s1-s2-hipparcos.csv"
COLS = ["hip", "V_mag", "B_V", "parallax_mas", "parallax_err_mas", "abs_V_mag"]
RESULTS = []

# 記載（寫死）。取自 sim_facts 的 S1、S2。太陽與下載註記只印 NOT CHECKED。
N_EXPECT = 17746
BRIGHTEST_M = -5.53
FAINTEST_M = 12.14
V_MIN = -0.62
V_MAX = 11.39
N_WD_BOX = 1
SUN_BV = 0.65
SUN_M = 4.83
RATIO_MAX = 0.10
TOL_M = 0.002
TOL_EXT = 0.005
TOL = 1e-9
MAX_BYTES = 1000000

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip(
        f"太陽在 B−V {SUN_BV}、絕對星等 {SUN_M}",
        "是圖上另加的符號，星表沒有太陽這一列",
    )
    skip(
        "下載在編號 111274 截斷、約 94%、原始上限 40000 列",
        "CSV 沒有星表總數，也沒有被截掉的列；相對誤差小於 0.10 已在上面核過",
    )

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def end():
    unchecked()
    done()

path = os.path.join(HERE, FN)
chk("檔案小於 100 萬位元組", os.path.getsize(path) < MAX_BYTES)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("hip,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("17,746 列", len(rows) == N_EXPECT, len(rows))
if not cols_ok:
    end()
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
if empty:
    end()
Vs = [float(r["V_mag"]) for r in rows]
bvs = [float(r["B_V"]) for r in rows]
plxs = [float(r["parallax_mas"]) for r in rows]
errs = [float(r["parallax_err_mas"]) for r in rows]
Ms = [float(r["abs_V_mag"]) for r in rows]
finite = all(math.isfinite(v) and math.isfinite(b) and math.isfinite(p) and math.isfinite(e) and math.isfinite(m) for v, b, p, e, m in zip(Vs, bvs, plxs, errs, Ms))
chk("星等、顏色、視差是有限數", finite)
if not finite:
    end()
ratios = []
ok_ratio = True
for e, p in zip(errs, plxs):
    if not p > 0:
        ok_ratio = False
        continue
    ratio = e / p
    ratios.append(ratio)
    if not ratio < RATIO_MAX:
        ok_ratio = False
chk(
    "每一顆視差都是正的，且視差誤差／視差小於 0.10",
    ok_ratio and len(ratios) == len(rows),
    max(ratios) if ratios else None,
)
abs_errs = []
ok_mag = ok_ratio
if ok_ratio:
    for V, p, M in zip(Vs, plxs, Ms):
        pred = V + 5 + 5 * math.log10(p / 1000)
        diff = abs(M - pred)
        abs_errs.append(diff)
        if diff > TOL_M:
            ok_mag = False
chk(
    "絕對星等重算為 V + 5 + 5*log10(視差毫角秒/1000)，容差 0.002",
    ok_mag and len(abs_errs) == len(rows),
    max(abs_errs) if abs_errs else None,
)
chk(
    "最亮絕對星等 -5.53、最暗 12.14",
    near(min(Ms), BRIGHTEST_M, TOL_EXT) and near(max(Ms), FAINTEST_M, TOL_EXT) and round(min(Ms), 2) == BRIGHTEST_M and round(max(Ms), 2) == FAINTEST_M,
    (min(Ms), max(Ms)),
)
chk(
    "視星等從 -0.62 到 11.39",
    near(min(Vs), V_MIN) and near(max(Vs), V_MAX),
    (min(Vs), max(Vs)),
)
n_wd = sum(1 for M, b in zip(Ms, bvs) if M > 10 and b < 0.6)
chk("白矮星框（絕對星等 > 10 且 B−V < 0.6）有 1 顆", n_wd == N_WD_BOX, n_wd)
end()
