#!/usr/bin/env python3
"""sample-swimmer-s4-duration-of-response-selfcheck.py：檢查虛構樣本 sample-swimmer-s4-duration-of-response.csv（數字未核）。
對應圖 S4（模擬）。驗證有緩解 9 人的反應持續時間（最長 P13 12.2 個月、設限）、以疾病惡化結束 5 人、設限 4 人（仍在治療 3、副作用 1）。
期望值與課程終稿圖說、繪圖程式事實檔一致（只用 Python 標準函式庫）。
用法：python3 sample-swimmer-s4-duration-of-response-selfcheck.py
"""
CSV_NAME = "sample-swimmer-s4-duration-of-response.csv"

import csv, sys
from pathlib import Path

path = Path(__file__).resolve().parent / (sys.argv[1] if len(sys.argv) > 1 else CSV_NAME)
STATUS = "虛構資料，數字未核"

def read_rows(head):
    with open(path, newline="", encoding="utf-8") as f:
        first = f.readline()
        assert first.startswith("# " + STATUS), first
        rows = list(csv.DictReader(f))
    assert list(rows[0].keys()) == head, list(rows[0].keys())
    assert all(r["data_status"] == STATUS for r in rows)
    return rows

def num(s):
    return None if s == "" else float(s)

def median(xs):
    xs = sorted(xs); n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2

def sort_by_dur(rows, key="treatment_months"):
    return sorted(rows, key=lambda r: (-float(r[key]), r["subject"]))

def count(rows, key, val):
    return sum(1 for r in rows if r[key] == val)

def avg_ranks(xs):
    """同分取平均名次（1 起算）。"""
    order = sorted(range(len(xs)), key=lambda i: xs[i]); rk = [0.0] * len(xs); i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]: j += 1
        for k in range(i, j + 1): rk[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return rk

def pearson(a, b):
    n = len(a); ma = sum(a) / n; mb = sum(b) / n
    sab = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    sa = sum((x - ma) ** 2 for x in a) ** 0.5; sb = sum((y - mb) ** 2 for y in b) ** 0.5
    return sab / (sa * sb)

def spearman_avg(a, b):
    return pearson(avg_ranks(a), avg_ranks(b))

rows = read_rows(["subject", "group", "treatment_months", "stop_reason", "dor_start_month", "dor_end_month", "dor_months", "dor_status", "data_status"])
assert len(rows) == 20
R_ = [r for r in rows if r["dor_start_month"] != ""]
assert len(R_) == 9
got = {r["subject"]: (float(r["dor_start_month"]), float(r["dor_end_month"]), float(r["dor_months"]), r["dor_status"]) for r in R_}
assert got == {'P13': (2.0, 14.2, 12.2, '設限：仍在治療'), 'P03': (6.0, 14.0, 8.0, '疾病惡化'), 'P14': (4.0, 14.0, 10.0, '設限：仍在治療'), 'P16': (4.0, 13.3, 9.3, '設限：仍在治療'), 'P04': (2.0, 12.5, 10.5, '設限：副作用'), 'P20': (4.0, 10.0, 6.0, '疾病惡化'), 'P01': (2.0, 8.0, 6.0, '疾病惡化'), 'P08': (2.0, 6.0, 4.0, '疾病惡化'), 'P10': (2.0, 4.0, 2.0, '疾病惡化')}, got
for r in R_:
    assert round(float(r["dor_end_month"]) - float(r["dor_start_month"]), 1) == float(r["dor_months"])
    assert float(r["dor_end_month"]) == float(r["treatment_months"])
L = sorted(R_, key=lambda r: (-float(r["dor_months"]), r["subject"]))[0]
assert (L["subject"], float(L["dor_months"]), L["dor_status"]) == ('P13', 12.2, '設限：仍在治療')
assert sum(r["dor_status"] == "疾病惡化" for r in R_) == 5
assert sum(r["dor_status"].startswith("設限") for r in R_) == 4
for k, v in {'副作用': 1, '撤回同意': 0, '資料截止時仍在治療': 3}.items():
    assert sum(r["dor_status"] == "設限：" + (k if k != "資料截止時仍在治療" else "仍在治療") for r in R_) == v, k
print("PASS sample-swimmer-s4-duration-of-response-selfcheck")
