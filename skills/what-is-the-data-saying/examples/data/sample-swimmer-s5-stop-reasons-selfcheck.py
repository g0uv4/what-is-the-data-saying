#!/usr/bin/env python3
"""sample-swimmer-s5-stop-reasons-selfcheck.py：檢查虛構樣本 sample-swimmer-s5-stop-reasons.csv（數字未核）。
對應圖 S5（模擬）。驗證停藥原因：疾病惡化 13、副作用 2（P04 12.5、P18 1.7）、撤回同意 1（P06 2.6）、仍在治療 4；P04 曾轉完全緩解卻因副作用停藥。
期望值與課程終稿圖說、繪圖程式事實檔一致（只用 Python 標準函式庫）。
用法：python3 sample-swimmer-s5-stop-reasons-selfcheck.py
"""
CSV_NAME = "sample-swimmer-s5-stop-reasons.csv"

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

rows = read_rows(["subject", "group", "treatment_months", "stop_reason", "data_status"])
assert len(rows) == 20
for k, v in {"疾病惡化": 13, "副作用": 2, "撤回同意": 1, "仍在治療": 4}.items():
    assert count(rows, "stop_reason", k) == v, k
assert {r["subject"]: float(r["treatment_months"]) for r in rows if r["stop_reason"] == "副作用"} == {'P04': 12.5, 'P18': 1.7}
assert {r["subject"]: float(r["treatment_months"]) for r in rows if r["stop_reason"] == "撤回同意"} == {'P06': 2.6}
assert [r["subject"] for r in sort_by_dur(rows) if r["stop_reason"] == "疾病惡化"] == ['P03', 'P15', 'P09', 'P20', 'P01', 'P05', 'P07', 'P08', 'P10', 'P11', 'P12', 'P17', 'P19']
print("PASS sample-swimmer-s5-stop-reasons-selfcheck")
