#!/usr/bin/env python3
"""sample-marey-s4-plan-vs-actual-selfcheck.py：檢查虛構樣本資料 sample-marey-s4-plan-vs-actual.csv（數字未核）。

資料範圍：同一班車（07:00 從甲站開）的計畫線 plan 與實際線 actual，6 個車站。對應課程稿圖 S4。
驗證：各站到站晚幾分鐘（乙 1、丙 2、丁 7、戊 7、己 7）；各站離站晚幾分鐘；丙站停 3 分鐘（計畫 1 分）；丙到丁實際行駛 14 分鐘（計畫 11 分）；
這 7 分鐘誤點是怎麼累積的：乙站前行駛 +1、乙站停站 +1、丙站停站 +2、丙到丁行駛 +3，合計 +7，其中丙站與丙到丁 +5（7 分鐘中的 5 分鐘），之後維持晚 7 分。
「晚幾分鐘」都是整數分鐘，沒有取整問題。
用法：在本資料夾執行  python3 sample-marey-s4-plan-vs-actual-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-marey-s4-plan-vs-actual.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
時刻一律用 Fraction（精確分數）計算，所以「06:24:30」這類結果是精確值，不是浮點近似。
取整一律四捨五入（逢 5 進位，不是 Python 內建 round 的銀行家捨入）。
"""
CSV_NAME = "sample-marey-s4-plan-vs-actual.csv"

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
plan, act = stops(rows, "plan"), stops(rows, "actual")
assert [s[0] for s in plan] == [s[0] for s in act] == [0, 6, 9, 20, 24, 35]
assert plan[0][2] == act[0][2] == hm("07:00") and clock(plan[-1][1]) == "07:39" and clock(act[-1][1]) == "07:46"
arr_delay = [a[1] - p[1] for p, a in zip(plan[1:], act[1:])]                      # 乙、丙、丁、戊、己的到站晚點
dep_delay = [a[2] - p[2] for p, a in zip(plan[1:-1], act[1:-1])]                  # 乙、丙、丁、戊的離站晚點
assert arr_delay == [1, 2, 7, 7, 7] and dep_delay == [2, 4, 7, 7]
# 丙站停 3 分鐘（計畫 1 分）；丙到丁實際開 14 分鐘（計畫 11 分），實線在這段比虛線平（斜率較小）
assert act[2][2] - act[2][1] == 3 and plan[2][2] - plan[2][1] == 1
assert act[3][1] - act[2][2] == 14 and plan[3][1] - plan[2][2] == 11
sl = lambda st: (st[3][0] - st[2][0]) / (st[3][1] - st[2][2])                      # 丙→丁的斜率（公里／分鐘）
assert sl(act) == Fr(11, 14) < sl(plan) == 1
# 誤點的組成（實際減計畫）：每個行駛區間與每次停站各增加幾分鐘，加起來剛好是終點的 7 分鐘
comp = []
for i in range(1, 6):
    comp.append(("行駛", i, (act[i][1] - act[i - 1][2]) - (plan[i][1] - plan[i - 1][2])))
    if i < 5: comp.append(("停站", i, (act[i][2] - act[i][1]) - (plan[i][2] - plan[i][1])))
assert sum(c for _, _, c in comp) == 7 == arr_delay[-1]
inc = {(k, i): c for k, i, c in comp if c != 0}
assert inc == {("行駛", 1): 1, ("停站", 1): 1, ("停站", 2): 2, ("行駛", 3): 3}      # i＝站序：行駛 1＝甲→乙；停站 1＝乙站；停站 2＝丙站；行駛 3＝丙→丁
assert inc[("停站", 2)] + inc[("行駛", 3)] == 5                                      # 丙站停站 +2 與丙到丁行駛 +3，共 7 分鐘中的 5 分鐘
print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）；到站晚分鐘", [int(x) for x in arr_delay], "；誤點組成", {k: int(v) for k, v in inc.items()})
