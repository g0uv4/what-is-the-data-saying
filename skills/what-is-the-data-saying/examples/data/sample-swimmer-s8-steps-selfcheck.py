#!/usr/bin/env python3
"""sample-swimmer-s8-steps-selfcheck.py：檢查虛構樣本 sample-swimmer-s8-steps.csv（數字未核）。
對應圖 S8（模擬）。驗證製作步驟用的 6 人資料表（P01–P06，最早入組）與排序 P02 22.5、P03 14.0、P04 12.5、P01 8.0、P05 6.0、P06 2.6。
期望值與課程終稿圖說、繪圖程式事實檔一致（只用 Python 標準函式庫）。
用法：python3 sample-swimmer-s8-steps-selfcheck.py
"""
CSV_NAME = "sample-swimmer-s8-steps.csv"

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

rows = read_rows(["subject", "group", "start_month", "end_month", "first_response_month", "cr_month", "stop_reason", "ongoing", "data_status"])
got = [(r["subject"], r["group"], r["start_month"], r["end_month"], r["first_response_month"], r["cr_month"], r["stop_reason"], r["ongoing"]) for r in rows]
assert got == [('P01', '低劑量', '0', '8.0', '2', '4', '疾病惡化', '否'), ('P02', '高劑量', '0', '22.5', '', '', '', '是'), ('P03', '低劑量', '0', '14.0', '6', '8', '疾病惡化', '否'), ('P04', '高劑量', '0', '12.5', '2', '4', '副作用', '否'), ('P05', '低劑量', '0', '6.0', '', '', '疾病惡化', '否'), ('P06', '低劑量', '0', '2.6', '', '', '撤回同意', '否')], got
assert [r["subject"] for r in sort_by_dur(rows, "end_month")] == ['P02', 'P03', 'P04', 'P01', 'P05', 'P06']
assert [float(r["end_month"]) for r in sort_by_dur(rows, "end_month")] == [22.5, 14.0, 12.5, 8.0, 6.0, 2.6]
print("PASS sample-swimmer-s8-steps-selfcheck")
