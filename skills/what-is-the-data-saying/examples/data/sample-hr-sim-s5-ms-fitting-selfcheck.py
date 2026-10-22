#!/usr/bin/env python3
"""sample-hr-sim-s5-ms-fitting-selfcheck.py：圖 S5 自我檢查。
從 sample-hr-sim-s5-ms-fitting.csv 數星團列數，並把記載的距離模數代進距離公式。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-hr-sim-s5-ms-fitting-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。距離模數 8.0、398.1 秒差距、235 顆、消光設成 0 取自 sim_facts。
398.1 是 10^(8/5+1) 四捨五入到一位小數。表裡沒有絕對星等，模數與消光印 NOT CHECKED。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-hr-sim-s5-ms-fitting.csv"
COLS = ["B_V", "apparent_V_mag", "branch"]
RESULTS = []

# 模擬記載（寫死）。模數、秒差距、人數、消光取自 sim_facts。秒差距由模數重算。
N_EXPECT = 235
DM = 8.0
DIST_PC = 398.1
TOL_PC = 0.05

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip(
        f"這團星的距離模數就是 {DM}",
        "表裡只有視星等，沒有絕對星等；上面的秒差距只是把寫死的模數代進公式，不是從這份 CSV 配出來的",
    )
    skip(
        "消光設成 0",
        "CSV 沒有消光欄，不能證明有沒有扣",
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
chk("星團 235 列", len(rows) == N_EXPECT, len(rows))
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
        bv, mag = float(r["B_V"]), float(r["apparent_V_mag"])
    except ValueError:
        nums_ok = False
        break
    if not (math.isfinite(bv) and math.isfinite(mag)):
        nums_ok = False
chk("顏色與視星等是有限數", nums_ok)
dist = 10 ** (DM / 5 + 1)
chk(
    "距離模數 8.0 代入 10^(模數/5+1) 得 398.1 秒差距",
    abs(dist - DIST_PC) <= TOL_PC and round(dist, 1) == DIST_PC,
    dist,
)
end()
