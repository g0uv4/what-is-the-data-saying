#!/usr/bin/env python3
"""sample-bode-sim-s3-order-slope-selfcheck.py：圖 S3 自我檢查。
從 sample-bode-sim-s3-order-slope.csv 用 10 kHz 與 100 kHz 兩列算每十倍頻斜率，並看最後相位。
只需 Python 標準函式庫。
用法：python3 sample-bode-sim-s3-order-slope-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。斜率 −19.96／−40.0 取自 sim_facts，可由 CSV 兩列相減重現。
最終相位記載是無限頻率的 −90／−180 度；CSV 最後一列是 100 kHz，相位 −89.427／−179.19，用 1 度對過漸近值。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-bode-sim-s3-order-slope.csv"
COLS = ["freq_Hz", "gain1_dB", "phase1_deg", "gain2_dB", "phase2_deg"]
RESULTS = []

# 模擬記載（寫死）。截止、斜率、最終相位取自 sim_facts；100 kHz 相位是 CSV 實際值。
N_EXPECT = 21
F0 = 10.0
F_END = 100000.0
CUTOFF_HZ = 1000.0
F_LO = 10000.0
F_HI = 100000.0
SLOPE_1ST = -19.96
SLOPE_2ND = -40.0
FINAL_PHASE_1ST = -90.0
FINAL_PHASE_2ND = -180.0
PHASE_1ST_AT_100K = -89.427
PHASE_2ND_AT_100K = -179.19
TOL = 1e-12
TOL_SLOPE = 0.01
TOL_PHASE = 1.0

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def at_freq(rows, f):
    for r in rows:
        if near(float(r["freq_Hz"]), f):
            return r
    return None

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("freq_Hz,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
chk("欄位", list(rows[0].keys()) == COLS)
chk("21 列", len(rows) == N_EXPECT)
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
fs = [float(r["freq_Hz"]) for r in rows]
chk("頻率從 10 到 100000 且嚴格遞增", near(fs[0], F0) and near(fs[-1], F_END) and all(fs[i] < fs[i + 1] for i in range(len(fs) - 1)))
logs = [math.log10(f) for f in fs]
step = (math.log10(F_END) - math.log10(F0)) / (N_EXPECT - 1)
chk("四個十倍頻、21 點對數等分（含捨入）", all(near(logs[i + 1] - logs[i], step, 1e-5) for i in range(len(logs) - 1)), step)
cut = at_freq(rows, CUTOFF_HZ)
lo = at_freq(rows, F_LO)
hi = at_freq(rows, F_HI)
chk("有 1000、10000、100000 赫茲三列", cut is not None and lo is not None and hi is not None)
if cut is None or lo is None or hi is None:
    done()
chk(
    "截止處一階約 -3.01 分貝、-45 度",
    near(float(cut["gain1_dB"]), -3.01) and near(float(cut["phase1_deg"]), -45.0),
    (cut["gain1_dB"], cut["phase1_deg"]),
)
chk(
    "截止處二階相位 -90 度",
    near(float(cut["phase2_deg"]), -90.0),
    cut["phase2_deg"],
)
slope1 = float(hi["gain1_dB"]) - float(lo["gain1_dB"])
slope2 = float(hi["gain2_dB"]) - float(lo["gain2_dB"])
chk("一階 10 kHz 到 100 kHz 斜率 -19.96 分貝／十倍頻", near(slope1, SLOPE_1ST, TOL_SLOPE), slope1)
chk("二階 10 kHz 到 100 kHz 斜率 -40.0 分貝／十倍頻", near(slope2, SLOPE_2ND, TOL_SLOPE), slope2)
p1 = float(hi["phase1_deg"])
p2 = float(hi["phase2_deg"])
chk("100 kHz 一階相位是 -89.427（漸近 -90）", near(p1, PHASE_1ST_AT_100K) and near(p1, FINAL_PHASE_1ST, TOL_PHASE), p1)
chk("100 kHz 二階相位是 -179.19（漸近 -180）", near(p2, PHASE_2ND_AT_100K) and near(p2, FINAL_PHASE_2ND, TOL_PHASE), p2)
done()
