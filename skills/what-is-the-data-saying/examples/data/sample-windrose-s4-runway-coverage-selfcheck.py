#!/usr/bin/env python3
"""sample-windrose-s4-runway-coverage-selfcheck.py：圖 S4 自我檢查。
從 sample-windrose-s4-runway-coverage.csv 核對兩機場跑道真方位、筆數與存檔覆蓋率。
只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-windrose-s4-runway-coverage-selfcheck.py   全部通過時結束碼為 0。
20 節轉 90 度、風向不定筆數、13 節換算公尺每秒都不在這一檔。
"""

import csv, os, sys
from decimal import Decimal
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-windrose-s4-runway-coverage.csv"
COLS = ["station", "runway_true_deg", "n_obs", "coverage_20kt_pct", "coverage_13kt_pct", "coverage_13kt_if_rotated90_pct"]
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("說明表 13 節 99.2／67.6／98.9／99.5 與 20 節 99.9", "存檔是 99.1986、67.5882、98.9451、99.4875 與 99.9446、99.9402")
    skip("facts 一位或兩位小數 99.94、99.2、67.59、98.95、99.49", "不等於上面的存檔字串")
    skip("20 節轉 90 度 93.19 與課程稿 93.2%", "這一檔沒有 20 節轉 90 度欄")
    skip("風向不定超過門檻的筆數與靜風百分比", "這一檔沒有這兩欄")
    skip("13 節約 6.7 或 6.69 公尺每秒", "不是存檔欄；13×0.514444 不能從這兩列算出")
    skip("高雄轉 90 度覆蓋率較高是因為風較弱", "這是推論，CSV 沒有風速分布欄")

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
    chk("第一行是表頭", first.startswith("station,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("2 列", len(rows) == 2, len(rows))
if not cols_ok or len(rows) != 2:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
by = {r["station"]: r for r in rows}
chk("兩列是 RCTP 與 RCKH", set(by) == {"RCTP", "RCKH"}, list(by))
if set(by) != {"RCTP", "RCKH"}:
    end()
tp, kh = by["RCTP"], by["RCKH"]
chk("桃園跑道真方位 49.3、筆數 86595", tp["runway_true_deg"] == "49.3" and tp["n_obs"] == "86595", (tp["runway_true_deg"], tp["n_obs"]))
chk("高雄跑道真方位 91.9、筆數 87022", kh["runway_true_deg"] == "91.9" and kh["n_obs"] == "87022", (kh["runway_true_deg"], kh["n_obs"]))
chk(
    "桃園 20 節 99.9446、13 節 99.1986、13 節轉 90 度 67.5882",
    tp["coverage_20kt_pct"] == "99.9446" and tp["coverage_13kt_pct"] == "99.1986" and tp["coverage_13kt_if_rotated90_pct"] == "67.5882",
    (tp["coverage_20kt_pct"], tp["coverage_13kt_pct"], tp["coverage_13kt_if_rotated90_pct"]),
)
chk(
    "高雄 20 節 99.9402、13 節 98.9451、13 節轉 90 度 99.4875",
    kh["coverage_20kt_pct"] == "99.9402" and kh["coverage_13kt_pct"] == "98.9451" and kh["coverage_13kt_if_rotated90_pct"] == "99.4875",
    (kh["coverage_20kt_pct"], kh["coverage_13kt_pct"], kh["coverage_13kt_if_rotated90_pct"]),
)
chk(
    "高雄 13 節轉 90 度高於現有跑道",
    Decimal(kh["coverage_13kt_if_rotated90_pct"]) > Decimal(kh["coverage_13kt_pct"]),
)
chk("桃園 13 節轉 90 度低於現有跑道", Decimal(tp["coverage_13kt_if_rotated90_pct"]) < Decimal(tp["coverage_13kt_pct"]))
end()
