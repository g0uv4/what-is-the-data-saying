#!/usr/bin/env python3
"""sample-rootlocus-sim-s5-unstable-open-loop-selfcheck.py：圖 S5 自我檢查。
從 sample-rootlocus-sim-s5-unstable-open-loop.csv 核對開迴路不穩定的兩條分支。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-rootlocus-sim-s5-unstable-open-loop-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
韋達用 s^2+(4+K)s+(2K−5)=0。穩定邊界取實部穿過 0 的線性內插，不是極點積穿過 0。
增益正好 2.5、另一極點正好 −6.5，以及增益 1 與 5 的極點，都不是這一檔的列。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-rootlocus-sim-s5-unstable-open-loop.csv"
COLS = ["K", "re_1", "im_1", "re_2", "im_2"]
RESULTS = []

N_EXPECT = 201
K_END = 937.542
VIETA_SUM = 0.0009400000000141517
VIETA_PROD = 0.004415699999981371
K_LO = 2.46111
RE_LO = 0.012017
OTH_LO = -6.47312
K_HI = 2.63718
RE_HI = -0.0415986
OTH_HI = -6.59559
T_B = 0.2241325285924246
K_B = 2.500573014309268
OTH_B = -6.500569510776714
K_PROD = 2.5000021076832537
N_STABLE = 86
N_UNSTABLE = 115
K_NEAR1 = 1.00231
NEAR1 = (-5.54272, 0.540418)
K_NEAR5 = 4.91168
NEAR5 = (-8.33285, -0.578838)
TOL = 1e-9

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def poles(row):
    return [complex(float(row["re_1"]), float(row["im_1"])), complex(float(row["re_2"]), float(row["im_2"]))]

def unchecked():
    skip("穩定邊界正好是增益 2.5、另一極點正好 −6.5", "實部內插是 2.500573014309268 與 −6.500569510776714；特徵式的 2K−5＝0 給出 2.5，這一檔沒有該列")
    skip("增益 1 的極點 −5.541 與 +0.541，以及增益 5 的極點 −8.405 與 −0.595", "最靠近的列是增益 1.00231 與 4.91168，不是這兩個增益")
    skip("增益格寫到 1000", "末列增益是 937.542")

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
chk("沒有增益正好 2.5 的列", all(not near(k, 2.5) for k in ks))
z0 = ps[0]
chk("增益 0 的極點是 −5 與 +1", near(z0[0].real, -5) and near(z0[1].real, 1) and z0[0].imag == 0 and z0[1].imag == 0)
chk("每一列的虛部都是 0", all(z.imag == 0 for zs in ps for z in zs))
max_sum = max_prod = 0.0
for k, zs in zip(ks, ps):
    s = zs[0] + zs[1]
    pr = zs[0] * zs[1]
    max_sum = max(max_sum, abs(s + (4 + k)))
    max_prod = max(max_prod, abs(pr - (2 * k - 5)))
chk("極點和加 (4+K) 的最大絕對差", near(max_sum, VIETA_SUM), max_sum)
chk("極點積減 (2K−5) 的最大絕對差", near(max_prod, VIETA_PROD), max_prod)
chk("4+K 在每一列都大於 0", all((4 + k) > 0 for k in ks))
bounds = []
for i in range(len(ks) - 1):
    for j in range(2):
        ra, rb = ps[i][j].real, ps[i + 1][j].real
        if ra > 0.0 >= rb:
            t = ra / (ra - rb)
            other = 1 - j
            oth = ps[i][other].real + t * (ps[i + 1][other].real - ps[i][other].real)
            bounds.append((ks[i] + t * (ks[i + 1] - ks[i]), oth, t, i))
chk("實部穿過 0 正好一次", len(bounds) == 1)
if bounds:
    kb, oth, tb, ib = bounds[0]
    chk(
        "實部內插的穩定邊界",
        near(kb, K_B) and near(oth, OTH_B) and near(tb, T_B) and near(ks[ib], K_LO) and near(ps[ib][1].real, RE_LO) and near(ps[ib][0].real, OTH_LO) and near(ks[ib + 1], K_HI) and near(ps[ib + 1][1].real, RE_HI) and near(ps[ib + 1][0].real, OTH_HI),
        (kb, oth),
    )
prod_hits = []
for i in range(len(ks) - 1):
    pa = (ps[i][0] * ps[i][1]).real
    pb = (ps[i + 1][0] * ps[i + 1][1]).real
    if pa < 0.0 <= pb or pb < 0.0 <= pa:
        t = pa / (pa - pb)
        if 0.0 <= t <= 1.0:
            prod_hits.append(ks[i] + t * (ks[i + 1] - ks[i]))
chk("極點積穿過 0 的增益是另一個數", len(prod_hits) == 1 and near(prod_hits[0], K_PROD) and not near(prod_hits[0], K_B), prod_hits)
n_stable = sum(1 for zs in ps if max(z.real for z in zs) < 0)
n_unstable = sum(1 for zs in ps if max(z.real for z in zs) > 0)
n_zero = sum(1 for zs in ps if max(z.real for z in zs) == 0)
chk("穩定 86 列、不穩定 115 列、實部為 0 的 0 列", n_stable == N_STABLE and n_unstable == N_UNSTABLE and n_zero == 0, (n_stable, n_unstable, n_zero))
i1 = min(range(len(ks)), key=lambda i: abs(ks[i] - 1.0))
i5 = min(range(len(ks)), key=lambda i: abs(ks[i] - 5.0))
chk(
    "最靠近增益 1 與 5 的存檔極點",
    near(ks[i1], K_NEAR1) and near(ps[i1][0].real, NEAR1[0]) and near(ps[i1][1].real, NEAR1[1]) and near(ks[i5], K_NEAR5) and near(ps[i5][0].real, NEAR5[0]) and near(ps[i5][1].real, NEAR5[1]),
    (ks[i1], ks[i5]),
)
end()
