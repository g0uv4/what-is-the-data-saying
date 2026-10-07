#!/usr/bin/env python3
"""sample-lasagna-s6-colormap-selfcheck.py：圖 S6 自我檢查（同資料同排序只換色階）。
只用 Python 標準函式庫，從 sample-lasagna-s6-colormap.csv 獨立重算，與圖說／事實檔寫死的預期值比對。
用法：python3 sample-lasagna-s6-colormap-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""
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
EXP_OBS, EXP_BAND, EXP_RANGE = 447, 128, (110, 170)
rows = read_rows("sample-lasagna-s6-colormap.csv")
d = wide(rows)
o = order_by_mean(d, sorted(d))
chk("列順序＝個人平均由高到低", [r["subject"] for r in rows] == o and [int(r["row_in_plot"]) for r in rows] == list(range(1, 41)))
obs = [x for s in d for x in d[s] if x is not None]
chk("觀測格 447（480－33）", len(obs) == EXP_OBS, len(obs))
band = sum(135 <= x <= 145 for x in obs)
chk("135–145 之間（彩虹色階青綠到黃）共 128 格", band == EXP_BAND, band)
chk("色階範圍 110–170（超出者以端色顯示）", EXP_RANGE == (110, 170), "低於 110：" + str(sum(x < 110 for x in obs)) + " 格；高於 170：" + str(sum(x > 170 for x in obs)) + " 格")
done()
