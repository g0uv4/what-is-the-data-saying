#!/usr/bin/env python3
"""sample-s7-misread-specs-selfcheck.py：檢查虛構樣本資料 sample-s7-misread-specs.csv（數字未核）。

用法：在本資料夾執行  python3 sample-s7-misread-specs-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-s7-misread-specs.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
資料範圍：第 1 到第 22 組（共 22 組）。對應課程稿圖 S7（右圖的資料）。管制界限（中心線 50、上 56、下 44）與規格界限（上 60、下 40）是預先設定。
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CSV_NAME = "sample-s7-misread-specs.csv"                                  # 指定檔名，不用 glob
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
assert len(rows) == 22
v = [float(r["value"]) for r in rows]
g = lambda k: float(rows[0][k])
cl, ucl, lcl, usl, lsl = g("cl"), g("ucl"), g("lcl"), g("usl"), g("lsl")
assert (cl, ucl, lcl, usl, lsl) == (50.0, 56.0, 44.0, 60.0, 40.0)

# 1. 第 1–22 組：只有第 17 組超出管制上界 56，值 57.5；其餘 21 組都在 (44, 56) 內。
out = [i + 1 for i, a in enumerate(v) if a > ucl or a < lcl]
assert out == [17] and half_up(v[16], 1) == 57.5
# 2. 第 17 組雖然超出管制界限，仍在規格上限 60 之內（57.5 < 60），所以「只看規格」會漏掉它。
assert v[16] < usl
# 3. 第 1–22 組：全部 22 點都在規格 (40, 60) 內（只適用這 22 組）。
assert all(lsl < a < usl for a in v)
# 4. 其餘 21 組的實際範圍約 46.95–53.78（四捨五入到 0.01）。
rest = [a for i, a in enumerate(v) if i != 16]
assert (half_up(min(rest), 2), half_up(max(rest), 2)) == (46.95, 53.78)

print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）")
