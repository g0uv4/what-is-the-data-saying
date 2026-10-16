#!/usr/bin/env python3
"""sample-periodogram-sim-s2-two-tones-selfcheck.py：圖 S2 自我檢查。
從 sample-periodogram-sim-s2-two-tones.csv 讀已算好的功率，找兩個局部極大。
這份檔是頻率格，不再做傅立葉轉換。只需 Python 標準函式庫。
用法：python3 sample-periodogram-sim-s2-two-tones-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。模擬記載的 12.01、37.01 赫茲與全長 2048 不在頻率格上，自檢不核對那兩個寫法。"""

import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-periodogram-sim-s2-two-tones.csv"
COLS = ["freq_Hz", "power"]
RESULTS = []

N_EXPECT = 257
F0 = 0.0
F_END = 100.0
STEP = 0.390625
# 高於 0.01 的局部極大只有這兩格，是距真實 12、37 赫茲最近的存檔格。
PEAKS = [
    (31, 12.109375, 0.0568727306453308),
    (95, 37.109375, 0.02650337611567428),
]
FLOOR = 0.01
TOL = 1e-12

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def near(got, exp):
    return abs(got - exp) <= TOL

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
chk("257 列", len(rows) == N_EXPECT)
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
fs = [float(r["freq_Hz"]) for r in rows]
ps = [float(r["power"]) for r in rows]
grid_ok = near(fs[0], F0) and near(fs[-1], F_END) and all(near(fs[i + 1] - fs[i], STEP) for i in range(len(fs) - 1))
chk("頻率從 0 到 100、步長 0.390625", grid_ok, repr(fs[1] - fs[0]))
locs = []
for i in range(1, len(ps) - 1):
    if ps[i] >= ps[i - 1] and ps[i] > ps[i + 1] and ps[i] > FLOOR:
        locs.append(i)
chk("高於 0.01 的局部極大正好兩個", locs == [PEAKS[0][0], PEAKS[1][0]], locs)
chk(
    "第一尖峰在 12.109375 赫茲",
    near(fs[PEAKS[0][0]], PEAKS[0][1]) and near(ps[PEAKS[0][0]], PEAKS[0][2]),
    repr(ps[PEAKS[0][0]]),
)
chk(
    "第二尖峰在 37.109375 赫茲",
    near(fs[PEAKS[1][0]], PEAKS[1][1]) and near(ps[PEAKS[1][0]], PEAKS[1][2]),
    repr(ps[PEAKS[1][0]]),
)
chk("12 赫茲那格的功率高於 37 赫茲那格", ps[PEAKS[0][0]] > ps[PEAKS[1][0]])
done()
