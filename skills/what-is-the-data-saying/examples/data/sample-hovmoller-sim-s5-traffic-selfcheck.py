#!/usr/bin/env python3
"""sample-hovmoller-sim-s5-traffic-selfcheck.py：圖 S5 自我檢查。
從 sample-hovmoller-sim-s5-traffic.csv 核對寬表格（第幾分鐘 × 公路里程）與車速範圍。
只需 Python 標準函式庫。
用法：python3 sample-hovmoller-sim-s5-traffic-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。自由流每小時 90 公里取自 sim_facts。
高速區平均接近 90；低於自由流一半的格子有 183 個。塞車波每小時 -18 公里印 NOT CHECKED，不計失敗。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-hovmoller-sim-s5-traffic.csv"
N_MIN = 61
COLS = ["minute"] + [str(i // 2) if i % 2 == 0 else str(i // 2) + ".5" for i in range(41)]
RESULTS = []

# 模擬記載（寫死）。自由流與塞車波取自 sim_facts。塞車波速度這份格子的單一谷線證不了。
FREE_FLOW_KMH = 90.0
JAM_WAVE_KMH = -18.0
N_LOW = 183

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

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("minute,"))
    fh.seek(0)
    rows = list(csv.reader(fh))
ok = rows[0] == COLS
chk("欄位：minute 加上里程 0 到 20 每 0.5 公里", ok, len(rows[0]))
if not ok:
    done()
data = rows[1:]
chk("61 列", len(data) == N_MIN)
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
    "分鐘從 0 到 60 且每分鐘一列",
    near(ts[0], 0.0) and near(ts[-1], 60.0) and all(near(ts[i + 1] - ts[i], 1.0) for i in range(len(ts) - 1)),
)
chk(
    "里程從 0 到 20、每 0.5 公里",
    len(xs) == 41 and near(xs[0], 0.0) and near(xs[-1], 20.0) and all(near(xs[i + 1] - xs[i], 0.5, 1e-6) for i in range(len(xs) - 1)),
)
flat = [v for row in Z for v in row]
vmin, vmax = min(flat), max(flat)
chk(
    "車速有限且落在 0 到 100",
    len(flat) == N_MIN * 41 and all(math.isfinite(v) and 0 < v <= 100 for v in flat),
    f"{vmin:.3f}…{vmax:.3f}",
)
hi = [v for v in flat if v >= 80.0]
mean_hi = sum(hi) / len(hi)
median = sorted(flat)[len(flat) // 2]
chk(
    "高速區平均與中位數接近自由流每小時 90 公里",
    near(mean_hi, FREE_FLOW_KMH, 1.5) and near(median, FREE_FLOW_KMH, 3.0) and vmax >= FREE_FLOW_KMH,
    f"高速平均 {mean_hi:.2f}、中位數 {median:.2f}、單格最大 {vmax:.1f}",
)
n_low = sum(1 for v in flat if v < FREE_FLOW_KMH / 2.0)
chk("低於自由流一半（每小時 45 公里）的格子有 183 個", n_low == N_LOW, n_low)
skip(
    f"塞車波每小時 {JAM_WAVE_KMH:.0f} 公里",
    "慢速谷有三團，每分鐘最慢的位置會換團，不是一條直線",
)
skip("波團 3 個、車輛駛離第 14.3 分鐘、雜訊標準差每小時 3 公里", "駛離時間要沿速度積分，CSV 沒有軌跡；波團要另外分群")
done()
