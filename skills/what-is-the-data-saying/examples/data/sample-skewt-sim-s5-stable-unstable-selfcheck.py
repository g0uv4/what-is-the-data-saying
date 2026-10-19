#!/usr/bin/env python3
"""sample-skewt-sim-s5-stable-unstable-selfcheck.py：圖 S5 自我檢查。
從 sample-skewt-sim-s5-stable-unstable.csv 看穩定與不穩定兩個面板裡，氣塊溫度減環境溫度的符號。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-skewt-sim-s5-stable-unstable-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。穩定面板位能 0、不穩定面板自由對流高度 756.0 百帕與平衡高度 164.2 百帕取自 sim_facts。
穩定面板每一層氣塊都不比環境暖，正的溫度差是 0，所以記載的位能 0 與欄位相符；不把負溫度差積成焦耳。
不穩定面板近地面還有一次很薄的正差，那一次不是記載的自由對流高度。
兩邊的舉升凝結高度、穩定面板的抑制 0，以及不穩定面板的 2455 與 −74 焦耳／公斤，印 NOT CHECKED。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-skewt-sim-s5-stable-unstable.csv"
COLS = ["panel", "pressure_hPa", "temperature_C", "dewpoint_C", "surface_parcel_C"]
LEVELS = [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 725, 700,
          650, 600, 550, 500, 450, 400, 350, 300, 250, 200, 175, 150, 125, 100]
RESULTS = []

# 模擬記載（寫死）。取自 sim_facts 的 S5。焦耳與舉升凝結高度只印 NOT CHECKED。
N_LEVEL = 27
N_EXPECT = 54
P_SFC = 1000.0
P_TOP = 100.0
CAPE_STABLE = 0
CIN_STABLE = 0
LCL_STABLE_HPA = 958.3
LCL_STABLE_C = 7.0
LCL_UNSTABLE_HPA = 886.2
LCL_UNSTABLE_C = 20.9
LFC_UNSTABLE_HPA = 756.0
EL_UNSTABLE_HPA = 164.2
CAPE_UNSTABLE = 2455
CIN_UNSTABLE = -74
TOL = 1e-9
TOL_HPA = 1.0
EPS = 1e-9

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def near(got, exp, tol=TOL):
    return abs(got - exp) <= tol

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip(
        f"穩定面板舉升凝結高度 {LCL_STABLE_HPA} 百帕、{LCL_STABLE_C} 度",
        "不是異號穿越；欄位沒有氣塊露點，標準函式庫不重算凝結",
    )
    skip(
        f"穩定面板對流抑制 {CIN_STABLE} 焦耳／公斤",
        "氣塊比環境冷的層還在；記載的 0 是沒有自由對流高度時的結果，不是把負溫度差積出來",
    )
    skip(
        f"不穩定面板舉升凝結高度 {LCL_UNSTABLE_HPA} 百帕、{LCL_UNSTABLE_C} 度",
        "不是異號穿越；欄位沒有氣塊露點，標準函式庫不重算凝結",
    )
    skip(
        f"不穩定面板對流可用位能 {CAPE_UNSTABLE} 焦耳／公斤、對流抑制 {CIN_UNSTABLE} 焦耳／公斤",
        "要沿高度積分浮力；標準函式庫不假算氣體常數或虛溫，只核溫度差的符號",
    )

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def end():
    unchecked()
    done()

def sgn(d):
    if d > EPS:
        return 1
    if d < -EPS:
        return -1
    return 0

def crossings(ps, delta):
    """相鄰異號時，在對數氣壓上內插零點。零正好落在某一層、且左右第一個非零異號，該層算一次。
    回傳 (氣壓, 下方差, 上方差)，由高氣壓排到低氣壓。"""
    out = []
    for i in range(len(delta) - 1):
        s1, s2 = sgn(delta[i]), sgn(delta[i + 1])
        if s1 == 0 or s2 == 0 or s1 == s2:
            continue
        t = (0.0 - delta[i]) / (delta[i + 1] - delta[i])
        p = math.exp(math.log(ps[i]) + t * (math.log(ps[i + 1]) - math.log(ps[i])))
        out.append((p, delta[i], delta[i + 1]))
    for i in range(len(delta)):
        if sgn(delta[i]) != 0:
            continue
        prev_s = next((sgn(delta[j]) for j in range(i - 1, -1, -1) if sgn(delta[j]) != 0), 0)
        next_s = next((sgn(delta[j]) for j in range(i + 1, len(delta)) if sgn(delta[j]) != 0), 0)
        if prev_s * next_s < 0:
            out.append((ps[i], float(prev_s), float(next_s)))
    out.sort(key=lambda h: -h[0])
    return out

def levels_ok(ps):
    return len(ps) == len(LEVELS) and all(near(a, float(b)) for a, b in zip(ps, LEVELS)) and all(ps[i] > ps[i + 1] for i in range(len(ps) - 1)) and near(ps[0], P_SFC) and near(ps[-1], P_TOP)

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("panel,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
chk("欄位", list(rows[0].keys()) == COLS)
chk("54 列", len(rows) == N_EXPECT)
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
if empty or list(rows[0].keys()) != COLS:
    end()
panels = [r["panel"] for r in rows]
chk("先 27 列 stable，再 27 列 unstable", panels == ["stable"] * N_LEVEL + ["unstable"] * N_LEVEL)
groups = {"stable": [r for r in rows if r["panel"] == "stable"], "unstable": [r for r in rows if r["panel"] == "unstable"]}
if panels != ["stable"] * N_LEVEL + ["unstable"] * N_LEVEL:
    end()

stable = groups["stable"]
sps = [float(r["pressure_hPa"]) for r in stable]
senv = [float(r["temperature_C"]) for r in stable]
std = [float(r["dewpoint_C"]) for r in stable]
spar = [float(r["surface_parcel_C"]) for r in stable]
chk("穩定面板氣壓就是 27 層，從 1000 到 100 百帕且嚴格遞減", levels_ok(sps))
chk("穩定面板露點不高於溫度", all(math.isfinite(t) and math.isfinite(d) and d <= t + TOL for t, d in zip(senv, std)))
chk("穩定面板地面氣塊溫度等於環境溫度", near(spar[0], senv[0]) and near(sps[0], P_SFC), (spar[0], senv[0]))
sdelta = [tp - te for tp, te in zip(spar, senv)]
# 正的溫度差整段是 0，所以沒有虛溫修正時的正浮力積分是 0。負的部分不積成焦耳。
chk("穩定面板每一層氣塊溫度都不高於環境", all(d <= EPS for d in sdelta), (min(sdelta), max(sdelta)))
chk("穩定面板只有地面那一層溫差是 0", sum(1 for d in sdelta if sgn(d) == 0) == 1 and sgn(sdelta[0]) == 0)
shits = crossings(sps, sdelta)
chk("穩定面板沒有異號穿越", len(shits) == 0, len(shits))
chk(
    "記載的穩定對流可用位能 0 與空的正溫度差相符",
    CAPE_STABLE == 0 and all(d <= EPS for d in sdelta),
)
chk("穩定面板近地逆溫：975 百帕比地面暖", senv[1] > senv[0], (senv[0], senv[1]))

unstable = groups["unstable"]
ups = [float(r["pressure_hPa"]) for r in unstable]
uenv = [float(r["temperature_C"]) for r in unstable]
utd = [float(r["dewpoint_C"]) for r in unstable]
upar = [float(r["surface_parcel_C"]) for r in unstable]
chk("不穩定面板氣壓就是 27 層，從 1000 到 100 百帕且嚴格遞減", levels_ok(ups))
chk("不穩定面板露點不高於溫度", all(math.isfinite(t) and math.isfinite(d) and d <= t + TOL for t, d in zip(uenv, utd)))
chk("不穩定面板地面氣塊溫度等於環境溫度", near(upar[0], uenv[0]) and near(ups[0], P_SFC), (upar[0], uenv[0]))
udelta = [tp - te for tp, te in zip(upar, uenv)]
uhits = crossings(ups, udelta)
neg_to_pos = [h for h in uhits if h[1] < 0 < h[2]]
pos_to_neg = [h for h in uhits if h[1] > 0 > h[2]]
chk("不穩定面板異號穿越正好三次", len(uhits) == 3 and len(neg_to_pos) + len(pos_to_neg) == len(uhits), [round(h[0], 2) for h in uhits])
chk("從冷到暖的穿越正好一次", len(neg_to_pos) == 1, len(neg_to_pos))
if len(neg_to_pos) != 1:
    end()
lfc_p = neg_to_pos[0][0]
chk("從冷到暖的穿越約 756.0 百帕（記載的自由對流高度）", near(lfc_p, LFC_UNSTABLE_HPA, TOL_HPA), lfc_p)
el_cands = [h for h in pos_to_neg if h[0] < lfc_p]
shallow = [h for h in pos_to_neg if h[0] > lfc_p]
chk("自由對流高度以上、從暖到冷的穿越正好一次", len(el_cands) == 1, [round(h[0], 2) for h in el_cands])
chk("自由對流高度以下還有一次從暖到冷（近地面的薄正差，不是平衡高度）", len(shallow) == 1, [round(h[0], 2) for h in shallow])
if len(el_cands) != 1:
    end()
el_p = el_cands[0][0]
chk("這一次約 164.2 百帕（記載的平衡高度）", near(el_p, EL_UNSTABLE_HPA, TOL_HPA), el_p)
mid = [d for p, d in zip(ups, udelta) if el_p < p < lfc_p]
chk("自由對流高度與平衡高度之間每一層氣塊都比環境暖", len(mid) > 0 and all(d > 0 for d in mid), len(mid))
end()
