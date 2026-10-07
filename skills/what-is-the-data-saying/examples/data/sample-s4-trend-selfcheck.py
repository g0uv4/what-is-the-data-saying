#!/usr/bin/env python3
"""sample-s4-trend-selfcheck.py：檢查虛構樣本資料 sample-s4-trend.csv（數字未核）。

用法：在本資料夾執行  python3 sample-s4-trend-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-s4-trend.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
資料範圍：第 1 到第 18 組（共 18 組）。對應課程稿圖 S4。界限（中心線 40、上 44.5、下 35.5，σ 設為 1.5）為預先設定。
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CSV_NAME = "sample-s4-trend.csv"                                  # 指定檔名，不用 glob
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
assert len(rows) == 18
v = [float(r["value"]) for r in rows]
cl, ucl, lcl = float(rows[0]["cl"]), float(rows[0]["ucl"]), float(rows[0]["lcl"])
assert (cl, ucl, lcl) == (40.0, 44.5, 35.5)

def longest_rise(vals):
    """最長『每一點都比前一點高』的連續點數（點數含起點本身，所以 12 點只有 11 個上升間隔）。"""
    best = cur = 1; start = bs = 0
    for i in range(1, len(vals)):
        if vals[i] > vals[i - 1]: cur += 1
        else: cur, start = 1, i
        if cur > best: best, bs = cur, start
    return best, bs + 1

# 1. 第 1–12 組一路上升：起點 38.1、第 12 組 43.2（43.24 四捨五入到 0.1），共 12 點、11 個上升間隔。
assert longest_rise(v) == (12, 1)
assert half_up(v[0], 1) == 38.1 and half_up(v[11], 1) == 43.2
# 2. 第 13 組（40.2）掉回中心線附近，所以上升段剛好 12 點。
assert v[12] < v[11] and v[12] == 40.2
# 3. 這 12 點都沒有超過上界 44.5（最高 43.24）；全部 18 點也都在界限內。
assert all(a < ucl for a in v[:12]) and max(v) < ucl and min(v) > lcl
# 4. 趨勢規則（Nelson 規則 3、NIST 手冊都是『連續 6 點遞增或遞減』）：6 點＝5 個間隔。
#    在第 6 組就湊滿 6 點上升，比整段 12 點早；之後每一組都仍在上升中，直到第 12 組。
def first_trend(vals, k):
    for i in range(k - 1, len(vals)):
        w = vals[i - k + 1:i + 1]
        if all(w[j + 1] > w[j] for j in range(k - 1)) or all(w[j + 1] < w[j] for j in range(k - 1)): return i + 1
    return None
assert first_trend(v, 6) == 6
# 5. 與中心線的關係（只算第 1–12 組）：第 1–5 組低於中心線 40，第 6–12 組（7 點）高於 40；
#    所以這個上升趨勢不是「同側」型態，不會觸發『連續同側』規則。
assert all(a < cl for a in v[:5]) and all(a > cl for a in v[5:12])

print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）")
