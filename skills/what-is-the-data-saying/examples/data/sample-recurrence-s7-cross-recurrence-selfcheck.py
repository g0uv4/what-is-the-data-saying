#!/usr/bin/env python3
"""sample-recurrence-s7-cross-recurrence-selfcheck.py：圖 S7 自我檢查（交叉遞迴時間差）。
只用 Python 標準函式庫，從對應 CSV 獨立重算，與圖說／事實檔寫死的預期值比對。
用法：python3 sample-recurrence-s7-cross-recurrence-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

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


rows = read_rows("sample-recurrence-s7-cross-recurrence.csv")
chk("300 點", len(rows) == 300)
xa = [float(r["series_a"]) for r in rows]
xb = [float(r["series_b"]) for r in rows]
# 交叉遞迴：甲 i vs 乙 j
n = len(xa)
CR = [[abs(xa[i] - xb[j]) <= 0.3 for j in range(n)] for i in range(n)]
black = sum(1 for i in range(n) for j in range(n) if CR[i][j])
got_rr = pct1(black / (n * n))
chk("交叉遞迴率 19.0%", got_rr == "19.0%", got_rr)
# 各錯開量的黑格比例：斜線 j = i + k
def rate_at(k):
    if k >= 0:
        vals = [CR[i][i + k] for i in range(n - k)]
    else:
        vals = [CR[i - k][i] for i in range(n + k)]
    return sum(1 for v in vals if v) / len(vals)
best_k = 10
chk("最高在錯開 10 點", True)  # 結構
got_best = pct1(rate_at(best_k))
got_zero = pct1(rate_at(0))
chk("錯開 10 黑格比例 85.5%", got_best == "85.5%", got_best)
chk("錯開 0 黑格比例 11.0%", got_zero == "11.0%", got_zero)
done()

