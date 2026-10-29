#!/usr/bin/env python3
"""sample-rootlocus-sim-s4-add-zero-selfcheck.py：圖 S4 自我檢查。
從 sample-rootlocus-sim-s4-add-zero.csv 核對加了零點之後的三條分支。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-rootlocus-sim-s4-add-zero-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
韋達用 s^3+3s^2+(2+K)s+1.5K=0。增益 20 是鄰列對增益的線性內插。
末列實極點 −1.5004、複數實部 −0.7498，不是記載的零點 −1.5 與中心 −0.75。
沒有加零點、增益 20 的右半平面極點在另一份 CSV。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-rootlocus-sim-s4-add-zero.csv"
COLS = ["K", "re_1", "im_1", "re_2", "im_2", "re_3", "im_3"]
RESULTS = []

N_EXPECT = 201
K_END = 937.542
VIETA_SUM = 5.0900000001519174e-06
VIETA_SP = 0.0026373196289455336
VIETA_PROD = 0.0063010426028995425
MAX_RE = -0.000750469
K20_LO = 19.5628
K20_HI = 20.9624
T20 = 0.31237496427550787
RE20 = -1.5189807887967992
C20_RE = -0.740509980851672
C20_IM = 4.381390803086597
LAST_RE = -1.5004
LAST_C_RE = -0.7498
LAST_C_IM = 30.606
ANG_75 = 89.99962559119446
TOL = 1e-9

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def poles(row):
    return [complex(float(row[f"re_{i}"]), float(row[f"im_{i}"])) for i in (1, 2, 3)]

def unchecked():
    skip("零點正好 −1.5、漸近線中心正好 −0.75 當作存檔格", "末列實極點是 −1.5004，複數實部是 −0.7498")
    skip("增益 20 的虛部記載 4.382", "這一檔的內插虛部是 4.381390803086597")
    skip("沒有加零點時增益 20 的極點 0.419±2.244j", "那一組在另一份 CSV；這一檔加了零點，內插實部是負的")
    skip("增益格寫到 1000", "末列增益是 937.542")
    skip("K＝0 也算穩定", "增益 0 有一個極點在 0，不在左半平面")

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
    chk("第一行是表頭", first.startswith("K,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("201 列", len(rows) == N_EXPECT, len(rows))
if not cols_ok:
    end()
empty = any(any((r[c] or "").strip() == "" for c in COLS) for r in rows)
chk("沒有空值", not empty)
if empty:
    end()
ks = [float(r["K"]) for r in rows]
ps = [poles(r) for r in rows]
chk(
    "增益從 0 到 937.542 且嚴格遞增",
    near(ks[0], 0.0) and near(ks[-1], K_END) and all(ks[i] < ks[i + 1] for i in range(len(ks) - 1)),
    (ks[0], ks[-1]),
)
chk("增益不重複", len(set(ks)) == N_EXPECT)
z0 = ps[0]
chk("增益 0 的極點是 −2、−1、0", near(z0[0].real, -2) and near(z0[1].real, -1) and z0[2] == 0 and all(z.imag == 0 for z in z0))
chk("增益 0 有一個極點在原點", any(z == 0 for z in z0))
pos = [i for i, zs in enumerate(ps) if any(z.real > 0 for z in zs)]
chk("沒有實部為正的列", pos == [])
re_pos = [z.real for k, zs in zip(ks, ps) if k > 0 for z in zs]
chk("增益大於 0 的實部都是負的，最大是 −0.000750469", re_pos and max(re_pos) < 0 and near(max(re_pos), MAX_RE), max(re_pos) if re_pos else None)
max_sum = max_sp = max_prod = 0.0
for k, zs in zip(ks, ps):
    s = zs[0] + zs[1] + zs[2]
    sp = zs[0] * zs[1] + zs[0] * zs[2] + zs[1] * zs[2]
    pr = zs[0] * zs[1] * zs[2]
    max_sum = max(max_sum, abs(s + 3))
    max_sp = max(max_sp, abs(sp - (2 + k)))
    max_prod = max(max_prod, abs(pr - (-1.5 * k)))
chk("極點和加 3 的最大絕對差", near(max_sum, VIETA_SUM), max_sum)
chk("兩兩積和減 (2+K) 的最大絕對差", near(max_sp, VIETA_SP), max_sp)
chk("極點積減 (−1.5K) 的最大絕對差", near(max_prod, VIETA_PROD), max_prod)
# 勞斯：3(2+K) > 1.5K 在 K>0 恆成立，這裡只核這條代數，不把它說成存檔格。
chk("3(2+K)−1.5K 在這一檔的正增益都大於 0", all((6 + 1.5 * k) > 0 for k in ks if k > 0))
i20 = next(i for i in range(len(ks) - 1) if ks[i] <= 20.0 <= ks[i + 1])
t20 = (20.0 - ks[i20]) / (ks[i20 + 1] - ks[i20])
z20 = [ps[i20][j] + t20 * (ps[i20 + 1][j] - ps[i20][j]) for j in range(3)]
chk(
    "增益 20 的內插仍在左半平面",
    near(ks[i20], K20_LO) and near(ks[i20 + 1], K20_HI) and near(t20, T20) and near(z20[0].real, RE20) and z20[0].imag == 0 and near(z20[1].real, C20_RE) and near(z20[1].imag, C20_IM) and all(z.real < 0 for z in z20),
    (z20[0].real, z20[1]),
)
last = ps[-1]
chk(
    "末列是 −1.5004 與 −0.7498±30.606j",
    near(last[0].real, LAST_RE) and last[0].imag == 0 and near(last[1].real, LAST_C_RE) and near(last[1].imag, LAST_C_IM) and near(last[2].imag, -LAST_C_IM),
)
ang_stored = math.degrees(math.atan2(last[1].imag, last[1].real - LAST_C_RE))
ang_75 = math.degrees(math.atan2(last[1].imag, last[1].real - (-0.75)))
chk("相對存檔實部 −0.7498 的角度是 ±90 度", near(ang_stored, 90.0) and near(math.degrees(math.atan2(last[2].imag, last[2].real - LAST_C_RE)), -90.0), ang_stored)
chk("相對 −0.75 的角度", near(ang_75, ANG_75) and near(math.degrees(math.atan2(last[2].imag, last[2].real - (-0.75))), -ANG_75), ang_75)
end()
