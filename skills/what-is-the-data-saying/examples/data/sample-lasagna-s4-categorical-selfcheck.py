#!/usr/bin/env python3
"""sample-lasagna-s4-categorical-selfcheck.py：圖 S4 自我檢查（類別狀態版：四級）。
只用 Python 標準函式庫，從 sample-lasagna-s4-categorical.csv 獨立重算，與圖說／事實檔寫死的預期值比對。
用法：python3 sample-lasagna-s4-categorical-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""
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
CATS = ['未滿 120', '120–129', '130–139', '140 以上']
EXP_W1, EXP_W12 = {'未滿 120': 0, '120–129': 1, '130–139': 5, '140 以上': 32, '缺值': 2}, {'未滿 120': 2, '120–129': 5, '130–139': 9, '140 以上': 19, '缺值': 5}
EXP_MOVED, EXP_MOVED_INT = ['P04', 'P10', 'P11', 'P14', 'P18', 'P26', 'P31', 'P35'], 6
def cat(x):
    if x is None: return ""
    return CATS[0] if x < 120 else CATS[1] if x < 130 else CATS[2] if x < 140 else CATS[3]
rows = read_rows("sample-lasagna-s4-categorical.csv")
d = wide(rows, "sbp_w"); grp = {r["subject"]: r["group"] for r in rows}
chk("40 人", len(rows) == 40)
chk("每格級別＝依收縮壓重算（未滿 120／120–129／130–139／140 以上）", all(r[f"cat_w{w}"] == cat(d[r["subject"]][w - 1]) for r in rows for w in range(1, 13)))
def counts(w):
    c = {k: sum(cat(d[s][w - 1]) == k for s in d) for k in CATS}
    c["缺值"] = sum(d[s][w - 1] is None for s in d); return c
chk("第 1 週：0、1、5、32，缺值 2", counts(1) == EXP_W1, counts(1))
chk("第 12 週：2、5、9、19，缺值 5", counts(12) == EXP_W12, counts(12))
moved = [s for s in sorted(d) if cat(d[s][0]) == CATS[3] and d[s][11] is not None and cat(d[s][11]) != CATS[3]]
chk("第 1 週 140 以上 → 第 12 週降到 140 以下：8 人", moved == EXP_MOVED, moved)
chk("其中介入組 6 人", sum(grp[s] == "介入組" for s in moved) == EXP_MOVED_INT)
lv = lambda x: -1 if x is None else CATS.index(cat(x))
o = sorted(d, key=lambda s: (-lv(d[s][11]), -lv(d[s][0]), s))
chk("列順序：第 12 週級別高到低（缺值最後）→第 1 週→編號", all(int(r["row_in_plot"]) == o.index(r["subject"]) + 1 for r in rows))
done()
