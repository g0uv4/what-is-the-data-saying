#!/usr/bin/env python3
"""sample-marey-s1-anatomy-selfcheck.py：檢查虛構樣本資料 sample-marey-s1-anatomy.csv（數字未核）。

資料範圍：2 班車（101 次下行甲→己、102 次上行己→甲），6 個車站（甲 0、乙 6、丙 9、丁 20、戊 24、己 35 公里）。對應課程稿圖 S1。
驗證：每分鐘 1 公里（時速 60 公里）、中途每站停 1 分鐘、丁站 06:22–06:23 的水平段、兩線交叉的時刻與位置（精確值 06:24:30、21.5 公里，落在丁站與戊站之間）。
圖說用「約 06:24:30、21.5 公里」，那是圖面標示用語；這份資料的精確值就是 06:24:30、21.5 公里。
用法：在本資料夾執行  python3 sample-marey-s1-anatomy-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-marey-s1-anatomy.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
時刻一律用 Fraction（精確分數）計算，所以「06:24:30」這類結果是精確值，不是浮點近似。
取整一律四捨五入（逢 5 進位，不是 Python 內建 round 的銀行家捨入）。
"""
CSV_NAME = "sample-marey-s1-anatomy.csv"

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
a, b = stops(rows, "101"), stops(rows, "102")
assert [s[0] for s in a] == [0, 6, 9, 20, 24, 35] and [s[0] for s in b] == [35, 24, 20, 9, 6, 0]
assert a[0][2] == hm("06:00") and b[0][2] == hm("06:10")                       # 101 次 06:00 開；102 次 06:10 從己站開
assert all(v == 60 for v in speeds_kmh(a)) and all(v == 60 for v in speeds_kmh(b))   # 時速 60 公里＝每分鐘 1 公里
assert all(x == 1 for x in dwells(a)) and all(x == 1 for x in dwells(b))        # 中途每站停 1 分鐘
ding = [s for s in a if s[0] == 20][0]
assert (clock(ding[1]), clock(ding[2])) == ("06:22", "06:23")                   # 丁站 06:22–06:23 是水平段
assert clock(a[-1][1]) == "06:39" and clock(b[-1][1]) == "06:49"                # 101 次 06:39 到己站、102 次 06:49 到甲站
ev = meets(poly(a), poly(b))
assert len(ev) == 1 and ev[0][0] == ev[0][1], ev                                # 只交叉一次，而且是單一時刻
t, km = ev[0][0], ev[0][2]
assert clock(t) == "06:24:30" and km == Fr(43, 2)                               # 精確：06:24:30、21.5 公里
assert where(km) == "丁站與戊站之間"                                              # 20 < 21.5 < 24：不在任何車站
# 手算對照：101 次在丁站 06:23（第 383 分鐘）離開，位置 = 20 + (t−383)；102 次在戊站 06:22（第 382 分鐘）離開，位置 = 24 − (t−382)；
#   兩式相等 → t = 384.5 分鐘 = 06:24:30，位置 = 21.5 公里。
assert 20 + (t - 383) == 24 - (t - 382) == km
print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）；交叉 =", clock(t), f"{float(km)} 公里", where(km))
