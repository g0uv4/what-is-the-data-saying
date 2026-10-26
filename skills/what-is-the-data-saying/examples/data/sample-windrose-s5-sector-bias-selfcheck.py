#!/usr/bin/env python3
"""sample-windrose-s5-sector-bias-selfcheck.py：圖 S5 自我檢查。
從 sample-windrose-s5-sector-bias.csv 核對 16 格、三向與二向平均，以及北、北北東、北北西、西的存檔。
只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-windrose-s5-sector-bias-selfcheck.py   全部通過時結束碼為 0。
四捨五入後的 16 格清單不是存檔字串。
"""

import csv, os, sys
from decimal import Decimal
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-windrose-s5-sector-bias.csv"
COLS = ["sector16_center_deg", "n_10deg_dirs", "pct_total_16"]
FACTS16 = ["14.01", "7.36", "7.54", "6.21", "5.87", "0.8", "0.88", "1.27", "4.01", "2.69", "3.33", "5.87", "13.03", "5.79", "5.45", "6.93"]
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked(stored):
    skip("課程稿北 14.0、北北東 7.4、北北西 6.9、西 13.0", "存檔是 14.0137、7.36251、6.92583、13.0312")
    skip("facts 14.01、7.36、6.93、13.03", "不是存檔字串")
    skip("facts 16 格清單", "存檔是 " + "、".join(stored) + "，不是 " + "、".join(FACTS16))
    skip("課程稿三向平均 9.2、二向 4.5 與 facts 9.23、4.51", "平均是 9.230715 與 4.5102585")
    skip("餘數寫成 9.0% 或 facts 8.95", "100 減總比例是 8.954038；這一檔沒有靜風欄")
    skip("真靜風 0.23 與課程稿 0.2%", "沒有任何練習 CSV 有真靜風欄")
    skip("高雄觀測筆數 87022", "不在這一檔")

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def end(stored):
    unchecked(stored)
    done()

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("sector16_center_deg,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("16 列", len(rows) == 16, len(rows))
if not cols_ok or len(rows) != 16:
    end([])
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end([r["pct_total_16"] for r in rows])
centers = [r["sector16_center_deg"] for r in rows]
dirs = [r["n_10deg_dirs"] for r in rows]
expect_c = ["0", "22.5", "45", "67.5", "90", "112.5", "135", "157.5", "180", "202.5", "225", "247.5", "270", "292.5", "315", "337.5"]
chk("中心從 0 到 337.5、步進 22.5", centers == expect_c)
chk("每格含幾個 10 度風向是 3、2、2、2 重複四次", dirs == ["3", "2", "2", "2"] * 4, dirs)
by = {r["sector16_center_deg"]: r["pct_total_16"] for r in rows}
chk("北 0 度 14.0137、西 270 度 13.0312", by["0"] == "14.0137" and by["270"] == "13.0312", (by["0"], by["270"]))
chk("北北東 22.5 度 7.36251、北北西 337.5 度 6.92583", by["22.5"] == "7.36251" and by["337.5"] == "6.92583", (by["22.5"], by["337.5"]))
three = [Decimal(r["pct_total_16"]) for r in rows if r["n_10deg_dirs"] == "3"]
two = [Decimal(r["pct_total_16"]) for r in rows if r["n_10deg_dirs"] == "2"]
mean3 = sum(three, Decimal(0)) / Decimal(len(three))
mean2 = sum(two, Decimal(0)) / Decimal(len(two))
chk("三向格 4 個、平均 9.230715", len(three) == 4 and mean3 == Decimal("9.230715"), mean3)
chk("二向格 12 個、平均 4.5102585", len(two) == 12 and mean2 == Decimal("4.5102585"), mean2)
tot = sum((Decimal(r["pct_total_16"]) for r in rows), Decimal(0))
chk("16 格加總 91.045962、餘數 8.954038", tot == Decimal("91.045962") and Decimal(100) - tot == Decimal("8.954038"), (tot, Decimal(100) - tot))
chk("三向平均大於二向平均", mean3 > mean2)
end([r["pct_total_16"] for r in rows])
