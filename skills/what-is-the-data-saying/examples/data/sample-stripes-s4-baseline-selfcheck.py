#!/usr/bin/env python3
"""sample-stripes-s4-baseline-selfcheck.py：圖 S4 自我檢查。
從 sample-stripes-s4-baseline.csv 重算兩個基準窗的和與平均，以及平移後偏紅的年數。
偏紅是平移後的距平大於 0。1901–2000 的平均恰好 0.0002。1991–2020 的和是 18.17，
未捨入平均是 1817/3000，小數是 0.605 之後的 6 無限循環。
有效位數 50 的商會在末位進位。記載的 0.0 與 0.606 不是未捨入平均。
除法用 decimal，有效位數 50。只需 Python 標準函式庫（csv、decimal、os、sys）。
用法：python3 sample-stripes-s4-baseline-selfcheck.py   全部通過時結束碼為 0。
"""

import csv, os, sys
from decimal import Decimal, getcontext
getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-stripes-s4-baseline.csv"
COLS = ["year", "anomaly_c"]
MEAN50 = "0.60566666666666666666666666666666666666666666666667"
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    skip("把 0.0 當成 1901–2000 的未捨入平均", "未捨入平均是 0.0002")
    skip("把 0.606 當成 1991–2020 的未捨入平均", "未捨入平均是 1817/3000，6 無限循環")
    skip("素材另存的第三欄 anomaly_c_vs_1991_2020", "這一檔沒有該欄")
    skip("圖 R4 三種基準期、以及基準期越晚藍色越多", "那張圖是柏克萊地球，不是這一檔的 NOAA 距平")

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def end():
    unchecked()
    done()

def cents_of(text):
    return int((Decimal(text) * 100).to_integral_value())

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first == "year,anomaly_c\n")
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("176 列", len(rows) == 176, len(rows))
if not cols_ok or len(rows) != 176:
    end()
empty = any((r[c] or "").strip() == "" for r in rows for c in COLS)
chk("沒有空值", not empty)
if empty:
    end()
years = [int(r["year"]) for r in rows]
chk("年份連續 1850 到 2025", years == list(range(1850, 2026)))
vals = [(int(r["year"]), r["anomaly_c"], Decimal(r["anomaly_c"]), cents_of(r["anomaly_c"])) for r in rows]
chk("每一列的百分之一度都是整數", all(Decimal(t[1]) * 100 == t[3] for t in vals))
w1 = [t for t in vals if 1901 <= t[0] <= 2000]
sum1 = sum((t[2] for t in w1), Decimal(0))
chk("1901–2000 是 100 年", len(w1) == 100, len(w1))
chk("1901–2000 的和恰好 0.02", sum1 == Decimal("0.02"), sum1)
mean1 = sum1 / Decimal(len(w1))
chk("1901–2000 的平均恰好 0.0002", mean1 == Decimal("0.0002"), mean1)
chk("0.0002 不是 0", mean1 != Decimal("0"))
red = zero = blue = 0
changed = []
pos_same = True
for t in vals:
    v = t[2] - mean1
    if v > 0:
        red += 1
    elif v == 0:
        zero += 1
    else:
        blue += 1
    before = 1 if t[2] > 0 else (0 if t[2] == 0 else -1)
    after = 1 if v > 0 else (0 if v == 0 else -1)
    if before != after:
        changed.append(t[0])
    if (t[2] > 0) != (v > 0):
        pos_same = False
chk("減去 0.0002 以後偏紅 71、零 0、偏藍 105", red == 71 and zero == 0 and blue == 105, (red, zero, blue))
chk("三分法有變的只有 1937 與 1947", changed == [1937, 1947], changed)
chk("大於 0 的成員沒有因減去 0.0002 而改變", pos_same)
nom_r = sum(1 for t in vals if t[2] > 0)
nom_z = sum(1 for t in vals if t[2] == 0)
nom_b = sum(1 for t in vals if t[2] < 0)
chk("以名目 0 計是偏紅 71、零 2、偏藍 103", nom_r == 71 and nom_z == 2 and nom_b == 103, (nom_r, nom_z, nom_b))
w2 = [t for t in vals if 1991 <= t[0] <= 2020]
sum2 = sum((t[2] for t in w2), Decimal(0))
sum_cents = sum(t[3] for t in w2)
chk("1991–2020 是 30 年", len(w2) == 30, len(w2))
chk("1991–2020 的和恰好 18.17", sum2 == Decimal("18.17"), sum2)
chk("和的百分之一度是 1817", sum_cents == 1817, sum_cents)
digits = []
rem = 1817
for _ in range(60):
    rem *= 10
    digits.append(rem // 3000)
    rem %= 3000
chk("1817/3000 的前三位小數是 605，其後都是 6", digits[:3] == [6, 0, 5] and digits[3:] == [6] * 57, digits[:8])
mean50 = Decimal("18.17") / Decimal(30)
chk("有效位數 50 的商是記載的那一串", str(mean50) == MEAN50, str(mean50))
exact_red = exact_zero = exact_blue = 0
round_red = 0
six_red = 0
disagree = []
for t in vals:
    gap = t[3] * 30 - 1817
    if gap > 0:
        exact_red += 1
    elif gap == 0:
        exact_zero += 1
    else:
        exact_blue += 1
    if t[2] - mean50 > 0:
        round_red += 1
    if t[2] - Decimal("0.606") > 0:
        six_red += 1
    if (gap > 0) != (t[2] - Decimal("0.606") > 0):
        disagree.append(t[0])
chk("減去精確平均以後偏紅 20、零 0、偏藍 156", exact_red == 20 and exact_zero == 0 and exact_blue == 156, (exact_red, exact_zero, exact_blue))
chk("減去有效位數 50 的商以後偏紅仍是 20", round_red == 20, round_red)
chk("減去 0.606 以後偏紅仍是 20，而且沒有一年跟精確平均的正負不同", six_red == 20 and disagree == [], (six_red, disagree))
chk("1817 不能被 30 整除，所以精確平移沒有零年", 1817 % 30 != 0)
max_abs_exact = max(abs(t[3] * 30 - 1817) for t in vals)
chk("減去精確平均以後的絕對值仍不大於 1.25", max_abs_exact <= 3750 and Decimal(max_abs_exact) / Decimal(3000) <= Decimal("1.25"), max_abs_exact)
max_abs_six = max(abs(t[2] - Decimal("0.606")) for t in vals)
max_abs_base = max(abs(t[2] - mean1) for t in vals)
chk("減去 0.606 以後絕對值最大是 1.026，仍不大於 1.25", max_abs_six == Decimal("1.026") and max_abs_six <= Decimal("1.25"), max_abs_six)
chk("減去 0.0002 以後絕對值最大是 1.2498，仍不大於 1.25", max_abs_base == Decimal("1.2498") and max_abs_base <= Decimal("1.25"), max_abs_base)
chk("記載 0.606 不等於有效位數 50 的商", Decimal("0.606") != mean50)
end()
