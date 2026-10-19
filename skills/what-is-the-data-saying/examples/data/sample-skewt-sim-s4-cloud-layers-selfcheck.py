#!/usr/bin/env python3
"""sample-skewt-sim-s4-cloud-layers-selfcheck.py：圖 S4 自我檢查。
從 sample-skewt-sim-s4-cloud-layers.csv 用溫度減露點不大於 2.0 度切連續層。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-skewt-sim-s4-cloud-layers-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。門檻 2.0 度與層 [975, 775]、[400, 350] 百帕取自 sim_facts。
至少連續兩層才算一層，與繪圖時相同。差 2 度當雲是經驗判斷，這裡只核對氣壓層，不斷言真的有雲。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-skewt-sim-s4-cloud-layers.csv"
COLS = ["pressure_hPa", "temperature_C", "dewpoint_C", "dewpoint_depression_C"]
LEVELS = [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 725, 700,
          650, 600, 550, 500, 450, 400, 350, 300, 250, 200, 175, 150, 125, 100]
RESULTS = []

# 模擬記載（寫死）。門檻與兩層氣壓取自 sim_facts，可由露點差欄重切。
N_EXPECT = 27
P_SFC = 1000.0
P_TOP = 100.0
THRESH_C = 2.0
LAYERS_HPA = [(975.0, 775.0), (400.0, 350.0)]
TOL = 1e-9

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip(
        f"露點差 {THRESH_C} 度以內是不是雲",
        "門檻是經驗判斷，各家不同；這裡只核對溫度減露點切出的氣壓層",
    )

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def end():
    unchecked()
    done()

def same_layers(got, exp):
    if len(got) != len(exp):
        return False
    return all(near(a, c) and near(b, d) for (a, b), (c, d) in zip(got, exp))

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("pressure_hPa,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
chk("欄位", list(rows[0].keys()) == COLS)
chk("27 列", len(rows) == N_EXPECT)
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
if empty or list(rows[0].keys()) != COLS:
    end()
ps = [float(r["pressure_hPa"]) for r in rows]
ts = [float(r["temperature_C"]) for r in rows]
tds = [float(r["dewpoint_C"]) for r in rows]
dep = [float(r["dewpoint_depression_C"]) for r in rows]
chk(
    "氣壓就是 27 層，從 1000 到 100 百帕且嚴格遞減",
    len(ps) == len(LEVELS) and all(near(a, float(b)) for a, b in zip(ps, LEVELS)) and all(ps[i] > ps[i + 1] for i in range(len(ps) - 1)) and near(ps[0], P_SFC) and near(ps[-1], P_TOP),
)
chk("溫度、露點、露點差是有限數，且露點不高於溫度", all(math.isfinite(t) and math.isfinite(d) and math.isfinite(x) and d <= t + TOL for t, d, x in zip(ts, tds, dep)))
chk("露點差欄等於溫度減露點", all(near(x, t - d, 1e-6) for t, d, x in zip(ts, tds, dep)))
runs, cur = [], []
for p, x in zip(ps, dep):
    if x <= THRESH_C:
        cur.append(p)
    elif cur:
        runs.append(cur)
        cur = []
if cur:
    runs.append(cur)
chk("沒有落單的一層（至少連續兩層才保留）", runs != [] and all(len(r) >= 2 for r in runs), [len(r) for r in runs])
got = [(max(r), min(r)) for r in runs if len(r) >= 2]
chk(
    "露點差不大於 2.0 度的層是 [975, 775] 與 [400, 350] 百帕",
    same_layers(got, LAYERS_HPA),
    got,
)
end()
