#!/usr/bin/env python3
"""sample-windrose-s1-rctp-36sector-selfcheck.py：圖 S1 自我檢查。
從 sample-windrose-s1-rctp-36sector.csv 核對 36 格、040 度存檔、三級加總、餘數與 0–90 度加總。
只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-windrose-s1-rctp-36sector-selfcheck.py   全部通過時結束碼為 0。
數字由本專案依愛荷華環境網機場例行天氣報告計算。頁上讀數用這一檔的加總，不用四捨五入記載。
"""

import csv, os, sys
from decimal import Decimal
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-windrose-s1-rctp-36sector.csv"
COLS = ["sector_center_deg", "pct_bf1to3", "pct_bf4to6", "pct_bf7plus", "pct_total"]
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("課程稿與說明表 11.8%", "存檔字串是 11.8286，不是 11.8")
    skip("facts 頂格 11.83", "存檔字串是 11.8286，不是 11.83")
    skip("facts 靜風與風向不定 4.44 與課程稿 4.4%", "100 減總比例是 4.43558；這一檔沒有靜風欄，也沒有風向不定欄")
    skip("facts 蒲福 4–6 的 47.87 與 7 以上的 0.51", "三級加總是 47.8653549 與 0.50811211")
    skip("facts 中心 0–90 度 55.3", "含 90 度的加總是 55.34846")
    skip("觀測筆數 86595", "不在這一檔；只在跑道覆蓋率那一檔")
    skip("真靜風 0.12 與課程稿 0.1%", "沒有任何練習 CSV 有真靜風欄")

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
    chk("第一行是表頭", first.startswith("sector_center_deg,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("36 列", len(rows) == 36, len(rows))
if not cols_ok or len(rows) != 36:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
centers = [int(r["sector_center_deg"]) for r in rows]
chk("中心 0 到 350、步進 10", centers == list(range(0, 360, 10)), centers[0] if centers else None)
totals = [Decimal(r["pct_total"]) for r in rows]
top_i = max(range(36), key=lambda i: totals[i])
chk(
    "唯一最大是 40 度、存檔字串 11.8286",
    centers[top_i] == 40 and rows[top_i]["pct_total"] == "11.8286" and totals.count(totals[top_i]) == 1,
    rows[top_i]["pct_total"],
)
b1 = sum((Decimal(r["pct_bf1to3"]) for r in rows), Decimal(0))
b4 = sum((Decimal(r["pct_bf4to6"]) for r in rows), Decimal(0))
b7 = sum((Decimal(r["pct_bf7plus"]) for r in rows), Decimal(0))
chk(
    "三級加總 47.190954、47.8653549、0.50811211",
    b1 == Decimal("47.190954") and b4 == Decimal("47.8653549") and b7 == Decimal("0.50811211"),
    (b1, b4, b7),
)
tot = sum(totals, Decimal(0))
chk("總比例加總 95.56442", tot == Decimal("95.56442"), tot)
rem = Decimal(100) - tot
chk("餘數 4.43558", rem == Decimal("4.43558"), rem)
mx = max(abs(Decimal(r["pct_bf1to3"]) + Decimal(r["pct_bf4to6"]) + Decimal(r["pct_bf7plus"]) - Decimal(r["pct_total"])) for r in rows)
chk("三級與總比例最大絕對差 0.0000363", mx == Decimal("0.0000363"), mx)
arc = sum((Decimal(r["pct_total"]) for r in rows if int(r["sector_center_deg"]) <= 90), Decimal(0))
chk("中心 0 到 90 度（含）加總 55.34846", arc == Decimal("55.34846"), arc)
end()
