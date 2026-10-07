#!/usr/bin/env python3
"""sample-recurrence-s5-period-spacing-selfcheck.py：圖 S5 自我檢查（週期間距）。
只用 Python 標準函式庫，從對應 CSV 獨立重算，與圖說／事實檔寫死的預期值比對。
用法：python3 sample-recurrence-s5-period-spacing-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

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


rows = read_rows("sample-recurrence-s5-period-spacing.csv")
xs = [float(r["z_value"]) for r in rows]
chk("300 點", len(xs) == 300)
R = recmat(xs, 0.3, 1, 1)
chk("遞迴率 18.6%", pct1(rr(R)) == "18.6%", pct1(rr(R)))
# 斜線黑格比例：對每個 offset k，主對角線平行線上黑格比例
def diag_rate(R, k):
    n = len(R); vals = [R[i][i + k] for i in range(n - k)]
    return sum(1 for v in vals if v) / len(vals)
peaks = [50, 100, 150]
rates = ['85.2%', '83.0%', '84.0%']
for k, want in zip(peaks, rates):
    got = pct1(diag_rate(R, k))
    chk(f"斜線距離 {k} 黑格比例 {want}", got == want, got)
chk("第一高峰 = 50", peaks[0] == 50)
done()

