#!/usr/bin/env python3
"""sample-nyquist-sim-s4-delay-selfcheck.py：圖 S4 自我檢查。
從 sample-nyquist-sim-s4-delay.csv 核對三種延遲的實部、虛部。
只需 Python 標準函式庫（cmath、csv、math、os、sys）。
用法：python3 sample-nyquist-sim-s4-delay-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
負實軸交點與單位圓交點都在頻率上線性內插存檔複數。
相位裕度用內插點的 atan2，並對到該條曲線展開後的連續相位。
延遲 1.5 的 atan2 落在約 +151 度，直接加 180 會得到約 331 度；那不是裕度。
臨界延遲不在 CSV。
"""

import cmath, csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-nyquist-sim-s4-delay.csv"
COLS = ["omega_rad_s", "re_T0", "im_T0", "re_T0.3", "im_T0.3", "re_T1.5", "im_T1.5"]
RESULTS = []

N_EXPECT = 201
W0 = 0.01
W_END = 39.8107
# 頻率上線性內插（寫死）。
W_GC = {
    0.0: 1.7324827197917119,
    0.3: 1.7324827783363994,
    1.5: 1.732483810173702,
}
PM = {
    0.0: 120.00862408820295,
    0.3: 90.23838196317779,
    1.5: -28.8415857745413,
}
PM_WRAPPED_T15 = 331.1584142254587
CROSS = {
    0.3: (5.807264954849834, -0.33927241957324733),
    1.5: (1.449894012044824, -1.135104924732878),
}
CROSS_SECOND_T03 = (26.306850566226515, -0.07595636322617443)
N_CROSS = {0.0: 0, 0.3: 2, 1.5: 10}
N_FLIP = {0.0: 0, 0.3: 4, 1.5: 19}
MODEL_ERR = {
    0.0: 5.487883306463444e-06,
    0.3: 6.421749779794289e-06,
    1.5: 1.0802616607636208e-05,
}
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
        if sign(im1) != sign(im2) and zs[i].real < 0.0:
            t = im1 / (im1 - im2)
            w = ws[i] + t * (ws[i + 1] - ws[i])
            re = zs[i].real + t * (zs[i + 1].real - zs[i].real)
            out.append((w, re))
    return out

def n_flip(zs):
    n = 0
    for i in range(len(zs) - 1):
        if sign(zs[i].imag) != sign(zs[i + 1].imag):
            n += 1
    return n

def unit_cross(ws, zs):
    m = [abs(z) for z in zs]
    out = []
    for i in range(len(ws) - 1):
        if (m[i] - 1.0) * (m[i + 1] - 1.0) < 0.0:
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

def unchecked():
    skip(
        "密格記載：延遲 0 的相位裕度 120.0、延遲 0.3 的交點 −0.34 與 90.2 度、延遲 1.5 的交點 −1.136 與 −28.9 度、增益穿越都寫 1.732",
        "那些是較密格子四捨五入後的記載；這一檔用上面印出的內插值",
    )
    skip(
        "臨界延遲 1.209 秒，以及素材說明的約 1.21 秒",
        "CSV 沒有臨界延遲欄",
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
for r in rows:
    if any((r[c] or "").strip() == "" for c in COLS):
        empty = True
        break
chk("沒有空值", not empty)
if empty:
    end()
ws = [float(r["omega_rad_s"]) for r in rows]
chk(
    "頻率從 0.01 到 39.8107 且嚴格遞增",
    near(ws[0], W0) and near(ws[-1], W_END) and all(ws[i] < ws[i + 1] for i in range(len(ws) - 1)),
    (ws[0], ws[-1]),
)
chk(
    "第一列三種延遲的實部、虛部",
    near(float(rows[0]["re_T0"]), 1.9998) and near(float(rows[0]["im_T0"]), -0.019998)
    and near(float(rows[0]["re_T0.3"]), 1.99973) and near(float(rows[0]["im_T0.3"]), -0.0259973)
    and near(float(rows[0]["re_T1.5"]), 1.99928) and near(float(rows[0]["im_T1.5"]), -0.0499916),
    rows[0],
)

pairs = [(0.0, "re_T0", "im_T0"), (0.3, "re_T0.3", "im_T0.3"), (1.5, "re_T1.5", "im_T1.5")]
for T, rek, imk in pairs:
    zs = [complex(float(r[rek]), float(r[imk])) for r in rows]
    err = 0.0
    for w, z in zip(ws, zs):
        err = max(err, abs(2.0 * cmath.exp(-1j * w * T) / (1j * w + 1.0) - z))
    chk(f"延遲 {T:g} 與 2·exp(−jωT)/(jω+1) 的最大絕對差", near(err, MODEL_ERR[T], 1e-15), err)
    hits = cross_real(ws, zs)
    flips = n_flip(zs)
    chk(f"延遲 {T:g} 虛部變號次數", flips == N_FLIP[T], flips)
    chk(f"延遲 {T:g} 起點實部為負的交點數", len(hits) == N_CROSS[T], len(hits))
    if T == 0.0:
        chk("延遲 0 沒有負實軸交點", len(hits) == 0)
    else:
        chk(
            f"延遲 {T:g} 第一個負實軸交點",
            near(hits[0][0], CROSS[T][0]) and near(hits[0][1], CROSS[T][1]),
            hits[0],
        )
        chk(f"延遲 {T:g} 的交點頻率隨序上升", all(hits[i][0] < hits[i + 1][0] for i in range(len(hits) - 1)))
    if T == 0.3:
        chk(
            "延遲 0.3 的第二個負實軸交點",
            near(hits[1][0], CROSS_SECOND_T03[0]) and near(hits[1][1], CROSS_SECOND_T03[1]),
            hits[1],
        )
    ucs = unit_cross(ws, zs)
    chk(f"延遲 {T:g} 模長穿越 1 正好一次", len(ucs) == 1, len(ucs))
    if len(ucs) != 1:
        continue
    w, zre, zim, i, t = ucs[0]
    phu = unwrap_deg(zs)
    raw = math.atan2(zim, zre) * 180.0 / math.pi
    ref = phu[i] + t * (phu[i + 1] - phu[i])
    ph = raw
    while ph - ref > 180.0:
        ph -= 360.0
    while ph - ref < -180.0:
        ph += 360.0
    pm = 180.0 + ph
    chk(f"延遲 {T:g} 單位圓交點頻率", near(w, W_GC[T]), w)
    chk(f"延遲 {T:g} 相位裕度（連續相位）", near(pm, PM[T]), pm)
    if T == 1.5:
        chk(
            "延遲 1.5 未展開的 atan2 加 180 是 331.1584142254587，不是相位裕度",
            near(180.0 + raw, PM_WRAPPED_T15) and pm < 0.0,
            (raw, 180.0 + raw, pm),
        )
end()
