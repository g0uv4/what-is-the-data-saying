#!/usr/bin/env python3
"""sample-periodogram-sim-s4-welch-selfcheck.py：圖 S4 自我檢查。
從 sample-periodogram-sim-s4-welch.csv 讀 Welch 功率，核對 25 赫茲尖峰。
這份檔只有分段平均後的功率，不再做傅立葉轉換。只需 Python 標準函式庫。
用法：python3 sample-periodogram-sim-s4-welch-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。圖說上格的單段週期圖不在這份 CSV，自檢不核對。"""

import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-periodogram-sim-s4-welch.csv"
COLS = ["freq_Hz", "welch_power"]
RESULTS = []

N_EXPECT = 129
F0 = 0.0
F_END = 100.0
STEP = 0.78125
PEAK_I = 32
PEAK_HZ = 25.0
EXPECT_PEAK = 0.41938521275201973
LEFT_HZ = 24.21875
LEFT_P = 0.11893171173452609
RIGHT_HZ = 25.78125
RIGHT_P = 0.11707927781973693
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
ps = [float(r["welch_power"]) for r in rows]
grid_ok = near(fs[0], F0) and near(fs[-1], F_END) and all(near(fs[i + 1] - fs[i], STEP) for i in range(len(fs) - 1))
chk("頻率從 0 到 100、步長 0.78125", grid_ok, repr(fs[1] - fs[0]))
k = max(range(len(ps)), key=lambda i: ps[i])
chk(
    "尖峰在 25.0 赫茲",
    k == PEAK_I and near(fs[k], PEAK_HZ) and near(ps[k], EXPECT_PEAK),
    repr(ps[k]),
)
chk(
    "左鄰 24.21875 赫茲",
    near(fs[k - 1], LEFT_HZ) and near(ps[k - 1], LEFT_P),
    repr(ps[k - 1]),
)
chk(
    "右鄰 25.78125 赫茲",
    near(fs[k + 1], RIGHT_HZ) and near(ps[k + 1], RIGHT_P),
    repr(ps[k + 1]),
)
order = sorted(range(len(ps)), key=lambda i: ps[i], reverse=True)
chk("第二高就是左鄰，尖峰嚴格高於其餘每一格", order[1] == k - 1 and ps[k] > ps[order[1]])
done()
