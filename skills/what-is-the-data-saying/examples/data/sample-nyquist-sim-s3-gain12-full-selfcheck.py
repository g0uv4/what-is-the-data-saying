#!/usr/bin/env python3
"""sample-nyquist-sim-s3-gain12-full-selfcheck.py：圖 S3 自我檢查。
從 sample-nyquist-sim-s3-gain12-full.csv 核對含負頻率的折線。
只需 Python 標準函式庫（cmath、csv、math、os、sys）。
用法：python3 sample-nyquist-sim-s3-gain12-full-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
負實軸交點：頻率上線性內插，虛部變號且該段起點實部小於 0。
繞圈數：閉合折線對 −1 的轉角，逆時針為正，再除以 2π。
只取正頻率再閉合，繞圈數不是 −2。
閉迴路極點不在 CSV。
"""

import cmath, csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-nyquist-sim-s3-gain12-full.csv"
COLS = ["omega_rad_s", "re", "im"]
RESULTS = []

N_EXPECT = 201
W0 = -100.0
W_END = 99.77
W_POS = 1.7324550341487142
RE_POS = -1.4994324581478504
W_NEG = -1.7333632389752902
RE_NEG = -1.498169511076016
WIND = -2.000000000000001
WIND_POS = -1.0000000000000002
MODEL_ERR = 4.931050754743703e-05
TOL = 1e-9

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def sign(x):
    return (x > 0) - (x < 0)

def winding(zs):
    c = -1.0 + 0.0j
    ang = 0.0
    prev = cmath.phase(zs[0] - c)
    seq = list(zs) + [zs[0]]
    for z in seq[1:]:
        a = cmath.phase(z - c)
        d = a - prev
        while d > math.pi:
            d -= 2.0 * math.pi
        while d <= -math.pi:
            d += 2.0 * math.pi
        ang += d
        prev = a
    return ang / (2.0 * math.pi)

def unchecked():
    skip(
        "密格記載的負實軸交點 −1.5",
        "這份檔的正頻率內插實部是 −1.4994324581478504，不是 −1.5",
    )
    skip(
        "開迴路右半平面極點數 0，以及閉迴路極點 −3.289+0.000j、0.145±1.983j",
        "CSV 沒有極點欄",
    )

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def end():
    unchecked()
    done()

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("omega_rad_s,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("201 列", len(rows) == N_EXPECT, len(rows))
if not cols_ok:
    end()
empty = False
nums = []
for r in rows:
    if any((r[c] or "").strip() == "" for c in COLS):
        empty = True
        break
    try:
        vals = [float(r[c]) for c in COLS]
    except ValueError:
        nums = None
        break
    if not all(math.isfinite(v) for v in vals):
        nums = None
        break
    nums.append(vals)
chk("沒有空值", not empty)
chk("頻率、實部、虛部是有限數", nums is not None and len(nums) == len(rows))
if empty or nums is None:
    end()

ws = [v[0] for v in nums]
zs = [complex(v[1], v[2]) for v in nums]
n_neg = sum(1 for w in ws if w < 0.0)
n_pos = sum(1 for w in ws if w > 0.0)
n_zero = sum(1 for w in ws if w == 0.0)
chk(
    "頻率從 −100 到 99.77、嚴格遞增、沒有 0",
    near(ws[0], W0) and near(ws[-1], W_END) and all(ws[i] < ws[i + 1] for i in range(len(ws) - 1)) and n_zero == 0,
    (ws[0], ws[-1], n_zero),
)
chk("負頻率 101 列、正頻率 100 列", n_neg == 101 and n_pos == 100, (n_neg, n_pos))
chk(
    "第一列實部 −3.5988e-07、虛部 −1.19928e-05",
    near(nums[0][1], -3.5988e-07) and near(nums[0][2], -1.19928e-05),
    nums[0],
)
chk(
    "末列 ω＝99.77、實部 −3.63209e-07、虛部 1.20759e-05",
    near(nums[-1][0], 99.77) and near(nums[-1][1], -3.63209e-07) and near(nums[-1][2], 1.20759e-05),
    nums[-1],
)
model_err = 0.0
for w, z in zip(ws, zs):
    model_err = max(model_err, abs(12.0 / (1j * w + 1.0) ** 3 - z))
chk("與 12/(jω+1)³ 的最大絕對差", near(model_err, MODEL_ERR, 1e-15), model_err)

flips = []
for i in range(len(ws) - 1):
    if sign(zs[i].imag) != sign(zs[i + 1].imag):
        t = zs[i].imag / (zs[i].imag - zs[i + 1].imag)
        w = ws[i] + t * (ws[i + 1] - ws[i])
        re = zs[i].real + t * (zs[i + 1].real - zs[i].real)
        flips.append((w, re, zs[i].real < 0.0))
neg_hits = [h for h in flips if h[2]]
chk("虛部變號正好三次", len(flips) == 3, len(flips))
chk("其中起點實部為負的正好兩次", len(neg_hits) == 2, len(neg_hits))
if len(neg_hits) != 2 or len(flips) != 3:
    end()
chk("負頻率交點", near(neg_hits[0][0], W_NEG) and near(neg_hits[0][1], RE_NEG), neg_hits[0])
chk("正頻率交點", near(neg_hits[1][0], W_POS) and near(neg_hits[1][1], RE_POS), neg_hits[1])
mid = [h for h in flips if not h[2]][0]
chk(
    "靠近 0 的那一次虛部變號，內插實部大於 0（不是穩定交點）",
    mid[0] > 0.0 and mid[0] < 1e-5 and mid[1] > 11.0,
    mid,
)
wind = winding(zs)
chk("整條閉合折線繞 −1 的圈數", near(wind, WIND, 1e-15), wind)
zs_pos = [z for w, z in zip(ws, zs) if w > 0.0]
wind_pos = winding(zs_pos)
chk("只把正頻率閉合，繞圈數不是 −2", near(wind_pos, WIND_POS, 1e-15) and abs(wind_pos - wind) > 0.5, wind_pos)
end()
