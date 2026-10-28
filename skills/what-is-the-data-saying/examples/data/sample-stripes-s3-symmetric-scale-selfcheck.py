#!/usr/bin/env python3
"""sample-stripes-s3-symmetric-scale-selfcheck.py：圖 S3 自我檢查。
從 sample-stripes-s3-symmetric-scale.csv 核對最小最大的中點，以及高於 0、低於中點的年份。
中點是 (−0.42+1.25)/2，恰好 0.415。那樣的年份是 42 個，最早 1877、最晚 2000。
1877 到 2000 之間距平大於 0 的年份是 46 個，不是 42。
除法用 decimal，有效位數 50。只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-stripes-s3-symmetric-scale-selfcheck.py   全部通過時結束碼為 0。
"""

import csv, os, sys
from decimal import Decimal, getcontext
getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-stripes-s3-symmetric-scale.csv"
COLS = ["year", "anomaly_c"]
BAND = (1877, 1878, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1952, 1953, 1957, 1958, 1959, 1961, 1962, 1963, 1969, 1970, 1972, 1973, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1991, 1992, 1993, 1994, 1996, 1999, 2000)
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("這 42 年被畫成藍色", "外觀，不在練習 CSV")
    skip("白落在 +0.415 的色階畫面", "外觀，不在練習 CSV")

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def end():
    unchecked()
    done()

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first == "year,anomaly_c\n")
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("176 列", len(rows) == 176, len(rows))
if not cols_ok or len(rows) != 176:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
years = [int(r["year"]) for r in rows]
chk("年份連續 1850 到 2025", years == list(range(1850, 2026)))
vals = [(int(r["year"]), Decimal(r["anomaly_c"])) for r in rows]
lo = min(t[1] for t in vals)
hi = max(t[1] for t in vals)
mid = (lo + hi) / 2
chk("最小是 −0.42、最大是 1.25", lo == Decimal("-0.42") and hi == Decimal("1.25"), (lo, hi))
chk("中點恰好 0.415", mid == Decimal("0.415"), mid)
chk("中點的小數位恰好三位", mid.as_tuple().exponent == -3, mid.as_tuple().exponent)
chk("中點不是 0", mid != 0)
band = [t[0] for t in vals if t[1] > 0 and t[1] < mid]
chk("高於 0 且低於中點的年份恰好 42 個", len(band) == 42, len(band))
chk("這 42 年最早 1877、最晚 2000", band[0] == 1877 and band[-1] == 2000, (band[0], band[-1]))
chk("這 42 年就是這份清單", tuple(band) == BAND)
span = [t[0] for t in vals if 1877 <= t[0] <= 2000 and t[1] > 0]
chk("1877 到 2000 之間距平大於 0 是 46 年", len(span) == 46, len(span))
chk("46 不等於 42", len(span) != len(band))
warm = sum(1 for t in vals if t[1] > 0)
chk("全期距平大於 0 是 71 年", warm == 71, warm)
inside = all(0 < t[1] < mid for t in vals if t[0] in BAND)
chk("清單裡的每一年都落在 0 與中點之間", inside and len(BAND) == 42)
end()
