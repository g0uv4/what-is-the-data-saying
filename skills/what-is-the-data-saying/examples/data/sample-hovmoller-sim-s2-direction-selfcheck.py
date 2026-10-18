#!/usr/bin/env python3
"""sample-hovmoller-sim-s2-direction-selfcheck.py：圖 S2 自我檢查。
從 sample-hovmoller-sim-s2-direction.csv 核對寬表格（第幾天 × 經度）與停在經度 200 的正距平。
只需 Python 標準函式庫。
用法：python3 sample-hovmoller-sim-s2-direction-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。停滯經度 200 取自 sim_facts。
往東每天 +6 度、往西每天 -8 度印 NOT CHECKED：最大絕對值在三條脊之間跳，不計失敗。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-hovmoller-sim-s2-direction.csv"
N_DAY = 31
COLS = ["day"] + [str(x) for x in range(0, 361, 5)]
RESULTS = []

# 模擬記載（寫死）。停滯經度取自 sim_facts。往東、往西的度／日這份格子的單一脊線證不了。
STATIONARY_LON = 200.0
EAST_DEG_PER_DAY = 6.0
WEST_DEG_PER_DAY = -8.0

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
chk("31 列", len(data) == N_DAY)
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
    "天從 0 到 30 且每天一列",
    near(ts[0], 0.0) and near(ts[-1], 30.0) and all(near(ts[i + 1] - ts[i], 1.0) for i in range(len(ts) - 1)),
)
flat = [v for row in Z for v in row]
vmin, vmax = min(flat), max(flat)
chk(
    "距平有限、有正有負",
    all(math.isfinite(v) for v in flat) and -2.5 < vmin < -1 and 1 < vmax < 2.5,
    f"{vmin:.3f}…{vmax:.3f}",
)
n_at = 0
best_v, best_x = None, None
for row in Z:
    j = max(range(len(row)), key=lambda k: row[k])
    if near(xs[j], STATIONARY_LON):
        n_at += 1
    for k, v in enumerate(row):
        if best_v is None or v > best_v:
            best_v, best_x = v, xs[k]
chk("有 19 天的列最大值落在經度 200（停滯）", n_at == 19, n_at)
chk("全場最大正值在經度 200", near(best_x, STATIONARY_LON) and best_v > 1, f"{best_v:.3f} 在 {best_x:.0f}")
mixed = lin_slope(ts, maxabs_lons(xs, Z))
skip(
    f"往東每天 {EAST_DEG_PER_DAY:.0f} 度與往西每天 {WEST_DEG_PER_DAY:.0f} 度",
    f"最大絕對值整段斜率 {mixed:.2f}，往東、往西、停滯三條脊混在一起",
)
skip("赤道每秒 7.7 與 10.3 公尺、雜訊標準差 0.1", "公尺每秒要先有分開的斜率；雜訊與訊號在同一格")
done()
