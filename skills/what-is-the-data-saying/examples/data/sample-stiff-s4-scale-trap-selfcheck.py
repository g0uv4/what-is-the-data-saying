#!/usr/bin/env python3
"""sample-stiff-s4-scale-trap-selfcheck.py：圖 S4 自我檢查。
從 sample-stiff-s4-scale-trap.csv 核對密西西比河與加拿大河的毫當量存檔，以及陽離子總量的兩個商。
除法用 decimal，有效位數 50。只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-stiff-s4-scale-trap-selfcheck.py   全部通過時結束碼為 0。
13.4 是事後捨入到一位小數，不是這兩個商。
"""

import csv, os, sys
from decimal import Decimal, getcontext
getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-stiff-s4-scale-trap.csv"
COLS = ["code", "name", "date", "鈉加鉀_meq", "鈣_meq", "鎂_meq", "氯_meq", "碳酸氫根_meq", "硫酸根_meq", "陽離子合計_meq", "陰離子合計_meq", "電荷差_pct"]
EXP = {
    "A": ("0.752", "2.026", "1.02", "0.592", "2.147", "0.739", "3.8", "3.48", "4.4", "3.798", "3.478", "4.3980208905992303463441451346893897746014293567894", "密西西比河（路易斯安那州巴頓魯治）", "2017-02-13"),
    "D": ("35.361", "9.432", "6.023", "33.284", "3.36", "12.222", "50.82", "48.87", "2.0", "50.816", "48.866", "1.9562207820870367769507032362914066732208422784455", "加拿大河（德州阿馬里洛附近）", "2023-11-02"),
}
RATIO_SUM = Decimal("13.379673512374934175882043180621379673512374934176")
RATIO_COL = Decimal("13.373684210526315789473684210526315789473684210526")
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("課程稿、說明表與 facts 的 13.4 倍", "陽離子三項相加的商是 13.379673512374934175882043180621379673512374934176；合計欄 50.82／3.8 是 13.373684210526315789473684210526315789473684210526")
    skip("各用各刻度時兩者看起來一樣大", "外觀不在這一檔")
    skip("R4 刻度 0–10，以及哪幾口井靠河", "看圖判讀；不在這一檔。標是「哪幾口井靠河為看圖判讀」")

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
chk("2 列", len(rows) == 2, len(rows))
if not cols_ok or len(rows) != 2:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
chk("代碼順序 A、D", [r["code"] for r in rows] == ["A", "D"], [r["code"] for r in rows])
by = {r["code"]: r for r in rows}
sums = {}
for code, exp in EXP.items():
    r = by[code]
    ions = [r["鈉加鉀_meq"], r["鈣_meq"], r["鎂_meq"], r["氯_meq"], r["碳酸氫根_meq"], r["硫酸根_meq"]]
    chk(code + " 六個毫當量存檔", ions == list(exp[:6]), ions)
    chk(code + " 名稱與日期", r["name"] == exp[12] and r["date"] == exp[13], (r["name"], r["date"]))
    chk(code + " 合計欄與電荷差欄存檔", (r["陽離子合計_meq"], r["陰離子合計_meq"], r["電荷差_pct"]) == exp[6:9], (r["陽離子合計_meq"], r["陰離子合計_meq"], r["電荷差_pct"]))
    cat = Decimal(r["鈉加鉀_meq"]) + Decimal(r["鈣_meq"]) + Decimal(r["鎂_meq"])
    an = Decimal(r["氯_meq"]) + Decimal(r["碳酸氫根_meq"]) + Decimal(r["硫酸根_meq"])
    bal = Decimal(100) * (cat - an) / (cat + an)
    sums[code] = cat
    chk(code + " 三項相加 " + exp[9] + "、" + exp[10], cat == Decimal(exp[9]) and an == Decimal(exp[10]), (cat, an))
    chk(code + " 電荷差全精度", bal == Decimal(exp[11]), bal)
    chk(code + " 三項相加不等於合計欄", cat != Decimal(r["陽離子合計_meq"]) and an != Decimal(r["陰離子合計_meq"]))
    chk(code + " 電荷差全精度的絕對值小於 5", abs(bal) < Decimal(5), abs(bal))
rD = by["D"]
cats = {"鈉＋鉀": Decimal(rD["鈉加鉀_meq"]), "鈣": Decimal(rD["鈣_meq"]), "鎂": Decimal(rD["鎂_meq"])}
ans = {"氯": Decimal(rD["氯_meq"]), "碳酸氫根": Decimal(rD["碳酸氫根_meq"]), "硫酸根": Decimal(rD["硫酸根_meq"])}
cat_max = max(cats, key=cats.get)
an_max = max(ans, key=ans.get)
chk("D 唯一最寬是鈉＋鉀 35.361、氯 33.284", cat_max == "鈉＋鉀" and an_max == "氯" and list(cats.values()).count(cats[cat_max]) == 1 and list(ans.values()).count(ans[an_max]) == 1, (cat_max, an_max))
ratio_sum = sums["D"] / sums["A"]
ratio_col = Decimal(by["D"]["陽離子合計_meq"]) / Decimal(by["A"]["陽離子合計_meq"])
chk("陽離子三項相加的商 13.379673512374934175882043180621379673512374934176", ratio_sum == RATIO_SUM, ratio_sum)
chk("合計欄 50.82／3.8 的商 13.373684210526315789473684210526315789473684210526", ratio_col == RATIO_COL, ratio_col)
chk("兩個商都不是 13.4，而且彼此不同", ratio_sum != Decimal("13.4") and ratio_col != Decimal("13.4") and ratio_sum != ratio_col)
chk("加拿大河陽離子三項相加大於密西西比河", sums["D"] > sums["A"])
end()
