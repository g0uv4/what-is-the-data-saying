#!/usr/bin/env python3
"""sample-stiff-s3-three-rivers-selfcheck.py：圖 S3 自我檢查。
從 sample-stiff-s3-three-rivers.csv 核對三條河的毫當量存檔、三項相加、電荷差全精度，以及哪一列最寬。
除法用 decimal，有效位數 50。只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-stiff-s3-three-rivers-selfcheck.py   全部通過時結束碼為 0。
合計欄與電荷差欄是存檔字串。頁上比大小用三項相加與全精度商。
"""

import csv, os, sys
from decimal import Decimal, getcontext
getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-stiff-s3-three-rivers.csv"
COLS = ["code", "name", "date", "鈉加鉀_meq", "鈣_meq", "鎂_meq", "氯_meq", "碳酸氫根_meq", "硫酸根_meq", "陽離子合計_meq", "陰離子合計_meq", "電荷差_pct"]
# 存檔離子、合計欄、電荷差欄、三項相加、電荷差全精度、陽離子最寬、陰離子最寬
EXP = {
    "A": ("0.752", "2.026", "1.02", "0.592", "2.147", "0.739", "3.8", "3.48", "4.4", "3.798", "3.478", "4.3980208905992303463441451346893897746014293567894", "鈣", "碳酸氫根", "密西西比河（路易斯安那州巴頓魯治）", "2017-02-13"),
    "B": ("2.102", "2.785", "1.498", "1.046", "2.393", "2.998", "6.38", "6.44", "-0.4", "6.385", "6.437", "-0.40555295585712057401341444392450475744813601622212", "鈣", "硫酸根", "科羅拉多河（亞利桑那州利斯渡口）", "2023-11-07"),
    "C": ("5.808", "3.428", "3.185", "5.19", "3.212", "3.352", "12.42", "11.75", "2.8", "12.421", "11.754", "2.7590486039296794208893485005170630816959669079628", "鈉＋鉀", "氯", "約旦河（猶他州鹽湖城）", "2018-05-29"),
}
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("說明表同刻度 0–7", "刻度數字不在這一檔；三條河單項最大是 5.808")
    skip("把合計欄 3.8、3.48、6.38、6.44、12.42、11.75 當成三項相加", "三項相加是 3.798、3.478、6.385、6.437、12.421、11.754")
    skip("把電荷差欄 4.4、-0.4、2.8 當成未捨入百分比", "全精度是 4.3980208905992303463441451346893897746014293567894、-0.40555295585712057401341444392450475744813601622212、2.7590486039296794208893485005170630816959669079628")
    skip("facts S3 的 D：陽離子 50.82、陰離子 48.87、電荷差 2.0", "D 不在這一檔")
    skip("水型名稱", "作者依最大離子判讀；這一檔沒有水型欄")
    skip("電荷平衡差逾 5% 或 10% 的門檻", "慣例，不是這一檔算出來的")
    skip("R3 水深 2 到 110 公尺", "論文主張；不在這一檔")
    skip("R2 四類水為論文劃分", "不在這一檔")

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
cat_sums = {}
for code, exp in EXP.items():
    r = by[code]
    ions = [r["鈉加鉀_meq"], r["鈣_meq"], r["鎂_meq"], r["氯_meq"], r["碳酸氫根_meq"], r["硫酸根_meq"]]
    chk(code + " 六個毫當量存檔", ions == list(exp[:6]), ions)
    chk(code + " 名稱與日期", r["name"] == exp[14] and r["date"] == exp[15], (r["name"], r["date"]))
    chk(code + " 合計欄與電荷差欄存檔", (r["陽離子合計_meq"], r["陰離子合計_meq"], r["電荷差_pct"]) == exp[6:9], (r["陽離子合計_meq"], r["陰離子合計_meq"], r["電荷差_pct"]))
    cat = Decimal(r["鈉加鉀_meq"]) + Decimal(r["鈣_meq"]) + Decimal(r["鎂_meq"])
    an = Decimal(r["氯_meq"]) + Decimal(r["碳酸氫根_meq"]) + Decimal(r["硫酸根_meq"])
    bal = Decimal(100) * (cat - an) / (cat + an)
    cat_sums[code] = cat
    chk(code + " 三項相加 " + exp[9] + "、" + exp[10], cat == Decimal(exp[9]) and an == Decimal(exp[10]), (cat, an))
    chk(code + " 電荷差全精度", bal == Decimal(exp[11]), bal)
    chk(code + " 三項相加不等於合計欄、全精度不等於電荷差欄", cat != Decimal(r["陽離子合計_meq"]) and an != Decimal(r["陰離子合計_meq"]) and bal != Decimal(r["電荷差_pct"]))
    cats = {"鈉＋鉀": Decimal(r["鈉加鉀_meq"]), "鈣": Decimal(r["鈣_meq"]), "鎂": Decimal(r["鎂_meq"])}
    ans = {"氯": Decimal(r["氯_meq"]), "碳酸氫根": Decimal(r["碳酸氫根_meq"]), "硫酸根": Decimal(r["硫酸根_meq"])}
    cat_max = max(cats, key=cats.get)
    an_max = max(ans, key=ans.get)
    chk(code + " 唯一最寬 " + exp[12] + "／" + exp[13], cat_max == exp[12] and an_max == exp[13] and list(cats.values()).count(cats[cat_max]) == 1 and list(ans.values()).count(ans[an_max]) == 1, (cat_max, an_max))
chk("陽離子三項相加 A 3.798 < B 6.385 < C 12.421", cat_sums["A"] < cat_sums["B"] < cat_sums["C"], (cat_sums["A"], cat_sums["B"], cat_sums["C"]))
wide = {code: max(Decimal(by[code][c]) for c in ["鈉加鉀_meq", "鈣_meq", "鎂_meq", "氯_meq", "碳酸氫根_meq", "硫酸根_meq"]) for code in "ABC"}
chk("單項最大 A 2.147 < B 2.998 < C 5.808", wide["A"] == Decimal("2.147") and wide["B"] == Decimal("2.998") and wide["C"] == Decimal("5.808") and wide["A"] < wide["B"] < wide["C"], wide)
abs_ok = True
for code in "ABC":
    r = by[code]
    cat = Decimal(r["鈉加鉀_meq"]) + Decimal(r["鈣_meq"]) + Decimal(r["鎂_meq"])
    an = Decimal(r["氯_meq"]) + Decimal(r["碳酸氫根_meq"]) + Decimal(r["硫酸根_meq"])
    if abs(Decimal(100) * (cat - an) / (cat + an)) >= Decimal(5):
        abs_ok = False
chk("三筆電荷差全精度的絕對值都小於 5", abs_ok)
end()
