#!/usr/bin/env python3
"""sample-splom-sim-s3-grouped-shapes-selfcheck.py：圖 S3 自我檢查。
從 sample-splom-sim-s3-grouped-shapes.csv 核對列數、三個品種與鰭長／體重的相對位置。
只需 Python 標準函式庫。
用法：python3 sample-splom-sim-s3-grouped-shapes-selfcheck.py   全部通過時結束碼為 0。
底層是 Palmer Penguins（CC0）四個測量欄加品種，不是虛構亂數；課程稿圖說仍標未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-splom-sim-s3-grouped-shapes.csv"
COLS = ["嘴峰長", "嘴峰深", "鰭長", "體重", "品種"]
NUMS = ["嘴峰長", "嘴峰深", "鰭長", "體重"]
RESULTS = []

EXPECT_N = 333
EXPECT_COUNTS = {"阿德利": 146, "帽帶": 68, "巴布亞": 119}
# 重疊邊界（寫死；自檢用來說明「偏右上」不是完全分開）
GENTOO_FLIP_MIN = 203.0
ADELIE_FLIP_MAX = 210.0
CHIN_FLIP_MAX = 212.0
GENTOO_MASS_MIN = 3950.0
ADELIE_MASS_MAX = 4775.0
CHIN_MASS_MAX = 4800.0

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def read_rows(fn):
    path = os.path.join(HERE, fn)
    chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
    with open(path, encoding="utf-8", newline="") as fh:
        first = fh.readline()
        chk("第一行是表頭", first.startswith("嘴峰長,"))
        fh.seek(0)
        rows = list(csv.DictReader(fh))
    chk("欄位", list(rows[0].keys()) == COLS)
    chk("333 列", len(rows) == EXPECT_N)
    return rows

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

rows = read_rows(FN)
empty = 0
counts = {}
flip = {}
mass = {}
for r in rows:
    g = r["品種"]
    counts[g] = counts.get(g, 0) + 1
    for c in NUMS:
        if (r[c] or "").strip() == "":
            empty += 1
    flip.setdefault(g, []).append(float(r["鰭長"]))
    mass.setdefault(g, []).append(float(r["體重"]))
chk("沒有空的測量值", empty == 0)
chk("恰好三個品種", set(counts) == set(EXPECT_COUNTS))
chk("品種人數", counts == EXPECT_COUNTS, counts)

def mean(xs):
    return sum(xs) / len(xs)

gentoo_flip = mean(flip["巴布亞"])
gentoo_mass = mean(mass["巴布亞"])
chk(
    "巴布亞平均鰭長與平均體重都最高",
    gentoo_flip > mean(flip["阿德利"]) and gentoo_flip > mean(flip["帽帶"])
    and gentoo_mass > mean(mass["阿德利"]) and gentoo_mass > mean(mass["帽帶"]),
    (gentoo_flip, gentoo_mass),
)
chk(
    "鰭長沒有完全分開",
    min(flip["巴布亞"]) == GENTOO_FLIP_MIN
    and max(flip["阿德利"]) == ADELIE_FLIP_MAX
    and max(flip["帽帶"]) == CHIN_FLIP_MAX
    and min(flip["巴布亞"]) < max(flip["阿德利"])
    and min(flip["巴布亞"]) < max(flip["帽帶"]),
)
chk(
    "體重沒有完全分開",
    min(mass["巴布亞"]) == GENTOO_MASS_MIN
    and max(mass["阿德利"]) == ADELIE_MASS_MAX
    and max(mass["帽帶"]) == CHIN_MASS_MAX
    and min(mass["巴布亞"]) < max(mass["阿德利"])
    and min(mass["巴布亞"]) < max(mass["帽帶"]),
)
done()
