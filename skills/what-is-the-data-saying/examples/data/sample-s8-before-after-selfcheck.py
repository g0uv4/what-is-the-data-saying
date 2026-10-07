#!/usr/bin/env python3
"""sample-s8-before-after-selfcheck.py：檢查虛構樣本資料 sample-s8-before-after.csv（數字未核）。

用法：在本資料夾執行  python3 sample-s8-before-after-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-s8-before-after.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
資料範圍：phase＝before 與 after 各第 1 到第 18 組（共 18 組，合計 36 列）。對應課程稿圖 S8。
改善前界限：中心線 12.0、上 17.4、下 6.6（σ 設 1.8）；改善後：中心線 10.0（＝目標 10）、上 12.1、下 7.9（σ 設 0.7）。界限皆預先設定。
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CSV_NAME = "sample-s8-before-after.csv"                                  # 指定檔名，不用 glob
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

assert list(rows[0].keys()) == ["phase", "subgroup", "value", "cl", "ucl", "lcl", "target", "data_status"]
assert len(rows) == 36
B = [r for r in rows if r["phase"] == "before"]; A = [r for r in rows if r["phase"] == "after"]
assert len(B) == 18 and len(A) == 18
b = [float(r["value"]) for r in B]; a = [float(r["value"]) for r in A]
gb = lambda k: float(B[0][k]); ga = lambda k: float(A[0][k])
assert (gb("cl"), gb("ucl"), gb("lcl")) == (12.0, 17.4, 6.6)
assert (ga("cl"), ga("ucl"), ga("lcl")) == (10.0, 12.1, 7.9)
assert gb("target") == ga("target") == 10

# 1. 改善前（第 1–18 組）：只有第 6 組超出上界，值 18.2（比上界 17.4 高 0.8）；其餘 17 組在界限內。
out = [i + 1 for i, x in enumerate(b) if x > gb("ucl") or x < gb("lcl")]
assert out == [6] and half_up(b[5], 1) == 18.2 and half_up(b[5] - gb("ucl"), 1) == 0.8
# 2. 改善後（第 1–18 組）：全部 18 點都在 (7.9, 12.1) 內，沒有點超界。實際範圍約 9.63–10.97。
assert all(ga("lcl") < x < ga("ucl") for x in a)
assert (half_up(min(a), 2), half_up(max(a), 2)) == (9.63, 10.97)
# 3. 改善後這 18 點的標準差（n-1）四捨五入到 0.01 是 0.35，約為設定 σ（0.7）的一半（0.35/0.7＝50.5%，不是剛好一半）。
s_a = sd(a)
assert half_up(s_a, 2) == 0.35 and half_up(100 * s_a / 0.7, 1) == 50.5
# 4. 平均：改善後 10.10，比設定的中心線 10.0 稍高 0.10；改善前 12.33（含第 6 組的 18.2），離目標 10 約 2.33。
assert half_up(sum(a) / 18, 2) == 10.10 and half_up(sum(b) / 18, 2) == 12.33
assert half_up(sum(b) / 18 - 10, 2) == 2.33
# 5. 改善前點的標準差約 1.81（含第 6 組的離群點），與設定的 σ＝1.8 相近；這是這 18 點的結果，不是通則。
assert half_up(sd(b), 2) == 1.81

print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）")
