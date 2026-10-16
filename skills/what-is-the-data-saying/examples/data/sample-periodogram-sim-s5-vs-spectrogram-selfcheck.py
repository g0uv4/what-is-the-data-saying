#!/usr/bin/env python3
"""sample-periodogram-sim-s5-vs-spectrogram-selfcheck.py：圖 S5 自我檢查。
從 sample-periodogram-sim-s5-vs-spectrogram.csv 讀整段週期圖，核對 15 與 40 赫茲。
這份檔沒有時間軸，不重做短時傅立葉轉換。只需 Python 標準函式庫。
用法：python3 sample-periodogram-sim-s5-vs-spectrogram-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。先 15 後 40 是下格頻譜圖的事，不在這份 CSV，自檢不核對先後。"""

import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-periodogram-sim-s5-vs-spectrogram.csv"
COLS = ["freq_Hz", "periodogram_power"]
RESULTS = []

N_EXPECT = 501
F0 = 0.0
F_END = 100.0
STEP = 0.2
I15 = 75
HZ15 = 15.0
P15 = 1.201085763474063
I40 = 200
HZ40 = 40.0
P40 = 1.2359419294357712
I3 = 13
HZ3 = 2.6
P3 = 0.0028335625683677795
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
chk("501 列", len(rows) == N_EXPECT)
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
fs = [float(r["freq_Hz"]) for r in rows]
ps = [float(r["periodogram_power"]) for r in rows]
steps_ok = all(abs(round(fs[i + 1] - fs[i], 10) - STEP) <= TOL for i in range(len(fs) - 1))
chk("頻率從 0 到 100、名義步長 0.2", near(fs[0], F0) and near(fs[-1], F_END) and steps_ok, repr(fs[1]))
chk(
    "15.0 赫茲那一格",
    near(fs[I15], HZ15) and near(ps[I15], P15),
    repr(ps[I15]),
)
chk(
    "40.0 赫茲那一格",
    near(fs[I40], HZ40) and near(ps[I40], P40),
    repr(ps[I40]),
)
locs = []
for i in range(1, len(ps) - 1):
    if ps[i] >= ps[i - 1] and ps[i] >= ps[i + 1] and ps[i] > ps[i - 1]:
        locs.append(i)
locs.sort(key=lambda i: ps[i], reverse=True)
chk("最高的兩個局部極大就是 40 與 15 赫茲", locs[0] == I40 and locs[1] == I15, (locs[0], locs[1]))
chk(
    "第三個局部極大在 2.6 赫茲，功率遠小於主峰",
    locs[2] == I3 and near(fs[I3], HZ3) and near(ps[I3], P3) and ps[I3] < 0.01 * ps[I40],
    repr(ps[I3]),
)
done()
