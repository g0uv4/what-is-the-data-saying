#!/usr/bin/env python3
"""sample-autocorr-s4-sample-size-ci-selfcheck.py：圖 S4 自我檢查。
從 sample-autocorr-s4-sample-size-ci.csv 獨立重算（自寫自相關、偏自相關〔Durbin–Levinson〕、信心半寬 1.96/√n），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-autocorr-s4-sample-size-ci-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
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

def col(rows, k):
    return [float(r[k]) for r in rows if r[k] != ""]

def mean(xs):
    return sum(xs) / len(xs)

def acf(x, m):
    # r(k)＝C(k)/C(0)，C(k)＝(1/n)Σ(x_t−μ)(x_(t+k)−μ)
    n = len(x)
    mu = mean(x)
    xc = [v - mu for v in x]
    c0 = sum(v * v for v in xc) / n
    out = [1.0]
    for k in range(1, m + 1):
        ck = sum(xc[t] * xc[t + k] for t in range(n - k)) / n
        out.append(ck / c0)
    return out

def pacf(x, m):
    # Durbin–Levinson 遞迴
    r = acf(x, m)
    out = [1.0, r[1]]
    phi = [r[1]]
    for k in range(2, m + 1):
        num = r[k] - sum(phi[j] * r[k - 1 - j] for j in range(k - 1))
        den = 1.0 - sum(phi[j] * r[j + 1] for j in range(k - 1))
        pkk = num / den
        phi = [phi[j] - pkk * phi[k - 2 - j] for j in range(k - 1)] + [pkk]
        out.append(pkk)
    return out

def half(n):
    return 1.96 / math.sqrt(n)

def eq(name, got, want, nd=3):
    g = float(round(got, nd)) + 0.0
    chk(f"{name}≈{want}", g == want, g)

def allclose(a, b, rtol=1e-05, atol=1e-08):
    if hasattr(a, "__len__") and not isinstance(a, (str, bytes)):
        return all(abs(x - y) <= atol + rtol * abs(y) for x, y in zip(a, b)) and len(a) == len(b)
    return abs(a - b) <= atol + rtol * abs(b)

def pearson(a, b):
    n = len(a)
    ma, mb = mean(a), mean(b)
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    da = math.sqrt(sum((v - ma) ** 2 for v in a))
    db = math.sqrt(sum((v - mb) ** 2 for v in b))
    return num / (da * db)

def argmax(seq):
    best_i, best = 0, seq[0]
    for i, v in enumerate(seq):
        if v > best:
            best_i, best = i, v
    return best_i

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows("sample-autocorr-s4-sample-size-ci.csv")
x = [float(r["x"]) for r in rows if r["series_n"] == "50"]
chk("n＝50 長度正確", len(x) == 50, len(x))
eq("n＝50 信心半寬", half(len(x)), 0.2772, 4)
eq("n＝50 滯後 1", acf(x, 25)[1], 0.026)
x = [float(r["x"]) for r in rows if r["series_n"] == "200"]
chk("n＝200 長度正確", len(x) == 200, len(x))
eq("n＝200 信心半寬", half(len(x)), 0.1386, 4)
eq("n＝200 滯後 1", acf(x, 25)[1], 0.04)
x = [float(r["x"]) for r in rows if r["series_n"] == "800"]
chk("n＝800 長度正確", len(x) == 800, len(x))
eq("n＝800 信心半寬", half(len(x)), 0.0693, 4)
eq("n＝800 滯後 1", acf(x, 25)[1], -0.025)
done()
