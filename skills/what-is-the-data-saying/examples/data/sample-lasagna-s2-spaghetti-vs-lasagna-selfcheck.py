#!/usr/bin/env python3
"""sample-lasagna-s2-spaghetti-vs-lasagna-selfcheck.py：圖 S2 自我檢查（義大利麵圖對千層麵圖：個人平均最高與最低）。
只用 Python 標準函式庫，從 sample-lasagna-s2-spaghetti-vs-lasagna.csv 獨立重算，與圖說／事實檔寫死的預期值比對。
用法：python3 sample-lasagna-s2-spaghetti-vs-lasagna-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""
import csv, os, sys
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP, getcontext
getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "虛構資料，數字未核"
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def read_rows(fn):
    with open(os.path.join(HERE, fn), encoding="utf-8", newline="") as fh:
        first = fh.readline()
        chk("第一行標示虛構資料", first.startswith("# " + STATUS), first.strip()[:30])
        rows = list(csv.DictReader(fh))
    chk("每列 data_status 都是「" + STATUS + "」", all(r["data_status"] == STATUS for r in rows))
    return rows

def num(s):
    return None if s == "" else int(s)

def mean(xs):
    xs = [x for x in xs if x is not None]
    return Fraction(sum(xs), len(xs))

def hu(fr, nd=1):
    """分數 → 四捨五入（逢 5 進位）到 nd 位小數，回傳字串。"""
    d = Decimal(fr.numerator) / Decimal(fr.denominator)
    return str(d.quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))

def hsub(a, b):
    """兩個已四捨五入的字串相減，回傳帶正負號的一位小數字串。"""
    d = Decimal(a) - Decimal(b)
    return ("+" if d > 0 else "") + str(d.quantize(Decimal("0.1")))

def wide(rows, prefix="w"):
    return {r["subject"]: [num(r[f"{prefix}{w}"]) for w in range(1, 13)] for r in rows}

def order_by_mean(d, ids):
    return sorted(ids, key=lambda s: (-mean(d[s]), s))

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(1 if bad else 0)

# ---- 預期值（寫死）與檢查 ----
EXP_HI, EXP_HI_M, EXP_LO, EXP_LO_M = 'P19', "164.0", 'P33', "121.4"
rows = read_rows("sample-lasagna-s2-spaghetti-vs-lasagna.csv")
d = wide(rows); ids = sorted(d)
chk("40 條線（40 人）", len(ids) == 40, len(ids))
pm = {s: mean(d[s]) for s in ids}
hi = max(ids, key=lambda s: (pm[s], -int(s[1:]))); lo = min(ids, key=lambda s: (pm[s], s))
chk("個人平均最高 P19＝164.0", (hi, hu(pm[hi])) == (EXP_HI, EXP_HI_M), (hi, hu(pm[hi])))
chk("個人平均最低 P33＝121.4", (lo, hu(pm[lo])) == (EXP_LO, EXP_LO_M), (lo, hu(pm[lo])))
chk("person_mean 欄＝重算值（四捨五入）", all(r["person_mean"] == hu(pm[r["subject"]]) for r in rows))
chk("n_observed 欄正確", all(int(r["n_observed"]) == sum(x is not None for x in d[r["subject"]]) for r in rows))
o = order_by_mean(d, ids)
chk("右圖列順序＝個人平均由高到低", all(int(r["row_in_lasagna"]) == o.index(r["subject"]) + 1 for r in rows))
chk("右圖最上 P19、最下 P33", (o[0], o[-1]) == ('P19', 'P33'), (o[0], o[-1]))
done()
