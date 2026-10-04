#!/usr/bin/env python3
"""sample-lorenz-s2-equal-vs-unequal-selfcheck.py：檢查虛構樣本資料 sample-lorenz-s2-equal-vs-unequal.csv（數字未核）。

用法：在本資料夾執行  python3 sample-lorenz-s2-equal-vs-unequal-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-lorenz-s2-equal-vs-unequal.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
資料範圍：2 組各 10 戶（more_equal＝左圖、more_unequal＝右圖），都由小到大排序。左圖合計 105（累計占比以 105 為 100%），右圖合計 100。對應課程稿圖 S2。
基尼係數兩種算法（10 戶資料）：折線下面積法 G＝1−2×曲線下面積（梯形）；小樣本修正版＝G×n／(n−1)，n 是單位數。
取整一律四捨五入（逢 5 進位，不是 Python 內建 round 的銀行家捨入）。
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CSV_NAME = "sample-lorenz-s2-equal-vs-unequal.csv"                                   # 指定檔名，不用 glob
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

ve, se = lorenz_check("more_equal"); vu, su = lorenz_check("more_unequal")
assert len(ve) == len(vu) == 10
assert ve == [8, 9, 9.5, 10, 10.2, 10.5, 11, 11.5, 12, 13.3] and abs(sum(ve) - 105) < 1e-9   # 左圖合計 105，不是 100
assert vu == [1, 1.5, 2, 3, 4, 6, 9, 14, 22, 37.5] and abs(sum(vu) - 100) < 1e-9
# 1. 基尼係數（折線下面積法，四捨五入到小數 2 位）：左 0.08（精確值約 0.0781）、右 0.55（精確值 0.552）。
ge, gu = gini(se), gini(su)
assert close(ge, gini_mean_difference(ve)) and close(gu, gini_mean_difference(vu))
assert half_up(ge) == 0.08 and half_up(gu) == 0.55
# 2. 左圖在累計單位 10%–90% 的每一個位置（第 1–9 戶）都高於右圖（0% 與 100% 兩端相等），所以左圖較平等是成立的。
assert all(se[i] > su[i] for i in range(1, 10))
# 3. 右圖最貧 50%（第 1–5 戶）累計 11.5%；左圖最貧 50% 累計約 44.5%（第 1–5 戶合計 46.7，占 105 的 44.48%，四捨五入到 0.1%）。
assert close(su[5], 0.115) and half_up(se[5] * 100, 1) == 44.5

print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）")
