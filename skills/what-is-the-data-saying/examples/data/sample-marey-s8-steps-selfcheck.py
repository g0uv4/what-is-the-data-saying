#!/usr/bin/env python3
"""sample-marey-s8-steps-selfcheck.py：檢查虛構樣本資料 sample-marey-s8-steps.csv（數字未核）。

資料範圍：製作步驟範例，只用甲到丁四站（0、6、9、20 公里）；501 次下行（10:00 從甲站開、10:22 到丁站）、502 次上行（10:05 從丁站開、10:27 到甲站）。對應課程稿圖 S8。
驗證：時刻表欄位（起點只有離站、終點只有到站，CSV 以空白表示，圖上以「—」表示）；兩線交叉的精確位置（10:13:30、11.5 公里，丙站與丁站之間）。
圖說的「約」是圖面標示用語；這份資料的精確值就是 10:13:30、11.5 公里。
用法：在本資料夾執行  python3 sample-marey-s8-steps-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-marey-s8-steps.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
時刻一律用 Fraction（精確分數）計算，所以「06:24:30」這類結果是精確值，不是浮點近似。
取整一律四捨五入（逢 5 進位，不是 Python 內建 round 的銀行家捨入）。
"""
CSV_NAME = "sample-marey-s8-steps.csv"

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
a, b = stops(rows, "501"), stops(rows, "502")
assert [s[0] for s in a] == [0, 6, 9, 20] and [s[0] for s in b] == [20, 9, 6, 0]
assert [s[3] for s in a] == ["甲站", "乙站", "丙站", "丁站"]
assert a[0][1] is None and a[-1][2] is None and b[0][1] is None and b[-1][2] is None       # 起點沒有到站時刻、終點沒有離站時刻
assert [(clock(s[1]) if s[1] is not None else "—", clock(s[2]) if s[2] is not None else "—") for s in a] == [("—", "10:00"), ("10:06", "10:07"), ("10:10", "10:11"), ("10:22", "—")]
assert [(clock(s[1]) if s[1] is not None else "—", clock(s[2]) if s[2] is not None else "—") for s in b] == [("—", "10:05"), ("10:16", "10:17"), ("10:20", "10:21"), ("10:27", "—")]
ev = meets(poly(a), poly(b))
assert len(ev) == 1 and ev[0][0] == ev[0][1]
t, km = ev[0][0], ev[0][2]
assert clock(t) == "10:13:30" and km == Fr(23, 2) and where(km, {0: "甲站", 6: "乙站", 9: "丙站", 20: "丁站"}) == "丙站與丁站之間"
# 手算對照：501 次 10:11（第 611 分鐘）離開丙站（9 公里）→ 位置 = 9 + (t−611)；502 次 10:05（第 605 分鐘）離開丁站（20 公里）→ 位置 = 20 − (t−605)；相等 → t = 613.5 分鐘 = 10:13:30，位置 = 11.5 公里。
assert 9 + (t - 611) == 20 - (t - 605) == km
print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）；交叉 =", clock(t), f"{float(km)} 公里")
