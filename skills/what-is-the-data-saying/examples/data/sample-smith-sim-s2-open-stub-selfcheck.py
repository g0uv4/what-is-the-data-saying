#!/usr/bin/env python3
"""sample-smith-sim-s2-open-stub-selfcheck.py：圖 S2 自我檢查。
從 sample-smith-sim-s2-open-stub.csv 核對開路短截線掃頻的反射係數。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-smith-sim-s2-open-stub-selfcheck.py   全部通過時結束碼為 0。
數字為虛構示範，未核。沒有隨機種子。反射係數由正規化阻抗重算。
長度 0.3 公尺、相速每秒 2e8 公尺、記載的最大電阻 367 歐姆不在這份表裡。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-smith-sim-s2-open-stub.csv"
COLS = ["freq_GHz", "R_ohm", "X_ohm", "gamma_re", "gamma_im"]
RESULTS = []

N_EXPECT = 91
Z0 = 50.0
G_TOL = 2e-5
# 模擬記載（寫死）。367 是較密曲線的峰值，不是這 91 列的最大值。
RECORDED_MAX_R = 367.0
LENGTH_M = 0.3
VP = 2e8

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip(
        "這段線長 0.3 公尺、相速每秒 200000000 公尺",
        "CSV 沒有長度與相速欄；上面代入公式得到的 2.7 圈用的是寫死的常數",
    )
    skip(
        f"最大電阻是 {RECORDED_MAX_R:g} 歐姆",
        "367 對不上這 91 列；表內最大電阻另項通過，不把較密曲線的峰值算成這一檔的列",
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
chk("91 列", len(rows) == N_EXPECT, len(rows))
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
chk("頻率、阻抗與反射係數是有限數", nums is not None and len(nums) == len(rows))
if empty or nums is None:
    end()

freq_ok = True
for i, (f, _R, _X, _gr, _gi) in enumerate(nums):
    if round(f * 1000) != 100 + i * 10:
        freq_ok = False
chk("0.100 到 1.000 吉赫、每 0.010", freq_ok, (nums[0][0], nums[-1][0]))

g_err = 0.0
mags = []
phases = []
max_abs_x = (-1.0, None)
max_r = (-1.0, None)
over = 0
for f, R, X, gre, gim in nums:
    z = complex(R, X) / Z0
    g = (z - 1) / (z + 1)
    g_err = max(g_err, abs(g.real - gre), abs(g.imag - gim))
    mags.append(abs(complex(gre, gim)))
    phases.append(math.atan2(gim, gre))
    if abs(X) > max_abs_x[0]:
        max_abs_x = (abs(X), f)
    if R > max_r[0]:
        max_r = (R, f)
    if abs(R) > 150 or abs(X) > 150:
        over += 1
chk("反射係數等於 (z−1)/(z+1)，容差 2e-5", g_err <= G_TOL, g_err)
chk(
    "起點反射係數大小四捨五入到三位小數是 0.861",
    round(mags[0], 3) == 0.861,
    mags[0],
)
chk(
    "終點反射係數大小四捨五入到三位小數是 0.622",
    round(mags[-1], 3) == 0.622,
    mags[-1],
)
chk("反射係數大小嚴格變小", all(mags[i] > mags[i + 1] for i in range(len(mags) - 1)))
chk("每一點反射係數大小小於 1", max(mags) < 1, max(mags))
chk(
    "最大電抗絕對值 183.852 歐姆在 0.32 吉赫，四捨五入是 184",
    abs(max_abs_x[0] - 183.852) < 1e-9 and abs(max_abs_x[1] - 0.32) < 1e-9 and round(max_abs_x[0]) == 184,
    max_abs_x,
)
chk(
    "這 91 列的最大電阻是 350.729 歐姆、在 0.33 吉赫",
    abs(max_r[0] - 350.729) < 1e-9 and abs(max_r[1] - 0.33) < 1e-9,
    max_r,
)
chk("至少有一點的電阻或電抗絕對值超過 150 歐姆", over >= 1, over)

unwrapped_list = [phases[0]]
for p in phases[1:]:
    d = p - unwrapped_list[-1]
    while d > math.pi:
        d -= 2 * math.pi
    while d < -math.pi:
        d += 2 * math.pi
    unwrapped_list.append(unwrapped_list[-1] + d)
turns = (unwrapped_list[-1] - unwrapped_list[0]) / (2 * math.pi)
chk("由反射係數相位展開，順時針 2.7 圈（容差 1e-4）", abs(turns - (-2.7)) <= 1e-4, turns)

model_turns = 2 * (1.0 - 0.1) * 1e9 * LENGTH_M / VP
chk(
    "寫死的 0.3 公尺、相速 2e8、頻寬 0.9 吉赫代入 2·Δf·L/vp 得 2.7",
    abs(model_turns - 2.7) <= 1e-12,
    model_turns,
)
end()
