#!/usr/bin/env python3
"""sample-marey-s5-bus-bunching-selfcheck.py：檢查虛構樣本資料 sample-marey-s5-bus-bunching.csv（數字未核）。

資料範圍：5 輛公車、13 個站牌（第 0–12 站，每站相隔 1 公里），表定班距 8 分鐘；3 號車晚 3 分鐘出發（17:19），其餘準時（1 號 17:00、2 號 17:08、4 號 17:24、5 號 17:32）。
到離站時刻從 17:00 起算（arrive_min／depart_min 是 00:00 起算的分鐘，保留 6 位小數）。對應課程稿圖 S5。
模型規則（驗證時用精確分數重新模擬一次，與 CSV 逐格相符，誤差 < 0.000001 分鐘）：站間行駛 2 分鐘；
停站時間 = max(0.3, 0.08 × g)，g ＝本車到站時刻減前車在同一站的離站時刻（1 號車沒有前車，g 用表定班距 8 分鐘）；不准超車：本車離站時刻至少比前車在同站的離站晚 0.2 分鐘。
注意：下面說的「3、4 號車相隔」是兩車到站時刻的差（圖上兩條線的水平距離），與模型裡的 g 定義不同（g 用前車離站時刻）。
驗證：3、4 號車相隔 5 → 0.2 分鐘，第 7 站首次不到 1 分鐘（0.81 分）；2→3 號車 11 → 16.13 分鐘（逐站拉大）；4→5 號車 8 → 9.76 分鐘（起點對終點；中途第 8 站最大 11.18 分，不是一路拉大）；0.2 是模型規定的最小跟車間隔。
用法：在本資料夾執行  python3 sample-marey-s5-bus-bunching-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-marey-s5-bus-bunching.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
時刻一律用 Fraction（精確分數）計算，所以「06:24:30」這類結果是精確值，不是浮點近似。
取整一律四捨五入（逢 5 進位，不是 Python 內建 round 的銀行家捨入）。
"""
CSV_NAME = "sample-marey-s5-bus-bunching.csv"

import csv, sys
from fractions import Fraction as Fr
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

path = Path(__file__).resolve().parent / (sys.argv[1] if len(sys.argv) > 1 else CSV_NAME)   # 指定檔名，不用 glob
STATUS = "虛構資料，數字未核"

def half_up(x, nd=0):
    """四捨五入（逢 5 進位）；Python 內建 round() 是「銀行家捨入」，不是四捨五入。x 可以是 Fraction。"""
    d = Decimal(x.numerator) / Decimal(x.denominator) if isinstance(x, Fr) else Decimal(repr(float(x)))
    return float(d.quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))

def hm(s):
    """'HH:MM' 或 'HH:MM:SS' → 從 00:00 起算的分鐘（Fraction，精確）。"""
    p = s.split(":"); return Fr(int(p[0]) * 60 + int(p[1])) + (Fr(int(p[2]), 60) if len(p) == 3 else 0)

def clock(m):
    sec = int(Fr(m) * 60); h, r = divmod(sec, 3600); mi, s = divmod(r, 60)
    return f"{h:02d}:{mi:02d}:{s:02d}" if s else f"{h:02d}:{mi:02d}"

def read_rows(head):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
    assert list(rows[0].keys()) == head, list(rows[0].keys())
    assert all(r["data_status"] == STATUS for r in rows)
    return rows

def stops(rows, train):
    """某班車的停靠站，依 seq 排序：[(km, arrive|None, depart|None, station)]（時刻是 Fraction 分鐘）。"""
    out = []
    for r in sorted((r for r in rows if r["train"] == train), key=lambda r: int(r["seq"])):
        out.append((Fr(r["km"]), hm(r["arrive"]) if r["arrive"] else None, hm(r["depart"]) if r["depart"] else None, r["station"]))
    assert out, train
    return out

def poly(st):
    """停靠站 → 折線頂點 [(時刻, 公里)]：到站點、離站點（水平段＝停站）。"""
    pts = []
    for km, a, d, _ in st:
        if a is not None: pts.append((a, km))
        if d is not None: pts.append((d, km))
    assert all(pts[i][0] <= pts[i + 1][0] for i in range(len(pts) - 1)), "時刻必須不倒退"
    return pts

def pos(P, t):
    if t < P[0][0] or t > P[-1][0]: return None
    for (t0, k0), (t1, k1) in zip(P, P[1:]):
        if t0 <= t <= t1: return k0 if t1 == t0 else k0 + (k1 - k0) * (t - t0) / (t1 - t0)

def meets(PA, PB):
    """兩班車位置重合的所有時刻／時段（精確算法：折線只在頂點轉折，所以逐段檢查位置差的正負號）。
    回傳 [(t0, t1, km)]：t0＝t1 是單一時刻（交叉或接觸），t0<t1 是兩車同時停在同一站的時段。"""
    lo, hi = max(PA[0][0], PB[0][0]), min(PA[-1][0], PB[-1][0])
    if lo > hi: return []
    ts = sorted({t for t, _ in PA + PB if lo <= t <= hi})
    d = [pos(PA, t) - pos(PB, t) for t in ts]
    iv = []
    for i in range(len(ts) - 1):
        d0, d1 = d[i], d[i + 1]
        if d0 == 0 and d1 == 0: iv.append([ts[i], ts[i + 1]])
        elif d0 == 0: iv.append([ts[i], ts[i]])
        elif d1 == 0: iv.append([ts[i + 1], ts[i + 1]])
        elif d0 * d1 < 0:
            t = ts[i] + (ts[i + 1] - ts[i]) * d0 / (d0 - d1); iv.append([t, t])
    if len(ts) == 1 and d[0] == 0: iv.append([ts[0], ts[0]])
    iv.sort(); merged = []
    for a, b in iv:
        if merged and a <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], b)
        else: merged.append([a, b])
    return [(a, b, pos(PA, a)) for a, b in merged]

