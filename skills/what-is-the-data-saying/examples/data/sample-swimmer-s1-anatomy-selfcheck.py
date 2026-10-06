#!/usr/bin/env python3
"""sample-swimmer-s1-anatomy-selfcheck.py：檢查虛構樣本 sample-swimmer-s1-anatomy.csv（數字未核）。
對應圖 S1（模擬）。驗證人數 20、最長 P02 22.5（仍在治療）、最短 P18 1.7（副作用）、仍在治療 4 人、有緩解 9 人、完全緩解 3 人、第一次緩解月分布、停藥原因、中位數 7.0、排序。
期望值與課程終稿圖說、繪圖程式事實檔一致（只用 Python 標準函式庫）。
用法：python3 sample-swimmer-s1-anatomy-selfcheck.py
"""
CSV_NAME = "sample-swimmer-s1-anatomy.csv"

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

rows = read_rows(["subject", "group", "enroll_month", "treatment_months", "stop_reason", "ongoing", "first_response_month", "cr_month", "progression_month", "data_status"])
assert len(rows) == 20
assert [r["subject"] for r in rows] == ["P%02d" % i for i in range(1, 21)]
enr = [float(r["enroll_month"]) for r in rows]; assert enr == sorted(enr), "編號應依入組先後"
srt = sort_by_dur(rows)
assert (srt[0]["subject"], float(srt[0]["treatment_months"]), srt[0]["stop_reason"], srt[0]["group"]) == ('P02', 22.5, "仍在治療", '高劑量')
assert srt[0]["first_response_month"] == "", "最長者沒有緩解符號"
assert (srt[-1]["subject"], float(srt[-1]["treatment_months"]), srt[-1]["stop_reason"]) == ('P18', 1.7, '副作用')
assert [r["subject"] for r in srt] == ['P02', 'P13', 'P03', 'P14', 'P16', 'P04', 'P15', 'P09', 'P20', 'P01', 'P05', 'P07', 'P08', 'P10', 'P06', 'P11', 'P12', 'P17', 'P19', 'P18']
assert {r["subject"]: float(r["treatment_months"]) for r in rows} == {'P02': 22.5, 'P13': 14.2, 'P03': 14.0, 'P14': 14.0, 'P16': 13.3, 'P04': 12.5, 'P15': 12.0, 'P09': 10.0, 'P20': 10.0, 'P01': 8.0, 'P05': 6.0, 'P07': 6.0, 'P08': 6.0, 'P10': 4.0, 'P06': 2.6, 'P11': 2.0, 'P12': 2.0, 'P17': 2.0, 'P19': 2.0, 'P18': 1.7}
on = [r["subject"] for r in srt if r["ongoing"] == "1"]
assert on == ['P02', 'P13', 'P14', 'P16'] and len(on) == 4
assert all((r["ongoing"] == "1") == (r["stop_reason"] == "仍在治療") for r in rows)
resp = [r for r in rows if r["first_response_month"] != ""]
assert len(resp) == 9
assert [r["subject"] for r in rows if r["cr_month"] != ""] == ['P01', 'P03', 'P04']
fr = sorted(float(r["first_response_month"]) for r in resp)
assert fr[0] == 2.0
assert [r["subject"] for r in resp if float(r["first_response_month"]) == fr[0]] == ['P01', 'P04', 'P08', 'P10', 'P13']
dist = {}
for x in fr: dist[str(x)] = dist.get(str(x), 0) + 1
assert dist == {'2.0': 5, '4.0': 3, '6.0': 1}, dist
assert all(float(x) % 2 == 0 for r in resp for x in [r["first_response_month"]]), "第一次緩解只會在掃描月（每 2 個月）"
assert all(float(r["progression_month"]) % 2 == 0 for r in rows if r["progression_month"] != ""), "疾病惡化只會在掃描月"
for k, v in {"疾病惡化": 13, "副作用": 2, "撤回同意": 1, "仍在治療": 4}.items():
    assert count(rows, "stop_reason", k) == v, (k, count(rows, "stop_reason", k))
assert median([float(r["treatment_months"]) for r in rows]) == 7.0
# 圖上標註範例：金星 P01（完全緩解）、藍三角 P10（第一次緩解）、紅叉 P07（疾病惡化）
d = {r["subject"]: r for r in rows}
assert d["P01"]["cr_month"] != "" and d["P10"]["first_response_month"] != "" and d["P07"]["stop_reason"] == "疾病惡化"
print("PASS sample-swimmer-s1-anatomy-selfcheck")
