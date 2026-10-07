#!/usr/bin/env python3
"""sample-lasagna-s5-missing-selfcheck.py：圖 S5 自我檢查（缺值留白對錯誤補 0）。
只用 Python 標準函式庫，從 sample-lasagna-s5-missing.csv 獨立重算，與圖說／事實檔寫死的預期值比對。
用法：python3 sample-lasagna-s5-missing-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""
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
EXP_MPW = [2, 2, 0, 2, 0, 0, 2, 6, 4, 4, 6, 5]
EXP_OK = ['147.8', '147.2', '147.1', '146.3', '146.0', '143.9', '144.6', '142.3', '142.0', '141.4', '141.0', '140.5']
EXP_ZERO = ['140.4', '139.8', '147.1', '139.0', '146.0', '143.9', '137.4', '120.9', '127.8', '127.3', '119.9', '122.9']
EXP_GAP_W, EXP_GAP = 8, "21.4"
rows = read_rows("sample-lasagna-s5-missing.csv")
chk("480 列", len(rows) == 480)
by = {w: [r for r in rows if int(r["week"]) == w] for w in range(1, 13)}
mpw = [sum(r["sbp"] == "" for r in by[w]) for w in range(1, 13)]
chk("每週缺值 2,2,0,2,0,0,2,6,4,4,6,5（共 33）", mpw == EXP_MPW and sum(mpw) == 33, mpw)
chk("補 0 欄只在缺值處是 0", all((r["sbp_if_zero_filled"] == "0") == (r["sbp"] == "") and (r["sbp"] == "" or r["sbp"] == r["sbp_if_zero_filled"]) for r in rows))
chk("is_missing 欄正確", all(int(r["is_missing"]) == (r["sbp"] == "") for r in rows))
ok = [hu(mean([num(r["sbp"]) for r in by[w]])) for w in range(1, 13)]
zr = [hu(mean([int(r["sbp_if_zero_filled"]) for r in by[w]])) for w in range(1, 13)]
chk("正確每週平均（缺值不計入）", ok == EXP_OK, ok)
chk("補 0 後每週平均", zr == EXP_ZERO, zr)
chk("第 12 週 140.5 對 122.9", (ok[11], zr[11]) == ("140.5", "122.9"))
gaps = [Decimal(a) - Decimal(b) for a, b in zip(ok, zr)]
gw = max(range(12), key=lambda k: (gaps[k], -k)) + 1
chk("差距最大在第 8 週，差 21.4（142.3 對 120.9）", (gw, str(gaps[gw - 1])) == (EXP_GAP_W, EXP_GAP) and (ok[7], zr[7]) == ("142.3", "120.9"), (gw, str(gaps[gw - 1])))
done()
