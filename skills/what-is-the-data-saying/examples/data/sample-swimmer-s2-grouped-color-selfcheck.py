#!/usr/bin/env python3
"""sample-swimmer-s2-grouped-color-selfcheck.py：檢查虛構樣本 sample-swimmer-s2-grouped-color.csv（數字未核）。
對應圖 S2（模擬）。驗證兩組各 10 人的中位數 4.3／11.25、有緩解 2／7、仍在治療 0／4、最長者、停藥原因，以及最長前 10 條中高劑量 6、低劑量 4。
期望值與課程終稿圖說、繪圖程式事實檔一致（只用 Python 標準函式庫）。
用法：python3 sample-swimmer-s2-grouped-color-selfcheck.py
"""
CSV_NAME = "sample-swimmer-s2-grouped-color.csv"

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

rows = read_rows(["subject", "group", "treatment_months", "stop_reason", "responder", "ongoing", "data_status"])
assert len(rows) == 20

G = [r for r in rows if r["group"] == '低劑量']
assert len(G) == 10
assert median([float(r["treatment_months"]) for r in G]) == 4.3
assert sum(r["responder"] == "1" for r in G) == 2
assert sum(r["ongoing"] == "1" for r in G) == 0
top = sort_by_dur(G)[0]
assert (top["subject"], float(top["treatment_months"])) == ('P03', 14.0)
for k, v in {"疾病惡化": 9, "副作用": 0, "撤回同意": 1, "仍在治療": 0}.items():
    assert count(G, "stop_reason", k) == v, ('低劑量', k)


G = [r for r in rows if r["group"] == '高劑量']
assert len(G) == 10
assert median([float(r["treatment_months"]) for r in G]) == 11.25
assert sum(r["responder"] == "1" for r in G) == 7
assert sum(r["ongoing"] == "1" for r in G) == 4
top = sort_by_dur(G)[0]
assert (top["subject"], float(top["treatment_months"])) == ('P02', 22.5)
for k, v in {"疾病惡化": 4, "副作用": 2, "撤回同意": 0, "仍在治療": 4}.items():
    assert count(G, "stop_reason", k) == v, ('高劑量', k)

top10 = sort_by_dur(rows)[:10]
assert sum(r["group"] == "高劑量" for r in top10) == 6 and sum(r["group"] == "低劑量" for r in top10) == 4
print("PASS sample-swimmer-s2-grouped-color-selfcheck")
