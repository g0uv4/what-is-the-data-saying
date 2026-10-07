#!/usr/bin/env python3
"""sample-horizon-selfcheck.py：檢查虛構樣本資料 sample-horizon-fictional.csv（數字未核）。

用法：在本資料夾執行  python3 sample-horizon-selfcheck.py
只讀指定檔名，不用萬用字元；全部用 assert 驗證，任何一項不符就會中止並顯示哪一項。

資料範圍（含兩端）：第 0 到 23 小時，共 24 個時間點；machine_01 到 machine_12，共 12 台；
24 × 12 = 288 筆。基準固定為 50（百分比）；地平線設定為 2 帶，每帶寬 25，
所以外層帶＝與基準相差超過 25（值大於 75 或小於 25）。
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

CSV_NAME = "sample-horizon-fictional.csv"          # 指定檔名，不用 glob
path = Path(__file__).resolve().parent / CSV_NAME

BASE, BAND_W, N_BANDS = 50.0, 25.0, 2

with open(path, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

# ---- 1. 形狀 -----------------------------------------------------------------
assert list(rows[0].keys()) == ["hour", "series", "cpu_percent", "data_status"]
assert len(rows) == 288                                   # 24 個時間點 × 12 台
assert all(r["data_status"] == "虛構資料，數字未核" for r in rows)
series = defaultdict(dict)
for r in rows:
    series[r["series"]][int(r["hour"])] = float(r["cpu_percent"])
assert len(series) == 12
assert sorted(series) == [f"machine_{i:02d}" for i in range(1, 13)]
for name, d in series.items():
    assert sorted(d) == list(range(24)), name             # 每台都有第 0 到 23 小時，共 24 點
values = [v for d in series.values() for v in d.values()]
assert min(values) >= 0.0 and max(values) <= 100.0

# ---- 2. 高於／低於基準 --------------------------------------------------------
above = sum(v > BASE for v in values)
below = sum(v < BASE for v in values)
equal = sum(v == BASE for v in values)
# 全部 288 筆（第 0 到 23 小時、12 台）：高於 50 的有 102 筆（約 35.4%）、
# 低於 50 的有 185 筆（約 64.2%）、剛好等於 50 的有 1 筆（約 0.3%）。三者相加 288。
assert (above, below, equal) == (102, 185, 1)
assert above + below + equal == 288
assert round(100 * above / 288, 1) == 35.4
assert round(100 * below / 288, 1) == 64.2
assert round(100 * equal / 288, 1) == 0.3

# ---- 3. 外層帶（與基準相差超過 25） -------------------------------------------
outer = [(r["series"], int(r["hour"]), float(r["cpu_percent"]))
         for r in rows if abs(float(r["cpu_percent"]) - BASE) > BAND_W]
# 288 筆中只有 5 筆在外層帶（約 1.7%）：第 14 小時的 machine_03、machine_06、machine_09
# （3 筆，都高於 75），以及 machine_11 的第 3、4 小時（2 筆，都低於 25）。
assert len(outer) == 5
assert round(100 * len(outer) / 288, 1) == 1.7
assert sorted(o for o in outer if o[1] == 14 and o[2] > BASE + BAND_W) == [
    ("machine_03", 14, 92.1), ("machine_06", 14, 100.0), ("machine_09", 14, 89.6)]
assert sorted(o[:2] for o in outer if o[2] < BASE - BAND_W) == [("machine_11", 3), ("machine_11", 4)]

# 同步衝擊：第 14 小時有 3 台同時在外層帶（12 台中的 3 台，25%）；
# 其餘 23 個小時（第 0 到 13、第 15 到 23 小時）每個小時最多只有 1 台在外層帶。
per_hour = defaultdict(int)
for _, h, _ in outer:
    per_hour[h] += 1
assert per_hour[14] == 3
assert 3 / 12 == 0.25
assert max(c for h, c in per_hour.items() if h != 14) == 1
assert sorted(h for h, c in per_hour.items() if h != 14) == [3, 4]     # 只有第 3、4 小時有 1 台（都是 machine_11）

# machine_11 連續在外層帶的長度：第 3 到 4 小時（含兩端）共 2 個點。
run = [h for s, h, _ in outer if s == "machine_11"]
assert run == [3, 4] and (run[-1] - run[0] + 1) == len(run) == 2

# ---- 4. 切帶與疊回：2 帶的矮條高度＝全距的 1/4 -------------------------------
def fold(v):
    """回傳 (方向, 第 1 帶高度, 第 2 帶高度)；方向 +1 高於基準、-1 低於基準、0 剛好等於。"""
    d = v - BASE
    a = abs(d)
    layer1 = min(a, BAND_W)
    layer2 = max(0.0, min(a, BAND_W * N_BANDS) - BAND_W)
    return (1 if d > 0 else -1 if d < 0 else 0), layer1, layer2

for v in values:
    sign, l1, l2 = fold(v)
    assert 0 <= l1 <= BAND_W and 0 <= l2 <= BAND_W
    assert abs((l1 + l2) - abs(v - BASE)) < 1e-9          # 本資料最大偏離為 50，兩帶剛好蓋住，疊回不丟資訊
assert BAND_W == (2 * BASE) / (2 * N_BANDS)                # 全距 100（0 到 100）÷（2 × 2 帶）＝25，即全距的 1/4
assert BAND_W / (2 * BASE) == 0.25
assert sum(fold(v)[2] > 0 for v in values) == len(outer) == 5   # 有第 2 帶的點，正好就是外層帶那 5 筆

# ---- 5. 常見錯誤示範：各列各自縮放，跨列不可比 ---------------------------------
# 若每台都改用「自己最大偏離的一半」當帶寬（各列各自縮放），第 14 小時進入各自外層帶的是 5 台
# （machine_03、06、07、09、12），而共用同一量尺（每帶 25）時只有 3 台。多出的 machine_07（59.4）
# 與 machine_12（58.0）只比基準高約 8 到 9 個百分點。
own_outer_14 = []
for name, d in series.items():
    own_max = max(abs(v - BASE) for v in d.values())
    if abs(d[14] - BASE) > own_max / 2:
        own_outer_14.append(name)
assert own_outer_14 == ["machine_03", "machine_06", "machine_07", "machine_09", "machine_12"]
assert len(own_outer_14) == 5 and len([o for o in outer if o[1] == 14]) == 3
assert round(series["machine_07"][14] - BASE, 1) == 9.4 and round(series["machine_12"][14] - BASE, 1) == 8.0

print("全部檢查通過：288 筆、12 台、第 0 到 23 小時；外層帶 5 筆；第 14 小時 3 台同步；共用量尺 3 台 vs 各自縮放 5 台。")
sys.exit(0)
