#!/usr/bin/env python3
"""sample-seasonal-subseries-sim-s7-acf-lag-subseries-selfcheck.py：圖 S7 自我檢查。
從 sample-seasonal-subseries-sim-s7-acf-lag-subseries.csv 獨立重算（自寫滯後 12 皮爾森相關與自相關），與圖說數字比對。
只需 Python 標準函式庫。
用法：python3 sample-seasonal-subseries-sim-s7-acf-lag-subseries-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "虛構資料，數字未核"
FN = "sample-seasonal-subseries-sim-s7-acf-lag-subseries.csv"
RESULTS = []

N_EXPECT = 120
ACF12 = 0.752
ACF24 = 0.701
ACF6 = -0.793
LAG12_PEARSON = 0.82
CI_HALF = 0.179

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def read_rows(fn):
    path = os.path.join(HERE, fn)
    with open(path, encoding="utf-8", newline="") as fh:
        first = fh.readline()
        chk("第一行標示資料性質", first.startswith("# " + STATUS.split("，")[0]))
        rows = list(csv.DictReader(fh))
    chk("每列 data_status 正確", all(r["data_status"] == STATUS for r in rows))
    chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
    return rows

def mean(xs):
    return math.fsum(xs) / len(xs)

def pearson(a, b):
    n = len(a)
    ma, mb = mean(a), mean(b)
    num = math.fsum((a[i] - ma) * (b[i] - mb) for i in range(n))
    da = math.sqrt(math.fsum((v - ma) ** 2 for v in a))
    db = math.sqrt(math.fsum((v - mb) ** 2 for v in b))
    return num / (da * db)

def acf_at(x, k):
    # r(k)＝C(k)/C(0)，C(k)＝(1/n)Σ(x_t−μ)(x_(t+k)−μ)
    n = len(x)
    mu = mean(x)
    xc = [v - mu for v in x]
    c0 = math.fsum(v * v for v in xc) / n
    ck = math.fsum(xc[t] * xc[t + k] for t in range(n - k)) / n
    return ck / c0

def season_matrix(rows, col, season_key="month"):
    years = sorted({r["year"] for r in rows}, key=float)
    n_season = max(int(r[season_key]) for r in rows)
    index = {y: i for i, y in enumerate(years)}
    grid = [[0.0] * n_season for _ in years]
    for r in rows:
        grid[index[r["year"]]][int(r[season_key]) - 1] = float(r[col])
    return grid

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
y = [v for row in season_matrix(rows, "value") for v in row]
n = len(y)
chk("120 點", n == N_EXPECT)
chk("自相關 12／24／6", [round(acf_at(y, k), 3) for k in (12, 24, 6)] == [ACF12, ACF24, ACF6])
chk("滯後 12 相關", round(pearson(y[:-12], y[12:]), 3) == LAG12_PEARSON)
chk("信心帶半寬", round(1.96 / math.sqrt(n), 3) == CI_HALF)
done()
