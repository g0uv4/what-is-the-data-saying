#!/usr/bin/env python3
"""sample-splom-sim-s5-outlier-multicell-selfcheck.py：圖 S5 自我檢查。
從 sample-splom-sim-s5-outlier-multicell.csv 核對離群點 (22, 4, 18) 在三個變數上都離開其餘點。
只需 Python 標準函式庫。
用法：python3 sample-splom-sim-s5-outlier-multicell-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-splom-sim-s5-outlier-multicell.csv"
COLS = ["變數甲", "變數乙", "變數丙", "標記"]
RESULTS = []

EXPECT_N = 61
OUT_X, OUT_Y, OUT_Z = 22.0, 4.0, 18.0

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def read_rows(fn):
    path = os.path.join(HERE, fn)
    chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
    with open(path, encoding="utf-8", newline="") as fh:
        first = fh.readline()
        chk("第一行是表頭", first.startswith("變數甲,"))
        fh.seek(0)
        rows = list(csv.DictReader(fh))
    chk("欄位", list(rows[0].keys()) == COLS)
    chk("61 列", len(rows) == EXPECT_N)
    return rows

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
outs = [r for r in rows if r["標記"] == "離群"]
rest = [r for r in rows if r["標記"] == "一般"]
chk("60 列一般、1 列離群", len(rest) == 60 and len(outs) == 1)
o = outs[0]
chk(
    "離群點是 (22, 4, 18)",
    float(o["變數甲"]) == OUT_X and float(o["變數乙"]) == OUT_Y and float(o["變數丙"]) == OUT_Z,
)
xa = [float(r["變數甲"]) for r in rest]
yb = [float(r["變數乙"]) for r in rest]
zc = [float(r["變數丙"]) for r in rest]
chk("甲高於其餘最大值", OUT_X > max(xa), max(xa))
chk("乙低於其餘最小值", OUT_Y < min(yb), min(yb))
chk("丙高於其餘最大值", OUT_Z > max(zc), max(zc))
done()
