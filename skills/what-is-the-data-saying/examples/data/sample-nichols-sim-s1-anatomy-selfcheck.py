#!/usr/bin/env python3
"""sample-nichols-sim-s1-anatomy-selfcheck.py：圖 S1 自我檢查。
從 sample-nichols-sim-s1-anatomy.csv 展開相位後，在對數頻率上線性內插
增益穿越與相位穿越，再算裕度；閉迴路峰值由存檔列重算 T=L/(1+L) 取最大。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-nichols-sim-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-nichols-sim-s1-anatomy.csv"
COLS = ["omega_rad_s", "open_loop_phase_deg", "open_loop_gain_dB"]
RESULTS = []

N_EXPECT = 21
W0 = 0.1
W_END = 10.0
GM = 15.595091495422169
WPC = 2.236075610614252
PM = 43.20281974826571
WGC = 0.7787726504594005
CL_PEAK = 2.6701705500584403
CL_W = 0.7943
WRAP_LO = 1.9953
WRAP_HI = 2.5119
WRAP_P1 = -175.136
WRAP_P2 = 175.034
UNW_P2 = -184.96600000000004
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

def cl_from_ol(phase_deg, gain_dB):
    mag = 10 ** (gain_dB / 20.0)
    th = phase_deg * math.pi / 180.0
    Lr = mag * math.cos(th)
    Li = mag * math.sin(th)
    den_r = 1.0 + Lr
    den_i = Li
    den2 = den_r * den_r + den_i * den_i
    Tr = (Lr * den_r + Li * den_i) / den2
    Ti = (Li * den_r - Lr * den_i) / den2
    return 20.0 * math.log10(math.hypot(Tr, Ti))

def unchecked():
    skip("課程稿密格增益裕度 15.56 分貝", "21 列對數頻率內插是 15.595091495422169，不是密格 15.56")
    skip("課程稿密格相位裕度 43.21 度", "21 列對數頻率內插是 43.20281974826571，不是密格 43.21")
    skip("課程稿密格閉迴路峰值 2.67 分貝、頻率 0.806", "存檔列重算峰值是 2.6701705500584403，頻率 0.7943")
    skip("課程稿密格相位穿越 2.236、增益穿越 0.779", "這一檔內插是 2.236075610614252 與 0.7787726504594005")
    skip("圖 R1 來源頁轉移函數的裕度 3.52 分貝、11.4 度、峰值 14.69 分貝", "沒有對應 CSV")

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
ps = [float(r["open_loop_phase_deg"]) for r in rows]
gs = [float(r["open_loop_gain_dB"]) for r in rows]
chk(
    "頻率從 0.1 到 10 且嚴格遞增",
    near(ws[0], W0) and near(ws[-1], W_END) and all(ws[i] < ws[i + 1] for i in range(len(ws) - 1)),
)
uw = unwrap_deg(ps)
g_hits = log_cross(ws, gs, 0.0)
p_hits = log_cross(ws, uw, -180.0)
chk("增益穿越 0 分貝正好一次", len(g_hits) == 1, len(g_hits))
chk("展開相位穿越 −180 度正好一次", len(p_hits) == 1, len(p_hits))
if len(g_hits) != 1 or len(p_hits) != 1:
    end()
ig, wgc, tg = g_hits[0]
ip, wpc, tp = p_hits[0]
pm = 180.0 + along(uw, ig, tg)
gm = -along(gs, ip, tp)
chk("增益裕度 15.595091495422169 分貝", near(gm, GM), gm)
chk("相位穿越頻率 2.236075610614252", near(wpc, WPC), wpc)
chk("相位裕度 43.20281974826571 度", near(pm, PM), pm)
chk("增益穿越頻率 0.7787726504594005", near(wgc, WGC), wgc)
cls = [cl_from_ol(uw[i], gs[i]) for i in range(len(ws))]
imax = max(range(len(cls)), key=lambda i: cls[i])
chk(
    "存檔列重算閉迴路峰值 2.6701705500584403 分貝、頻率 0.7943",
    near(cls[imax], CL_PEAK) and near(ws[imax], CL_W),
    (cls[imax], ws[imax]),
)
wraps = [i for i in range(len(ps) - 1) if abs(ps[i + 1] - ps[i]) > 180.0]
chk("折回正好一次，在 1.9953 與 2.5119 之間", len(wraps) == 1, len(wraps))
if len(wraps) == 1:
    i = wraps[0]
    chk(
        "折回鄰列相位 −175.136 與 175.034，展開 −184.96600000000004",
        near(ws[i], WRAP_LO)
        and near(ws[i + 1], WRAP_HI)
        and near(ps[i], WRAP_P1)
        and near(ps[i + 1], WRAP_P2)
        and near(uw[i + 1], UNW_P2),
        (ws[i], ws[i + 1], ps[i], ps[i + 1], uw[i + 1]),
    )
end()
