#!/usr/bin/env python3
"""sample-skewt-sim-s2-why-skew-selfcheck.py：圖 S2 自我檢查。
從 sample-skewt-sim-s2-why-skew.csv 核對同一份探空的 27 層氣壓。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-skewt-sim-s2-why-skew-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。左圖旋轉 0 度、右圖 45 度取自 sim_facts，是同一份探空畫兩次的圖參數。
CSV 只有一條溫度與露點，沒有旋轉角，印 NOT CHECKED。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-skewt-sim-s2-why-skew.csv"
COLS = ["pressure_hPa", "temperature_C", "dewpoint_C"]
LEVELS = [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 725, 700,
          650, 600, 550, 500, 450, 400, 350, 300, 250, 200, 175, 150, 125, 100]
RESULTS = []

# 模擬記載（寫死）。兩個旋轉角取自 sim_facts，CSV 核不到，只印 NOT CHECKED。
N_EXPECT = 27
P_SFC = 1000.0
P_TOP = 100.0
LEFT_ROTATION_DEG = 0
RIGHT_ROTATION_DEG = 45
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
        f"左圖旋轉 {LEFT_ROTATION_DEG} 度、右圖旋轉 {RIGHT_ROTATION_DEG} 度",
        "同一份探空畫兩次的圖參數；CSV 只有一條溫度與露點，不假造第二條曲線",
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
end()
