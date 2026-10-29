#!/usr/bin/env python3
"""sample-stripes-s5-bar-instead-selfcheck.py：圖 S5 自我檢查。
從 sample-stripes-s5-bar-instead.csv 核對 2016–2025 的存檔字串。
2016 與 2019 都是 0.99。2020 減 2016 恰好 0.02。
只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-stripes-s5-bar-instead-selfcheck.py   全部通過時結束碼為 0。
"""

import csv, os, sys
from decimal import Decimal
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-stripes-s5-bar-instead.csv"
COLS = ["year", "anomaly_c"]
EXP = {
    2016: "0.99", 2017: "0.92", 2018: "0.86", 2019: "0.99", 2020: "1.01",
    2021: "0.86", 2022: "0.89", 2023: "1.17", 2024: "1.25", 2025: "1.12",
}
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("2016、2019、2020 的條紋幾乎同色", "外觀，不在練習 CSV")

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
chk("10 列", len(rows) == 10, len(rows))
if not cols_ok or len(rows) != 10:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
years = [int(r["year"]) for r in rows]
chk("年份連續 2016 到 2025", years == list(range(2016, 2026)), years)
got = {int(r["year"]): r["anomaly_c"] for r in rows}
chk("十年存檔字串與表一致", got == EXP, got)
chk("2016 與 2019 的存檔都是 0.99", got[2016] == "0.99" and got[2019] == "0.99")
chk("2016 與 2019 的差是 0", Decimal(got[2016]) - Decimal(got[2019]) == 0)
chk("2020 減 2016 恰好 0.02", Decimal(got[2020]) - Decimal(got[2016]) == Decimal("0.02"), Decimal(got[2020]) - Decimal(got[2016]))
chk("2018 與 2021 的存檔都是 0.86", got[2018] == "0.86" and got[2021] == "0.86")
mx = max(rows, key=lambda r: Decimal(r["anomaly_c"]))
n_mx = sum(1 for r in rows if Decimal(r["anomaly_c"]) == Decimal(mx["anomaly_c"]))
chk("這十年唯一最大是 2024、存檔 1.25", int(mx["year"]) == 2024 and mx["anomaly_c"] == "1.25" and n_mx == 1, (mx["year"], mx["anomaly_c"], n_mx))
chk("這十年每一筆都大於 0", all(Decimal(r["anomaly_c"]) > 0 for r in rows))
chk("每一筆都是恰好兩位小數的存檔", all(len(r["anomaly_c"].split(".", 1)[1]) == 2 for r in rows))
end()
