#!/usr/bin/env python3
"""sample-nichols-sim-s3-tangent-peak-selfcheck.py：圖 S3 自我檢查。
從 sample-nichols-sim-s3-tangent-peak.csv 核對存檔閉迴路峰值、由開迴路重算閉迴路，
以及對數頻率內插的裕度。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-nichols-sim-s3-tangent-peak-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-nichols-sim-s3-tangent-peak.csv"
COLS = ["omega_rad_s", "open_loop_phase_deg", "open_loop_gain_dB", "closed_loop_gain_dB"]
RESULTS = []

N_EXPECT = 21
W0 = 0.01
W_END = 100.0
CL_MAX = 4.8886
CL_W = 1.0
CL_PH = -146.31
CL_G = 0.341192
RECOMP_ERR = 7.550167966030585e-05
GM = 12.135038696826124
WPC = 2.2356387854599795
PM = 32.7197002731605
WGC = 1.0237623247680192
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
    skip("課程稿密格切到 5.10 分貝圈、切點 −149.47 度與 −0.73 分貝", "存檔閉迴路最大是 4.8886，沒有切點欄")
    skip("課程稿增益 1.5", "CSV 沒有 K 欄")
    skip("課程稿密格增益裕度 12.04、相位裕度 32.68", "21 列內插是 12.135038696826124 與 32.7197002731605")
    skip("課程稿密格峰值頻率 1.082、增益穿越 1.026、相位穿越 2.236", "存檔峰值在頻率 1.0；內插是 1.0237623247680192 與 2.2356387854599795")

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
cls = [float(r["closed_loop_gain_dB"]) for r in rows]
chk(
    "頻率從 0.01 到 100 且嚴格遞增",
    near(ws[0], W0) and near(ws[-1], W_END) and all(ws[i] < ws[i + 1] for i in range(len(ws) - 1)),
)
chk("開迴路相位嚴格遞減", all(ps[i] > ps[i + 1] for i in range(len(ps) - 1)))
imax = max(range(len(cls)), key=lambda i: cls[i])
chk(
    "存檔閉迴路最大 4.8886，頻率 1、相位 −146.31、開迴路增益 0.341192",
    near(cls[imax], CL_MAX) and near(ws[imax], CL_W) and near(ps[imax], CL_PH) and near(gs[imax], CL_G),
    (cls[imax], ws[imax], ps[imax], gs[imax]),
)
recomp = [cl_from_ol(ps[i], gs[i]) for i in range(len(ws))]
errs = [abs(recomp[i] - cls[i]) for i in range(len(ws))]
chk("由開迴路重算閉迴路，最大絕對差 7.550167966030585e-05", near(max(errs), RECOMP_ERR), max(errs))
g_hits = log_cross(ws, gs, 0.0)
p_hits = log_cross(ws, ps, -180.0)
chk("增益穿越 0 分貝正好一次", len(g_hits) == 1, len(g_hits))
chk("相位穿越 −180 度正好一次", len(p_hits) == 1, len(p_hits))
if len(g_hits) != 1 or len(p_hits) != 1:
    end()
ig, wgc, tg = g_hits[0]
ip, wpc, tp = p_hits[0]
pm = 180.0 + along(ps, ig, tg)
gm = -along(gs, ip, tp)
chk("增益裕度 12.135038696826124 分貝", near(gm, GM), gm)
chk("相位穿越頻率 2.2356387854599795", near(wpc, WPC), wpc)
chk("相位裕度 32.7197002731605 度", near(pm, PM), pm)
chk("增益穿越頻率 1.0237623247680192", near(wgc, WGC), wgc)
end()
