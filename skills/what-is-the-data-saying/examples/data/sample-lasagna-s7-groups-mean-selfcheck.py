#!/usr/bin/env python3
"""sample-lasagna-s7-groups-mean-selfcheck.py：圖 S7 自我檢查（分組面板＋每組每週平均折線；四捨五入 148.4／＋1.8）。
只用 Python 標準函式庫，從 sample-lasagna-s7-groups-mean.csv 獨立重算，與圖說／事實檔寫死的預期值比對。
用法：python3 sample-lasagna-s7-groups-mean-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""
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
EXP_C1, EXP_C12, EXP_I1, EXP_I12 = "148.4", "150.2", "147.2", "130.2"
EXP_CCH, EXP_ICH, EXP_GAP = "+1.8", "-17.0", "+20.0"
EXP_MC, EXP_MI, EXP_CTOP, EXP_ITOP = 15, 18, 'P19', 'P02'
rows = read_rows("sample-lasagna-s7-groups-mean.csv")
val = lambda g, w: [num(r["sbp"]) for r in rows if r["group"] == g and int(r["week"]) == w]
mc1 = mean(val("對照組", 1))
chk("對照組第 1 週平均精確值＝148.35（落在進位邊界）", mc1 == Fraction(14835, 100), str(mc1))
c1, c12 = hu(mc1), hu(mean(val("對照組", 12)))
i1, i12 = hu(mean(val("介入組", 1))), hu(mean(val("介入組", 12)))
chk("對照組 148.4 → 150.2（四捨五入，逢 5 進位）", (c1, c12) == (EXP_C1, EXP_C12), (c1, c12))
chk("對照組變化 ＋1.8", hsub(c12, c1) == EXP_CCH, hsub(c12, c1))
chk("介入組 147.2 → 130.2，變化 －17.0", (i1, i12, hsub(i12, i1)) == (EXP_I1, EXP_I12, EXP_ICH), (i1, i12, hsub(i12, i1)))
chk("第 12 週對照組比介入組高 20.0", hsub(c12, i12) == EXP_GAP, hsub(c12, i12))
chk("提醒：圖上標籤的格式化會顯示 148.3（與圖說 148.4 差在進位方式）", "%.1f" % float(mc1) == "148.3" and c1 == "148.4", "%.1f" % float(mc1))
mc = sum(r["sbp"] == "" for r in rows if r["group"] == "對照組"); mi = sum(r["sbp"] == "" for r in rows if r["group"] == "介入組")
chk("缺值：對照組 15 格、介入組 18 格", (mc, mi) == (EXP_MC, EXP_MI), (mc, mi))
subj = sorted({r["subject"] for r in rows})
d = {s: [num(r["sbp"]) for r in sorted((r for r in rows if r["subject"] == s), key=lambda r: int(r["week"]))] for s in subj}
grp = {r["subject"]: r["group"] for r in rows}
oc = order_by_mean(d, [s for s in subj if grp[s] == "對照組"]); oi = order_by_mean(d, [s for s in subj if grp[s] == "介入組"])
chk("組內最上方：對照組 P19、介入組 P02", (oc[0], oi[0]) == (EXP_CTOP, EXP_ITOP), (oc[0], oi[0]))
chk("row_in_group_panel 與組內排序一致", all(int(r["row_in_group_panel"]) == (oc if grp[r["subject"]] == "對照組" else oi).index(r["subject"]) + 1 for r in rows))
done()
