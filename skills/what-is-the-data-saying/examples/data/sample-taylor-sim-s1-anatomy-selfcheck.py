#!/usr/bin/env python3
"""sample-taylor-sim-s1-anatomy-selfcheck.py：圖 S1 自我檢查。
從 sample-taylor-sim-s1-anatomy.csv 用餘弦定理重算中心化均方根誤差。
E'^2 = s_r^2 + s_m^2 - 2 * s_r * s_m * R。只需 Python 標準函式庫。
用法：python3 sample-taylor-sim-s1-anatomy-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。參考標準差 s_r 取觀測列的標準差。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-taylor-sim-s1-anatomy.csv"
COLS = ["id", "std", "corr", "note"]
RESULTS = []

# 模擬記載（寫死）。標準差與相關取自 sim_facts，並對過 CSV。
# 觀測列的 note「參考點」、模型甲的 note「示意」是 CSV 原文，不是圖說的「紅方」。
REF_STD = 1.0
REF_CORR = 1.0
REF_NOTE = "參考點"
MODEL_STD = 1.2
MODEL_CORR = 0.75
MODEL_NOTE = "示意"
# math.sqrt(1^2 + 1.2^2 - 2*1*1.2*0.75)；平方和的 repr 是 0.6400000000000001，開根是 0.8。
EXPECT_E = 0.8
TOL = 1e-12

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
    chk("第一行是表頭", first.startswith("id,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
chk("欄位", list(rows[0].keys()) == COLS)
chk("2 列", len(rows) == 2)
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
obs = rows[0]
mod = rows[1]
chk(
    "觀測是參考點",
    obs["id"] == "觀測"
    and obs["note"] == REF_NOTE
    and near(float(obs["std"]), REF_STD)
    and near(float(obs["corr"]), REF_CORR),
)
chk(
    "模型甲標準差 1.2、相關 0.75、註記示意",
    mod["id"] == "模型甲"
    and mod["note"] == MODEL_NOTE
    and near(float(mod["std"]), MODEL_STD)
    and near(float(mod["corr"]), MODEL_CORR),
)
sr = float(obs["std"])
chk("觀測對自己的中心化均方根誤差是 0，且 s_r 為 1", near(sr, 1.0) and near(crmse(sr, sr, float(obs["corr"])), 0.0))
got = crmse(sr, float(mod["std"]), float(mod["corr"]))
chk("模型甲中心化均方根誤差是 0.8", near(got, EXPECT_E), got)
done()
