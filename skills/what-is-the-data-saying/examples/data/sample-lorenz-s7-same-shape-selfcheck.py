#!/usr/bin/env python3
"""sample-lorenz-s7-same-shape-selfcheck.py：檢查虛構樣本資料 sample-lorenz-s7-same-shape.csv（數字未核）。

用法：在本資料夾執行  python3 sample-lorenz-s7-same-shape-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-lorenz-s7-same-shape.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
資料範圍：2 組各 10 戶（甲、乙，由小到大排序，各合計 100）。對應課程稿圖 S7（Liora 重畫版：基尼係數相同、曲線形狀不同）。
基尼係數兩種算法（10 戶資料）：折線下面積法 G＝1−2×曲線下面積（梯形）；小樣本修正版＝G×n／(n−1)，n 是單位數。
取整一律四捨五入（逢 5 進位，不是 Python 內建 round 的銀行家捨入）。
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CSV_NAME = "sample-lorenz-s7-same-shape.csv"                                   # 指定檔名，不用 glob
path = Path(__file__).resolve().parent / (sys.argv[1] if len(sys.argv) > 1 else CSV_NAME)

def half_up(x, nd=2):
    """四捨五入（逢 5 進位）；Python 內建 round() 是「銀行家捨入」，不是四捨五入。"""
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))

def close(a, b, tol=1e-9):
    return abs(a - b) <= tol

with open(path, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
assert list(rows[0].keys()) == ["group", "label", "rank", "value", "cum_units", "cum_value_share", "data_status"]
assert all(r["data_status"] == "虛構資料，數字未核" for r in rows)

def grp(name):
    """取出某一組（依 CSV 內的順序）：回傳 [(value, cum_units, cum_value_share), ...]"""
    return [(float(r["value"]), float(r["cum_units"]) if r["cum_units"] else None,
             float(r["cum_value_share"]) if r["cum_value_share"] else None) for r in rows if r["group"] == name]

def lorenz_check(name):
    """由 value 重算累計；與 CSV 的 cum_units、cum_value_share 逐列相符；回傳 (values, cum_share 含 0 起點)。"""
    g = grp(name); v = [a for a, _, _ in g]; n = len(v); tot = sum(v)
    assert v == sorted(v), name + " 的 value 必須由小到大排序"
    cum = 0.0; shares = [0.0]
    for i, (a, cu, cs) in enumerate(g):
        cum += a; shares.append(cum / tot)
        assert close(cu, (i + 1) / n, 5e-7) and close(cs, cum / tot, 5e-7), (name, i + 1)
    return v, shares

def gini(shares):
    """折線下面積法：梯形面積合計（橫軸等距 1/n），G＝1−2×面積。"""
    n = len(shares) - 1
    area = sum((shares[i] + shares[i + 1]) / 2 for i in range(n)) / n
    return 1 - 2 * area

def gini_mean_difference(v):
    """離散公式 G＝2Σ(i×y_i)／(n×Σy)−(n+1)／n（y 由小到大，i 從 1 起）；應與梯形算法完全相同。"""
    n = len(v); return 2 * sum((i + 1) * a for i, a in enumerate(v)) / (n * sum(v)) - (n + 1) / n

def corrected(g, n):
    return g * n / (n - 1)

va, sa = lorenz_check("甲"); vb, sb = lorenz_check("乙")
assert va == [3, 4, 5, 6, 7, 9, 11, 14, 18, 23] and vb == [4, 4, 5, 7, 7, 8, 10, 11, 16, 28]
assert sum(va) == sum(vb) == 100 and len(va) == len(vb) == 10
# 1. 基尼係數（折線下面積法）兩組都是 0.340（精確值相同），四捨五入 0.34；小樣本修正版兩組都是 0.378，四捨五入 0.38。
ga, gb = gini(sa), gini(sb)
assert close(ga, gb) and close(ga, 0.34) and half_up(ga) == half_up(gb) == 0.34
assert close(ga, gini_mean_difference(va)) and close(gb, gini_mean_difference(vb))
assert half_up(corrected(ga, 10)) == half_up(corrected(gb, 10)) == 0.38
# 2. 曲線交叉：累計單位 10%–60%（第 1–6 戶）乙高於甲；70%（第 7 戶）兩者相同（都累計 45%）；80%–90%（第 8–9 戶）甲高於乙。
#    所以交叉點在 70%，落在 50%～80% 之間（50% 時乙 27% 高於甲 25%，80% 時甲 59% 高於乙 56%）。
d = [round(sa[i] - sb[i], 9) for i in range(11)]
assert all(x < 0 for x in d[1:7]) and d[7] == 0 and all(x > 0 for x in d[8:10]) and d[0] == d[10] == 0
assert half_up(sa[5] * 100, 0) == 25 and half_up(sb[5] * 100, 0) == 27          # 最貧 50%（第 1–5 戶）：甲 25%、乙 27%
assert half_up(sa[7] * 100, 0) == half_up(sb[7] * 100, 0) == 45                 # 70%（第 1–7 戶）：都是 45%
assert half_up(sa[8] * 100, 0) == 59 and half_up(sb[8] * 100, 0) == 56          # 80%（第 1–8 戶）：甲 59%、乙 56%
# 3. 最富 10%（第 10 戶）占比：甲 23%、乙 28%（＝100% 減去前 9 戶累計 77%、72%）。
assert half_up((1 - sa[9]) * 100, 0) == 23 and half_up((1 - sb[9]) * 100, 0) == 28

print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）")
