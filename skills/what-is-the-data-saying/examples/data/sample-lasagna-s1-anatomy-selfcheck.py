#!/usr/bin/env python3
"""sample-lasagna-s1-anatomy-selfcheck.py：圖 S1 自我檢查（構造：40 人 × 12 週、缺值 33 格）。
只用 Python 標準函式庫，從 sample-lasagna-s1-anatomy.csv 獨立重算，與圖說／事實檔寫死的預期值比對。
用法：python3 sample-lasagna-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""
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
EXP_N, EXP_T, EXP_CELLS, EXP_MISS = 40, 12, 480, 33
EXP_SPOR = [('P01', 4), ('P02', 2), ('P03', 12), ('P05', 4), ('P05', 11), ('P08', 8), ('P10', 8), ('P18', 11), ('P23', 8), ('P30', 2), ('P37', 1), ('P38', 1)]
EXP_DROP = [('P12', 8, '對照組'), ('P15', 7, '對照組'), ('P32', 7, '介入組'), ('P34', 9, '介入組')]
EXP_DROP_CELLS, EXP_MIN, EXP_MAX, EXP_NINT = 21, 107, 170, 20
rows = read_rows("sample-lasagna-s1-anatomy.csv")
chk("共 480 列（格）", len(rows) == EXP_CELLS, len(rows))
ids = sorted({r["subject"] for r in rows})
chk("40 位受試者 P01–P40", ids == [f"P{i:02d}" for i in range(1, EXP_N + 1)], len(ids))
chk("每人 12 週各一格", all(sorted(int(r["week"]) for r in rows if r["subject"] == s) == list(range(1, EXP_T + 1)) for s in ids))
miss = [(r["subject"], int(r["week"])) for r in rows if r["sbp"] == ""]
chk("缺值 33 格", len(miss) == EXP_MISS, len(miss))
spor = sorted((r["subject"], int(r["week"])) for r in rows if r["missing_type"] == "零星缺值")
chk("零星缺值 12 格且位置相符", spor == EXP_SPOR, spor)
v = {(r["subject"], int(r["week"])): num(r["sbp"]) for r in rows}
grp = {r["subject"]: r["group"] for r in rows}
drop = []
for s in ids:
    w = EXP_T
    while w >= 1 and v[(s, w)] is None and (s, w) not in spor:
        w -= 1
    if w < EXP_T:
        drop.append((s, w + 1, grp[s]))
chk("中途退出 4 人（編號、起缺週、組別）", drop == EXP_DROP, drop)
dcells = sum(EXP_T - w + 1 for _, w, _ in drop)
chk("中途退出共 21 格，加零星 12 格＝33", dcells == EXP_DROP_CELLS and dcells + len(spor) == EXP_MISS, dcells)
chk("missing_type 與空白一致", all((r["sbp"] == "") == (r["missing_type"] != "") for r in rows))
chk("綠框格 P07 第 5 週＝153", v[("P07", 5)] == 153 and any(r["highlight"].endswith("綠框格") and r["subject"] == "P07" and r["week"] == "5" for r in rows), v[("P07", 5)])
chk("缺值例：P01 第 4 週沒量（零星）", ("P01", 4) in spor)
chk("退出例：P12 第 7 週有值、第 8 週起都沒有", v[("P12", 7)] is not None and all(v[("P12", w)] is None for w in range(8, 13)))
obs = [x for x in v.values() if x is not None]
chk("觀測值範圍 107–170", (min(obs), max(obs)) == (EXP_MIN, EXP_MAX), (min(obs), max(obs)))
chk("介入組 20 人", sum(1 for s in ids if grp[s] == "介入組") == EXP_NINT)
done()
