#!/usr/bin/env python3
"""sample-km-s7-y-axis-selfcheck.py：檢查虛構樣本 sample-km-s7-y-axis.csv（數字未核）。
對應圖 S7。驗證兩組各 400 人、第 24 月存活差 3.5 百分點、對數等級檢定、縱軸佔比。
圖說 P=0.092 為四捨五入到小數第 3 位（精確 0.0917）。
用法：python3 sample-km-s7-y-axis-selfcheck.py
"""
CSV_NAME = "sample-km-s7-y-axis.csv"

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
A=[r for r in rows if r["group"]=="甲組"]; B=[r for r in rows if r["group"]=="乙組"]
assert len(A)==400 and len(B)==400
ta=np.array([float(r["time"]) for r in A]); ea=np.array([int(r["event"]) for r in A])
tb=np.array([float(r["time"]) for r in B]); eb=np.array([int(r["event"]) for r in B])
ra, rb = km(ta,ea), km(tb,eb)
sa, sb = S_at(ra,24), S_at(rb,24)
assert half_up(sa,3)==0.923 and half_up(sb,3)==0.888
assert half_up(100*(sa-sb),1)==3.5
chi2,p=logrank(ta,ea,tb,eb)
assert half_up(p,4)==0.0917
assert half_up(p,3)==0.092
left_share=half_up((sa-sb)/(1.01-0.6)*100,1)
right_share=half_up((sa-sb)/(1.01-0.0)*100,1)
assert left_share==8.5 and right_share==3.5
print("PASS sample-km-s7-y-axis-selfcheck")
