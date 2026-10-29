#!/usr/bin/env python3
"""sample-stiff-s1-anatomy-selfcheck.py：圖 S1 自我檢查。
從 sample-stiff-s1-anatomy.csv 核對科羅拉多河六個毫當量存檔、三項相加，以及電荷差的全精度商。
除法用 decimal，有效位數 50。只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-stiff-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。
頁上讀數用存檔字串或由存檔重算的全精度。課程稿的 2.79、3.00 不是存檔。
"""

import csv, os, sys
from decimal import Decimal, getcontext
getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-stiff-s1-anatomy.csv"
COLS = ["code", "name", "date", "鈉加鉀_meq", "鈣_meq", "鎂_meq", "氯_meq", "碳酸氫根_meq", "硫酸根_meq", "陽離子合計_meq", "陰離子合計_meq", "電荷差_pct"]
IONS = ["鈉加鉀_meq", "鈣_meq", "鎂_meq", "氯_meq", "碳酸氫根_meq", "硫酸根_meq"]
EXP = ["2.102", "2.785", "1.498", "1.046", "2.393", "2.998"]
CAT_SUM = Decimal("6.385")
AN_SUM = Decimal("6.437")
BAL = Decimal("-0.40555295585712057401341444392450475744813601622212")
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("課程稿與說明表鈣 2.79、硫酸根 3.00", "存檔字串是 2.785、2.998")
    skip("把合計欄 6.38、6.44 當成三項相加", "三項相加是 6.385、6.437")
    skip("把電荷差欄 -0.4 當成未捨入百分比", "100×(6.385−6.437)/(6.385+6.437) 是 -0.40555295585712057401341444392450475744813601622212")
    skip("facts 站號 USGS-09380000", "這一檔沒有站號欄")
    skip("作者毫當量換算、Hem 表 9 與說明表當量重", "這一檔沒有毫克欄，當量重也不在列上；來源把作者換算標未核")
    skip("課程稿 1951 年", "不在這一檔")
    skip("說明表 R1 最近鄰放大 3 倍", "圖檔改作，不在練習 CSV")
    skip("R1 下方水樣鈣與硫酸根（含硝酸根）衝出 10 毫當量刻度", "看圖判讀；沒有練習 CSV")
    skip("R2 四類水、R3 水深 2 到 110 公尺、R4 刻度 0–10", "論文主張或看圖判讀；沒有練習 CSV")

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
chk("代碼 B、日期 2023-11-07、名稱是科羅拉多河（亞利桑那州利斯渡口）", r["code"] == "B" and r["date"] == "2023-11-07" and r["name"] == "科羅拉多河（亞利桑那州利斯渡口）", (r["code"], r["date"], r["name"]))
got = [r[c] for c in IONS]
chk("六個毫當量存檔 2.102、2.785、1.498、1.046、2.393、2.998", got == EXP, got)
cat = Decimal(r["鈉加鉀_meq"]) + Decimal(r["鈣_meq"]) + Decimal(r["鎂_meq"])
an = Decimal(r["氯_meq"]) + Decimal(r["碳酸氫根_meq"]) + Decimal(r["硫酸根_meq"])
chk("陽離子三項相加 6.385、陰離子三項相加 6.437", cat == CAT_SUM and an == AN_SUM, (cat, an))
chk("合計欄存檔 6.38、6.44，電荷差欄存檔 -0.4", r["陽離子合計_meq"] == "6.38" and r["陰離子合計_meq"] == "6.44" and r["電荷差_pct"] == "-0.4", (r["陽離子合計_meq"], r["陰離子合計_meq"], r["電荷差_pct"]))
chk("三項相加不等於合計欄", cat != Decimal(r["陽離子合計_meq"]) and an != Decimal(r["陰離子合計_meq"]))
bal = Decimal(100) * (cat - an) / (cat + an)
chk("電荷差全精度 -0.40555295585712057401341444392450475744813601622212", bal == BAL, bal)
chk("全精度電荷差不等於電荷差欄", bal != Decimal(r["電荷差_pct"]))
cats = {"鈉＋鉀": Decimal(r["鈉加鉀_meq"]), "鈣": Decimal(r["鈣_meq"]), "鎂": Decimal(r["鎂_meq"])}
ans = {"氯": Decimal(r["氯_meq"]), "碳酸氫根": Decimal(r["碳酸氫根_meq"]), "硫酸根": Decimal(r["硫酸根_meq"])}
cat_max = max(cats, key=cats.get)
an_max = max(ans, key=ans.get)
chk("陽離子唯一最寬是鈣 2.785、陰離子唯一最寬是硫酸根 2.998", cat_max == "鈣" and an_max == "硫酸根" and list(cats.values()).count(cats["鈣"]) == 1 and list(ans.values()).count(ans["硫酸根"]) == 1, (cat_max, an_max))
end()
