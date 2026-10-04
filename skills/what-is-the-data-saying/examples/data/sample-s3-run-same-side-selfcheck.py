#!/usr/bin/env python3
"""sample-s3-run-same-side-selfcheck.py：檢查虛構樣本資料 sample-s3-run-same-side.csv（數字未核）。

用法：在本資料夾執行  python3 sample-s3-run-same-side-selfcheck.py  （可選：後面接 CSV 檔名，預設 sample-s3-run-same-side.csv）
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。
資料範圍：第 1 到第 18 組（共 18 組）。對應課程稿圖 S3（Liora 重畫版：前 9 點全部標紅）。界限（中心線 20、上 23.6、下 16.4，σ 設為 1.2）為預先設定。
"""
import csv, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CSV_NAME = "sample-s3-run-same-side.csv"                                  # 指定檔名，不用 glob
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
assert (cl, ucl, lcl) == (20.0, 23.6, 16.4)

def longest_same_side_run(vals, center):
    """回傳（最長連續同側點數, 起點組別 1 起算）；剛好等於中心線的點算「不在任何一側」，會中斷連續。"""
    best, best_start, cur, start, prev = 0, 0, 0, 0, 0
    for i, a in enumerate(vals):
        s = (a > center) - (a < center)
        if s != 0 and s == prev: cur += 1
        elif s != 0: cur, start = 1, i
        else: cur = 0
        prev = s
        if cur > best: best, best_start = cur, start + 1
    return best, best_start

# 1. 第 1–9 組：連續 9 點全在中心線 20 的上方（點數含第 1 組本身，所以是 9 點，不是 8 個間隔）。
assert all(a > cl for a in v[:9])
assert [a for a in v[:9]] == [20.6, 20.8, 20.7, 21.0, 20.9, 21.2, 21.1, 20.6, 20.3]
# 2. 第 10 組（19.8）回到中心線下方，所以這一段同側連續剛好是 9 點，不是 10 點。
assert v[9] == 19.8 and v[9] < cl
# 3. 整個 18 點裡最長的同側連續是 9 點，起點第 1 組；第 10–18 組沒有任何一段達到 8 點同側。
assert longest_same_side_run(v, cl) == (9, 1)
assert longest_same_side_run(v[9:], cl)[0] < 8
#    第 10–18 組（9 點）：低於中心線 5 點、高於 3 點、第 15 組剛好等於 20.0（在線上，不算任何一側）。
tail = v[9:]
assert (sum(a < cl for a in tail), sum(a > cl for a in tail), sum(a == cl for a in tail)) == (5, 3, 1)
# 4. 規則點數（各套規則不同，事先約定用哪一套）：
#    Western Electric 規則 4＝連續 8 點同側，在第 8 組湊滿；Nelson 規則 2＝連續 9 點同側，在第 9 組湊滿。
#    這份資料兩套規則都會發出訊號（前 9 點同側 ≥ 8，也 ≥ 9）；但 7 點同側（舊圖的標法）兩套都不算訊號。
def first_complete(vals, center, k):
    for i in range(k - 1, len(vals)):
        w = vals[i - k + 1:i + 1]
        if all(a > center for a in w) or all(a < center for a in w): return i + 1
    return None
assert first_complete(v, cl, 8) == 8 and first_complete(v, cl, 9) == 9 and first_complete(v, cl, 10) is None
# 5. 全部 18 點都在界限 (16.4, 23.6) 內：沒有單點超界；最大 21.2，最小 19.6。
assert all(lcl < a < ucl for a in v) and max(v) == 21.2 and min(v) == 19.6

print("OK：", path.name, "全部檢查通過（虛構資料，數字未核）")
