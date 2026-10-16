#!/usr/bin/env python3
"""sample-periodogram-sim-s1-anatomy-selfcheck.py：圖 S1 自我檢查。
從 sample-periodogram-sim-s1-anatomy.csv 用純 Python 離散傅立葉轉換重算功率。
功率是實部平方加虛部平方，不除以長度。只需 Python 標準函式庫。
用法：python3 sample-periodogram-sim-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。模擬記載的全長 1024 點與尖峰 19.922 赫茲不在這份 CSV，自檢不核對。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-periodogram-sim-s1-anatomy.csv"
COLS = ["t_s", "x"]
RESULTS = []

# 模擬記載（寫死）裡 fs＝200、真實頻率 20 赫茲。這份 CSV 只有 200 列，不是 1024。
N_EXPECT = 200
FS = 200.0
DT = 0.005
T_END = 0.995
TRUE_HZ = 20.0
# 檔內平均的 repr。未扣平均與扣平均的尖峰功率差約 9e-12，分開寫死，不要求兩者相等。
EXPECT_MEAN = -0.045295208871729976
EXPECT_RAW = 10192.720424279498
EXPECT_DEMEAN = 10192.720424279489
SECOND_HZ = 30.0
EXPECT_SECOND = 108.83774896837525
# 對稱漢寧：w[t]＝0.5*(1-cos(2πt/(n-1)))，乘在扣平均之後。週期漢寧（除以 n）不拿來核對。
EXPECT_HANN = 2351.9007398023687
TOL = 1e-12

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def near(got, exp):
    return abs(got - exp) <= TOL

def dft_pow(xs):
    n = len(xs)
    out = []
    for k in range(n // 2 + 1):
        re = im = 0.0
        for t, x in enumerate(xs):
            ang = -2 * math.pi * k * t / n
            re += x * math.cos(ang)
            im += x * math.sin(ang)
        out.append(re * re + im * im)
    return out

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("t_s,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
chk("欄位", list(rows[0].keys()) == COLS)
chk("200 列", len(rows) == N_EXPECT)
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
ts = [float(r["t_s"]) for r in rows]
xs = [float(r["x"]) for r in rows]
grid_ok = near(ts[0], 0.0) and near(ts[-1], T_END) and all(near(ts[i + 1] - ts[i], DT) for i in range(len(ts) - 1))
chk("時間從 0 到 0.995、步長 0.005（取樣率 200）", grid_ok, ts[1] - ts[0])
mu = sum(xs) / len(xs)
chk("平均", near(mu, EXPECT_MEAN), repr(mu))
P = dft_pow(xs)
k = max(range(len(P)), key=lambda i: P[i])
hz = k * FS / len(xs)
chk("未扣平均的尖峰在 20.0 赫茲", near(hz, TRUE_HZ) and k == 20, hz)
chk("未扣平均的尖峰功率", near(P[k], EXPECT_RAW), repr(P[k]))
xd = [x - mu for x in xs]
Pd = dft_pow(xd)
kd = max(range(len(Pd)), key=lambda i: Pd[i])
chk("扣平均後尖峰仍在 20.0 赫茲，功率分開寫死", kd == 20 and near(Pd[kd], EXPECT_DEMEAN), repr(Pd[kd]))
order = sorted(range(len(P)), key=lambda i: P[i], reverse=True)
second_hz = order[1] * FS / len(xs)
chk(
    "第二高在 30.0 赫茲",
    order[1] == 30 and near(second_hz, SECOND_HZ) and near(P[order[1]], EXPECT_SECOND),
    repr(P[order[1]]),
)
n = len(xs)
w = [0.5 * (1.0 - math.cos(2.0 * math.pi * t / (n - 1))) for t in range(n)]
Ph = dft_pow([xd[i] * w[i] for i in range(n)])
kh = max(range(len(Ph)), key=lambda i: Ph[i])
chk("對稱漢寧後尖峰仍在 20.0 赫茲", kh == 20 and near(kh * FS / n, TRUE_HZ), kh * FS / n)
chk("對稱漢寧的尖峰功率", near(Ph[kh], EXPECT_HANN), repr(Ph[kh]))
done()
