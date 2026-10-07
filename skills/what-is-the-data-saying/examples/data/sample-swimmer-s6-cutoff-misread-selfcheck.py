#!/usr/bin/env python3
"""sample-swimmer-s6-cutoff-misread-selfcheck.py：檢查虛構樣本 sample-swimmer-s6-cutoff-misread.csv（數字未核）。
對應圖 S6（模擬）。驗證第 12 個月截止：17 人入組、P18–P20 尚未入組、仍在治療 11 人、最長 P02 10.5、最短 P17 1.0；第 24 個月：20 人、仍在治療 4 人、P02 22.5；早截止仍在治療者後來的棒長。
期望值與課程終稿圖說、繪圖程式事實檔一致（只用 Python 標準函式庫）。
用法：python3 sample-swimmer-s6-cutoff-misread-selfcheck.py
"""
CSV_NAME = "sample-swimmer-s6-cutoff-misread.csv"

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

rows = read_rows(["subject", "enroll_month", "months_at_cutoff_12", "status_at_cutoff_12", "months_at_cutoff_24", "status_at_cutoff_24", "data_status"])
assert len(rows) == 20
E = [r for r in rows if r["status_at_cutoff_12"] != "尚未入組"]
assert len(E) == 17
assert sorted(r["subject"] for r in rows if r["status_at_cutoff_12"] == "尚未入組") == ['P18', 'P19', 'P20']
assert all(float(r["enroll_month"]) >= 12.0 for r in rows if r["status_at_cutoff_12"] == "尚未入組")
assert count(E, "status_at_cutoff_12", "仍在治療") == 11
assert count(rows, "status_at_cutoff_24", "仍在治療") == 4
le = sort_by_dur(E, "months_at_cutoff_12")
assert (le[0]["subject"], float(le[0]["months_at_cutoff_12"])) == ('P02', 10.5)
assert (le[-1]["subject"], float(le[-1]["months_at_cutoff_12"]), le[-1]["status_at_cutoff_12"]) == ('P17', 1.0, "仍在治療")
ll = sort_by_dur(rows, "months_at_cutoff_24")
assert (ll[0]["subject"], float(ll[0]["months_at_cutoff_24"])) == ('P02', 22.5)
got = {r["subject"]: (float(r["months_at_cutoff_12"]), float(r["months_at_cutoff_24"]), r["status_at_cutoff_24"]) for r in E if r["status_at_cutoff_12"] == "仍在治療"}
assert got == {'P02': (10.5, 22.5, '仍在治療'), 'P13': (2.2, 14.2, '仍在治療'), 'P03': (10.2, 14.0, '疾病惡化'), 'P14': (2.0, 14.0, '仍在治療'), 'P16': (1.3, 13.3, '仍在治療'), 'P04': (9.4, 12.5, '副作用'), 'P15': (1.4, 12.0, '疾病惡化'), 'P09': (4.3, 10.0, '疾病惡化'), 'P07': (4.9, 6.0, '疾病惡化'), 'P08': (4.4, 6.0, '疾病惡化'), 'P17': (1.0, 2.0, '疾病惡化')}, got
# 仍在治療者在早截止時的棒長＝截止月 − 入組月
for r in E:
    if r["status_at_cutoff_12"] == "仍在治療":
        assert round(12.0 - float(r["enroll_month"]), 1) == float(r["months_at_cutoff_12"]), r["subject"]
print("PASS sample-swimmer-s6-cutoff-misread-selfcheck")
