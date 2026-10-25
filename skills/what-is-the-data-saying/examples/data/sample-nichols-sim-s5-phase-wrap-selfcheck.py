#!/usr/bin/env python3
"""sample-nichols-sim-s5-phase-wrap-selfcheck.py：圖 S5 自我檢查。
從 sample-nichols-sim-s5-phase-wrap.csv 核對折回相位展開後等於存檔展開欄，
以及展開相位穿越 −180 度的對數頻率內插。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-nichols-sim-s5-phase-wrap-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-nichols-sim-s5-phase-wrap.csv"
COLS = ["omega_rad_s", "phase_wrapped_deg", "phase_unwrapped_deg", "open_loop_gain_dB"]
RESULTS = []

N_EXPECT = 21
W0 = 0.1
W_END = 31.6228
WRAP_LO = 1.77828
WRAP_HI = 2.37137
WRAP_P1 = -170.227
WRAP_P2 = 177.491
UNW_P2 = -182.509
G1 = -11.7106
G2 = -16.592
W180 = 2.235960633968452
G180 = -15.594814476469633
TOL = 1e-12

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def log_cross(xs, ys, target):
    found = []
    for i in range(len(ys) - 1):
        y1, y2 = ys[i], ys[i + 1]
        if (y1 - target) * (y2 - target) > 0:
            continue
        if y1 == y2:
            continue
        t = (target - y1) / (y2 - y1)
        if t < 0.0 or t > 1.0:
            continue
        x = math.exp(math.log(xs[i]) + t * (math.log(xs[i + 1]) - math.log(xs[i])))
        found.append((i, x, t))
    return found

def along(zs, i, t):
    return zs[i] + t * (zs[i + 1] - zs[i])

def unwrap_deg(ph):
    out = []
    prev = None
    acc = 0.0
    for a in ph:
        if prev is None:
            acc = a
        else:
            d = a - prev
            while d > 180.0:
                d -= 360.0
            while d < -180.0:
                d += 360.0
            acc += d
        out.append(acc)
        prev = a
    return out

def unchecked():
    skip("課程稿折回頻率正好 2.236、從 −180.0 跳到 179.9", "沒有存檔列在 2.236；鄰列是 −170.227 與 177.491／−182.509")
    skip("課程稿折回增益 −15.56", "這一檔內插增益是 −15.594814476469633")

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
    chk("第一行是表頭", first.startswith("omega_rad_s,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("21 列", len(rows) == N_EXPECT, len(rows))
if not cols_ok or len(rows) != N_EXPECT:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
ws = [float(r["omega_rad_s"]) for r in rows]
pw = [float(r["phase_wrapped_deg"]) for r in rows]
pu = [float(r["phase_unwrapped_deg"]) for r in rows]
gs = [float(r["open_loop_gain_dB"]) for r in rows]
chk(
    "頻率從 0.1 到 31.6228 且嚴格遞增",
    near(ws[0], W0) and near(ws[-1], W_END) and all(ws[i] < ws[i + 1] for i in range(len(ws) - 1)),
)
uw = unwrap_deg(pw)
diffs = [abs(uw[i] - pu[i]) for i in range(len(uw))]
chk("由折回欄展開後與存檔展開欄一致，最大絕對差 0.0", near(max(diffs), 0.0), max(diffs))
wraps = [i for i in range(len(pw) - 1) if abs(pw[i + 1] - pw[i]) > 180.0]
chk("折回正好一次，在 1.77828 與 2.37137 之間", len(wraps) == 1, len(wraps))
if len(wraps) == 1:
    i = wraps[0]
    chk(
        "折回鄰列 −170.227 → 177.491，展開 −170.227 → −182.509",
        near(ws[i], WRAP_LO)
        and near(ws[i + 1], WRAP_HI)
        and near(pw[i], WRAP_P1)
        and near(pw[i + 1], WRAP_P2)
        and near(pu[i], WRAP_P1)
        and near(pu[i + 1], UNW_P2)
        and near(gs[i], G1)
        and near(gs[i + 1], G2),
        (ws[i], ws[i + 1], pw[i], pw[i + 1], pu[i], pu[i + 1]),
    )
p_hits = log_cross(ws, pu, -180.0)
chk("展開相位穿越 −180 度正好一次", len(p_hits) == 1, len(p_hits))
if len(p_hits) != 1:
    end()
ip, w, t = p_hits[0]
g180 = along(gs, ip, t)
chk("展開 −180 度在頻率 2.235960633968452", near(w, W180), w)
chk("同一內插的開迴路增益 −15.594814476469633", near(g180, G180), g180)
end()
