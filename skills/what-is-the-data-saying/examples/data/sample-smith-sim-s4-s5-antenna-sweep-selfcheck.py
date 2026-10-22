#!/usr/bin/env python3
"""sample-smith-sim-s4-s5-antenna-sweep-selfcheck.py：圖 S4、圖 S5 自我檢查。
從 sample-smith-sim-s4-s5-antenna-sweep.csv 核對 5 百萬赫一點的掃頻。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-smith-sim-s4-s5-antenna-sweep-selfcheck.py   全部通過時結束碼為 0。
數字為虛構示範，未核。沒有隨機種子。
較密曲線上的 2.396、2.507、2.451、1.01、2.411、2.448、1.47 不是這 61 列的原格。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-smith-sim-s4-s5-antenna-sweep.csv"
COLS = [
    "freq_GHz", "R_ohm", "X_ohm",
    "gamma50_re", "gamma50_im", "vswr_ref50",
    "gamma75_re", "gamma75_im", "vswr_ref75",
]
RESULTS = []

N_EXPECT = 61
G_TOL = 2e-5
VS_TOL = 0.001
# 駐波比 2 的圓，半徑是 (2−1)/(2+1)。
GAMMA_R2 = 1.0 / 3.0

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip(
        "50 歐姆可用頻段是 2.396–2.507 吉赫、最佳 2.451 吉赫、駐波比 1.01",
        "這些是較密曲線的註記，不是這 5 百萬赫一格的原列；表內圈內端點與最小列另項通過",
    )
    skip(
        "75 歐姆可用頻段是 2.411–2.485 吉赫、最佳 2.448 吉赫、駐波比 1.47",
        "1.477 四捨五入到兩位小數是 1.48，不是 1.47；較密曲線的端點不是這份表的列",
    )
    skip(
        "模型是並聯諧振加串聯電感",
        "CSV 沒有電路參數欄，不能證明模型名稱",
    )
    skip(
        "網路分析儀標記 27.80+j10.14 到 39.07+j23.88 歐姆",
        "那些歐姆數不在這份 CSV，也不能用這份表證明參考阻抗",
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
    chk("第一行是表頭", first.startswith("freq_GHz,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("61 列", len(rows) == N_EXPECT, len(rows))
if not cols_ok:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
pts = []
nums_ok = True
for r in rows:
    try:
        vals = [float(r[c]) for c in COLS]
    except ValueError:
        nums_ok = False
        break
    if not all(math.isfinite(v) for v in vals):
        nums_ok = False
        break
    pts.append(vals)
chk("頻率、阻抗、反射係數與駐波比是有限數", nums_ok and len(pts) == len(rows))
if empty or not nums_ok:
    end()

freq_ok = all(round(p[0] * 1000) == 2300 + i * 5 for i, p in enumerate(pts))
chk("2.300 到 2.600 吉赫、每 0.005", freq_ok and abs(pts[0][0] - 2.3) < 1e-9 and abs(pts[-1][0] - 2.6) < 1e-9)

err50 = err75 = 0.0
vs50 = vs75 = 0.0
circle_ok = True
for f, R, X, g50r, g50i, v50, g75r, g75i, v75 in pts:
    for Z0, gre, gim, vs, bag in (
        (50.0, g50r, g50i, v50, "50"),
        (75.0, g75r, g75i, v75, "75"),
    ):
        z = complex(R, X) / Z0
        g = (z - 1) / (z + 1)
        e = max(abs(g.real - gre), abs(g.imag - gim))
        ag = math.hypot(gre, gim)
        pred = (1 + ag) / (1 - ag)
        if bag == "50":
            err50 = max(err50, e)
            vs50 = max(vs50, abs(pred - vs))
        else:
            err75 = max(err75, e)
            vs75 = max(vs75, abs(pred - vs))
        if ag >= 1:
            circle_ok = False
        if vs <= 2:
            if ag > GAMMA_R2 + 0.002:
                circle_ok = False
        elif ag < GAMMA_R2 - 0.002:
            circle_ok = False
chk("50 歐姆反射係數等於 (z−1)/(z+1)，容差 2e-5", err50 <= G_TOL, err50)
chk("75 歐姆反射係數等於 (z−1)/(z+1)，容差 2e-5", err75 <= G_TOL, err75)
chk("50 歐姆駐波比由反射係數重算，容差 0.001", vs50 <= VS_TOL, vs50)
chk("75 歐姆駐波比由反射係數重算，容差 0.001", vs75 <= VS_TOL, vs75)
chk("駐波比 2 的半徑是 1/3", abs((2 - 1) / (2 + 1) - GAMMA_R2) < 1e-15)
chk("反射係數都在單位圓內，而且駐波比 2 的內外與半徑 1/3 同側", circle_ok)

def band(idx_vs):
    inside = [(i, pts[i][0], pts[i][idx_vs]) for i in range(len(pts)) if pts[i][idx_vs] <= 2]
    return inside

b50 = band(5)
b75 = band(8)
idx50 = [t[0] for t in b50]
idx75 = [t[0] for t in b75]
chk(
    "50 歐姆駐波比 ≤ 2 是連續 22 列，從 2.400（1.899）到 2.505（1.935）",
    len(b50) == 22
    and idx50 == list(range(idx50[0], idx50[-1] + 1))
    and abs(b50[0][1] - 2.400) < 1e-9 and abs(b50[0][2] - 1.899) < 1e-9
    and abs(b50[-1][1] - 2.505) < 1e-9 and abs(b50[-1][2] - 1.935) < 1e-9,
    (len(b50), b50[0], b50[-1]),
)
by_f = {round(p[0] * 1000): p for p in pts}
chk(
    "50 歐姆緊鄰的外側是 2.395 的 2.018、2.510 的 2.049",
    abs(by_f[2395][5] - 2.018) < 1e-9 and abs(by_f[2510][5] - 2.049) < 1e-9
    and by_f[2395][5] > 2 and by_f[2510][5] > 2,
)
chk(
    "75 歐姆駐波比 ≤ 2 是連續 15 列，從 2.415（1.886）到 2.485（1.981）",
    len(b75) == 15
    and idx75 == list(range(idx75[0], idx75[-1] + 1))
    and abs(b75[0][1] - 2.415) < 1e-9 and abs(b75[0][2] - 1.886) < 1e-9
    and abs(b75[-1][1] - 2.485) < 1e-9 and abs(b75[-1][2] - 1.981) < 1e-9,
    (len(b75), b75[0], b75[-1]),
)
chk(
    "75 歐姆緊鄰的外側是 2.410 的 2.005、2.490 的 2.105",
    abs(by_f[2410][8] - 2.005) < 1e-9 and abs(by_f[2490][8] - 2.105) < 1e-9
    and by_f[2410][8] > 2 and by_f[2490][8] > 2,
)

v50s = [p[5] for p in pts]
v75s = [p[8] for p in pts]
i50 = v50s.index(min(v50s))
i75 = v75s.index(min(v75s))
p50 = pts[i50]
chk(
    "50 歐姆最小駐波比只有一列：2.450 吉赫、1.020、電阻 50.787、電抗 0.594",
    v50s.count(min(v50s)) == 1
    and abs(p50[0] - 2.450) < 1e-9 and abs(p50[5] - 1.020) < 1e-9
    and abs(p50[1] - 50.787) < 1e-9 and abs(p50[2] - 0.594) < 1e-9,
    (p50[0], p50[5], p50[1], p50[2]),
)
p75 = pts[i75]
chk(
    "75 歐姆最小駐波比只有一列：2.450 吉赫、1.477",
    v75s.count(min(v75s)) == 1
    and abs(p75[0] - 2.450) < 1e-9 and abs(p75[8] - 1.477) < 1e-9
    and round(p75[8], 2) == 1.48,
    (p75[0], p75[8]),
)
rs = [p[1] for p in pts]
xs = [p[2] for p in pts]
chk(
    "電阻從 11.259 到 51.0 歐姆，電抗從 −21.028 到 28.723 歐姆",
    abs(min(rs) - 11.259) < 1e-9 and abs(max(rs) - 51.0) < 1e-9
    and abs(min(xs) - (-21.028)) < 1e-9 and abs(max(xs) - 28.723) < 1e-9,
    (min(rs), max(rs), min(xs), max(xs)),
)
end()
