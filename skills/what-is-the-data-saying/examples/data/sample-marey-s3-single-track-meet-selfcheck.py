#!/usr/bin/env python3
"""sample-marey-s3-single-track-meet-selfcheck.py：檢查虛構樣本資料 sample-marey-s3-single-track-meet.csv（數字未核）。

資料範圍：下行 401 次（甲→己）、上行 402 次（己→甲，在戊站等 9 分鐘）、對照線 402-nowait（上行車不等就開，只有己、戊、丁三站）。
可交會的車站（有會車設備）：乙、丙、丁、戊（圖面右側標「◎ 可交會」）。對應課程稿圖 S3。
驗證：兩車實際線的會車點與時段（兩車同時停在戊站 08:27–08:28，只有這一處重合；站間完全沒有交叉）；
若上行車不等就開，兩線在 08:23:30、20.5 公里（丁站與戊站之間，單線區間）交叉＝正面衝突。圖說的「約」是圖面標示用語；這份資料的精確值就是 08:23:30、20.5 公里。
用法：在本資料夾執行  python3 sample-marey-s3-single-track-meet-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-marey-s3-single-track-meet.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
時刻一律用 Fraction（精確分數）計算，所以「06:24:30」這類結果是精確值，不是浮點近似。
取整一律四捨五入（逢 5 進位，不是 Python 內建 round 的銀行家捨入）。
"""
CSV_NAME = "sample-marey-s3-single-track-meet.csv"

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
dn, up, nw = stops(rows, "401"), stops(rows, "402"), stops(rows, "402-nowait")
MEET_STATIONS = {6, 9, 20, 24}                                                  # 乙、丙、丁、戊：有會車設備
assert dn[0][2] == hm("08:00") and up[0][2] == hm("08:08") and [s[0] for s in up] == [35, 24, 20, 9, 6, 0]
wu_dn = [s for s in dn if s[0] == 24][0]; wu_up = [s for s in up if s[0] == 24][0]
assert (clock(wu_dn[1]), clock(wu_dn[2])) == ("08:27", "08:28")                 # 401 次 08:27 到戊站、08:28 開
assert (clock(wu_up[1]), clock(wu_up[2])) == ("08:19", "08:28") and wu_up[2] - wu_up[1] == 9   # 402 次 08:19 到戊站，等 9 分鐘到 08:28
# 1. 實際線：兩車只有一處重合——同時停在戊站 08:27–08:28（交會），沒有任何站間交叉
ev = meets(poly(dn), poly(up))
assert len(ev) == 1, ev
t0, t1, km = ev[0]
assert (clock(t0), clock(t1), km) == ("08:27", "08:28", 24) and 24 in MEET_STATIONS and where(km) == "在戊站"
# 2. 位置差（401 次減 402 次）的正負號：08:27 以前恆為負（401 次還沒到戊站），08:28 以後恆為正（兩車已錯開）→ 只在戊站換位
P1, P2 = poly(dn), poly(up)
ts = sorted({t for t, _ in P1 + P2 if max(P1[0][0], P2[0][0]) <= t <= min(P1[-1][0], P2[-1][0])})
sg = [(t, pos(P1, t) - pos(P2, t)) for t in ts]
assert all(d < 0 for t, d in sg if t < t0) and all(d > 0 for t, d in sg if t > t1)
# 3. 對照：上行車 08:19 到戊站後不等、08:20 就開 → 與 401 次在丁站與戊站之間交叉（單線區間，兩車會迎面相撞）
evn = meets(poly(dn), poly(nw))
assert len(evn) == 1 and evn[0][0] == evn[0][1]
tn, kn = evn[0][0], evn[0][2]
assert clock(tn) == "08:23:30" and kn == Fr(41, 2) and where(kn) == "丁站與戊站之間" and kn not in MEET_STATIONS
assert [clock(s[2]) if s[2] is not None else None for s in nw] == ["08:08", "08:20", None] and clock(nw[2][1]) == "08:24"
# 手算對照：401 次 08:23 離開丁站（20 公里）→ 位置 = 20 + (t−503)；對照線 08:20（第 500 分鐘）離開戊站（24 公里）→ 位置 = 24 − (t−500)；相等 → t = 503.5 分鐘 = 08:23:30，位置 = 20.5 公里。
assert 20 + (tn - 503) == 24 - (tn - 500) == kn
print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）；會車", clock(t0), "–", clock(t1), where(km), "；若不等", clock(tn), f"{float(kn)} 公里", where(kn))
