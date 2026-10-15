#!/usr/bin/env python3
"""sample-taylor-sim-s3-normalize-selfcheck.py：圖 S3 自我檢查。
從 sample-taylor-sim-s3-normalize.csv 核對未正規化與正規化兩格。
中心化均方根誤差只在正規化後、以 s_r = 1 用餘弦定理重算。
E'^2 = s_r^2 + s_m^2 - 2 * s_r * s_m * R。只需 Python 標準函式庫。
用法：python3 sample-taylor-sim-s3-normalize-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。sim_facts 沒有這四列的數字，預期值是對過 CSV 後寫死的。
不把原始雨量的標準差拿去除，也不用 s_r = 1 去算原始雨量的中心化均方根誤差。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-taylor-sim-s3-normalize.csv"
COLS = ["panel", "var", "std_or_norm", "corr"]
RESULTS = []
SR = 1.0
TOL = 1e-12

# 列順序與數值寫死（對過 CSV）。中心化均方根誤差只給正規化後兩列。
EXPECT_ROWS = [
    ("raw", "雨量", 3.2, 0.85),
    ("raw", "氣溫", 1.1, 0.9),
    ("norm", "雨量", 1.07, 0.85),
    ("norm", "氣溫", 1.1, 0.9),
]
EXPECT_E = {
    "雨量": 0.5708765190476832,
    "氣溫": 0.4795831523312717,
}

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
order = [(r["panel"], r["var"]) for r in rows]
chk("4 列且順序是 raw 雨量、raw 氣溫、norm 雨量、norm 氣溫", order == [(a, b) for a, b, _, _ in EXPECT_ROWS])
empty = False
vals_ok = True
for r, e in zip(rows, EXPECT_ROWS):
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
    if not (near(float(r["std_or_norm"]), e[2]) and near(float(r["corr"]), e[3])):
        vals_ok = False
chk("沒有空值", not empty)
chk("四列的標準差或正規化值與相關", vals_ok)
by = {}
for r in rows:
    by[(r["panel"], r["var"])] = (float(r["std_or_norm"]), float(r["corr"]))
chk(
    "同一變數兩格的相關相同",
    near(by[("raw", "雨量")][1], by[("norm", "雨量")][1])
    and near(by[("raw", "氣溫")][1], by[("norm", "氣溫")][1]),
)
chk(
    "氣溫標準差不變、雨量有變",
    near(by[("raw", "氣溫")][0], by[("norm", "氣溫")][0])
    and not near(by[("raw", "雨量")][0], by[("norm", "雨量")][0]),
)
e_rain = crmse(SR, by[("norm", "雨量")][0], by[("norm", "雨量")][1])
e_temp = crmse(SR, by[("norm", "氣溫")][0], by[("norm", "氣溫")][1])
chk("正規化雨量的中心化均方根誤差", near(e_rain, EXPECT_E["雨量"]), e_rain)
chk("正規化氣溫的中心化均方根誤差", near(e_temp, EXPECT_E["氣溫"]), e_temp)
chk("正規化後氣溫比雨量更靠近觀測", e_temp < e_rain)
done()
