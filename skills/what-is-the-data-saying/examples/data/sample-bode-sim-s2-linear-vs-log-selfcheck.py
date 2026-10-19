#!/usr/bin/env python3
"""sample-bode-sim-s2-linear-vs-log-selfcheck.py：圖 S2 自我檢查。
從 sample-bode-sim-s2-linear-vs-log.csv 找增益最大值，對過帶通峰值。
只需 Python 標準函式庫。
用法：python3 sample-bode-sim-s2-linear-vs-log-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。模擬記載峰值 −0.17 分貝來自 600 點密格；這份 CSV 只有 26 點，最大是 −0.176。
上轉折 5000 赫茲不在這份頻率格上，自檢不核對那一列。下轉折 100 赫茲有列，增益約 −3 分貝。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-bode-sim-s2-linear-vs-log.csv"
COLS = ["freq_Hz", "gain_dB"]
RESULTS = []

# 模擬記載（寫死）。峰值取自 sim_facts；CSV 26 點最大值對過後寫在 PEAK_GAIN_CSV。
N_EXPECT = 26
F0 = 1.0
F_END = 100000.0
LOW_CORNER_HZ = 100.0
PEAK_GAIN_DB = -0.17
PEAK_GAIN_CSV = -0.176
PEAK_FREQ_CSV = 630.957
GAIN_AT_100_HZ = -3.012
TOL = 1e-12
TOL_PEAK = 0.01

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
chk("26 列", len(rows) == N_EXPECT)
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
fs = [float(r["freq_Hz"]) for r in rows]
gs = [float(r["gain_dB"]) for r in rows]
chk("頻率從 1 到 100000 且嚴格遞增", near(fs[0], F0) and near(fs[-1], F_END) and all(fs[i] < fs[i + 1] for i in range(len(fs) - 1)))
logs = [math.log10(f) for f in fs]
step = (math.log10(F_END) - math.log10(F0)) / (N_EXPECT - 1)
# 頻率已捨入到三位小數，低頻 log10 步長會偏到約 4e-5。
chk("五個十倍頻、26 點對數等分（含捨入）", all(near(logs[i + 1] - logs[i], step, 1e-4) for i in range(len(logs) - 1)), step)
k = max(range(len(gs)), key=lambda i: gs[i])
chk("CSV 峰值在 630.957 赫茲、增益 -0.176 分貝", near(fs[k], PEAK_FREQ_CSV) and near(gs[k], PEAK_GAIN_CSV), (fs[k], gs[k]))
chk("峰值約 -0.17 分貝（密格記載，容差 0.01）", near(gs[k], PEAK_GAIN_DB, TOL_PEAK), gs[k])
chk("峰值在兩端之間，不是格的頭或尾", 0 < k < len(gs) - 1, k)
low = None
for r in rows:
    if near(float(r["freq_Hz"]), LOW_CORNER_HZ):
        low = r
        break
chk("有下轉折 100 赫茲那一列", low is not None)
if low is not None:
    chk("100 赫茲增益約 -3 分貝", near(float(low["gain_dB"]), GAIN_AT_100_HZ), low["gain_dB"])
done()
