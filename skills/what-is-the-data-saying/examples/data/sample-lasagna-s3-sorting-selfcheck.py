#!/usr/bin/env python3
"""sample-lasagna-s3-sorting-selfcheck.py：圖 S3 自我檢查（三種列的排序）。
只用 Python 標準函式庫，從 sample-lasagna-s3-sorting.csv 獨立重算，與圖說／事實檔寫死的預期值比對。
用法：python3 sample-lasagna-s3-sorting-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""
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
EXP_TOP5, EXP_BOT5 = ['P19', 'P25', 'P12', 'P02', 'P13'], ['P39', 'P34', 'P30', 'P24', 'P33']
EXP_T10, EXP_B10 = 2, 9
EXP_GM = {"對照組": "149.7", "介入組": "138.8"}
EXP_CTOP, EXP_ITOP = 'P19', 'P02'
rows = read_rows("sample-lasagna-s3-sorting.csv")
d = wide(rows); ids = sorted(d); grp = {r["subject"]: r["group"] for r in rows}
oB = order_by_mean(d, ids)
chk("B 最高前 5", oB[:5] == EXP_TOP5, oB[:5])
chk("B 最低後 5", oB[-5:] == EXP_BOT5, oB[-5:])
t10 = sum(grp[s] == "介入組" for s in oB[:10]); b10 = sum(grp[s] == "介入組" for s in oB[-10:])
chk("前 10 名介入組 2 位、後 10 名介入組 9 位", (t10, b10) == (EXP_T10, EXP_B10), (t10, b10))
oc = order_by_mean(d, [s for s in ids if grp[s] == "對照組"]); oi = order_by_mean(d, [s for s in ids if grp[s] == "介入組"])
chk("C 對照組最上 P19、介入組最上 P02", (oc[0], oi[0]) == (EXP_CTOP, EXP_ITOP), (oc[0], oi[0]))
g = {k: hu(sum(mean(d[s]) for s in ids if grp[s] == k) / sum(1 for s in ids if grp[s] == k)) for k in EXP_GM}
chk("個人平均的組平均 149.7／138.8", g == EXP_GM, g)
chk("row_A 依編號", all(int(r["row_A_by_id"]) == int(r["subject"][1:]) for r in rows))
chk("row_B 依個人平均", all(int(r["row_B_by_mean"]) == oB.index(r["subject"]) + 1 for r in rows))
oC = oc + oi
chk("row_C 先分組再依平均", all(int(r["row_C_group_then_mean"]) == oC.index(r["subject"]) + 1 for r in rows))
done()
