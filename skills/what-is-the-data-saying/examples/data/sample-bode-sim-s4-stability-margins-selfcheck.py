#!/usr/bin/env python3
"""sample-bode-sim-s4-stability-margins-selfcheck.py：圖 S4 自我檢查。
從 sample-bode-sim-s4-stability-margins.csv 在對數頻率上線性內插增益穿越與相位穿越，再算裕度。
只需 Python 標準函式庫。
用法：python3 sample-bode-sim-s4-stability-margins-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。2.052 赫茲、4.468 赫茲、12.02 分貝、32.67 度取自 sim_facts（2000 點密格的最近點）。
這份 CSV 只有 29 列，內插結果會偏一點，用 0.02 赫茲／0.1 分貝／0.1 度容差。開迴路 K＝3 的公式無法只從 29 列還原，不重解。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-bode-sim-s4-stability-margins.csv"
COLS = ["freq_Hz", "open_loop_gain_dB", "open_loop_phase_deg"]
RESULTS = []

# 模擬記載（寫死）。穿越頻率與裕度取自 sim_facts。
N_EXPECT = 29
F0 = 0.0316
F_END = 100.0
GAIN_CROSS_HZ = 2.052
PHASE_CROSS_HZ = 4.468
GAIN_MARGIN_DB = 12.02
PHASE_MARGIN_DEG = 32.67
TOL = 1e-12
TOL_HZ = 0.02
TOL_DB = 0.1
TOL_DEG = 0.1

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def log_cross(xs, ys, target):
    """y 對 log(x) 線性，回傳唯一穿越的 (i, x, t)。"""
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

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("freq_Hz,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
chk("欄位", list(rows[0].keys()) == COLS)
chk("29 列", len(rows) == N_EXPECT)
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
fs = [float(r["freq_Hz"]) for r in rows]
gs = [float(r["open_loop_gain_dB"]) for r in rows]
ps = [float(r["open_loop_phase_deg"]) for r in rows]
chk("頻率從 0.0316 到 100 且嚴格遞增", near(fs[0], F0) and near(fs[-1], F_END) and all(fs[i] < fs[i + 1] for i in range(len(fs) - 1)))
chk("增益嚴格遞減、相位嚴格遞減", all(gs[i] > gs[i + 1] for i in range(len(gs) - 1)) and all(ps[i] > ps[i + 1] for i in range(len(ps) - 1)))
g_hits = log_cross(fs, gs, 0.0)
p_hits = log_cross(fs, ps, -180.0)
chk("增益穿越 0 分貝正好一次", len(g_hits) == 1, len(g_hits))
chk("相位穿越 -180 度正好一次", len(p_hits) == 1, len(p_hits))
if len(g_hits) != 1 or len(p_hits) != 1:
    done()
ig, f_gc, tg = g_hits[0]
ip, f_pc, tp = p_hits[0]
pm = 180.0 + along(ps, ig, tg)
gm = -along(gs, ip, tp)
chk("增益穿越約 2.052 赫茲", near(f_gc, GAIN_CROSS_HZ, TOL_HZ), f_gc)
chk("相位穿越約 4.468 赫茲", near(f_pc, PHASE_CROSS_HZ, TOL_HZ), f_pc)
chk("增益裕度約 12.02 分貝", near(gm, GAIN_MARGIN_DB, TOL_DB), gm)
chk("相位裕度約 32.67 度", near(pm, PHASE_MARGIN_DEG, TOL_DEG), pm)
chk("增益穿越在相位穿越之前", f_gc < f_pc, (f_gc, f_pc))
done()
