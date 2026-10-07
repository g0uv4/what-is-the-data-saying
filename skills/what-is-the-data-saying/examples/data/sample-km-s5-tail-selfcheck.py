#!/usr/bin/env python3
"""sample-km-s5-tail-selfcheck.py：檢查虛構樣本 sample-km-s5-tail.csv（數字未核）。
對應圖 S5。驗證中位數、風險人數首次 <5 的時間、最後事件、尾端設限人數、風險人數表。
用法：python3 sample-km-s5-tail-selfcheck.py
"""
CSV_NAME = "sample-km-s5-tail.csv"

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

rows = read_rows(['subject', 'time', 'event', 'group', 'data_status'])
time=np.array([float(r["time"]) for r in rows]); event=np.array([int(r["event"]) for r in rows])
assert len(rows)==40 and int(event.sum())==36 and int((event==0).sum())==4
kmr=km(time,event)
assert half_up(median(kmr),1)==8.5
# 風險人數首次 <5
t5=None
for t in np.arange(0, float(time.max())+0.05, 0.1):
    if at_risk(time,t)<5:
        t5=half_up(t,1); break
assert t5==22.2
last=kmr[-1]
assert half_up(last["t"],1)==27.3
assert last["n"]==3 and last["d"]==1
assert half_up(last["S"],3)==0.07
assert half_up(float(time.max()),1)==40.6
assert at_risk(time, last["t"]+0.1)==2
for t,n in {"0.0": 40, "6.0": 24, "12.0": 13, "18.0": 9, "24.0": 4, "30.0": 2, "36.0": 2}.items():
    assert at_risk(time, float(t))==n
print("PASS sample-km-s5-tail-selfcheck")
