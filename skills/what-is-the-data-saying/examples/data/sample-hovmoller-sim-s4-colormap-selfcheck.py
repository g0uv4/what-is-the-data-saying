#!/usr/bin/env python3
"""sample-hovmoller-sim-s4-colormap-selfcheck.py：圖 S4 自我檢查。
從 sample-hovmoller-sim-s4-colormap.csv 核對寬表格（第幾天 × 經度）與沿經度的波數。
只需 Python 標準函式庫。
用法：python3 sample-hovmoller-sim-s4-colormap-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。波數 3 取自 sim_facts，對的是每一天繞經度一圈的 6 次變號。
色盤名稱與相速每天 6 度印 NOT CHECKED，不計失敗。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-hovmoller-sim-s4-colormap.csv"
N_DAY = 31
COLS = ["day"] + [str(x) for x in range(0, 361, 5)]
RESULTS = []

# 模擬記載（寫死）。波數取自 sim_facts。色盤名稱與相速不在這份數值格裡。
WAVENUMBER = 3
PHASE_DEG_PER_DAY = 6.0

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

def n_cross(row):
    c = 0
    m = len(row)
    for i in range(m):
        a, b = row[i], row[(i + 1) % m]
        if a == 0 or a * b < 0:
            c += 1
    return c

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
    "距平有限、正負都超過 1",
    all(math.isfinite(v) for v in flat) and -2.5 < vmin < -1 and 1 < vmax < 2.5,
    f"{vmin:.3f}…{vmax:.3f}",
)
# 去掉重複的 360°，沿 0…355 繞一圈。一次波有兩次變號。
circle = [row[:-1] for row in Z]
crosses = [n_cross(row) for row in circle]
chk(
    "每一天沿經度有 6 次變號（波數 3）",
    all(c == 2 * WAVENUMBER for c in crosses),
    crosses[0],
)
mixed = lin_slope(ts, maxabs_lons(xs, Z))
skip("色盤 jet（反例）與 RdBu_r＋等值線", "CSV 只有距平數字，沒有色盤名稱")
skip(
    f"相速每天 {PHASE_DEG_PER_DAY:.0f} 度與雜訊標準差 0.15",
    f"最大絕對值整段斜率 {mixed:.2f}，三條脊會互換，追不出相速；雜訊已混進數值",
)
done()
