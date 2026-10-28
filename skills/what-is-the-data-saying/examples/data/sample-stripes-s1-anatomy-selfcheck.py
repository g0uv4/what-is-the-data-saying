#!/usr/bin/env python3
"""sample-stripes-s1-anatomy-selfcheck.py：圖 S1 自我檢查。
從 sample-stripes-s1-anatomy.csv 核對 NOAA 全球陸海年均溫距平的存檔字串。
年份 1850–2025，176 列。最冷、最熱、絕對值最大、正負與零的筆數，都從存檔重算。
只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-stripes-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。
頁上讀數用存檔字串或由存檔重算。課程稿的看圖判讀不是存檔。
"""

import csv, os, sys
from decimal import Decimal
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-stripes-s1-anatomy.csv"
COLS = ["year", "anomaly_c"]
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("圖 R1 前段淺藍、末段幾乎全是深紅", "看圖判讀，不在練習 CSV")
    skip("圖 R2 最右一條最紅", "看圖判讀；資料來源與基準期無法確認，不在這一檔")
    skip("Hawkins 2018-05-22 發表", "不在練習 CSV")
    skip("官方要求署名並連到 showyourstripes.info", "授權註記的要求，不是這一檔的欄位")
    skip("把 1937 與 1947 的存檔寫成 -0.0", "這一檔的字串是 -0")
    skip("圖上用了哪一張 ColorBrewer 色票", "不在練習 CSV")
    skip("Hawkins 原帖寫了哪些地區", "貼文內容不在練習 CSV")
    skip("圖 R3 攝於 2021-08-04、牆上條紋設計是 Hawkins", "授權註記，不在練習 CSV")
    skip("圖 R4 三列中文基準期標籤", "圖檔改作，不在練習 CSV")

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
chk("欄位", cols_ok, list(rows[0].keys()) if rows else None)
chk("176 列", len(rows) == 176, len(rows))
if not cols_ok or len(rows) != 176:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
years = [int(r["year"]) for r in rows]
chk("年份連續 1850 到 2025", years == list(range(1850, 2026)), (years[0], years[-1], len(years)))
vals = [(int(r["year"]), r["anomaly_c"], Decimal(r["anomaly_c"])) for r in rows]
cold = min(vals, key=lambda t: t[2])
hot = max(vals, key=lambda t: t[2])
n_cold = sum(1 for t in vals if t[2] == cold[2])
n_hot = sum(1 for t in vals if t[2] == hot[2])
chk("唯一最冷是 1917、存檔 -0.42", cold[0] == 1917 and cold[1] == "-0.42" and n_cold == 1, (cold[0], cold[1], n_cold))
chk("唯一最熱是 2024、存檔 1.25", hot[0] == 2024 and hot[1] == "1.25" and n_hot == 1, (hot[0], hot[1], n_hot))
abs_max = max(abs(t[2]) for t in vals)
abs_years = [t[0] for t in vals if abs(t[2]) == abs_max]
chk("絕對值最大恰為 1.25，只有 2024", abs_max == Decimal("1.25") and abs_years == [2024], (abs_max, abs_years))
zeros = [(t[0], t[1]) for t in vals if t[1] == "-0"]
chk("存檔字串 -0 只有 1937 與 1947", zeros == [(1937, "-0"), (1947, "-0")], zeros)
chk("這兩年的 Decimal 是 0", all(t[2] == 0 and t[1] == "-0" for t in vals if t[0] in (1937, 1947)))
gt = sum(1 for t in vals if t[2] > 0)
eq = sum(1 for t in vals if t[2] == 0)
lt = sum(1 for t in vals if t[2] < 0)
chk("距平大於 0 是 71 年", gt == 71, gt)
chk("距平等於 0 是 2 年", eq == 2, eq)
chk("距平小於 0 是 103 年", lt == 103, lt)
chk("71、2、103 加總是 176", gt + eq + lt == 176)
def places(s):
    if "." not in s:
        return 0
    return len(s.split(".", 1)[1])
pc = {0: 0, 1: 0, 2: 0}
for t in vals:
    pc[places(t[1])] = pc.get(places(t[1]), 0) + 1
chk("小數位是 159 個兩位、15 個一位、2 個沒有小數點", pc == {0: 2, 1: 15, 2: 159} and sum(pc.values()) == 176, pc)
pos = [t for t in vals if t[2] > 0]
minpos = min(pos, key=lambda t: t[2])
n_minpos = sum(1 for t in pos if t[2] == minpos[2])
chk("最小正值是 1938、存檔 0.01", minpos[0] == 1938 and minpos[1] == "0.01" and n_minpos == 1, (minpos[0], minpos[1], n_minpos))
end()