KMS = {0: "甲站", 6: "乙站", 9: "丙站", 20: "丁站", 24: "戊站", 35: "己站"}
def where(km, kms=KMS):
    """km 剛好是車站 → '在X站'；否則 → 'X站與Y站之間'。"""
    km = Fr(km); ks = sorted(kms)
    if km in ks: return "在" + kms[int(km)]
    for a, b in zip(ks, ks[1:]):
        if a < km < b: return f"{kms[a]}與{kms[b]}之間"
    raise AssertionError(km)

def speeds_kmh(st):
    """每個行駛區間的平均時速（公里／小時）：公里數 ÷ （下一站到站 − 本站離站）× 60。"""
    return [abs(b[0] - a[0]) / (b[1] - a[2]) * 60 for a, b in zip(st, st[1:])]

def dwells(st):
    return [d - a for _, a, d, _ in st[1:-1]]

rows = read_rows(["group", "train", "seq", "station", "km", "arrive", "depart", "arrive_min", "depart_min", "data_status"])
N_BUS, N_STOP = 5, 13
BASE = hm("17:00")
M = {(int(r["train"][3:]) - 1, int(r["seq"])): (Fr(r["arrive_min"]), Fr(r["depart_min"])) for r in rows}
assert len(M) == N_BUS * N_STOP == len(rows) and all(r["km"] == r["seq"] for r in rows)   # 每站相隔 1 公里
# 以精確分數重新模擬，與 CSV 比對
RUN, K, MIN_DWELL, FOLLOW, HEADWAY, LATE = Fr(2), Fr(8, 100), Fr(3, 10), Fr(1, 5), Fr(8), Fr(3)
arr, dep = {}, {}
for b in range(N_BUS):
    t = BASE + b * HEADWAY + (LATE if b == 2 else 0)                               # 3 號車（b＝2）晚 3 分鐘
    for s in range(N_STOP):
        if s > 0: t = dep[b, s - 1] + RUN
        arr[b, s] = t
        g = (t - dep[b - 1, s]) if b > 0 else HEADWAY
        d = t + max(MIN_DWELL, K * g)
        if b > 0: d = max(d, dep[b - 1, s] + FOLLOW)
        dep[b, s] = d
for k in arr:
    assert abs(float(arr[k]) - float(M[k][0])) < 1e-6 and abs(float(dep[k]) - float(M[k][1])) < 1e-6, k
assert [clock(arr[b, 0]) for b in range(N_BUS)] == ["17:00", "17:08", "17:19", "17:24", "17:32"]   # 3 號車 17:19、4 號車 17:24
# 不超車：每個站牌，後車都比前車晚到、晚離
assert all(arr[b, s] > arr[b - 1, s] and dep[b, s] > dep[b - 1, s] for b in range(1, N_BUS) for s in range(N_STOP))
# 3、4 號車（b＝2、3）相隔＝到站時刻差
gap34 = [arr[3, s] - arr[2, s] for s in range(N_STOP)]
assert gap34[0] == 5 and half_up(gap34[-1], 2) == 0.2
assert [half_up(g, 2) for g in gap34[:9]] == [5.0, 4.5, 3.95, 3.37, 2.77, 2.15, 1.5, 0.81, 0.2]
first_lt1 = next(s for s, g in enumerate(gap34) if g < 1)
assert first_lt1 == 7 and half_up(gap34[7], 2) == 0.81                              # 第 7 站首次不到 1 分鐘（0.81 分）
assert all(gap34[s] > gap34[s + 1] for s in range(8)) and all(float(g) - 0.2 < 1e-9 for g in gap34[8:])   # 前 8 站逐站縮小，第 8 站起固定 0.2
# 0.2 分鐘是「最小跟車間隔」規則造成的：第 8–12 站 4 號車離站時刻正好比 3 號車晚 0.2 分鐘
assert all(dep[3, s] - dep[2, s] == FOLLOW for s in range(8, N_STOP))
# 2→3 號車：11 → 16.13；4→5 號車：8 → 9.76（取兩位小數，四捨五入）
g23 = [arr[2, s] - arr[1, s] for s in range(N_STOP)]; g45 = [arr[4, s] - arr[3, s] for s in range(N_STOP)]
assert g23[0] == 11 and half_up(g23[-1], 2) == 16.13 and half_up(g23[-1], 1) == 16.1
assert g45[0] == 8 and half_up(g45[-1], 2) == 9.76 and half_up(g45[-1], 1) == 9.8
assert all(a < b for a, b in zip(g23, g23[1:]))                                    # 2→3 號車的間隔逐站拉大
# 4→5 號車：起點 8 → 終點 9.76 是「起點對終點」的比較；中途並非一路拉大——第 8 站最大（11.18 分），之後回縮到 9.76
assert max(g45) == g45[8] and half_up(g45[8], 2) == 11.18 and g45[0] < g45[8] and g45[12] < g45[8]
# 最後一輛車（5 號）到第 12 站的時刻（圖的橫軸終點附近）
assert clock(arr[4, 12]) == "18:04:48"                                              # 5 號車 18:04:48 到第 12 站
print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）；3-4 號車相隔", [half_up(g, 2) for g in gap34])
