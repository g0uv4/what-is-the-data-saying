#!/usr/bin/env python3
"""sample-stiff-s2-mg-vs-meq-selfcheck.py：圖 S2 自我檢查。
從 sample-stiff-s2-mg-vs-meq.csv 核對毫克與毫當量存檔，以及鈉加鉀的毫克和。
只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-stiff-s2-mg-vs-meq-selfcheck.py   全部通過時結束碼為 0。
毫克誰大、毫當量誰大，用這一檔的存檔字串比。當量重不在列上，換算不計入通過。
"""

import csv, os, sys
from decimal import Decimal
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-stiff-s2-mg-vs-meq.csv"
COLS = ["code", "name", "date", "鈣_mg", "鎂_mg", "鈉_mg", "鉀_mg", "碳酸氫根_mg", "硫酸根_mg", "氯_mg", "鈣_meq", "鎂_meq", "鈉加鉀_meq", "碳酸氫根_meq", "硫酸根_meq", "氯_meq"]
MG = ["鈣_mg", "鎂_mg", "鈉_mg", "鉀_mg", "碳酸氫根_mg", "硫酸根_mg", "氯_mg"]
MEQ = ["鈣_meq", "鎂_meq", "鈉加鉀_meq", "碳酸氫根_meq", "硫酸根_meq", "氯_meq"]
EXP_MG = ["55.8", "18.2", "46.6", "2.95", "146.0", "144.0", "37.1"]
EXP_MEQ = ["2.785", "1.498", "2.102", "2.393", "2.998", "1.046"]
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("課程稿與說明表碳酸氫根 146、硫酸根 144、硫酸根 3.00、碳酸氫根 2.39", "存檔字串是 146.0、144.0、2.998、2.393")
    skip("facts 鈉加鉀毫克 49.550000000000004", "鈉 46.6 與鉀 2.95 以 decimal 相加是 49.55")
    skip("作者毫當量換算", "毫克與毫當量都在列上，當量重不在列上；來源把作者換算標未核")
    skip("facts Hem 1985 表 9 當量重 20.04、12.15、22.99、39.1、35.45、48.03、61.02", "不在這一檔")
    skip("說明表當量重 20.039、12.1525、22.990、39.098、61.017、48.03、35.453", "不在這一檔")
    skip("略去碳酸根的前提酸鹼值約 8.3，以及四個樣本酸鹼值", "這一檔沒有酸鹼值欄；來源寫未逐一查核")

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
chk("1 列", len(rows) == 1, len(rows))
if not cols_ok or len(rows) != 1:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
r = rows[0]
chk("代碼 B、日期 2023-11-07、名稱是科羅拉多河（亞利桑那州利斯渡口）", r["code"] == "B" and r["date"] == "2023-11-07" and r["name"] == "科羅拉多河（亞利桑那州利斯渡口）", (r["code"], r["date"]))
chk("七個毫克存檔 55.8、18.2、46.6、2.95、146.0、144.0、37.1", [r[c] for c in MG] == EXP_MG, [r[c] for c in MG])
chk("六個毫當量存檔 2.785、1.498、2.102、2.393、2.998、1.046", [r[c] for c in MEQ] == EXP_MEQ, [r[c] for c in MEQ])
nak = Decimal(r["鈉_mg"]) + Decimal(r["鉀_mg"])
chk("鈉加鉀毫克 49.55", nak == Decimal("49.55"), nak)
chk("碳酸氫根毫克 146.0 大於硫酸根毫克 144.0", Decimal(r["碳酸氫根_mg"]) > Decimal(r["硫酸根_mg"]))
chk("硫酸根毫當量 2.998 大於碳酸氫根毫當量 2.393", Decimal(r["硫酸根_meq"]) > Decimal(r["碳酸氫根_meq"]))
chk("毫克的大小順序與毫當量相反", (Decimal(r["碳酸氫根_mg"]) - Decimal(r["硫酸根_mg"])) * (Decimal(r["碳酸氫根_meq"]) - Decimal(r["硫酸根_meq"])) < 0)
end()
