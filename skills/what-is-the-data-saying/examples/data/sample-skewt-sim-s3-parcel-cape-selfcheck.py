#!/usr/bin/env python3
"""sample-skewt-sim-s3-parcel-cape-selfcheck.py：圖 S3 自我檢查。
從 sample-skewt-sim-s3-parcel-cape.csv 看地面氣塊溫度減環境溫度在哪裡換號。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-skewt-sim-s3-parcel-cape-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。自由對流高度 747.4 百帕、平衡高度 163.0 百帕取自 sim_facts。
溫度只到 0.1 度，零點在 25 百帕格上可以移大約 1 百帕，所以對數氣壓內插的容差是 1 百帕。
舉升凝結高度 895.2 百帕／21.2 度不是這個換號。位能 2311 與抑制 −87 焦耳／公斤要積分浮力，印 NOT CHECKED。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-skewt-sim-s3-parcel-cape.csv"
COLS = ["pressure_hPa", "temperature_C", "dewpoint_C", "surface_parcel_C"]
LEVELS = [1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 725, 700,
          650, 600, 550, 500, 450, 400, 350, 300, 250, 200, 175, 150, 125, 100]
RESULTS = []

# 模擬記載（寫死）。高度與焦耳取自 sim_facts。焦耳與舉升凝結高度只印 NOT CHECKED。
N_EXPECT = 27
P_SFC = 1000.0
P_TOP = 100.0
LCL_HPA = 895.2
LCL_C = 21.2
LFC_HPA = 747.4
EL_HPA = 163.0
CAPE_J_PER_KG = 2311
CIN_J_PER_KG = -87
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
        f"舉升凝結高度 {LCL_HPA} 百帕、{LCL_C} 度",
        "不是氣塊減環境的異號穿越（穿越在約 747 與 163 百帕）；乾絕熱線與混合比線的交點這四欄重算不了",
    )
    skip(
        f"對流可用位能 {CAPE_J_PER_KG} 焦耳／公斤、對流抑制 {CIN_J_PER_KG} 焦耳／公斤",
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
    回傳 (氣壓, 下方差, 上方差)，由高氣壓排到低氣壓。下方是較靠近地面的那一側。"""
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

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("pressure_hPa,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
chk("欄位", list(rows[0].keys()) == COLS)
chk("27 列", len(rows) == N_EXPECT)
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
if empty or list(rows[0].keys()) != COLS:
    end()
ps = [float(r["pressure_hPa"]) for r in rows]
env = [float(r["temperature_C"]) for r in rows]
tds = [float(r["dewpoint_C"]) for r in rows]
parcel = [float(r["surface_parcel_C"]) for r in rows]
chk(
    "氣壓就是 27 層，從 1000 到 100 百帕且嚴格遞減",
    len(ps) == len(LEVELS) and all(near(a, float(b)) for a, b in zip(ps, LEVELS)) and all(ps[i] > ps[i + 1] for i in range(len(ps) - 1)) and near(ps[0], P_SFC) and near(ps[-1], P_TOP),
)
chk("溫度與露點是有限數，且露點不高於溫度", all(math.isfinite(t) and math.isfinite(d) and d <= t + TOL for t, d in zip(env, tds)))
chk("地面氣塊溫度等於環境溫度", near(parcel[0], env[0]) and near(ps[0], P_SFC), (parcel[0], env[0]))
delta = [tp - te for tp, te in zip(parcel, env)]
zero_p = [p for p, d in zip(ps, delta) if sgn(d) == 0]
# 950 百帕兩邊都是 26.2 度，差是 0，但上下仍是氣塊較冷，不是自由對流高度。
chk("溫差正好為 0 的只有地面與 950 百帕", len(zero_p) == 2 and near(zero_p[0], 1000.0) and near(zero_p[1], 950.0), zero_p)
hits = crossings(ps, delta)
chk("氣塊減環境的異號穿越正好兩次", len(hits) == 2, [(round(h[0], 2), round(h[1], 2), round(h[2], 2)) for h in hits])
if len(hits) != 2:
    end()
chk("較低的那次是從冷到暖", hits[0][1] < 0 < hits[0][2], hits[0])
chk("較高的那次是從暖到冷", hits[1][1] > 0 > hits[1][2], hits[1])
chk("從冷到暖的穿越約 747.4 百帕（記載的自由對流高度）", near(hits[0][0], LFC_HPA, TOL_HPA), hits[0][0])
chk("從暖到冷的穿越約 163.0 百帕（記載的平衡高度）", near(hits[1][0], EL_HPA, TOL_HPA), hits[1][0])
lfc_p, el_p = hits[0][0], hits[1][0]
mid = [d for p, d in zip(ps, delta) if el_p < p < lfc_p]
below = [d for p, d in zip(ps, delta) if p > lfc_p]
above = [d for p, d in zip(ps, delta) if p < el_p]
chk("兩次穿越之間每一層氣塊都比環境暖", len(mid) > 0 and all(d > 0 for d in mid), len(mid))
chk("自由對流高度以下氣塊不比環境暖", len(below) > 0 and all(d <= EPS for d in below))
chk("平衡高度以上氣塊比環境冷", len(above) > 0 and all(d < 0 for d in above))
end()
