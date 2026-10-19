#!/usr/bin/env python3
"""sample-skewt-sim-s1-anatomy-selfcheck.py：圖 S1 自我檢查。
從 sample-skewt-sim-s1-anatomy.csv 核對 27 層氣壓，並在對數氣壓上內插 500 百帕的溫度。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-skewt-sim-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。500 百帕 −5.7 度取自 sim_facts。該層有列，內插落在端點，不是拿 550 與 450 跨過去。
垂直誤讀 20.2 度與斜角 45 度是圖軸的座標變換，探空欄位重算不了，印 NOT CHECKED。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-skewt-sim-s1-anatomy.csv"
COLS = ["pressure_hPa", "temperature_C", "dewpoint_C", "wind_speed_kt", "wind_dir_deg"]
LEVELS = [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 725, 700,
          650, 600, 550, 500, 450, 400, 350, 300, 250, 200, 175, 150, 125, 100]
RESULTS = []

# 模擬記載（寫死）。500 百帕溫度取自 sim_facts。誤讀與斜角只印 NOT CHECKED。
N_EXPECT = 27
P_SFC = 1000.0
P_TOP = 100.0
P_READ = 500.0
T500_C = -5.7
VERTICAL_MISREAD_C = 20.2
ROTATION_DEG = 45
TOL = 1e-9
TOL_T = 0.05

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip(
        f"垂直往下誤讀 {VERTICAL_MISREAD_C} 度",
        "要斜溫圖的座標變換；探空欄位沒有圖軸，不假算螢幕上的讀數",
    )
    skip(
        f"等溫線斜角 {ROTATION_DEG} 度",
        "是畫圖參數，不在 CSV",
    )

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def end():
    unchecked()
    done()

def interp_logp(ps, ys, target):
    """y 對 log(氣壓) 線性。目標落在某一層（含端點）就回該層，不跨過已有的層。"""
    for i in range(len(ps) - 1):
        p1, p2 = ps[i], ps[i + 1]
        if (p1 - target) * (p2 - target) > 0:
            continue
        if p1 == p2:
            continue
        t = (math.log(target) - math.log(p1)) / (math.log(p2) - math.log(p1))
        if t < -1e-9 or t > 1.0 + 1e-9:
            continue
        return ys[i] + t * (ys[i + 1] - ys[i])
    return None

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
chk(
    "氣壓就是 27 層，從 1000 到 100 百帕且嚴格遞減",
    len(ps) == len(LEVELS) and all(near(a, float(b)) for a, b in zip(ps, LEVELS)) and all(ps[i] > ps[i + 1] for i in range(len(ps) - 1)) and near(ps[0], P_SFC) and near(ps[-1], P_TOP),
)
chk("溫度與露點是有限數，且露點不高於溫度", all(math.isfinite(t) and math.isfinite(d) and d <= t + TOL for t, d in zip(ts, tds)))
row500 = None
for r in rows:
    if near(float(r["pressure_hPa"]), P_READ):
        row500 = r
        break
chk("有 500 百帕那一層", row500 is not None)
t500 = interp_logp(ps, ts, P_READ)
chk("500 百帕落在相鄰兩層的閉區間，可以內插", t500 is not None, t500)
if row500 is None or t500 is None:
    end()
chk(
    "對數氣壓內插的 500 百帕溫度約 -5.7 度（落在該層）",
    near(t500, T500_C, TOL_T) and near(t500, float(row500["temperature_C"]), TOL_T),
    t500,
)
end()
