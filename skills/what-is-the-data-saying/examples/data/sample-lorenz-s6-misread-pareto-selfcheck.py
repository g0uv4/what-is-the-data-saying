#!/usr/bin/env python3
"""sample-lorenz-s6-misread-pareto-selfcheck.py：檢查虛構樣本資料 sample-lorenz-s6-misread-pareto.csv（數字未核）。

用法：在本資料夾執行  python3 sample-lorenz-s6-misread-pareto-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-lorenz-s6-misread-pareto.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
資料範圍：同一組 5 個數字 40、25、15、12、8（合計 100）。pareto 組＝柏拉圖（類別由大到小排，cum_units 是類別累計比例，cum_value_share 是折線累計％）；lorenz 組＝同樣 5 個數字由小到大排的洛倫茲曲線。對應課程稿圖 S6。
基尼係數兩種算法（10 戶資料）：折線下面積法 G＝1−2×曲線下面積（梯形）；小樣本修正版＝G×n／(n−1)，n 是單位數。
取整一律四捨五入（逢 5 進位，不是 Python 內建 round 的銀行家捨入）。
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CSV_NAME = "sample-lorenz-s6-misread-pareto.csv"                                   # 指定檔名，不用 glob
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

pg = grp("pareto")
pv = [a for a, _, _ in pg]
assert pv == [40, 25, 15, 12, 8] and pv == sorted(pv, reverse=True) and sum(pv) == 100
pc = [c for _, _, c in pg]
assert [half_up(c * 100, 0) for c in pc] == [40, 65, 80, 92, 100]           # 柏拉圖累計折線 40、65、80、92、100（%）
lv, ls = lorenz_check("lorenz")
assert lv == [8, 12, 15, 25, 40]
assert [half_up(c * 100, 0) for c in ls[1:]] == [8, 20, 35, 60, 100]        # 洛倫茲累計 8、20、35、60、100（%）
# 轉半圈關係：柏拉圖第 k 點的累計 C_k＝1−L(1−k／5)，k＝1..5（L 是洛倫茲累計，ls[0]＝0 起點）；5 個點全部成立。
for k in range(1, 6):
    assert close(pc[k - 1], 1 - ls[5 - k], 1e-6), k
# 把 5 個類別當 5 個單位（僅示意）時，洛倫茲曲線的基尼係數（折線下面積法）＝0.31；小樣本修正版 0.385 四捨五入 0.39。
g = gini(ls)
assert close(g, 0.308) and half_up(g) == 0.31 and half_up(corrected(g, 5)) == 0.39

print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）")
