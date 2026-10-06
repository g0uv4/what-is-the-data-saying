#!/usr/bin/env python3
"""sample-swimmer-s7-too-many-vs-km-selfcheck.py：檢查虛構樣本 sample-swimmer-s7-too-many-vs-km.csv（數字未核）。
對應圖 S7（模擬）。驗證 150 人：疾病惡化 84、副作用 26、撤回同意 24、仍在治療 16；最長 P005 22.0；Kaplan–Meier（事件＝任何原因停藥，共 134）中位數 6.0、第 6／12／18 個月 0.433／0.202／0.061；風險人數 150／79／28／7／0。
期望值與課程終稿圖說、繪圖程式事實檔一致（只用 Python 標準函式庫）。
用法：python3 sample-swimmer-s7-too-many-vs-km-selfcheck.py
"""
CSV_NAME = "sample-swimmer-s7-too-many-vs-km.csv"

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

rows = read_rows(["subject", "group", "treatment_months", "stop_reason", "event", "data_status"])
assert len(rows) == 150
for k, v in {"疾病惡化": 84, "副作用": 26, "撤回同意": 24, "仍在治療": 16}.items():
    assert count(rows, "stop_reason", k) == v, k
top = sort_by_dur(rows)[0]
assert (top["subject"], float(top["treatment_months"]), top["stop_reason"]) == ('P005', 22.0, '疾病惡化')
t = [float(r["treatment_months"]) for r in rows]; e = [int(r["event"]) for r in rows]
assert all((ev == 0) == (r["stop_reason"] == "仍在治療") for ev, r in zip(e, rows))
assert sum(e) == 134
S = 1.0; curve = []
for tt in sorted(set(x for x, ev in zip(t, e) if ev == 1)):
    n = sum(1 for x in t if x >= tt); d = sum(1 for x, ev in zip(t, e) if x == tt and ev == 1)
    S *= 1 - d / n; curve.append((tt, S))
def S_at(x):
    s = 1.0
    for tt, v in curve:
        if tt <= x + 1e-12: s = v
        else: break
    return s
med = next(tt for tt, v in curve if v <= 0.5 + 1e-12)
assert med == 6.0, med
for m, v in {'6': 0.433, '12': 0.202, '18': 0.061}.items():
    assert round(S_at(float(m)), 3) == v, (m, S_at(float(m)))
for m, v in {'0': 150, '6': 79, '12': 28, '18': 7, '24': 0}.items():
    assert sum(1 for x in t if x >= float(m)) == v, m
print("PASS sample-swimmer-s7-too-many-vs-km-selfcheck")
