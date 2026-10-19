#!/usr/bin/env python3
"""sample-taylor-sim-s4-crowded-vs-few-selfcheck.py：圖 S4 自我檢查。
從 sample-taylor-sim-s4-crowded-vs-few.csv 核對 few 面板的四個點。
中心化均方根誤差以 s_r = 1 用餘弦定理重算。
E'^2 = s_r^2 + s_m^2 - 2 * s_r * s_m * R。只需 Python 標準函式庫。
用法：python3 sample-taylor-sim-s4-crowded-vs-few-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。模擬記載的擁擠面板是 24 點，這份 CSV 沒有那 24 列，本腳本不核對它們。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-taylor-sim-s4-crowded-vs-few.csv"
COLS = ["panel", "id", "std", "corr"]
RESULTS = []
SR = 1.0
TOL = 1e-12
FEW_N = 4

# 模擬記載的 few 四點（寫死），並對過 CSV。中心化均方根誤差是 math.sqrt 的 repr。
EXPECT = [
    ("甲", 1.02, 0.93, 0.3784177585684897),
    ("乙", 1.25, 0.8, 0.75),
    ("丙", 0.88, 0.7, 0.7364781055808788),
    ("丁", 1.4, 0.55, 1.1916375287812984),
]

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def crmse(sr, sm, r):
    return math.sqrt(sr * sr + sm * sm - 2.0 * sr * sm * r)

def near(got, exp):
    return abs(got - exp) <= TOL

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("panel,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
chk("欄位", list(rows[0].keys()) == COLS)
chk("4 列", len(rows) == FEW_N)
panels = {r["panel"] for r in rows}
chk("只有 few 面板，沒有 crowded，也不是 24 列", panels == {"few"} and len(rows) != 24)
empty = False
vals_ok = True
errs = []
for r, e in zip(rows, EXPECT):
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
    if r["id"] != e[0] or not (near(float(r["std"]), e[1]) and near(float(r["corr"]), e[2])):
        vals_ok = False
    errs.append(crmse(SR, float(r["std"]), float(r["corr"])))
chk("沒有空值", not empty)
chk("甲乙丙丁的標準差與相關", vals_ok and [r["id"] for r in rows] == [e[0] for e in EXPECT])
err_ok = all(near(got, e[3]) for got, e in zip(errs, EXPECT))
chk("四個中心化均方根誤差", err_ok, errs)
chk("乙的中心化均方根誤差是 0.75", near(errs[1], 0.75), errs[1])
chk("甲的中心化均方根誤差最小", errs[0] < min(errs[1:]))
done()
