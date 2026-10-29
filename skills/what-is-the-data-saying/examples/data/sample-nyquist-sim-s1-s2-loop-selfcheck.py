#!/usr/bin/env python3
"""sample-nyquist-sim-s1-s2-loop-selfcheck.py：圖 S1 與圖 S2 自我檢查。
從 sample-nyquist-sim-s1-s2-loop.csv 核對開迴路實部、虛部。
圖 S2 與圖 S1 共用這一份 CSV。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-nyquist-sim-s1-s2-loop-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
裕度的定義：在頻率上線性內插存檔的實部與虛部。
負實軸交點＝虛部變號，且該段起點實部小於 0，再以同一比例內插實部。
單位圓交點＝存檔模長穿越 1，同一比例內插複數；線性內插後的模長不必正好是 1。
相位裕度用該內插點的 atan2，並對到由存檔點展開的連續相位。
對數頻率上內插 mag_dB、phase_deg 只作對照，不是這份裕度的定義。
密格記載的 1.732、−0.5、2.0 倍、6.0 分貝、1.233、27.1 度不在這 161 列裡。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-nyquist-sim-s1-s2-loop.csv"
COLS = ["omega_rad_s", "re", "im", "mag_dB", "phase_deg"]
RESULTS = []

N_EXPECT = 161
W0 = 0.01
W_END = 100.0
# 頻率上線性內插存檔複數（寫死）。不是密格記載。
W_PC = 1.736279175827654
RE_PC = -0.49816319848922835
GM_TIMES = 2.007374296280183
GM_DB = 6.052567177234536
W_GC = 1.233760931584715
Z_GC_RE = -0.888407240623332
Z_GC_IM = -0.45721368793697187
PM_DEG = 27.232355441124582
# 對數頻率內插存檔 mag_dB==0、phase_deg==−180（寫死，只作對照）。
W_LOG_MAG = 1.2324423484129903
W_LOG_PH = 1.7324105010639035
MODEL_ERR = 1.0230480278004436e-05
DB_ERR = 0.0004459338908588961
PH_ERR = 0.0005132431712979724
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

def cross_real(ws, zs):
    out = []
    for i in range(len(ws) - 1):
        im1, im2 = zs[i].imag, zs[i + 1].imag
        if sign(im1) != sign(im2) and zs[i].real < 0:
            t = im1 / (im1 - im2)
            w = ws[i] + t * (ws[i + 1] - ws[i])
            re = zs[i].real + t * (zs[i + 1].real - zs[i].real)
            out.append((w, re, i, t))
    return out

def unit_cross(ws, zs):
    m = [abs(z) for z in zs]
    out = []
    for i in range(len(ws) - 1):
        if (m[i] - 1.0) * (m[i + 1] - 1.0) < 0:
            t = (m[i] - 1.0) / (m[i] - m[i + 1])
            w = ws[i] + t * (ws[i + 1] - ws[i])
            re = zs[i].real + t * (zs[i + 1].real - zs[i].real)
            im = zs[i].imag + t * (zs[i + 1].imag - zs[i].imag)
            out.append((w, re, im, i, t))
    return out

def unwrap_deg(zs):
    out = []
    prev = None
    acc = 0.0
    for z in zs:
        a = math.atan2(z.imag, z.real) * 180.0 / math.pi
        if prev is None:
            acc = a
        else:
            d = a - prev
            while d > 180.0:
                d -= 360.0
            while d < -180.0:
                d += 360.0
            acc += d
        out.append(acc)
        prev = a
    return out

def log_cross(xs, ys, target):
    found = []
    for i in range(len(ys) - 1):
        y1, y2 = ys[i], ys[i + 1]
        if (y1 - target) * (y2 - target) > 0:
            continue
        if y1 == y2:
            continue
        t = (target - y1) / (y2 - y1)
        if t < 0.0 or t > 1.0:
            continue
        x = math.exp(math.log(xs[i]) + t * (math.log(xs[i + 1]) - math.log(xs[i])))
        found.append(x)
    return found

def unchecked():
    skip(
        "密格記載：相位穿越 1.732、實部 −0.5、增益裕度 2.0 倍與 6.0 分貝、增益穿越 1.233、相位裕度 27.1 度",
        "那是較密格子四捨五入後的記載，不是這 161 列的頻率線性內插",
    )
    skip(
        "圖說「頻率 0：增益 4」",
        "CSV 沒有 ω＝0 那一列；第一列是 0.01，實部 3.9976",
    )
    skip(
        "圖 S2 標了哪三個頻率",
        "CSV 沒有標記欄",
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
chk("161 列", len(rows) == N_EXPECT, len(rows))
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
chk("頻率、實部、虛部、分貝與相位是有限數", nums is not None and len(nums) == len(rows))
if empty or nums is None:
    end()

ws = [v[0] for v in nums]
zs = [complex(v[1], v[2]) for v in nums]
dbs = [v[3] for v in nums]
phs = [v[4] for v in nums]
chk(
    "頻率從 0.01 到 100 且嚴格遞增",
    near(ws[0], W0) and near(ws[-1], W_END) and all(ws[i] < ws[i + 1] for i in range(len(ws) - 1)),
    (ws[0], ws[-1]),
)
chk("相位嚴格遞減", all(phs[i] > phs[i + 1] for i in range(len(phs) - 1)))
row1 = None
for v in nums:
    if v[0] == 1.0:
        row1 = v
        break
chk(
    "ω＝1 那一列是實部 −1、虛部 −1、3.0103 分貝、相位 −135",
    row1 is not None and near(row1[1], -1.0) and near(row1[2], -1.0) and near(row1[3], 3.0103) and near(row1[4], -135.0),
    row1,
)
chk(
    "第一列 ω＝0.01、實部 3.9976、虛部 −0.11996、12.0399 分貝、相位 −1.71882",
    near(nums[0][1], 3.9976) and near(nums[0][2], -0.11996) and near(nums[0][3], 12.0399) and near(nums[0][4], -1.71882),
    nums[0],
)
chk(
    "末列實部 −1.1996e-07、虛部 3.9976e-06、−107.96 分貝、相位 −268.281",
    near(nums[-1][1], -1.1996e-07) and near(nums[-1][2], 3.9976e-06) and near(nums[-1][3], -107.96) and near(nums[-1][4], -268.281),
    nums[-1],
)
db_err = max(abs(dbs[i] - 20.0 * math.log10(abs(zs[i]))) for i in range(len(zs)))
chk("存檔分貝對 20·log10(|z|) 的最大差", near(db_err, DB_ERR, 1e-12), db_err)
phu = unwrap_deg(zs)
ph_err = max(abs(phs[i] - phu[i]) for i in range(len(zs)))
chk("存檔相位對 atan2 展開的最大差", near(ph_err, PH_ERR, 1e-12), ph_err)
model_err = 0.0
for w, z in zip(ws, zs):
    model_err = max(model_err, abs(4.0 / (1j * w + 1.0) ** 3 - z))
chk("與 4/(jω+1)³ 的最大絕對差", near(model_err, MODEL_ERR, 1e-15), model_err)

hits = cross_real(ws, zs)
chk("負實軸交點正好一個", len(hits) == 1, len(hits))
if len(hits) != 1:
    end()
w_pc, re_pc, i_pc, t_pc = hits[0]
chk("負實軸交點頻率", near(w_pc, W_PC), w_pc)
chk("負實軸交點實部", near(re_pc, RE_PC), re_pc)
gm = -1.0 / re_pc
gm_db = 20.0 * math.log10(gm)
chk("增益裕度倍數", near(gm, GM_TIMES), gm)
chk("增益裕度分貝", near(gm_db, GM_DB), gm_db)
chk(
    "虛部變號的鄰列是 1.6788 與 1.77828",
    near(ws[i_pc], 1.6788) and near(ws[i_pc + 1], 1.77828) and near(zs[i_pc].real, -0.535646) and near(zs[i_pc + 1].real, -0.470774),
    (ws[i_pc], ws[i_pc + 1]),
)

ucs = unit_cross(ws, zs)
chk("模長穿越 1 正好一次", len(ucs) == 1, len(ucs))
if len(ucs) != 1:
    end()
w_gc, zre, zim, i_gc, t_gc = ucs[0]
ph = math.atan2(zim, zre) * 180.0 / math.pi
ref = phu[i_gc] + t_gc * (phu[i_gc + 1] - phu[i_gc])
while ph - ref > 180.0:
    ph -= 360.0
while ph - ref < -180.0:
    ph += 360.0
pm = 180.0 + ph
chk("單位圓交點頻率", near(w_gc, W_GC), w_gc)
chk("單位圓交點實部", near(zre, Z_GC_RE), zre)
chk("單位圓交點虛部", near(zim, Z_GC_IM), zim)
chk("相位裕度（連續相位）", near(pm, PM_DEG), pm)
chk(
    "增益變號的鄰列是 1.1885（0.566977 分貝）與 1.25893（−0.332078 分貝）",
    near(ws[i_gc], 1.1885) and near(dbs[i_gc], 0.566977) and near(ws[i_gc + 1], 1.25893) and near(dbs[i_gc + 1], -0.332078),
    (ws[i_gc], dbs[i_gc], ws[i_gc + 1], dbs[i_gc + 1]),
)
log_m = log_cross(ws, dbs, 0.0)
log_p = log_cross(ws, phs, -180.0)
chk("對數頻率上分貝穿越 0 的頻率（對照，不是裕度定義）", len(log_m) == 1 and near(log_m[0], W_LOG_MAG), log_m)
chk("對數頻率上相位穿越 −180 的頻率（對照，不是裕度定義）", len(log_p) == 1 and near(log_p[0], W_LOG_PH), log_p)
end()
