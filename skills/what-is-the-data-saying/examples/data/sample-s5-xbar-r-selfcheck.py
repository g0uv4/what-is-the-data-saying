#!/usr/bin/env python3
"""sample-s5-xbar-r-selfcheck.py：檢查虛構樣本資料 sample-s5-xbar-r.csv（數字未核）。

用法：在本資料夾執行  python3 sample-s5-xbar-r-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-s5-xbar-r.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
資料範圍：第 1 到第 20 組（共 20 組）。對應課程稿圖 S5。X̄ 圖界限（中心線 10.0、8.8／11.2）與 R 圖界限（中心線 1.2、上 2.25、下 0.15）
是示意設定，不是用 A2、D3、D4 係數由資料算出的。
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CSV_NAME = "sample-s5-xbar-r.csv"                                  # 指定檔名，不用 glob
path = Path(__file__).resolve().parent / (sys.argv[1] if len(sys.argv) > 1 else CSV_NAME)

def half_up(x, nd=1):
    """四捨五入（逢 5 進位）；Python 內建 round() 是「銀行家捨入」，不是四捨五入。"""
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))

def sd(v):
    """樣本標準差（分母 n-1，與 Excel STDEV.S 相同）。"""
    m = sum(v) / len(v)
    return (sum((a - m) ** 2 for a in v) / (len(v) - 1)) ** 0.5

with open(path, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
assert all(r["data_status"] == "虛構資料，數字未核" for r in rows)

assert list(rows[0].keys()) == ["subgroup", "xbar", "range", "xbar_cl", "xbar_ucl", "xbar_lcl", "r_cl", "r_ucl", "r_lcl", "data_status"]
assert len(rows) == 20
xb = [float(r["xbar"]) for r in rows]; R = [float(r["range"]) for r in rows]
g = lambda k: float(rows[0][k])
assert (g("xbar_cl"), g("xbar_ucl"), g("xbar_lcl")) == (10.0, 11.2, 8.8)
assert (g("r_cl"), g("r_ucl"), g("r_lcl")) == (1.2, 2.25, 0.15)

# 1. 第 1–20 組：X̄ 全在 (8.8, 11.2) 內，R 全在 (0.15, 2.25) 內，沒有超界。
assert all(8.8 < a < 11.2 for a in xb) and all(0.15 < a < 2.25 for a in R)
# 2. 實際範圍：X̄ 約 9.61–10.48、平均 10.04（四捨五入到 0.01）；R 約 0.99–1.48、平均 1.21。
assert (half_up(min(xb), 2), half_up(max(xb), 2)) == (9.61, 10.48) and half_up(sum(xb) / 20, 2) == 10.04
assert (half_up(min(R), 2), half_up(max(R), 2)) == (0.99, 1.48) and half_up(sum(R) / 20, 2) == 1.21
# 3. R 圖下界 0.15 只是示意：腳本把 R 的最小值限制在 0.15，但這 20 組沒有任何一組被限制到（R 最小約 0.99）。
#    真實做法：NIST 係數表 D3＝0（每組 n≤6 時），下界是 0 而不是 0.15；本資料沒有用到 n 或係數。
assert all(a != 0.15 for a in R)
# 4. 界限寬度：X̄ 界限 10.0 ± 1.2（σ 設 0.4 的 3 倍）；R 上界 2.25＝1.2 + 3×0.35。
assert round(g("xbar_ucl") - g("xbar_cl"), 6) == 1.2 and round(g("r_ucl") - g("r_cl"), 6) == 1.05

print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）")
