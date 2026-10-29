#!/usr/bin/env python3
"""sample-stiff-s5-bar-instead-selfcheck.py：圖 S5 自我檢查。
從 sample-stiff-s5-bar-instead.csv 核對三條河的毫當量存檔，以及約旦河對密西西比河的鈉＋鉀商。
除法用 decimal，有效位數 50。只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-stiff-s5-bar-instead-selfcheck.py   全部通過時結束碼為 0。
5.81、0.75、7.7 是事後捨入，不是存檔字串，也不是全精度商。
"""

import csv, os, sys
from decimal import Decimal, getcontext
getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-stiff-s5-bar-instead.csv"
COLS = ["code", "name", "date", "鈉加鉀_meq", "鈣_meq", "鎂_meq", "氯_meq", "碳酸氫根_meq", "硫酸根_meq", "陽離子合計_meq", "陰離子合計_meq", "電荷差_pct"]
EXP = {
    "A": ("0.752", "2.026", "1.02", "0.592", "2.147", "0.739", "3.8", "3.48", "4.4", "密西西比河（路易斯安那州巴頓魯治）", "2017-02-13"),
    "B": ("2.102", "2.785", "1.498", "1.046", "2.393", "2.998", "6.38", "6.44", "-0.4", "科羅拉多河（亞利桑那州利斯渡口）", "2023-11-07"),
    "C": ("5.808", "3.428", "3.185", "5.19", "3.212", "3.352", "12.42", "11.75", "2.8", "約旦河（猶他州鹽湖城）", "2018-05-29"),
}
RATIO = Decimal("7.7234042553191489361702127659574468085106382978723")
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("課程稿與說明表約旦河鈉＋鉀 5.81、密西西比河 0.75", "存檔字串是 5.808、0.752")
    skip("課程稿、說明表與 facts 的 7.7 倍", "5.808／0.752 是 7.7234042553191489361702127659574468085106382978723")

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
    chk("第一行是表頭", first.startswith("code,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("3 列", len(rows) == 3, len(rows))
if not cols_ok or len(rows) != 3:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
chk("代碼順序 A、B、C", [r["code"] for r in rows] == ["A", "B", "C"], [r["code"] for r in rows])
by = {r["code"]: r for r in rows}
for code, exp in EXP.items():
    r = by[code]
    ions = [r["鈉加鉀_meq"], r["鈣_meq"], r["鎂_meq"], r["氯_meq"], r["碳酸氫根_meq"], r["硫酸根_meq"], r["陽離子合計_meq"], r["陰離子合計_meq"], r["電荷差_pct"]]
    chk(code + " 毫當量、合計欄、電荷差欄存檔", ions == list(exp[:9]), ions)
    chk(code + " 名稱與日期", r["name"] == exp[9] and r["date"] == exp[10], (r["name"], r["date"]))
ratio = Decimal(by["C"]["鈉加鉀_meq"]) / Decimal(by["A"]["鈉加鉀_meq"])
chk("約旦河鈉＋鉀存檔 5.808、密西西比河存檔 0.752", by["C"]["鈉加鉀_meq"] == "5.808" and by["A"]["鈉加鉀_meq"] == "0.752", (by["C"]["鈉加鉀_meq"], by["A"]["鈉加鉀_meq"]))
chk("鈉＋鉀商 7.7234042553191489361702127659574468085106382978723", ratio == RATIO, ratio)
chk("商不是 7.7", ratio != Decimal("7.7"))
chk("約旦河鈉＋鉀大於密西西比河", Decimal(by["C"]["鈉加鉀_meq"]) > Decimal(by["A"]["鈉加鉀_meq"]))
end()
