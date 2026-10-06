#!/usr/bin/env python3
"""sample-swimmer-s3-sorting-selfcheck.py：檢查虛構樣本 sample-swimmer-s3-sorting.csv（數字未核）。
對應圖 S3（模擬）。驗證兩種排序與入組先後對棒長的 Spearman 等級相關（同長度取平均名次）＝ −0.32；若同分任意排名可能得 −0.28，不可用。
期望值與課程終稿圖說、繪圖程式事實檔一致（只用 Python 標準函式庫）。
用法：python3 sample-swimmer-s3-sorting-selfcheck.py
"""
CSV_NAME = "sample-swimmer-s3-sorting.csv"

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

rows = read_rows(["subject", "enroll_month", "treatment_months", "row_if_sorted_by_duration", "row_if_sorted_by_id", "data_status"])
assert len(rows) == 20
assert [r["subject"] for r in sort_by_dur(rows)] == ['P02', 'P13', 'P03', 'P14', 'P16', 'P04', 'P15', 'P09', 'P20', 'P01', 'P05', 'P07', 'P08', 'P10', 'P06', 'P11', 'P12', 'P17', 'P19', 'P18']
assert [r["subject"] for r in sorted(rows, key=lambda r: int(r["row_if_sorted_by_duration"]))] == ['P02', 'P13', 'P03', 'P14', 'P16', 'P04', 'P15', 'P09', 'P20', 'P01', 'P05', 'P07', 'P08', 'P10', 'P06', 'P11', 'P12', 'P17', 'P19', 'P18']
assert [r["subject"] for r in sorted(rows, key=lambda r: int(r["row_if_sorted_by_id"]))] == ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15', 'P16', 'P17', 'P18', 'P19', 'P20']
enr = [float(r["enroll_month"]) for r in rows]; bar = [float(r["treatment_months"]) for r in rows]
assert len(set(bar)) < len(bar), "棒長有同分（例如 4 位 2.0 個月），所以必須取平均名次"
rho = spearman_avg(enr, bar)
assert round(rho, 2) == -0.32, rho
assert round(rho, 2) != -0.28
try:
    from scipy.stats import spearmanr
    assert round(float(spearmanr(enr, bar).statistic), 2) == -0.32
except ImportError:
    pass
print("Spearman（平均名次）=", round(rho, 4))
print("PASS sample-swimmer-s3-sorting-selfcheck")
