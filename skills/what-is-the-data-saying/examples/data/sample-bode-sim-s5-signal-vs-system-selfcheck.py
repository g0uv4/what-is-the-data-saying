#!/usr/bin/env python3
"""sample-bode-sim-s5-signal-vs-system-selfcheck.py：圖 S5 自我檢查。
從 sample-bode-sim-s5-signal-vs-system.csv 找輸出週期圖功率最大的頻率格。
只需 Python 標準函式庫。
用法：python3 sample-bode-sim-s5-signal-vs-system-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。輸出尖峰 48.83 赫茲取自 sim_facts，對應 CSV 的 48.828（三位小數）。
bode_peak_Hz 49.68 與 bode_peak_gain_dB 14.02 是系統波德圖，不在這份輸入／輸出功率 CSV，自檢不核對。
時間序列長度 32768 也不在檔內；460 列是 0 < f ≤ 450 的 Welch 頻率格（fs＝1000、nperseg＝1024）。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-bode-sim-s5-signal-vs-system.csv"
COLS = ["freq_Hz", "input_power_dB", "output_power_dB"]
RESULTS = []

# 模擬記載（寫死）。輸出週期圖尖峰取自 sim_facts；列數與頻率格由 CSV 能核對的 Welch 參數寫死。
N_EXPECT = 460
FS = 1000.0
NPERSEG = 1024
F_MAX = 450.0
OUTPUT_PEAK_HZ = 48.83
OUTPUT_PEAK_HZ_CSV = 48.828
OUTPUT_PEAK_DB_CSV = -12.908
TOL = 1e-12
TOL_HZ = 0.01

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
chk("460 列（Welch 格，不是時間序列 32768）", len(rows) == N_EXPECT)
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
fs = [float(r["freq_Hz"]) for r in rows]
pin = [float(r["input_power_dB"]) for r in rows]
pout = [float(r["output_power_dB"]) for r in rows]
df = FS / NPERSEG
grid_ok = all(near(fs[i], round((i + 1) * df, 3)) for i in range(len(fs)))
chk("頻率格是 k * 1000 / 1024（k＝1…460，三位小數）", grid_ok and fs[-1] <= F_MAX, (fs[0], fs[-1], df))
chk("頻率嚴格遞增", all(fs[i] < fs[i + 1] for i in range(len(fs) - 1)))
k = max(range(len(pout)), key=lambda i: pout[i])
chk(
    "輸出尖峰在 48.828 赫茲",
    near(fs[k], OUTPUT_PEAK_HZ_CSV) and near(pout[k], OUTPUT_PEAK_DB_CSV),
    (fs[k], pout[k]),
)
chk("輸出尖峰約 48.83 赫茲", near(fs[k], OUTPUT_PEAK_HZ, TOL_HZ) and near(round(fs[k], 2), OUTPUT_PEAK_HZ), fs[k])
chk("輸出尖峰是嚴格局部最大", 0 < k < len(pout) - 1 and pout[k] > pout[k - 1] and pout[k] > pout[k + 1], k)
chk("同一格輸出高於輸入", pout[k] > pin[k], (pout[k], pin[k]))
# 輸入週期圖沒有對應的 50 赫茲凸起；用與輸出同一格的相對高度粗看。
in_span = max(pin) - min(pin)
out_span = max(pout) - min(pout)
chk("輸出起伏大於輸入（訊號尖峰，不是系統波德圖）", out_span > in_span, (out_span, in_span))
done()
