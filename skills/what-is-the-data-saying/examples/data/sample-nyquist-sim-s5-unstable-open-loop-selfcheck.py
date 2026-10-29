#!/usr/bin/env python3
"""sample-nyquist-sim-s5-unstable-open-loop-selfcheck.py：圖 S5 自我檢查。
從 sample-nyquist-sim-s5-unstable-open-loop.csv 核對兩種增益。
只需 Python 標準函式庫（cmath、csv、math、os、sys）。
用法：python3 sample-nyquist-sim-s5-unstable-open-loop-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
繞圈數：閉合折線對 −1 的轉角，逆時針為正，再除以 2π。
增益 2 的繞圈數是正的 1，也就是逆時針一圈，不是順時針一圈。
頻率由負跳到正時的虛部變號，是近直流的實軸點，不是圖 S1 那種相位穿越。
開迴路極點與閉迴路極點不在 CSV。圓的端點記載 [−K, 0] 也不是這 201 列的極值。
"""

import cmath, csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-nyquist-sim-s5-unstable-open-loop.csv"
COLS = ["omega_rad_s", "re_K0.5", "im_K0.5", "re_K2", "im_K2"]
RESULTS = []

N_EXPECT = 201
W0 = -100.0
W_END = 99.77
# K＝0.5
RE_MIN_05 = -0.49995
RE_MAX_05 = -4.9995e-05
IM_AT_MIN_05 = 0.0049995
WIND_05 = -1.6565388965955816e-18
W_DC_05 = 1.1751298880681438e-07
RE_DC_05 = -0.49994522430346666
MODEL_05 = 1.2014066586665813e-06
# K＝2
RE_MIN_2 = -1.9998
RE_MAX_2 = -0.00019998
IM_AT_MIN_2 = 0.019998
WIND_2 = 1.0000000000000002
N_LEFT_2 = 100
W_DC_2 = 1.222892213655763e-07
RE_DC_2 = -1.9997808972047428
MODEL_2 = 5.3312003921361915e-06
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

def dc_cross(ws, zs):
    out = []
    for i in range(len(ws) - 1):
        im1, im2 = zs[i].imag, zs[i + 1].imag
        if sign(im1) != sign(im2) and zs[i].real < 0.0:
            t = im1 / (im1 - im2)
            w = ws[i] + t * (ws[i + 1] - ws[i])
            re = zs[i].real + t * (zs[i + 1].real - zs[i].real)
            out.append((w, re))
    return out

def unchecked():
    skip(
        "記載的圓弧範圍 [−0.5, 0] 與 [−2, 0]",
        "那是 ω→0 與 ω→∞ 的式子極限，不是這 201 列的實部極值",
    )
    skip(
        "開迴路右半平面極點數 1，以及閉迴路極點 +0.5、−1",
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
for r in rows:
    if any((r[c] or "").strip() == "" for c in COLS):
        empty = True
        break
chk("沒有空值", not empty)
if empty:
    end()
ws = [float(r["omega_rad_s"]) for r in rows]
chk(
    "頻率從 −100 到 99.77 且嚴格遞增",
    near(ws[0], W0) and near(ws[-1], W_END) and all(ws[i] < ws[i + 1] for i in range(len(ws) - 1)),
    (ws[0], ws[-1]),
)
chk("最負的實部在 ω＝−0.01 那一列", rows[100]["omega_rad_s"] == "-0.01")

zs05 = [complex(float(r["re_K0.5"]), float(r["im_K0.5"])) for r in rows]
res05 = [z.real for z in zs05]
i05 = res05.index(min(res05))
chk("增益 0.5 的最負實部是 −0.49995、在 ω＝−0.01", near(res05[i05], RE_MIN_05) and near(ws[i05], -0.01) and near(zs05[i05].imag, IM_AT_MIN_05), (ws[i05], zs05[i05]))
chk("增益 0.5 的最大實部是 −4.9995e-05、在 ω＝−100", near(max(res05), RE_MAX_05) and near(ws[res05.index(max(res05))], -100.0))
chk("增益 0.5 沒有實部小於 −1 的點", sum(1 for re in res05 if re < -1.0) == 0)
err05 = max(abs(0.5 / (1j * w - 1.0) - z) for w, z in zip(ws, zs05))
chk("增益 0.5 與 0.5/(jω−1) 的最大絕對差", near(err05, MODEL_05, 1e-15), err05)
wind05 = winding(zs05)
chk("增益 0.5 閉合折線的繞圈數", near(wind05, WIND_05, 1e-18) and abs(wind05) < 1e-15, wind05)
hits05 = dc_cross(ws, zs05)
chk("增益 0.5 虛部變號正好一次", len(hits05) == 1, len(hits05))
if hits05:
    chk(
        "增益 0.5 近直流的實軸內插在 −1 右邊",
        near(hits05[0][0], W_DC_05) and near(hits05[0][1], RE_DC_05) and hits05[0][1] > -1.0,
        hits05[0],
    )

zs2 = [complex(float(r["re_K2"]), float(r["im_K2"])) for r in rows]
res2 = [z.real for z in zs2]
i2 = res2.index(min(res2))
chk("增益 2 的最負實部是 −1.9998、在 ω＝−0.01", near(res2[i2], RE_MIN_2) and near(ws[i2], -0.01) and near(zs2[i2].imag, IM_AT_MIN_2), (ws[i2], zs2[i2]))
chk("增益 2 的最大實部是 −0.00019998、在 ω＝−100", near(max(res2), RE_MAX_2) and near(ws[res2.index(max(res2))], -100.0))
chk("增益 2 有 100 個實部小於 −1 的點", sum(1 for re in res2 if re < -1.0) == N_LEFT_2)
err2 = max(abs(2.0 / (1j * w - 1.0) - z) for w, z in zip(ws, zs2))
chk("增益 2 與 2/(jω−1) 的最大絕對差", near(err2, MODEL_2, 1e-15), err2)
wind2 = winding(zs2)
chk("增益 2 閉合折線的繞圈數是逆時針 1", near(wind2, WIND_2, 1e-15) and wind2 > 0.0, wind2)
hits2 = dc_cross(ws, zs2)
chk("增益 2 虛部變號正好一次", len(hits2) == 1, len(hits2))
if hits2:
    chk(
        "增益 2 近直流的實軸內插在 −1 左邊",
        near(hits2[0][0], W_DC_2) and near(hits2[0][1], RE_DC_2) and hits2[0][1] < -1.0,
        hits2[0],
    )
end()
