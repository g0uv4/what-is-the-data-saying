#!/usr/bin/env python3
"""sample-periodogram-sim-s3-leakage-selfcheck.py：圖 S3 自我檢查。
從 sample-periodogram-sim-s3-leakage.csv 比較矩形窗與漢寧窗的分貝。
這份檔已是功率（分貝），不再做傅立葉轉換。只需 Python 標準函式庫。
用法：python3 sample-periodogram-sim-s3-leakage-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。真實頻率 10.3 赫茲不落在頻率格上。"""

import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-periodogram-sim-s3-leakage.csv"
COLS = ["freq_Hz", "rect_dB", "hann_dB"]
RESULTS = []

N_EXPECT = 129
F0 = 0.0
F_END = 50.0
STEP = 0.390625
PEAK_I = 26
PEAK_HZ = 10.15625
PEAK_DB = 0.0
ADJ_I = 27
ADJ_HZ = 10.546875
ADJ_RECT = -4.664634257021721
ADJ_HANN = -1.521502330503378
SIDE_I = 29
SIDE_HZ = 11.328125
SIDE_RECT = -17.019584057359197
SIDE_HANN = -34.20898840629693
DC_RECT = -160.0
DC_HANN = -34.44905398987196
OUTSIDE_N = 124
RECT_LOUDER = 98
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
chk("129 列", len(rows) == N_EXPECT)
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
fs = [float(r["freq_Hz"]) for r in rows]
rect = [float(r["rect_dB"]) for r in rows]
hann = [float(r["hann_dB"]) for r in rows]
grid_ok = near(fs[0], F0) and near(fs[-1], F_END) and all(near(fs[i + 1] - fs[i], STEP) for i in range(len(fs) - 1))
chk("頻率從 0 到 50、步長 0.390625", grid_ok, repr(fs[1] - fs[0]))
ir = max(range(len(rect)), key=lambda i: rect[i])
ih = max(range(len(hann)), key=lambda i: hann[i])
chk(
    "兩種窗的尖峰都在 10.15625 赫茲、都是 0.0 分貝",
    ir == PEAK_I and ih == PEAK_I and near(fs[ir], PEAK_HZ) and near(rect[ir], PEAK_DB) and near(hann[ih], PEAK_DB),
)
chk(
    "鄰格 10.546875 赫茲漢寧較響（主瓣較寬）",
    near(fs[ADJ_I], ADJ_HZ) and near(rect[ADJ_I], ADJ_RECT) and near(hann[ADJ_I], ADJ_HANN) and hann[ADJ_I] > rect[ADJ_I],
    repr(hann[ADJ_I]),
)
outside = [i for i in range(len(rect)) if abs(i - PEAK_I) > 2]
side_r = max(outside, key=lambda i: rect[i])
side_h = max(outside, key=lambda i: hann[i])
chk(
    "主峰兩格以外，最高旁瓣都在 11.328125 赫茲，漢寧更低",
    len(outside) == OUTSIDE_N
    and side_r == SIDE_I
    and side_h == SIDE_I
    and near(fs[SIDE_I], SIDE_HZ)
    and near(rect[SIDE_I], SIDE_RECT)
    and near(hann[SIDE_I], SIDE_HANN)
    and hann[SIDE_I] < rect[SIDE_I],
    repr(hann[SIDE_I]),
)
louder = sum(1 for i in outside if rect[i] > hann[i])
chk("主峰兩格以外，矩形高於漢寧的格數是 98／124", louder == RECT_LOUDER, louder)
chk(
    "直流格：矩形 -160.0、漢寧另記",
    near(rect[0], DC_RECT) and near(hann[0], DC_HANN),
    repr(hann[0]),
)
done()
