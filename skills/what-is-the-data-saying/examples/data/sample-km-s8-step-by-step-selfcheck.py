#!/usr/bin/env python3
"""sample-km-s8-step-by-step-selfcheck.py：檢查虛構樣本 sample-km-s8-step-by-step.csv（數字未核）。
對應圖 S8。驗證 8 人資料列、逐步乘積、中位數第 7 月、設限者名單。
用法：python3 sample-km-s8-step-by-step-selfcheck.py
"""
CSV_NAME = "sample-km-s8-step-by-step.csv"

import csv, sys, math
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import numpy as np

path = Path(__file__).resolve().parent / (sys.argv[1] if len(sys.argv) > 1 else CSV_NAME)
STATUS = "虛構資料，數字未核"

def half_up(x, nd=0):
    d = Decimal(repr(float(x)))
    return float(d.quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))

def read_rows(head):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
    assert list(rows[0].keys()) == head, list(rows[0].keys())
    assert all(r["data_status"] == STATUS for r in rows)
    return rows

def km(time, event):
    time = np.asarray(time, float); event = np.asarray(event, int)
    order = np.argsort(time, kind="mergesort")
    time, event = time[order], event[order]
    rows = []; i = 0; n = len(time); S = 1.0; g = 0.0
    while i < n:
        t = time[i]; j = i
        while j < n and abs(time[j] - t) < 1e-12: j += 1
        d = int(event[i:j].sum()); at = n - i
        if d > 0:
            S = S * (1 - d / at)
            if at > d: g += d / (at * (at - d))
            rows.append(dict(t=float(t), n=at, d=d, S=S, g=g))
        i = j
    return rows

def S_at(rows, t):
    s = 1.0
    for r in rows:
        if r["t"] <= t + 1e-12: s = r["S"]
        else: break
    return s

def median(rows):
    for r in rows:
        if r["S"] <= 0.5 + 1e-12: return r["t"]
    return None

def at_risk(time, t):
    return int(np.sum(np.asarray(time, float) >= t - 1e-12))

def logrank(t1, e1, t2, e2):
    from scipy.stats import chi2
    t1=np.asarray(t1,float); e1=np.asarray(e1,int); t2=np.asarray(t2,float); e2=np.asarray(e2,int)
    times=np.unique(np.concatenate([t1[e1==1], t2[e2==1]]))
    O1=E1=V=0.0
    for t in times:
        d1=int(((t1==t)&(e1==1)).sum()); d2=int(((t2==t)&(e2==1)).sum()); d=d1+d2
        n1=int((t1>=t).sum()); n2=int((t2>=t).sum()); n=n1+n2
        if n==0 or d==0: continue
        e1_=d*n1/n; O1+=d1; E1+=e1_
        if n>1: V+=d*(n1/n)*(n2/n)*((n-d)/(n-1))
    if V<=0: return 0.0, 1.0
    stat=(O1-E1)**2/V
    return float(stat), float(chi2.sf(stat,1))

def cox_binary(time, event, x, entry=None):
    time=np.asarray(time,float); event=np.asarray(event,int); x=np.asarray(x,float)
    entry=np.zeros(len(time)) if entry is None else np.asarray(entry,float)
    b=0.0
    for _ in range(40):
        score=0.0; info=0.0
        for t in np.unique(time[event==1]):
            risk=(time>=t)&(entry<=t)
            if not risk.any(): continue
            xr=x[risk]; wr=np.exp(b*xr); sw=wr.sum()
            dmask=(time==t)&(event==1)&(entry<=t)
            d=int(dmask.sum())
            if d==0: continue
            mean=(xr*wr).sum()/sw
            score += (x[dmask].sum() - d*mean)
            info += d * (((xr**2)*wr).sum()/sw - mean**2)
        if info<=1e-12: break
        step=score/info; b+=step
        if abs(step)<1e-10: break
    se=math.sqrt(1/info) if info>1e-12 else float("nan")
    return dict(HR=math.exp(b), lo=math.exp(b-1.959964*se), hi=math.exp(b+1.959964*se))

def ci_greenwood_ll(rows, t, z=1.959964):
    s = 1.0; g = 0.0
    for r in rows:
        if r["t"] <= t + 1e-12: s, g = r["S"], r.get("g", 0.0)
        else: break
    if s >= 1.0 or s <= 0.0 or not np.isfinite(g) or g <= 0:
        return (s, s)
    se = math.sqrt(g) / abs(math.log(s))
    lo = s ** math.exp(z * se); hi = s ** math.exp(-z * se)
    return (lo, hi)

rows = read_rows(['subject', 'name', 'time', 'event', 'group', 'data_status'])
assert len(rows)==8
data={(r["name"], int(float(r["time"])), int(r["event"])) for r in rows}
expect={(d["name"], d["t"], d["event"]) for d in [{"name": "甲", "t": 6, "event": 1}, {"name": "乙", "t": 2, "event": 1}, {"name": "丙", "t": 9, "event": 0}, {"name": "丁", "t": 4, "event": 0}, {"name": "戊", "t": 7, "event": 1}, {"name": "己", "t": 12, "event": 0}, {"name": "庚", "t": 4, "event": 1}, {"name": "辛", "t": 10, "event": 1}]}
assert data==expect
time=np.array([float(r["time"]) for r in rows]); event=np.array([int(r["event"]) for r in rows])
kmr=km(time,event)
assert len(kmr)==5
for i, exp in enumerate([{"t": 2.0, "n": 8, "d": 1, "factor": "7/8", "S_before": 1.0, "S": 0.875}, {"t": 4.0, "n": 7, "d": 1, "factor": "6/7", "S_before": 0.875, "S": 0.75}, {"t": 6.0, "n": 5, "d": 1, "factor": "4/5", "S_before": 0.75, "S": 0.6}, {"t": 7.0, "n": 4, "d": 1, "factor": "3/4", "S_before": 0.6, "S": 0.45}, {"t": 10.0, "n": 2, "d": 1, "factor": "1/2", "S_before": 0.45, "S": 0.225}]):
    r=kmr[i]
    assert r["t"]==exp["t"] and r["n"]==exp["n"] and r["d"]==exp["d"]
    assert half_up(r["S"],3)==exp["S"]
assert median(kmr)==7.0
cens={(c["name"], c["t"]) for c in [{"name": "丙", "t": 9}, {"name": "丁", "t": 4}, {"name": "己", "t": 12}]}
got={(r["name"], int(float(r["time"]))) for r in rows if int(r["event"])==0}
assert cens==got
print("PASS sample-km-s8-step-by-step-selfcheck")
