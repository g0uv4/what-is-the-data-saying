#!/usr/bin/env python3
"""sample-s6-spec-vs-control-selfcheck.py：檢查虛構樣本資料 sample-s6-spec-vs-control.csv（數字未核）。

用法：在本資料夾執行  python3 sample-s6-spec-vs-control-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-s6-spec-vs-control.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
資料範圍：第 1 到第 24 組（共 24 點）。對應課程稿圖 S6。管制界限（中心線 50、上 56、下 44）與規格界限（上 58、下 42）都是預先設定的。
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CSV_NAME = "sample-s6-spec-vs-control.csv"                                  # 指定檔名，不用 glob
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

assert list(rows[0].keys()) == ["subgroup", "value", "cl", "ucl", "lcl", "usl", "lsl", "data_status"]
assert len(rows) == 24
v = [float(r["value"]) for r in rows]
g = lambda k: float(rows[0][k])
cl, ucl, lcl, usl, lsl = g("cl"), g("ucl"), g("lcl"), g("usl"), g("lsl")
assert (cl, ucl, lcl, usl, lsl) == (50.0, 56.0, 44.0, 58.0, 42.0)

# 1. 管制界限在規格界限之內：lsl < lcl < cl < ucl < usl（兩組界限是不同的線）。
assert lsl < lcl < cl < ucl < usl
# 2. 第 1–24 組：全部 24 點都在管制界限 (44, 56) 內，所以也都在規格 (42, 58) 內。
#    實際範圍約 46.4–54.7；「全部在規格內」只適用這 24 點，不能推到之後的流程。
assert all(lcl < a < ucl for a in v) and all(lsl < a < usl for a in v)
assert (half_up(min(v), 1), half_up(max(v), 1)) == (46.4, 54.7)
# 3. 用這 24 點自己的平均與標準差（n-1）估界限（平均 ± 3s）：約 44.9 到 55.0（四捨五入到 0.1），
#    與圖上預先設定的 44–56 相近但不相同。
m = sum(v) / 24
assert (half_up(m - 3 * sd(v), 1), half_up(m + 3 * sd(v), 1)) == (44.9, 55.0)
# 4. 寬度（只對這幾個預設數字成立，不是通用比值，也不是製程能力指數）：
#    管制界限寬 12（56−44），規格界限寬 16（58−42），12/16＝0.75。
assert ucl - lcl == 12 and usl - lsl == 16 and (ucl - lcl) / (usl - lsl) == 0.75

print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）")
