#!/usr/bin/env python3
"""sample-hr-sim-s4-overplotting-3000-selfcheck.py：圖 S4 自我檢查。
從 sample-hr-sim-s4-overplotting-3000.csv 核對 3,000 列樣本的三群比例。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-hr-sim-s4-overplotting-3000-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。母體 200,000（主序 170,000、巨星 24,000、白矮星 6,000）取自 sim_facts。
CSV 只是樣本，母體人數印 NOT CHECKED。樣本比例對母體的 85%、12%、3%，容許差 2 個百分點。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-hr-sim-s4-overplotting-3000.csv"
COLS = ["B_V", "abs_V_mag", "group"]
RESULTS = []

# 模擬記載（寫死）。母體人數取自 sim_facts，樣本核不到。85/12/3 是母體份額。
N_EXPECT = 3000
N_TOTAL = 200000
N_MS = 170000
N_GIANT = 24000
N_WD = 6000
SHARES = (("main_sequence", 0.85, "主序"), ("giant", 0.12, "巨星"), ("white_dwarf", 0.03, "白矮星"))
SHARE_TOL = 0.02

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip(
        f"母體 {N_TOTAL:,} 顆（主序 {N_MS:,}、巨星 {N_GIANT:,}、白矮星 {N_WD:,}）",
        "CSV 只是抽 3,000 列的樣本，沒有母體總數；上面只核樣本比例跟 85/12/3 差不到 2 個百分點",
    )

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
    chk("第一行是表頭", first.startswith("B_V,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("3,000 列", len(rows) == N_EXPECT, len(rows))
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
nums_ok = True
for r in rows:
    try:
        bv, mag = float(r["B_V"]), float(r["abs_V_mag"])
    except ValueError:
        nums_ok = False
        break
    if not (math.isfinite(bv) and math.isfinite(mag)):
        nums_ok = False
chk("顏色與絕對星等是有限數", nums_ok)
if not nums_ok:
    end()
counts = {key: 0 for key, _, _ in SHARES}
extra = 0
for r in rows:
    if r["group"] in counts:
        counts[r["group"]] += 1
    else:
        extra += 1
chk("群組只有主序、巨星、白矮星", extra == 0 and sum(counts.values()) == len(rows), extra)
for key, exp, label in SHARES:
    share = counts[key] / len(rows)
    chk(
        f"{label}約 {round(exp * 100)}%（差在 2 個百分點以內）",
        abs(share - exp) <= SHARE_TOL,
        (counts[key], round(share * 100, 2)),
    )
end()
