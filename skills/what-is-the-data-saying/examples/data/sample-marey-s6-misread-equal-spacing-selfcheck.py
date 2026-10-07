#!/usr/bin/env python3
"""sample-marey-s6-misread-equal-spacing-selfcheck.py：檢查虛構樣本資料 sample-marey-s6-misread-equal-spacing.csv（數字未核）。

資料範圍：同一班車（09:00 從甲站開）、6 個車站（甲 0、乙 2、丙 4、丁 18、戊 20、己 30 公里），每站停 1 分鐘，每段時速 60 公里。對應課程稿圖 S6。
驗證：各段距離 2、2、14、2、10 公里＝行駛 2、2、14、2、10 分鐘，每段時速都是 60 公里；
把六站等距排列（每站間隔 1 格）時，圖上的視覺斜率＝1 格 ÷ 行駛分鐘，丙到丁是 1／14 格每分鐘，是五段中最平的（其他 2 公里段是 1／2，也就是 7 倍；戊到己是 1／10），
讀者會誤以為丙到丁最慢；依實際距離排列時五段斜率都是 1 公里每分鐘。
用法：在本資料夾執行  python3 sample-marey-s6-misread-equal-spacing-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-marey-s6-misread-equal-spacing.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
時刻一律用 Fraction（精確分數）計算，所以「06:24:30」這類結果是精確值，不是浮點近似。
取整一律四捨五入（逢 5 進位，不是 Python 內建 round 的銀行家捨入）。
"""
CSV_NAME = "sample-marey-s6-misread-equal-spacing.csv"

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
tr = stops(rows, "601")
assert [s[0] for s in tr] == [0, 2, 4, 18, 20, 30] and [s[3] for s in tr] == ["甲站", "乙站", "丙站", "丁站", "戊站", "己站"]
assert tr[0][2] == hm("09:00") and all(x == 1 for x in dwells(tr)) and clock(tr[-1][1]) == "09:34"
seg_km = [b[0] - a[0] for a, b in zip(tr, tr[1:])]; seg_min = [b[1] - a[2] for a, b in zip(tr, tr[1:])]
assert seg_km == [2, 2, 14, 2, 10] and seg_min == [2, 2, 14, 2, 10]
assert speeds_kmh(tr) == [60] * 5                                                    # 每段都是時速 60 公里
real_slope = [k / m for k, m in zip(seg_km, seg_min)]
assert real_slope == [1] * 5                                                         # 依實際距離排：每段都是 1 公里／分鐘
eq_slope = [Fr(1) / m for m in seg_min]                                              # 等距排列：每段都只佔 1 格
assert eq_slope == [Fr(1, 2), Fr(1, 2), Fr(1, 14), Fr(1, 2), Fr(1, 10)]
flat = min(range(5), key=lambda i: eq_slope[i])
assert flat == 2 and (tr[flat][3], tr[flat + 1][3]) == ("丙站", "丁站")                # 最平的是丙到丁
assert eq_slope[0] / eq_slope[2] == 7 and eq_slope[4] / eq_slope[2] == Fr(7, 5)       # 2 公里段的視覺斜率是丙到丁的 7 倍；戊到己（10 公里）是 1.4 倍
print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）；等距排列最平的一段：", tr[flat][3], "→", tr[flat + 1][3])
