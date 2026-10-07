#!/usr/bin/env python3
"""sample-marey-s2-local-vs-express-selfcheck.py：檢查虛構樣本資料 sample-marey-s2-local-vs-express.csv（數字未核）。

資料範圍：普通車 201 次（07:00 開，時速 60 公里，每站停 1 分鐘，丁站待避 3 分鐘）、快車 301 次（07:14 從甲站開，時速 120 公里，不停站）、
對照線 201-nowait（普通車若不待避，丁站也只停 1 分鐘）。對應課程稿圖 S2。
驗證：快車超越待避普通車的時刻與地點（精確值 07:24:00，丁站，20 公里）；若不待避，快車追上普通車的時刻與地點（07:25:00，22 公里，丁站與戊站之間，不是車站）。
用法：在本資料夾執行  python3 sample-marey-s2-local-vs-express-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-marey-s2-local-vs-express.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
時刻一律用 Fraction（精確分數）計算，所以「06:24:30」這類結果是精確值，不是浮點近似。
取整一律四捨五入（逢 5 進位，不是 Python 內建 round 的銀行家捨入）。
"""
CSV_NAME = "sample-marey-s2-local-vs-express.csv"

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
loc, exp, nw = stops(rows, "201"), stops(rows, "301"), stops(rows, "201-nowait")
assert loc[0][2] == hm("07:00") and exp[0][2] == hm("07:14")
assert [s[0] for s in exp] == [0, 35] and clock(exp[1][1]) == "07:31:30"          # 快車只有起訖兩點，07:31:30 到己站
assert speeds_kmh(exp) == [120]                                                   # 35 公里 ÷ 17.5 分鐘 = 時速 120 公里
assert all(v == 60 for v in speeds_kmh(loc)) and all(v == 60 for v in speeds_kmh(nw))
ding = [s for s in loc if s[0] == 20][0]
assert (clock(ding[1]), clock(ding[2])) == ("07:22", "07:25") and ding[2] - ding[1] == 3   # 丁站待避 3 分鐘
assert dwells(loc) == [1, 1, 3, 1] and dwells(nw) == [1, 1, 1, 1]                 # 其餘各站都停 1 分鐘
assert clock(loc[-1][1]) == "07:41" and clock(nw[-1][1]) == "07:39"
# 1. 超車：快車線與（待避的）普通車線只交叉一次，在丁站（20 公里）07:24:00，正好在普通車 07:22–07:25 的待避時段內
ev = meets(poly(exp), poly(loc))
assert len(ev) == 1 and ev[0][0] == ev[0][1]
t, km = ev[0][0], ev[0][2]
assert clock(t) == "07:24" and km == 20 and where(km) == "在丁站" and ding[1] < t < ding[2]
# 2. 若普通車不待避：快車線與對照線交叉一次，在 07:25:00、22 公里，丁站與戊站之間（不是車站，所以現實中不能這樣追上）
ev2 = meets(poly(exp), poly(nw))
assert len(ev2) == 1 and ev2[0][0] == ev2[0][1]
t2, km2 = ev2[0][0], ev2[0][2]
assert clock(t2) == "07:25" and km2 == 22 and where(km2) == "丁站與戊站之間"
# 3. 快車比普通車（有待避）早 9.5 分鐘到己站：07:31:30 對 07:41
assert loc[-1][1] - exp[-1][1] == Fr(19, 2)
print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）；超車", clock(t), where(km), "；不待避追上", clock(t2), f"{float(km2)} 公里", where(km2))
