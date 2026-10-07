#!/usr/bin/env python3
"""sample-lasagna-s8-steps-selfcheck.py：圖 S8 自我檢查（製作步驟：4 人前 4 週）。
只用 Python 標準函式庫，從 sample-lasagna-s8-steps.csv 獨立重算，與圖說／事實檔寫死的預期值比對。
用法：python3 sample-lasagna-s8-steps-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""
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
EXP_IDS = ['P01', 'P03', 'P04', 'P06']
EXP_VALUES = {'P01': [148, 150, 146, None], 'P03': [144, 152, 144, 143], 'P04': [154, 153, 150, 143], 'P06': [156, 156, 154, 157]}
EXP_MEANS = {k: "%.1f" % v for k, v in {'P01': 148.0, 'P03': 145.8, 'P04': 150.0, 'P06': 155.8}.items()}
EXP_ORDER, EXP_LONG = ['P06', 'P04', 'P01', 'P03'], 16
rows = read_rows("sample-lasagna-s8-steps.csv")
chk("長表 16 列（4 人 × 4 週）", len(rows) == EXP_LONG, len(rows))
ids = sorted({r["subject"] for r in rows})
chk("取 P01、P03、P04、P06", ids == EXP_IDS, ids)
d = {s: [num(r["sbp"]) for r in sorted((r for r in rows if r["subject"] == s), key=lambda r: int(r["week"]))] for s in ids}
chk("寬表數值相符", d == EXP_VALUES, d)
m = {s: hu(mean(d[s])) for s in ids}
chk("4 週個人平均（缺值不計入）148.0／145.8／150.0／155.8", m == EXP_MEANS, m)
o = sorted(ids, key=lambda s: (-mean(d[s]), s))
chk("排序 P06、P04、P01、P03", o == EXP_ORDER, o)
miss = [(r["subject"], int(r["week"])) for r in rows if r["sbp"] == ""]
chk("唯一缺值是 P01 第 4 週", miss == [("P01", 4)], miss)
done()
