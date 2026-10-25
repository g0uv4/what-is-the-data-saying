#!/usr/bin/env python3
"""sample-nichols-sim-s2-gain-shift-selfcheck.py：圖 S2 自我檢查。
從 sample-nichols-sim-s2-gain-shift.csv 核對增益 1 與 2 的存檔裕度與峰值，
以及 20·log10(2)。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-nichols-sim-s2-gain-shift-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-nichols-sim-s2-gain-shift.csv"
COLS = ["K", "gain_margin_dB", "phase_margin_deg", "closed_loop_peak_dB"]
RESULTS = []

SHIFT = 6.020599913279624
TOL = 1e-12

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def unchecked():
    skip("課程稿把 20·log10(2) 寫成 6.02 分貝", "公式是 6.020599913279624，存檔沒有 shift 欄")
    skip("圖 S1 的 21 列內插對上圖 S2 增益 1 的存檔", "圖 S2 存檔是密格 15.56／43.21／2.67，與圖 S1 內插不同檔")

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
    chk("第一行是表頭", first.startswith("K,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("2 列", len(rows) == 2, len(rows))
if not cols_ok or len(rows) != 2:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
ks = [float(r["K"]) for r in rows]
gms = [float(r["gain_margin_dB"]) for r in rows]
pms = [float(r["phase_margin_deg"]) for r in rows]
pks = [float(r["closed_loop_peak_dB"]) for r in rows]
chk("增益欄是 1 與 2", near(ks[0], 1.0) and near(ks[1], 2.0), ks)
chk(
    "增益 1 存檔 15.56、43.21、2.67",
    near(gms[0], 15.56) and near(pms[0], 43.21) and near(pks[0], 2.67),
    (gms[0], pms[0], pks[0]),
)
chk(
    "增益 2 存檔 9.54、25.39、7.32",
    near(gms[1], 9.54) and near(pms[1], 25.39) and near(pks[1], 7.32),
    (gms[1], pms[1], pks[1]),
)
shift = 20.0 * math.log10(2.0)
chk("20·log10(2) 是 6.020599913279624", near(shift, SHIFT), shift)
end()
