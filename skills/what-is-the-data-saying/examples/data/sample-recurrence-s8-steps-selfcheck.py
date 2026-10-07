#!/usr/bin/env python3
"""sample-recurrence-s8-steps-selfcheck.py：圖 S8 自我檢查（製作步驟數字）。
只用 Python 標準函式庫，從對應 CSV 獨立重算，與圖說／事實檔寫死的預期值比對。
用法：python3 sample-recurrence-s8-steps-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

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


rows = read_rows("sample-recurrence-s8-steps.csv")
chk("8 點", len(rows) == 8)
raw = [int(r["raw"]) for r in rows]
chk("原始讀數", raw == [12, 15, 13, 12, 15, 13, 12, 16], raw)
xs = [float(r["z"]) for r in rows]
chk("標準化", [f"{x:.2f}" for x in xs] == ['-1.00', '1.00', '-0.33', '-1.00', '1.00', '-0.33', '-1.00', '1.67'], [f"{x:.2f}" for x in xs])
# 重算平均／標準差
m = sum(raw) / len(raw); sd = math.sqrt(sum((x - m) ** 2 for x in raw) / len(raw))
chk("平均 13.50", f"{m:.2f}" == "13.50")
chk("標準差 1.50", f"{sd:.2f}" == "1.50")
V = embed(xs, 2, 1)
chk("狀態數 7", len(V) == 7)
chk("狀態 1 = (-1.00, 1.00)", [f"{v:.2f}" for v in V[0]] == ['-1.00', '1.00'])
D14 = dist(V[0], V[3]); D17 = dist(V[0], V[6])
chk("距離 (1,4) = 0.00", f"{D14:.2f}" == "0.00")
chk("距離 (1,7) = 0.67", f"{D17:.2f}" == "0.67")
R = [[dist(V[i], V[j]) <= 0.5 for j in range(len(V))] for i in range(len(V))]
black = sum(1 for i in range(len(V)) for j in range(len(V)) if R[i][j])
chk("黑格 13／49", black == 13 and len(V) * len(V) == 49)
chk("遞迴率 26.5%", pct1(black / (len(V) * len(V))) == "26.5%")
upper = [[i + 1, j + 1] for i in range(len(V)) for j in range(len(V)) if R[i][j] and j > i]
chk("上三角黑對", upper == [[1, 4], [2, 5], [3, 6]], upper)
done()

