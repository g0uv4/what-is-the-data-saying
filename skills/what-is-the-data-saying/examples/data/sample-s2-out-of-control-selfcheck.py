#!/usr/bin/env python3
"""sample-s2-out-of-control-selfcheck.py：檢查虛構樣本資料 sample-s2-out-of-control.csv（數字未核）。

用法：在本資料夾執行  python3 sample-s2-out-of-control-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-s2-out-of-control.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
資料範圍：左右兩圖各第 1 到第 20 組（共 20 組）。對應課程稿圖 S2。界限（中心線 100、上 109、下 91，σ 設為 3）為預先設定。
右圖與左圖只有第 15 組不同：其餘 19 組完全相同。
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CSV_NAME = "sample-s2-out-of-control.csv"                                  # 指定檔名，不用 glob
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

assert list(rows[0].keys()) == ["subgroup", "left_value", "right_value", "cl", "ucl", "lcl", "data_status"]
assert len(rows) == 20
L = [float(r["left_value"]) for r in rows]; Rr = [float(r["right_value"]) for r in rows]
cl, ucl, lcl = float(rows[0]["cl"]), float(rows[0]["ucl"]), float(rows[0]["lcl"])
assert (cl, ucl, lcl) == (100.0, 109.0, 91.0)

# 1. 左圖（第 1–20 組）：全部 20 點都在 (91, 109) 之內，沒有超界。
assert all(lcl < a < ucl for a in L)
assert half_up(min(L), 1) == 96.4 and half_up(max(L), 1) == 103.1   # 實際範圍，與界限無關
# 2. 右圖（第 1–20 組）：只有第 15 組超出上界，值 110.8（比上界 109 高 1.8）；其餘 19 組都在界限內。
out = [i + 1 for i, a in enumerate(Rr) if a > ucl or a < lcl]
assert out == [15] and half_up(Rr[14], 1) == 110.8 and half_up(Rr[14] - ucl, 1) == 1.8
# 3. 左右兩圖只差第 15 組（20 組裡 19 組相同）。
diff = [i + 1 for i in range(20) if L[i] != Rr[i]]
assert diff == [15]
# 4. 超界比例：右圖 20 組中 1 組，剛好是 5.0%（只是這 20 組的實際比例，不是理論誤報率；
#    3σ 界限的理論單點誤報率約 0.27%，兩者不同，不能互相代替）。
assert 100 * len(out) / 20 == 5.0
# 5. 左圖點的標準差（n-1）約 1.6，比設定的 σ＝3 小（所以左圖看起來很緊）。
assert half_up(sd(L), 1) == 1.6 and sd(L) < 3

print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）")
