#!/usr/bin/env python3
"""sample-marey-s7-too-dense-zoom-selfcheck.py：檢查虛構樣本資料 sample-marey-s7-too-dense-zoom.csv（數字未核）。

資料範圍：全天雙向 284 班（每班一列，不展開每站）。普通車（local）每站停、6 站，每 10 分鐘一班雙向各一：下行 05:00–23:00（含兩端）共 109 班，上行晚 5 分鐘（05:05–23:05）共 109 班，合計 218 班；
快車（express）不停站、只有起訖 2 點，每 30 分鐘一班雙向各一：下行在整點／半點後 3 分鐘出發（06:03–22:03）共 33 班，上行 06:08–22:08 共 33 班，合計 66 班。對應課程稿圖 S7。
驗證：總數 284＝普通 218＋快車 66；放大圖（07:00–09:00 從甲站出發的下行車，不含 09:00 整）共 16 班＝普通 12（07:00、07:10…08:50）＋快車 4（07:03、07:33、08:03、08:33）；
放大圖班次占全天 16／284 ＝ 5.6%（四捨五入到小數第一位）。
用法：在本資料夾執行  python3 sample-marey-s7-too-dense-zoom-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-marey-s7-too-dense-zoom.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
時刻一律用 Fraction（精確分數）計算，所以「06:24:30」這類結果是精確值，不是浮點近似。
取整一律四捨五入（逢 5 進位，不是 Python 內建 round 的銀行家捨入）。
"""
CSV_NAME = "sample-marey-s7-too-dense-zoom.csv"

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

rows = read_rows(["group", "train", "direction", "kind", "stops", "first_depart_min", "last_arrive_min", "in_zoom", "data_status"])
R = [dict(r, fd=Fr(r["first_depart_min"]), la=Fr(r["last_arrive_min"]), z=int(r["in_zoom"])) for r in rows]
assert len(R) == 284 and len({r["train"] for r in R}) == 284
loc = [r for r in R if r["kind"] == "local"]; exp = [r for r in R if r["kind"] == "express"]
assert (len(loc), len(exp)) == (218, 66) and all(r["stops"] == "6" for r in loc) and all(r["stops"] == "2" for r in exp)
dn_l = [r for r in loc if r["direction"] == "down"]; up_l = [r for r in loc if r["direction"] == "up"]
dn_e = [r for r in exp if r["direction"] == "down"]; up_e = [r for r in exp if r["direction"] == "up"]
assert (len(dn_l), len(up_l), len(dn_e), len(up_e)) == (109, 109, 33, 33)
assert sorted(r["fd"] for r in dn_l) == [Fr(t) for t in range(300, 1381, 10)]    # 05:00、05:10 … 23:00
assert sorted(r["fd"] for r in up_l) == [Fr(t + 5) for t in range(300, 1381, 10)]                  # 晚 5 分鐘
assert sorted(r["fd"] for r in dn_e) == [Fr(t + 3) for t in range(360, 1321, 30)]                  # 06:03 … 22:03
assert sorted(r["fd"] for r in up_e) == [Fr(t + 8) for t in range(360, 1321, 30)]                  # 06:08 … 22:08
assert all(r["la"] - r["fd"] == 39 for r in loc) and all(r["la"] - r["fd"] == Fr(35, 2) for r in exp)   # 普通車全程 39 分鐘；快車 17.5 分鐘
# 放大圖：下行、從甲站出發的時刻在 07:00（含）到 09:00（不含）之間
zoom = [r for r in R if r["z"] == 1]
assert len(zoom) == 16 and all(r["direction"] == "down" for r in zoom)
assert zoom == [r for r in R if r["direction"] == "down" and hm("07:00") <= r["fd"] < hm("09:00")]
zl = [r for r in zoom if r["kind"] == "local"]; ze = [r for r in zoom if r["kind"] == "express"]
assert (len(zl), len(ze)) == (12, 4)
assert [clock(r["fd"]) for r in zl] == ["07:00", "07:10", "07:20", "07:30", "07:40", "07:50", "08:00", "08:10", "08:20", "08:30", "08:40", "08:50"]
assert [clock(r["fd"]) for r in ze] == ["07:03", "07:33", "08:03", "08:33"]
assert half_up(Fr(16, 284) * 100, 1) == 5.6                                                         # 16／284 = 5.6%
# 密度：同一分鐘最多有幾班車在線上（從出發到抵達之間），只是補充說明，不是圖說的數字
online = max(sum(1 for r in R if r["fd"] <= m <= r["la"]) for m in range(0, 1441))
print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）；284 班 =", len(loc), "普通 +", len(exp), "快車；放大圖", len(zoom), "班；同時在線最多", online, "班")
