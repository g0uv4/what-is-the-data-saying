#!/usr/bin/env python3
"""sample-bode-sim-s1-anatomy-selfcheck.py：圖 S1 自我檢查。
從 sample-bode-sim-s1-anatomy.csv 核對 17 個對數頻率點，以及截止 1000 赫茲理論欄的增益與相位。
只需 Python 標準函式庫。
用法：python3 sample-bode-sim-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。增益 −3.01 分貝、相位 −45 度取自 sim_facts，對的是理論欄。
量測雜訊標準差 0.35 分貝／1.5 度無法從 17 點重估，本腳本不核對量測欄是否等於理論。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-bode-sim-s1-anatomy.csv"
COLS = ["freq_Hz", "gain_dB_measured", "phase_deg_measured", "gain_dB_theory", "phase_deg_theory"]
RESULTS = []

# 模擬記載（寫死）。點數、截止頻率、截止處理論增益與相位取自 sim_facts，並對過 CSV。
N_EXPECT = 17
F0 = 10.0
F_END = 100000.0
CUTOFF_HZ = 1000.0
GAIN_AT_CUTOFF_DB = -3.01
PHASE_AT_CUTOFF_DEG = -45.0
SLOPE_DB_PER_DECADE = -20
TOL = 1e-12
TOL_SLOPE = 0.05

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

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
chk("17 列", len(rows) == N_EXPECT)
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
fs = [float(r["freq_Hz"]) for r in rows]
gth = [float(r["gain_dB_theory"]) for r in rows]
pth = [float(r["phase_deg_theory"]) for r in rows]
chk("頻率從 10 到 100000 且嚴格遞增", near(fs[0], F0) and near(fs[-1], F_END) and all(fs[i] < fs[i + 1] for i in range(len(fs) - 1)))
logs = [math.log10(f) for f in fs]
step = (math.log10(F_END) - math.log10(F0)) / (N_EXPECT - 1)
chk("四個十倍頻、17 點對數等分（含捨入）", all(near(logs[i + 1] - logs[i], step, 1e-5) for i in range(len(logs) - 1)), step)
cut = None
for r in rows:
    if near(float(r["freq_Hz"]), CUTOFF_HZ):
        cut = r
        break
chk("有 1000 赫茲那一列", cut is not None)
if cut is None:
    done()
chk(
    "截止處理論增益 -3.01 分貝",
    near(float(cut["gain_dB_theory"]), GAIN_AT_CUTOFF_DB),
    cut["gain_dB_theory"],
)
chk(
    "截止處理論相位 -45 度",
    near(float(cut["phase_deg_theory"]), PHASE_AT_CUTOFF_DEG),
    cut["phase_deg_theory"],
)
i10 = next(i for i, f in enumerate(fs) if near(f, 10000.0))
i100 = next(i for i, f in enumerate(fs) if near(f, 100000.0))
slope = gth[i100] - gth[i10]
chk("10 kHz 到 100 kHz 理論斜率約每十倍頻 -20 分貝", near(slope, SLOPE_DB_PER_DECADE, TOL_SLOPE), slope)
done()
