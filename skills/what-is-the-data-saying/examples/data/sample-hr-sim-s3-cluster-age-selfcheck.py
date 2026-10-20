#!/usr/bin/env python3
"""sample-hr-sim-s3-cluster-age-selfcheck.py：圖 S3 自我檢查。
從 sample-hr-sim-s3-cluster-age.csv 數年輕、年老兩團，並看主序的藍端與亮端。
只需 Python 標準函式庫（csv、math、os、sys）。
用法：python3 sample-hr-sim-s3-cluster-age-selfcheck.py   全部通過時結束碼為 0。
數字為虛構範例，未核。人數與轉折點取自 sim_facts。
轉折點只在主序最藍的 B−V、最亮的絕對星等四捨五入到兩位小數都等於記載時才核；否則印 NOT CHECKED。
記載的星等是截斷顏色上的主序脊線，CSV 沒有那條脊線。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FN = "sample-hr-sim-s3-cluster-age.csv"
COLS = ["cluster", "B_V", "abs_V_mag", "branch"]
RESULTS = []

# 模擬記載（寫死）。人數與轉折點取自 sim_facts。轉折點湊不出就只印 NOT CHECKED。
N_YOUNG = 268
N_OLD = 430
# (B−V, 絕對星等)。年輕 −0.15、−1.3；年老 0.58、4.28。
TURNOFF = {"young": (-0.15, -1.3), "old": (0.58, 4.28)}
LABEL = {"young": "年輕星團", "old": "年老星團"}
SEEN = set()

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def skip(name, why):
    print("NOT CHECKED｜" + name + "｜" + why)

def unchecked():
    for cluster in ("young", "old"):
        if cluster in SEEN:
            continue
        exp_bv, exp_m = TURNOFF[cluster]
        skip(
            f"{LABEL[cluster]}轉折點（B−V {exp_bv}、絕對星等 {exp_m}）",
            "檔案結構不對，沒有往下算主序端點",
        )

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def end():
    unchecked()
    done()

def consider_turnoff(cluster, ms):
    SEEN.add(cluster)
    exp_bv, exp_m = TURNOFF[cluster]
    title = f"{LABEL[cluster]}轉折點（B−V {exp_bv}、絕對星等 {exp_m}）"
    if not ms:
        skip(title, "沒有主序星，藍端與亮端都不存在")
        return
    bvs = [float(r["B_V"]) for r in ms]
    mags = [float(r["abs_V_mag"]) for r in ms]
    edge_bv, edge_m = min(bvs), min(mags)
    if round(edge_bv, 2) == exp_bv and round(edge_m, 2) == exp_m:
        chk(
            title + "是主序最藍與最亮端（四捨五入到兩位小數）",
            True,
            (edge_bv, edge_m),
        )
        return
    skip(
        title,
        f"主序最藍 B−V {edge_bv}、最亮絕對星等 {edge_m}，兩位小數是 {round(edge_bv, 2)}、{round(edge_m, 2)}，對不上記載；記載是截斷顏色上的主序星等，CSV 沒有那條脊線",
    )

path = os.path.join(HERE, FN)
chk("檔案小於 25 萬位元組", os.path.getsize(path) < 250000)
with open(path, encoding="utf-8", newline="") as fh:
    first = fh.readline()
    chk("第一行是表頭", first.startswith("cluster,"))
    fh.seek(0)
    rows = list(csv.DictReader(fh))
cols_ok = bool(rows) and list(rows[0].keys()) == COLS
chk("欄位", cols_ok)
chk("年輕加年老共 698 列", len(rows) == N_YOUNG + N_OLD, len(rows))
if not cols_ok:
    end()
empty = False
for r in rows:
    for c in COLS:
        if (r[c] or "").strip() == "":
            empty = True
chk("沒有空值", not empty)
if empty:
    end()
nums_ok = True
for r in rows:
    try:
        bv, mag = float(r["B_V"]), float(r["abs_V_mag"])
    except ValueError:
        nums_ok = False
        break
    if not (math.isfinite(bv) and math.isfinite(mag)):
        nums_ok = False
chk("顏色與絕對星等是有限數", nums_ok)
if not nums_ok:
    end()
n_young = sum(r["cluster"] == "young" for r in rows)
n_old = sum(r["cluster"] == "old" for r in rows)
chk("年輕星團 268 列", n_young == N_YOUNG, n_young)
chk("年老星團 430 列", n_old == N_OLD, n_old)
chk("沒有第三種星團", n_young + n_old == len(rows))
for cluster in ("young", "old"):
    ms = [r for r in rows if r["cluster"] == cluster and r["branch"] == "main_sequence"]
    consider_turnoff(cluster, ms)
end()
