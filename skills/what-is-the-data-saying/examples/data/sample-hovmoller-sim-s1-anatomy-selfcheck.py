#!/usr/bin/env python3
"""sample-hovmoller-sim-s1-anatomy-selfcheck.py：圖 S1 自我檢查。
從 sample-hovmoller-sim-s1-anatomy.csv 核對寬表格（第幾天 × 經度）與雲團脊線斜率。
只需 Python 標準函式庫。
用法：python3 sample-hovmoller-sim-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。每天 3.89 度、約每秒 5 公尺取自 sim_facts。
最大絕對值的經度斜率量到約 3.915 度／日。起始經度與雜訊標準差印 NOT CHECKED，不計失敗。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-hovmoller-sim-s1-anatomy.csv"
N_DAY = 61
COLS = ["day"] + [str(x) for x in range(0, 361, 5)]
RESULTS = []

# 模擬記載（寫死）。度／日與每秒公尺取自 sim_facts。斜率對的是格子上的最大絕對值。
DEG_PER_DAY = 3.89
SPEED_M_PER_S = 5.0
MEASURED_SLOPE = 3.915
KM_PER_DEG = 111.2
SEC_PER_DAY = 86400.0

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def near(got, exp, tol=1e-9):
    return abs(got - exp) <= tol

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def lin_slope(ts, ys):
    n = len(ts)
    mt = sum(ts) / n
    my = sum(ys) / n
    num = sum((t - mt) * (y - my) for t, y in zip(ts, ys))
    den = sum((t - mt) ** 2 for t in ts)
    return num / den

def maxabs_lons(xs, Z):
    # 0° 與 360° 是同一條經線，去掉尾欄，避免兩格搶最大絕對值。
    if abs((xs[-1] - xs[0]) - 360.0) <= 1e-6:
        xs = xs[:-1]
        Z = [row[:-1] for row in Z]
    raw = []
    for row in Z:
        j = max(range(len(row)), key=lambda k: abs(row[k]))
        raw.append(xs[j])
    out = [raw[0]]
    for lon in raw[1:]:
        shift = round((out[-1] - lon) / 360.0)
        out.append(lon + shift * 360.0)
    return out

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("day,"))
    fh.seek(0)
    rows = list(csv.reader(fh))
ok = rows[0] == COLS
chk("欄位：day 加上經度 0 到 360 每 5 度", ok, len(rows[0]))
if not ok:
    done()
data = rows[1:]
chk("61 列", len(data) == N_DAY)
empty = False
for row in data:
    if len(row) != len(COLS):
        empty = True
    for c in row:
        if (c or "").strip() == "":
            empty = True
chk("沒有空值且每列等寬", not empty)
if empty:
    done()
ts = [float(row[0]) for row in data]
xs = [float(c) for c in rows[0][1:]]
Z = [[float(v) for v in row[1:]] for row in data]
chk(
    "天從 0 到 60 且每天一列",
    near(ts[0], 0.0) and near(ts[-1], 60.0) and all(near(ts[i + 1] - ts[i], 1.0) for i in range(len(ts) - 1)),
)
flat = [v for row in Z for v in row]
vmin, vmax = min(flat), max(flat)
chk(
    "數值有限，深負值到近零（負＝雲）",
    all(math.isfinite(v) for v in flat) and vmin < -2 and vmin > -3 and 0 < vmax < 0.5,
    f"{vmin:.3f}…{vmax:.3f}",
)
slope = lin_slope(ts, maxabs_lons(xs, Z))
chk(
    "最大絕對值經度斜率約 3.915 度／日（記載 3.89）",
    near(slope, MEASURED_SLOPE, 0.005) and near(slope, DEG_PER_DAY, 0.05),
    f"{slope:.3f}",
)
mps = slope * KM_PER_DEG * 1000.0 / SEC_PER_DAY
chk(
    "斜率換算赤道附近約每秒 5 公尺",
    near(mps, SPEED_M_PER_S, 0.15),
    f"{mps:.2f}",
)
skip("起始經度 50 與第 60 天經度 283.1", "記載的是連續中心；5 度格上的最大絕對值對不到這兩個數")
skip("雜訊標準差 0.12", "平滑後的雲團與雜訊在同一格，拆不出標準差")
done()
