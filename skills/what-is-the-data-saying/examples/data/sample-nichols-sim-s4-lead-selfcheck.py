#!/usr/bin/env python3
"""sample-nichols-sim-s4-lead-selfcheck.py：圖 S4 自我檢查。
從 sample-nichols-sim-s4-lead.csv 核對補償前與領先補償後的存檔裕度與峰值，
以及 6 分貝圈公式 20·log10((M+1)/M) 與 2·arcsin(1/(2M))，M=2。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-nichols-sim-s4-lead-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-nichols-sim-s4-lead.csv"
COLS = ["case", "gain_margin_dB", "phase_margin_deg", "closed_loop_peak_dB"]
RESULTS = []

FORM_GM = 3.5218251811136247
FORM_PM = 28.955024371859846
TOL = 1e-12

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def unchecked():
    skip("課程稿增益 3", "CSV 沒有 K 欄")
    skip("領先補償 (1+0.6s)/(1+0.1s)", "CSV 沒有轉移函數欄")
    skip("6 分貝圈公式寫成 3.52 分貝、28.96 度", "公式是 3.5218251811136247 與 28.955024371859846")
    skip("six_dB_circle_check 的 −151.25、28.75、−150.25、−3.5、3.5", "不在這一檔")

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
    chk("第一行是表頭", first.startswith("case,"))
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
cases = [r["case"] for r in rows]
gms = [float(r["gain_margin_dB"]) for r in rows]
pms = [float(r["phase_margin_deg"]) for r in rows]
pks = [float(r["closed_loop_peak_dB"]) for r in rows]
chk("兩列是 before 與 lead", cases == ["before", "lead"], cases)
chk(
    "補償前存檔 6.02、15.55、11.67",
    near(gms[0], 6.02) and near(pms[0], 15.55) and near(pks[0], 11.67),
    (gms[0], pms[0], pks[0]),
)
chk(
    "補償後存檔 16.43、44.51、2.46",
    near(gms[1], 16.43) and near(pms[1], 44.51) and near(pks[1], 2.46),
    (gms[1], pms[1], pks[1]),
)
M = 2.0
form_gm = 20.0 * math.log10((M + 1.0) / M)
form_pm = 2.0 * math.asin(1.0 / (2.0 * M)) * 180.0 / math.pi
chk("6 分貝圈公式增益下限 3.5218251811136247 分貝", near(form_gm, FORM_GM), form_gm)
chk("6 分貝圈公式相位下限 28.955024371859846 度", near(form_pm, FORM_PM), form_pm)
end()
