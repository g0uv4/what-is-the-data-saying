#!/usr/bin/env python3
"""sample-s1-anatomy-selfcheck.py：檢查虛構樣本資料 sample-s1-anatomy.csv（數字未核）。

用法：在本資料夾執行  python3 sample-s1-anatomy-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-s1-anatomy.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
資料範圍：第 1 到第 25 組（共 25 點）。對應課程稿圖 S1。界限（中心線 50、上 56、下 44）是預先設定的（σ 設為 2），
不是由這 25 點算出來的。
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CSV_NAME = "sample-s1-anatomy.csv"                                  # 指定檔名，不用 glob
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

assert list(rows[0].keys()) == ["subgroup", "value", "cl", "ucl", "lcl", "data_status"]
assert len(rows) == 25
v = [float(r["value"]) for r in rows]
cl, ucl, lcl = float(rows[0]["cl"]), float(rows[0]["ucl"]), float(rows[0]["lcl"])
assert all(float(r["cl"]) == cl and float(r["ucl"]) == ucl and float(r["lcl"]) == lcl for r in rows)
assert (cl, ucl, lcl) == (50.0, 56.0, 44.0)
sigma_set = (ucl - cl) / 3
assert sigma_set == 2.0                              # 設定的 σ；界限＝中心線 ± 3σ

# 1. 第 1–25 組：全部 25 點都在 (44, 56) 之內（沒有點超界）。
assert all(lcl < a < ucl for a in v)
assert min(v) > 47 and max(v) < 52                   # 實際範圍約 47.3–51.9（只是範圍，與界限無關）

# 2. 這 25 點本身的標準差（n-1）四捨五入到 0.1 是 1.1，比設定的 2 小，所以全擠在界限內。
assert half_up(sd(v), 1) == 1.1 and sd(v) < sigma_set

# 3. 用這 25 點自己的平均與標準差估界限（平均 ± 3s），會是約 46.1 到 52.8，比圖上的 44–56 窄。
m = sum(v) / len(v)
assert (half_up(m - 3 * sd(v), 1), half_up(m + 3 * sd(v), 1)) == (46.1, 52.8)

# 4. 區域色帶只適用「設定值」：中心線 ± 1σ ＝ [48, 52]、± 2σ ＝ [46, 54]。
#    在這 25 點（第 1–25 組）裡：落在 [48, 52] 的有 23 點（92%），不是常態分布理論的約 68%——
#    因為資料的實際 σ（約 1.1）比設定的 2 小。落在 [46, 54] 的是全部 25 點。
in1 = sum(1 for a in v if cl - sigma_set <= a <= cl + sigma_set)
in2 = sum(1 for a in v if cl - 2 * sigma_set <= a <= cl + 2 * sigma_set)
assert in1 == 23 and half_up(100 * in1 / 25, 0) == 92
assert in2 == 25

# 5. 高於／低於中心線（只算這 25 點，沒有剛好等於 50 的點）：高於 10 點、低於 15 點。
above = sum(1 for a in v if a > cl); below = sum(1 for a in v if a < cl)
assert (above, below) == (10, 15) and above + below == 25
assert half_up(m, 2) == 49.48                        # 平均略低於設定的中心線 50

print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）")
