#!/usr/bin/env python3
"""sample-stripes-s2-stripes-vs-line-selfcheck.py：圖 S2 自我檢查。
從 sample-stripes-s2-stripes-vs-line.csv 核對最冷與最熱的存檔，以及兩者的差。
差是 1.25−(−0.42)，恰好 1.67，不是再四捨五入。
只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-stripes-s2-stripes-vs-line-selfcheck.py   全部通過時結束碼為 0。
"""

import csv, os, sys
from decimal import Decimal
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-stripes-s2-stripes-vs-line.csv"
COLS = ["year", "anomaly_c"]
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("條紋只說變暖", "外觀，不在練習 CSV")
    skip("疊細線以後色弱讀不讀得懂", "外觀，不在練習 CSV")

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
chk("年份沒有重複", len(set(years)) == 176)
vals = [(int(r["year"]), r["anomaly_c"], Decimal(r["anomaly_c"])) for r in rows]
cold = min(vals, key=lambda t: t[2])
hot = max(vals, key=lambda t: t[2])
chk("唯一最冷是 1917、存檔 -0.42", cold[0] == 1917 and cold[1] == "-0.42" and sum(1 for t in vals if t[2] == cold[2]) == 1)
chk("唯一最熱是 2024、存檔 1.25", hot[0] == 2024 and hot[1] == "1.25" and sum(1 for t in vals if t[2] == hot[2]) == 1)
diff = Decimal(hot[1]) - Decimal(cold[1])
chk("1.25 減 −0.42 恰好是 1.67", diff == Decimal("1.67"), diff)
chk("差的百分之一度是整數 167", (Decimal(hot[1]) * 100) - (Decimal(cold[1]) * 100) == Decimal("167"))
chk("167／100 等於這個差", Decimal(167) / Decimal(100) == diff)
chk("差的小數位恰好兩位", diff.as_tuple().exponent == -2, diff.as_tuple().exponent)
end()
