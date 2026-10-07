#!/usr/bin/env python3
"""sample-lorenz-s3-gini-area-selfcheck.py：檢查虛構樣本資料 sample-lorenz-s3-gini-area.csv（數字未核）。

用法：在本資料夾執行  python3 sample-lorenz-s3-gini-area-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-lorenz-s3-gini-area.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
資料範圍：1 組（all），第 1 到第 10 戶（共 10 戶，由小到大排序），合計 100。對應課程稿圖 S3（Liora 重畫版：字母 A 在對角線與曲線之間）。
基尼係數兩種算法（10 戶資料）：折線下面積法 G＝1−2×曲線下面積（梯形）；小樣本修正版＝G×n／(n−1)，n 是單位數。
取整一律四捨五入（逢 5 進位，不是 Python 內建 round 的銀行家捨入）。
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CSV_NAME = "sample-lorenz-s3-gini-area.csv"                                   # 指定檔名，不用 glob
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

v, sh = lorenz_check("all")
assert len(v) == 10 and v == [2, 3, 4, 5, 7, 9, 12, 16, 20, 22] and sum(v) == 100
# 1. 面積：B＝曲線下方面積 0.309；A＝0.5−B＝0.191；A＋B＝對角線下三角形 0.5。基尼＝A／(A＋B)＝2A＝1−2B＝0.382。
n = 10
B = sum((sh[i] + sh[i + 1]) / 2 for i in range(n)) / n
A = 0.5 - B
assert close(B, 0.309) and close(A, 0.191) and close(A + B, 0.5)
g = gini(sh)
assert close(g, A / (A + B)) and close(g, 2 * A) and close(g, 1 - 2 * B) and close(g, gini_mean_difference(v))
assert half_up(g) == 0.38 and close(g, 0.382)
# 2. 小樣本修正（乘 n／(n−1)＝10／9）：0.382×10／9≈0.424，四捨五入 0.42；比折線下面積法高約 11%（10／9＝1.111…）。
gc = corrected(g, n)
assert half_up(gc) == 0.42 and close(gc, 0.4244444444, 1e-6)
assert half_up((gc / g - 1) * 100, 0) == 11
# 3. 圖上字母 A（約在 x＝0.60、y＝0.40）要落在對角線與曲線之間：該處對角線高度 0.60，曲線高度在第 6 戶（0.6）處＝0.21。
assert close(sh[6], 0.3) and sh[6] < 0.40 < 0.6           # x＝0.6 處曲線高度 0.30，A 的 y＝0.40 在 0.30 與對角線 0.60 之間

print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）")
