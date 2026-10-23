#!/usr/bin/env python3
"""sample-rootlocus-sim-s1-s2-s3-loop-selfcheck.py：圖 S1、圖 S2、圖 S3 自我檢查。
三張圖共用 sample-rootlocus-sim-s1-s2-s3-loop.csv。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-rootlocus-sim-s1-s2-s3-loop-selfcheck.py   全部通過時結束碼為 0。
數字為模擬、虛構未核。沒有隨機種子。
分離點用離開實軸後頭兩列的虛部平方對增益做兩點外推。
虛軸交點與阻尼比 0.5 是鄰列對增益的線性內插。阻尼比 0.5 解的是內插極點正好落在這條射線上。
步階過衝不在 CSV。記載的增益正好 6、分離點增益 0.3849、末點角度正好 60 度，都不是這一檔的內插。
"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-rootlocus-sim-s1-s2-s3-loop.csv"
COLS = ["K", "re_1", "im_1", "re_2", "im_2", "re_3", "im_3"]
RESULTS = []

N_EXPECT = 201
K_END = 937.542
# 韋達：s^3+3s^2+2s+K=0。和為 −3，兩兩積和為 2，積為 −K。
VIETA_SUM = 4.000000000070614e-05
VIETA_SP = 0.00032755850000398823
VIETA_PROD = 0.0028973210773983737
# 末列
LAST_RE = -10.8214
LAST_C_RE = 3.91069
LAST_C_IM = 8.44657
LAST_ANG = 59.8270199518355
# 分離點鄰列（0 起算索引 87、88）
K_REAL = 0.380943
RE_REAL = (-2.15338, -0.47113, -0.375491)
K_CPLX = 0.408197
RE1_CPLX = -2.1624
RE_PAIR = -0.418801
IM_PAIR = 0.115656
# 虛部平方兩點外推（索引 88 與 89）
KB = 0.38461305790181505
RE_B = -0.4226214290384014
THIRD_B = -2.1547607569851452
# 虛軸交點（索引 126 與 127）
K_LO = 5.63963
K_HI = 6.04311
K_X = 6.00078034376338
IM_X = 1.4141960660849822
THIRD_X = -2.9999999517003597
T_X = 0.8950885886868744
N_POS = 74
I_POS = 127
# 阻尼比 0.5（索引 101 與 102）
K_Z = 1.0375331444568823
RE_Z = -0.3333078113277144
IM_Z = 0.5773060637791827
WN_Z = 0.6666156226554288
THIRD_Z = -2.3333853948300813
T_Z = 0.49125724486586314
ZETA_LO = 0.5138579169133127
ZETA_HI = 0.48595696104593455
K_Z_LO = 1.00231
K_Z_HI = 1.07401
RE_Z_LO = -0.337371
IM_Z_LO = 0.563234
THIRD_Z_LO = -2.32526
RE_Z_HI = -0.3291
IM_Z_HI = 0.591879
THIRD_Z_HI = -2.3418
OS_FORMULA = 16.303353482158048
# 增益 20 的線性內插（索引 144 與 145）。這是沒有加零點的極點。
T20 = 0.31237496427550787
K20_LO = 19.5628
K20_HI = 20.9624
RE20 = -3.8368531266076022
C20_RE = 0.41842650042869395
C20_IM = 2.2440291454701344
# 最靠近增益 0.3 的存檔列
K_NEAR03 = 0.309621
NEAR03 = (-2.12884, -0.646028, -0.225131)
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

def zeta(z):
    return -z.real / abs(z)

def unchecked():
    skip("步階過衝 15.5%，以及增益 0.3、1、3、6 的過衝 −0.3、14.5、56.5、90.5", "CSV 沒有時間響應")
    skip("記載的分離點增益 0.3849、實部 −0.4226 當作存檔格", "這一檔的兩點外推是 0.38461305790181505 與 −0.4226214290384014；−0.4226 只是外推實部四捨五入到四位小數")
    skip("記載的增益正好 6、虛部正好 1.4142 當作存檔格", "虛軸交點內插是 6.00078034376338 與 ±1.4141960660849822；1.4142 是四位小數")
    skip("記載的阻尼比交點增益 1.037、極點 −0.3333±0.5774j、第三極點 −2.3333、自然頻率 0.6667", "這一檔把內插極點解到阻尼比正好 0.5，增益是 1.0375331444568823")
    skip("末列角度正好 60 度", "由 K＝0 的極點算出的漸近線規則是 60 度；末列相對中心 −1 的角度是 59.8270199518355 度")
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
z0 = ps[0]
chk("增益 0 的極點是 −2、−1、0", near(z0[0].real, -2) and near(z0[1].real, -1) and near(z0[2].real, 0) and all(z.imag == 0 for z in z0))
cent = (z0[0].real + z0[1].real + z0[2].real) / 3.0
angs = [(2 * q + 1) * 180.0 / 3.0 for q in (0, 1, 2)]
chk("漸近線中心由開迴路極點算出是 −1", near(cent, -1.0) and cent == -1.0)
chk("漸近線角度規則是 60、180、300 度", angs == [60.0, 180.0, 300.0])
max_sum = max_sp = max_prod = 0.0
for k, zs in zip(ks, ps):
    s = zs[0] + zs[1] + zs[2]
    sp = zs[0] * zs[1] + zs[0] * zs[2] + zs[1] * zs[2]
    pr = zs[0] * zs[1] * zs[2]
    max_sum = max(max_sum, abs(s + 3))
    max_sp = max(max_sp, abs(sp - 2))
    max_prod = max(max_prod, abs(pr + k))
chk("極點和加 3 的最大絕對差", near(max_sum, VIETA_SUM), max_sum)
chk("兩兩積和減 2 的最大絕對差", near(max_sp, VIETA_SP), max_sp)
chk("極點積加增益的最大絕對差", near(max_prod, VIETA_PROD), max_prod)
last = ps[-1]
chk(
    "末列極點是 −10.8214 與 3.91069±8.44657j",
    near(last[0].real, LAST_RE) and last[0].imag == 0 and near(last[1].real, LAST_C_RE) and near(last[1].imag, LAST_C_IM) and near(last[2].imag, -LAST_C_IM),
)
ang = math.degrees(math.atan2(last[1].imag, last[1].real - cent))
chk("末列相對中心 −1 的角度", near(ang, LAST_ANG) and near(math.degrees(math.atan2(last[0].imag, last[0].real - cent)), 180.0), ang)
i_c = next(i for i, zs in enumerate(ps) if any(z.imag != 0 for z in zs))
chk("第一個離開實軸的列是索引 88、增益 0.408197", i_c == 88 and near(ks[i_c], K_CPLX))
a, b = ps[i_c - 1], ps[i_c]
chk(
    "前一列仍全實數：−2.15338、−0.47113、−0.375491",
    near(ks[i_c - 1], K_REAL) and all(z.imag == 0 for z in a) and all(near(a[j].real, RE_REAL[j]) for j in range(3)),
)
chk(
    "離開實軸的那一列是 −2.1624 與 −0.418801±0.115656j",
    near(b[0].real, RE1_CPLX) and b[0].imag == 0 and near(b[1].real, RE_PAIR) and near(b[1].imag, IM_PAIR) and near(b[2].imag, -IM_PAIR),
)
y1 = ps[i_c][1].imag ** 2
y2 = ps[i_c + 1][1].imag ** 2
k1, k2 = ks[i_c], ks[i_c + 1]
kb = (y2 * k1 - y1 * k2) / (y2 - y1)
t_b = (kb - k1) / (k2 - k1)
re_b = ps[i_c][1].real + t_b * (ps[i_c + 1][1].real - ps[i_c][1].real)
third_b = ps[i_c][0].real + t_b * (ps[i_c + 1][0].real - ps[i_c][0].real)
chk("虛部平方外推的分離點", near(kb, KB) and near(re_b, RE_B) and near(third_b, THIRD_B), (kb, re_b, third_b))
cross = []
for i in range(len(ks) - 1):
    for j in range(3):
        ra, rb = ps[i][j].real, ps[i + 1][j].real
        if ra < 0.0 <= rb and abs(ps[i][j].imag) > 0.1:
            t = ra / (ra - rb)
            cross.append((
                ks[i] + t * (ks[i + 1] - ks[i]),
                ps[i][j].imag + t * (ps[i + 1][j].imag - ps[i][j].imag),
                t,
                i,
            ))
chk("虛軸交點正好一對", len(cross) == 2 and near(cross[0][0], cross[1][0]) and near(cross[0][1], -cross[1][1]))
if cross:
    kx, imx, tx, ix = cross[0]
    third = ps[ix][0].real + tx * (ps[ix + 1][0].real - ps[ix][0].real)
    chk(
        "虛軸交點內插",
        near(kx, K_X) and near(imx, IM_X) and near(third, THIRD_X) and near(tx, T_X) and near(ks[ix], K_LO) and near(ks[ix + 1], K_HI),
        (kx, imx, third),
    )
i_pos = next(i for i, zs in enumerate(ps) if any(z.real > 0 for z in zs))
n_pos = sum(1 for zs in ps if any(z.real > 0 for z in zs))
chk("實部為正的列有 74 列，第一列索引 127", n_pos == N_POS and i_pos == I_POS and near(ks[i_pos], K_HI))

def ray_t(i, j):
    ra, ia = ps[i][j].real, ps[i][j].imag
    rb, ib = ps[i + 1][j].real, ps[i + 1][j].imag
    dre, dim = rb - ra, ib - ia
    A = dim * dim - 3.0 * dre * dre
    B = 2.0 * ia * dim - 6.0 * ra * dre
    C = ia * ia - 3.0 * ra * ra
    disc = B * B - 4.0 * A * C
    ts = []
    if abs(A) < 1e-18:
        if abs(B) > 1e-18:
            ts = [-C / B]
    elif disc >= 0.0:
        sd = math.sqrt(disc)
        ts = [(-B + sd) / (2.0 * A), (-B - sd) / (2.0 * A)]
    return [t for t in ts if 0.0 <= t <= 1.0]

hits = []
for i in range(len(ks) - 1):
    if ps[i][1].imag == 0 or ps[i + 1][1].imag == 0:
        continue
    za, zb = zeta(ps[i][1]), zeta(ps[i + 1][1])
    if (za - 0.5) * (zb - 0.5) > 0:
        continue
    for t in ray_t(i, 1):
        re = ps[i][1].real + t * (ps[i + 1][1].real - ps[i][1].real)
        im = ps[i][1].imag + t * (ps[i + 1][1].imag - ps[i][1].imag)
        third = ps[i][0].real + t * (ps[i + 1][0].real - ps[i][0].real)
        hits.append((ks[i] + t * (ks[i + 1] - ks[i]), re, im, third, t, i, za, zb))
chk("阻尼比 0.5 的內插正好一次", len(hits) == 1)
if hits:
    kz, re, im, third, tz, iz, za, zb = hits[0]
    wn = math.hypot(re, im)
    chk(
        "阻尼比正好 0.5 的增益與極點",
        near(kz, K_Z) and near(re, RE_Z) and near(im, IM_Z) and near(third, THIRD_Z) and near(wn, WN_Z) and near(tz, T_Z) and near(zeta(complex(re, im)), 0.5) and near(za, ZETA_LO) and near(zb, ZETA_HI) and near(ks[iz], K_Z_LO) and near(ks[iz + 1], K_Z_HI) and near(ps[iz][1].real, RE_Z_LO) and near(ps[iz][1].imag, IM_Z_LO) and near(ps[iz][0].real, THIRD_Z_LO) and near(ps[iz + 1][1].real, RE_Z_HI) and near(ps[iz + 1][1].imag, IM_Z_HI) and near(ps[iz + 1][0].real, THIRD_Z_HI),
        (kz, re, im, third, wn),
    )
    ang_z = math.degrees(math.atan2(im, -re))
    chk("這點相對負實軸的角度是 60 度", near(ang_z, 60.0) and near(math.degrees(math.acos(0.5)), 60.0), ang_z)
os_formula = 100.0 * math.exp(-math.pi * 0.5 / math.sqrt(1.0 - 0.5 * 0.5))
chk("阻尼比 0.5 的二階過衝公式", near(os_formula, OS_FORMULA) and round(os_formula, 1) == 16.3, os_formula)
i20 = next(i for i in range(len(ks) - 1) if ks[i] <= 20.0 <= ks[i + 1])
t20 = (20.0 - ks[i20]) / (ks[i20 + 1] - ks[i20])
z20 = [ps[i20][j] + t20 * (ps[i20 + 1][j] - ps[i20][j]) for j in range(3)]
chk(
    "增益 20 的內插極點在右半平面",
    near(ks[i20], K20_LO) and near(ks[i20 + 1], K20_HI) and near(t20, T20) and near(z20[0].real, RE20) and z20[0].imag == 0 and near(z20[1].real, C20_RE) and near(z20[1].imag, C20_IM) and z20[1].real > 0,
    (z20[0].real, z20[1]),
)
i03 = min(range(len(ks)), key=lambda i: abs(ks[i] - 0.3))
chk(
    "最靠近增益 0.3 的列全是實數",
    near(ks[i03], K_NEAR03) and all(ps[i03][j].imag == 0 and near(ps[i03][j].real, NEAR03[j]) for j in range(3)),
    ks[i03],
)
end()
