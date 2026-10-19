#!/usr/bin/env python3
"""sample-hovmoller-sim-s3-phase-group-selfcheck.py：圖 S3 自我檢查。
從 sample-hovmoller-sim-s3-phase-group.csv 核對寬表格（第幾天 × 經度）與波包脊線斜率。
只需 Python 標準函式庫。
用法：python3 sample-hovmoller-sim-s3-phase-group-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。群速每天 28 度、相速每天 10 度取自 sim_facts。
最大絕對值跟的是群速（量到約 27.99 度／日），不是單一個槽的相速。相速印 NOT CHECKED，不計失敗。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-hovmoller-sim-s3-phase-group.csv"
N_DAY = 51
COLS = ["day"] + [str(x) for x in range(0, 361, 4)]
RESULTS = []

# 模擬記載（寫死）。群速、相速取自 sim_facts。最大絕對值對的是群速。
GROUP_DEG_PER_DAY = 28.0
PHASE_DEG_PER_DAY = 10.0
MEASURED_SLOPE = 27.99

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
chk("欄位：day 加上經度 0 到 360 每 4 度", ok, len(rows[0]))
if not ok:
    done()
data = rows[1:]
chk("51 列", len(data) == N_DAY)
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
    "天從 0 到 10、每 0.2 天",
    near(ts[0], 0.0) and near(ts[-1], 10.0) and all(near(ts[i + 1] - ts[i], 0.2, 1e-6) for i in range(len(ts) - 1)),
)
flat = [v for row in Z for v in row]
vmin, vmax = min(flat), max(flat)
chk(
    "高度距平有限，正負都超過 100 公尺",
    all(math.isfinite(v) for v in flat) and -200 < vmin < -100 and 100 < vmax < 200,
    f"{vmin:.3f}…{vmax:.3f}",
)
slope = lin_slope(ts, maxabs_lons(xs, Z))
chk(
    "最大絕對值跟群速：斜率約 27.99 度／日（記載 28），不是相速 10",
    near(slope, MEASURED_SLOPE, 0.01) and near(slope, GROUP_DEG_PER_DAY, 0.15) and abs(slope - GROUP_DEG_PER_DAY) < abs(slope - PHASE_DEG_PER_DAY),
    f"{slope:.2f}",
)
skip(f"相速每天 {PHASE_DEG_PER_DAY:.0f} 度", "最大絕對值黏在波包中心，跟的是群速；單一個槽沒有分開追")
skip("波數 7、北緯 50 度、相速每秒 8.3 公尺、群速每秒 23.2 公尺、雜訊 6 公尺", "過零次數不穩定；緯度與公尺每秒不在 CSV")
done()
