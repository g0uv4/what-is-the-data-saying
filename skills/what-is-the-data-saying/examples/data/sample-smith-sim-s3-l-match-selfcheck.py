#!/usr/bin/env python3
"""sample-smith-sim-s3-l-match-selfcheck.py：圖 S3 自我檢查。
從 sample-smith-sim-s3-l-match.csv 核對 L 型匹配的三個點，
並把寫死的 2.44 吉赫代進電感、電容公式。
另核一組自算的導納例：z=0.80+j1.40 繞圓心轉半圈。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-smith-sim-s3-l-match-selfcheck.py   全部通過時結束碼為 0。
數字為虛構示範，未核。2.44 吉赫不在 CSV。圖紙讀到的 0.30−j0.54 不採用。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-smith-sim-s3-l-match.csv"
COLS = ["step", "z_norm_re", "z_norm_im", "gamma_re", "gamma_im", "note"]
RESULTS = []

Z0 = 50.0
G_TOL = 2e-5
# 模擬記載（寫死）。頻率不在 CSV，只用來代公式。
F_HZ = 2.44e9
# 自算例題（寫死）。不是從任何圖上量的。
Z_EX = complex(0.80, 1.40)

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip(
        "匹配頻率就是 2.44 吉赫",
        "CSV 沒有頻率欄；電感與電容只是把寫死的頻率代進公式",
    )
    skip(
        "導納讀成 0.30−j0.54",
        "那是圖紙讀值。公式到三位小數是 0.308−j0.538，不把 0.30−j0.54 當成量到的數",
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
    chk("第一行是表頭", first.startswith("step,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("3 列", len(rows) == 3, len(rows))
if not cols_ok or len(rows) != 3:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
steps = [r["step"] for r in rows]
chk("順序是負載、串聯電感、並聯電容", steps == ["load", "after_series_L", "after_shunt_C"], steps)
notes = [r["note"] for r in rows]
chk(
    "註記是負載 20-j30 歐姆、串聯電感 3.55 nH、並聯電容 1.60 pF",
    notes == ["負載 20-j30 歐姆", "串聯電感 3.55 nH", "並聯電容 1.60 pF"],
    notes,
)

pts = []
nums_ok = True
for r in rows:
    try:
        re, im = float(r["z_norm_re"]), float(r["z_norm_im"])
        gre, gim = float(r["gamma_re"]), float(r["gamma_im"])
    except ValueError:
        nums_ok = False
        break
    if not all(math.isfinite(v) for v in (re, im, gre, gim)):
        nums_ok = False
        break
    pts.append((re, im, gre, gim))
chk("正規化阻抗與反射係數是有限數", nums_ok and len(pts) == 3)
if not nums_ok or len(pts) != 3:
    end()

g_err = 0.0
for re, im, gre, gim in pts:
    z = complex(re, im)
    g = (z - 1) / (z + 1)
    g_err = max(g_err, abs(g.real - gre), abs(g.imag - gim))
chk("三點反射係數都等於 (z−1)/(z+1)，容差 2e-5", g_err <= G_TOL, g_err)

re0, im0, gre0, gim0 = pts[0]
chk("負載是 0.4000−j0.6000", abs(re0 - 0.4) < 1e-9 and abs(im0 - (-0.6)) < 1e-9, (re0, im0))
chk("乘上 50 歐姆是 20−j30 歐姆", abs(re0 * Z0 - 20) < 1e-9 and abs(im0 * Z0 - (-30)) < 1e-9)
ag0 = math.hypot(gre0, gim0)
vswr0 = (1 + ag0) / (1 - ag0)
chk("負載反射係數大小四捨五入到三位小數是 0.557", round(ag0, 3) == 0.557, ag0)
chk("負載駐波比四捨五入到兩位小數是 3.52", round(vswr0, 2) == 3.52, vswr0)

re1, im1, _gre1, _gim1 = pts[1]
chk("串聯之後實部仍是 0.4000", abs(re1 - re0) < 1e-9 and abs(re1 - 0.4) < 1e-9, re1)
x_hit = math.sqrt(0.4 - 0.4 * 0.4)
chk(
    "虛部 0.4899 是 r=0.4 與 g=1 的交點，四捨五入到四位小數",
    abs(im1 - 0.4899) < 1e-9 and round(x_hit, 4) == 0.4899,
    (im1, x_hit),
)
dx = im1 - im0
chk("正規化電抗增加 1.0899，三位小數是 1.09", abs(dx - 1.0899) < 1e-9 and round(dx, 3) == 1.09, dx)
y1 = 1 / complex(re1, im1)
chk("串聯之後導納實部四捨五入到三位小數是 1.000", round(y1.real, 3) == 1.0, y1.real)
b_need = -y1.imag
chk("補到圓心要的正規化電納，三位小數是 1.225", round(b_need, 3) == 1.225, b_need)

omega = 2 * math.pi * F_HZ
l_nH = (dx * Z0) / omega * 1e9
c_pF = b_need / (omega * Z0) * 1e12
chk(
    "寫死的 2.44 吉赫代入 X/ω 得 3.55 奈亨",
    abs(l_nH - 3.5545691081118185) < 1e-9 and round(l_nH, 2) == 3.55,
    l_nH,
)
chk(
    "同一頻率代入 B/(ω·Z0) 得 1.60 皮法",
    abs(c_pF - 1.5977380086763324) < 1e-9 and round(c_pF, 2) == 1.6,
    c_pF,
)

re2, im2, gre2, gim2 = pts[2]
chk(
    "並聯之後落在 1+j0，反射係數是 0",
    abs(re2 - 1) < 1e-9 and abs(im2) < 1e-9 and abs(gre2) < 1e-9 and abs(gim2) < 1e-9,
    (re2, im2, gre2, gim2),
)

y_ex = 1 / Z_EX
g_z = (Z_EX - 1) / (Z_EX + 1)
g_y = (y_ex - 1) / (y_ex + 1)
chk(
    "z=0.80+j1.40 的倒數，三位小數是 0.308−j0.538",
    abs(y_ex.real - 0.3076923076923077) < 1e-12
    and abs(y_ex.imag - (-0.5384615384615384)) < 1e-12
    and round(y_ex.real, 3) == 0.308
    and round(y_ex.imag, 3) == -0.538,
    y_ex,
)
chk("導納的反射係數等於阻抗反射係數的相反", abs(g_y + g_z) < 1e-12, g_y + g_z)
chk("這組例題的反射係數大小四捨五入到三位小數是 0.620", round(abs(g_z), 3) == 0.620, abs(g_z))
end()
