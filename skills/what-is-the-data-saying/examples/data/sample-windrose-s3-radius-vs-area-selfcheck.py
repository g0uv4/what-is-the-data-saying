#!/usr/bin/env python3
"""sample-windrose-s3-radius-vs-area-selfcheck.py：圖 S3 自我檢查。
從 sample-windrose-s3-radius-vs-area.csv 核對 040 度對 230 度的比值、面積比，以及開根號半徑。
除法與開根號用 decimal，有效位數 50。只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-windrose-s3-radius-vs-area-selfcheck.py   全部通過時結束碼為 0。
頁上的倍數用這一檔兩格相除，不用 3.5 與 12.1。
"""

import csv, os, sys
from decimal import Decimal, getcontext
getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-windrose-s3-radius-vs-area.csv"
COLS = ["sector_center_deg", "pct_total", "radius_if_length_prop", "radius_if_area_prop"]
EXP_RATIO = Decimal("3.4828208593545271724568423594119431022857428885218")
EXP_AREA = Decimal("12.130041138355007143755651209279624464396864304419")
EXP_ROUNDED_AREA = Decimal("3.4828239987404338029909609259854959973696635961809")
EXP_SQRT_MAX = Decimal("0.0000068209692909013030952155055282160145464134992")
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("課程稿 11.8% 對 3.4%、說明表 11.83% 對 3.40%、facts 11.83 與 3.4", "存檔字串是 11.8286 與 3.39627")
    skip("課程稿與說明表 3.5 倍、facts 3.48", "兩格相除是 3.4828208593545271724568423594119431022857428885218")
    skip("課程稿與說明表面積 12.1 倍、facts 12.13", "比值平方是 12.130041138355007143755651209279624464396864304419")
    skip("把四捨五入後的開根號半徑再平方當成百分比比值", "3.43928／1.8429 的平方是 3.4828239987404338029909609259854959973696635961809，與百分比比值不同")

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
chk("中心 0 到 350、步進 10", centers == list(range(0, 360, 10)))
by = {r["sector_center_deg"]: r for r in rows}
chk("長度照比例的半徑字串等於總比例", all(r["radius_if_length_prop"] == r["pct_total"] for r in rows))
r40, r230 = by["40"], by["230"]
chk("40 度存檔 11.8286、230 度存檔 3.39627", r40["pct_total"] == "11.8286" and r230["pct_total"] == "3.39627", (r40["pct_total"], r230["pct_total"]))
ratio = Decimal(r40["pct_total"]) / Decimal(r230["pct_total"])
chk("百分比比值 3.4828208593545271724568423594119431022857428885218", ratio == EXP_RATIO, ratio)
chk("比值平方 12.130041138355007143755651209279624464396864304419", ratio * ratio == EXP_AREA, ratio * ratio)
chk("40 度與 230 度的開根號半徑存檔 3.43928、1.8429", r40["radius_if_area_prop"] == "3.43928" and r230["radius_if_area_prop"] == "1.8429", (r40["radius_if_area_prop"], r230["radius_if_area_prop"]))
mx = max(abs(Decimal(r["radius_if_area_prop"]) - Decimal(r["pct_total"]).sqrt()) for r in rows)
chk("存檔開根號半徑與 decimal 開根號的最大絕對差", mx == EXP_SQRT_MAX, mx)
rounded = (Decimal("3.43928") / Decimal("1.8429")) ** 2
chk("四捨五入半徑的平方 3.4828239987404338029909609259854959973696635961809", rounded == EXP_ROUNDED_AREA, rounded)
chk("四捨五入半徑的平方不等於百分比比值", rounded != ratio)
end()
