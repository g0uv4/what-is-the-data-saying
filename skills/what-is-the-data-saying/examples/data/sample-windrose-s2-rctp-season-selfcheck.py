#!/usr/bin/env python3
"""sample-windrose-s2-rctp-season-selfcheck.py：圖 S2 自我檢查。
從 sample-windrose-s2-rctp-season.csv 核對冬夏各 36 格、頂格存檔與扇區加總。
只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-windrose-s2-rctp-season-selfcheck.py   全部通過時結束碼為 0。
季節依臺北時間月份。頁上讀數用這一檔的加總。
"""

import csv, os, sys
from decimal import Decimal
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-windrose-s2-rctp-season.csv"
COLS = ["season", "sector_center_deg", "pct_bf1to3", "pct_bf4to6", "pct_bf7plus", "pct_total"]
WINTER = "冬季（12–2 月）"
SUMMER = "夏季（6–8 月）"
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("課程稿與說明表冬季 19.0%", "存檔字串是 19.03，不是 19.0")
    skip("課程稿與說明表夏季 11.0% 與 facts 10.99", "存檔字串是 10.9934")
    skip("facts 冬季 0–90 度 80.7、180–260 度 4.3、餘數 3.24", "加總是 80.66568、4.288189、餘數 3.239571")
    skip("facts 夏季 0–90 度 19.0、180–260 度 44.1、餘數 5.14", "加總是 19.01943、44.12035、餘數 5.14128")
    skip("冬季觀測 21361、夏季 21804", "這一檔沒有筆數欄")

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def end():
    unchecked()
    done()

def band(rows, lo, hi):
    return sum((Decimal(r["pct_total"]) for r in rows if lo <= int(r["sector_center_deg"]) <= hi), Decimal(0))

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("season,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("72 列", len(rows) == 72, len(rows))
if not cols_ok or len(rows) != 72:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
winter = [r for r in rows if r["season"] == WINTER]
summer = [r for r in rows if r["season"] == SUMMER]
chk("冬夏各 36 列、季節字串相符", len(winter) == 36 and len(summer) == 36 and len(winter) + len(summer) == 72, (len(winter), len(summer)))
expect_c = list(range(0, 360, 10))
w_ok = [int(r["sector_center_deg"]) for r in winter] == expect_c
s_ok = [int(r["sector_center_deg"]) for r in summer] == expect_c
chk("兩季中心都是 0 到 350、步進 10", w_ok and s_ok)
if not (len(winter) == 36 and len(summer) == 36 and w_ok and s_ok):
    end()
wtop = max(winter, key=lambda r: Decimal(r["pct_total"]))
stop = max(summer, key=lambda r: Decimal(r["pct_total"]))
chk("冬季唯一最大是 40 度、存檔字串 19.03", wtop["sector_center_deg"] == "40" and wtop["pct_total"] == "19.03" and sum(1 for r in winter if r["pct_total"] == "19.03") == 1, wtop["pct_total"])
chk("夏季唯一最大是 240 度、存檔字串 10.9934", stop["sector_center_deg"] == "240" and stop["pct_total"] == "10.9934" and sum(1 for r in summer if Decimal(r["pct_total"]) == Decimal("10.9934")) == 1, stop["pct_total"])
wsum = sum((Decimal(r["pct_total"]) for r in winter), Decimal(0))
ssum = sum((Decimal(r["pct_total"]) for r in summer), Decimal(0))
chk("冬季總比例 96.760429、餘數 3.239571", wsum == Decimal("96.760429") and Decimal(100) - wsum == Decimal("3.239571"), (wsum, Decimal(100) - wsum))
chk("夏季總比例 94.85872、餘數 5.14128", ssum == Decimal("94.85872") and Decimal(100) - ssum == Decimal("5.14128"), (ssum, Decimal(100) - ssum))
chk("冬季 0–90 度 80.66568、180–260 度 4.288189", band(winter, 0, 90) == Decimal("80.66568") and band(winter, 180, 260) == Decimal("4.288189"), (band(winter, 0, 90), band(winter, 180, 260)))
chk("夏季 0–90 度 19.01943、180–260 度 44.12035", band(summer, 0, 90) == Decimal("19.01943") and band(summer, 180, 260) == Decimal("44.12035"), (band(summer, 0, 90), band(summer, 180, 260)))
def mxbin(part):
    return max(abs(Decimal(r["pct_bf1to3"]) + Decimal(r["pct_bf4to6"]) + Decimal(r["pct_bf7plus"]) - Decimal(r["pct_total"])) for r in part)
chk("三級與總比例最大絕對差 冬季 0.0000286、夏季 0.00001", mxbin(winter) == Decimal("0.0000286") and mxbin(summer) == Decimal("0.00001"), (mxbin(winter), mxbin(summer)))
end()
