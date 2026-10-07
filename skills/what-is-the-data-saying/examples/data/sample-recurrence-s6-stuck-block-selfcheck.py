#!/usr/bin/env python3
"""sample-recurrence-s6-stuck-block-selfcheck.py：圖 S6 自我檢查（停滯方塊）。
只用 Python 標準函式庫，從對應 CSV 獨立重算，與圖說／事實檔寫死的預期值比對。
用法：python3 sample-recurrence-s6-stuck-block-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "虛構資料，數字未核"
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def read_rows(fn):
    with open(os.path.join(HERE, fn), encoding="utf-8", newline="") as fh:
        first = fh.readline()
        chk("第一行標示虛構資料", first.startswith("# " + STATUS), first.strip()[:40])
        rows = list(csv.DictReader(fh))
    chk("每列 data_status 都是「" + STATUS + "」", all(r["data_status"] == STATUS for r in rows))
    return rows

def zscore(xs):
    n = len(xs); m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / n)
    return [(x - m) / sd for x in xs]

def embed(x, m=1, tau=1):
    n = len(x) - (m - 1) * tau
    return [[x[i + k * tau] for k in range(m)] for i in range(n)]

def dist(a, b):
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))

def recmat(x, eps, m=1, tau=1):
    V = embed(x, m, tau); n = len(V)
    R = [[dist(V[i], V[j]) <= eps for j in range(n)] for i in range(n)]
    return R

def rr(R):
    n = len(R); black = sum(1 for i in range(n) for j in range(n) if R[i][j])
    return black / (n * n)

def pct1(x):
    return f"{100 * x:.1f}%"

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)


rows = read_rows("sample-recurrence-s6-stuck-block.csv")
chk("300 點", len(rows) == 300)
zn = [float(r["z_normal"]) for r in rows]
zs = [float(r["z_stuck"]) for r in rows]
stuck = [r["in_stuck_window"] == "yes" for r in rows]
chk("卡住窗 50 點", sum(stuck) == 50, sum(stuck))
chk("卡住起迄", stuck.index(True) == 120 and (len(stuck) - 1 - stuck[::-1].index(True)) == 169)
EXPECT = {'正常（沒有停滯）': '14.3%', '第 120–169 點數值卡住不動': '16.6%'}
R0 = recmat(zn, 0.25, 1, 1)
R1 = recmat(zs, 0.25, 1, 1)
chk("正常遞迴率 " + EXPECT['正常（沒有停滯）'], pct1(rr(R0)) == EXPECT['正常（沒有停滯）'], pct1(rr(R0)))
chk("卡住遞迴率 " + EXPECT['第 120–169 點數值卡住不動'], pct1(rr(R1)) == EXPECT['第 120–169 點數值卡住不動'], pct1(rr(R1)))
done()

