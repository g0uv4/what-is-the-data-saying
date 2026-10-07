#!/usr/bin/env python3
"""sample-lorenz-s4-steps-selfcheck.py：檢查虛構樣本資料 sample-lorenz-s4-steps.csv（數字未核）。

用法：在本資料夾執行  python3 sample-lorenz-s4-steps-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-lorenz-s4-steps.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
資料範圍：兩組各 10 戶——step1_unsorted（步驟 1：未排序，rank 欄是原始位置，合計 100）、step2_sorted（步驟 2：由小到大排序）。對應課程稿圖 S4。
基尼係數兩種算法（10 戶資料）：折線下面積法 G＝1−2×曲線下面積（梯形）；小樣本修正版＝G×n／(n−1)，n 是單位數。
取整一律四捨五入（逢 5 進位，不是 Python 內建 round 的銀行家捨入）。
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CSV_NAME = "sample-lorenz-s4-steps.csv"                                   # 指定檔名，不用 glob
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

raw = [float(r["value"]) for r in rows if r["group"] == "step1_unsorted"]
assert raw == [14, 3, 22, 5, 8, 28, 2, 6, 10, 2] and sum(raw) == 100
assert all(r["cum_units"] == "" and r["cum_value_share"] == "" for r in rows if r["group"] == "step1_unsorted")
v, sh = lorenz_check("step2_sorted")
assert v == sorted(raw) == [2, 2, 3, 5, 6, 8, 10, 14, 22, 28]            # 排序後數列與圖說相同
# 圖上標出的 3 個讀點（累計單位比例 20%、50%、90%，即前 2、5、9 戶）：
assert half_up(sh[2] * 100, 0) == 4 and sum(v[:2]) == 4        # 20% 的人累計 4%（2＋2）
assert half_up(sh[5] * 100, 0) == 18 and sum(v[:5]) == 18      # 50% 累計 18%（2＋2＋3＋5＋6）
assert half_up(sh[9] * 100, 0) == 72 and sum(v[:9]) == 72      # 90% 累計 72%（100−28）
# 排序前後合計相同（只是換順序）。
assert sum(raw) == sum(v) == 100

print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）")
