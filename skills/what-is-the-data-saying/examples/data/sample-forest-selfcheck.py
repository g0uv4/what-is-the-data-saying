# -*- coding: utf-8 -*-
"""
森林圖素材包的自我檢查程式。
用指定檔名讀取同資料夾的 sample-forest-fictional.csv（虛構、數字未核；不用 glob），
重算每個資料集（S1–S8，對應教學稿的圖 S1–S8）的權重、合併估計、Cochran 的 Q、I²、τ²，
並用 assert 驗證教學稿圖說裡的數字與文字判斷。任何一句不符就會中止並顯示是哪一句。
執行：python3 sample-forest-selfcheck.py      （只需要 numpy；若已安裝 statsmodels，會多做一道交叉核對）

方法固定如下，註解與輸出都以此為準：
  * 區間：95% 信賴區間 = 效應量（比值先取自然對數）± 1.96 × 標準誤；比值類的結果再取指數換回風險比。
  * 固定效應：權重 = 1／標準誤²；合併估計 = Σ(權重×效應)／Σ權重；合併標準誤 = 1／√Σ權重。
  * Q = Σ 權重×(效應 − 合併估計)²；df = 研究數 − 1；I² = max(0, (Q − df)/Q) × 100%。
  * 隨機效應用 DerSimonian–Laird（DL）：τ² = max(0, (Q − df)/(Σ權重 − Σ權重²/Σ權重))，
    隨機效應權重 = 1／(標準誤² + τ²)。
  * statsmodels 的 combine_effects 預設 method_re='iterated'，那是 Paule–Mandel（PM）迭代法，不是 DL；
    要得到 DL 必須寫 method_re='dl'。DL 的 τ² 在 statsmodels 裡不截為 0（Q 小於 df 時會是負值），本程式的 τ² 截為 0。
  * 文字中的「顯示值」一律是實際值四捨五入到指定小數位（不是無條件捨去）。
"""
import csv
import math
import os
from collections import defaultdict

import numpy as np

CSV_NAME = 'sample-forest-fictional.csv'            # 指定檔名，不用 glob
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), CSV_NAME)
Z = 1.96
LINES = []


def say(s):
    LINES.append(s)
    print(s)


def f(x, n):
    """顯示值：四捨五入到小數 n 位。"""
    return f'{x:.{n}f}'


# ------------------------------------------------------------------ 讀檔
with open(CSV_PATH, encoding='utf8') as fh:
    ROWS = list(csv.DictReader(line for line in fh if not line.startswith('#')))
assert len(ROWS) == 61, len(ROWS)
G = defaultdict(list)
for r in ROWS:
    G[(r['dataset'], r['panel'])].append(r)
assert sorted({r['dataset'] for r in ROWS}) == [f'S{i}' for i in range(1, 9)]
assert len(G) == 10                                   # S3 與 S4 各有 2 個分析單位，其餘各 1 個


def arr(ds, panel, col):
    return np.array([float(r[col]) for r in G[(ds, panel)]])


def meta(y, se):
    y = np.asarray(y, float)
    se = np.asarray(se, float)
    w = 1 / se**2
    sw = w.sum()
    mu = float((w * y).sum() / sw)
    se_mu = 1 / math.sqrt(sw)
    Q = float((w * (y - mu)**2).sum())
    df = len(y) - 1
    tau2_raw = (Q - df) / (sw - (w**2).sum() / sw)
    i2_raw = (Q - df) / Q * 100
    wr = 1 / (se**2 + max(0.0, tau2_raw))
    mur = float((wr * y).sum() / wr.sum())
    se_mur = 1 / math.sqrt(wr.sum())
    return dict(w=w, wpct=100 * w / sw, mu=mu, se=se_mu, lo=mu - Z * se_mu, hi=mu + Z * se_mu, Q=Q, df=df,
                tau2_raw=tau2_raw, tau2=max(0.0, tau2_raw), i2_raw=i2_raw, i2=max(0.0, i2_raw),
                wr=wr, wrpct=100 * wr / wr.sum(), mur=mur, lor=mur - Z * se_mur, hir=mur + Z * se_mur)


def study_ci(y, se):
    return y - Z * se, y + Z * se


def pooled_rr(m):
    return math.exp(m['mu']), math.exp(m['lo']), math.exp(m['hi'])


def crosses(lo, hi, null):
    """區間 [lo, hi] 是否含無效線：下限 < 無效值 < 上限。"""
    return bool(lo < null < hi)


M = {}
for key in G:
    M[key] = meta(arr(*key, 'analysis_value'), arr(*key, 'se'))

# ------------------------------------------------------------------ 0. CSV 推導欄與重算相符
for key, rows in G.items():
    y, se = arr(*key, 'analysis_value'), arr(*key, 'se')
    lo, hi = study_ci(y, se)
    if rows[0]['measure'] == 'RR':
        lo, hi = np.exp(lo), np.exp(hi)
        assert np.allclose(np.exp(y), arr(*key, 'effect'), atol=5e-7), key   # 顯示值是 RR 本身（S8 存 6 位小數）
    else:
        assert np.allclose(y, arr(*key, 'effect'), atol=1e-12), key
    assert np.allclose(lo, arr(*key, 'ci_lower'), atol=5.01e-5), key       # CSV 的區間欄以 4 位小數存放
    assert np.allclose(hi, arr(*key, 'ci_upper'), atol=5.01e-5), key
    assert np.allclose(M[key]['wpct'], arr(*key, 'weight_fixed_pct'), atol=5.01e-5), key
    assert abs(arr(*key, 'weight_fixed_pct').sum() - 100) < 5e-4, key      # 每個分析單位的固定效應權重合計 100%
say(f'[CSV] 61 列、8 個資料集、10 個分析單位；區間欄與權重欄重算相符')

# ------------------------------------------------------------------ S1：6 項模擬研究（圖 S1）
key = ('S1', 'main')
m = M[key]
y, se = arr(*key, 'analysis_value'), arr(*key, 'se')
lo, hi = np.exp(study_ci(y, se)[0]), np.exp(study_ci(y, se)[1])
assert [f(v, 2) for v in lo] == ['0.51', '0.47', '0.37', '0.75', '0.34', '0.60']
assert [f(v, 2) for v in hi] == ['0.96', '1.53', '0.98', '1.20', '1.64', '1.07']
assert [f(v, 1) for v in m['wpct']] == ['21.0', '6.0', '8.6', '37.3', '3.4', '23.9']   # 權重百分比，小數 1 位
assert abs(m['wpct'].sum() - 100) < 1e-9
assert [f(v, 2) for v in pooled_rr(m)] == ['0.81', '0.70', '0.94']                    # 合併 RR 0.81，95% 信賴區間 [0.70, 0.94]
assert pooled_rr(m)[2] < 1                                                            # 合併區間上限 < 1：菱形整個在 1 的左側
assert f(m['Q'], 2) == '4.11' and m['df'] == 5
# Q（4.11）小於 df（5），所以 (Q−df)/Q 為負值，I² 依定義取 0；DL 的 τ² 原始值也是負的，取 0
assert m['i2_raw'] < 0 and f(m['i2'], 1) == '0.0' and m['tau2_raw'] < 0 and m['tau2'] == 0
# 以各研究的 95% 信賴區間判定：上限 < 1 的是研究 A、C 共 2 項；其餘 4 項區間含 1（下限 < 1 < 上限）
not_cross = [not crosses(a, b, 1) for a, b in zip(lo, hi)]
assert not_cross == [True, False, True, False, False, False] and sum(not_cross) == 2
assert all(b < 1 for a, b, nc in zip(lo, hi, not_cross) if nc)
# 研究 D 對研究 E 的權重比 = (0.40/0.12)² ≈ 11.1；方塊面積與權重成正比是畫圖的設計，這裡只驗權重比
assert abs(m['w'][3] / m['w'][4] - (0.40 / 0.12)**2) < 1e-9
say(f'[S1] 合併 RR {f(pooled_rr(m)[0], 2)} [{f(pooled_rr(m)[1], 2)}, {f(pooled_rr(m)[2], 2)}]；Q={f(m["Q"], 2)}，df={m["df"]}，'
    f'I²={f(m["i2"], 1)}%（原始值 {f(m["i2_raw"], 1)}% 截為 0），τ²={f(m["tau2"], 3)}（DL 原始值 {f(m["tau2_raw"], 4)} 截為 0）；'
    f'95% 區間不跨過 1 的研究 {sum(not_cross)} 項、含 1 的 {len(not_cross) - sum(not_cross)} 項')

# ------------------------------------------------------------------ S2：5 項（圖 S2）
key = ('S2', 'main')
m = M[key]
y, se = arr(*key, 'analysis_value'), arr(*key, 'se')
lo, hi = np.exp(study_ci(y, se)[0]), np.exp(study_ci(y, se)[1])
assert [f(v, 2) for v in lo] == ['0.44', '0.53', '0.46', '0.70', '0.78']
assert [f(v, 2) for v in hi] == ['0.82', '0.92', '1.48', '1.88', '1.11']
cross = [crosses(a, b, 1) for a, b in zip(lo, hi)]
assert cross == [False, False, True, True, True]       # 前兩項區間不含 1（藍），後三項區間含 1（橘）
assert [f(v, 2) for v in pooled_rr(m)] == ['0.82', '0.72', '0.93'] and pooled_rr(m)[2] < 1   # 固定效應合併，菱形上限 < 1
assert f(m['i2'], 1) == '54.9'
assert 50 <= m['i2'] <= 60      # 54.9% 同時落在 Cochrane 手冊粗略分級的「30–60%」與「50–90%」兩個重疊區間（要 50 ≤ I² ≤ 60）
say(f'[S2] 前 2 項 95% 區間不含 1、後 3 項含 1；固定效應合併 RR {f(pooled_rr(m)[0], 2)} [{f(pooled_rr(m)[1], 2)}, {f(pooled_rr(m)[2], 2)}]（上限 < 1）；'
    f'I²={f(m["i2"], 1)}%（落在 30–60% 與 50–90% 兩個重疊區間）')

# ------------------------------------------------------------------ S3：RR 線性軸 vs 對數軸，以及差值（圖 S3）
key = ('S3', 'RR')
m = M[key]
y, se = arr(*key, 'analysis_value'), arr(*key, 'se')
est = np.exp(y)
lo, hi = np.exp(study_ci(y, se)[0]), np.exp(study_ci(y, se)[1])
assert [f(v, 2) for v in lo] == ['0.28', '0.60', '0.84', '1.16', '0.17']
assert [f(v, 2) for v in hi] == ['0.90', '1.07', '1.85', '3.46', '0.97']
assert [f(v, 2) for v in pooled_rr(m)] == ['0.92', '0.76', '1.13'] and crosses(pooled_rr(m)[1], pooled_rr(m)[2], 1)   # 合併區間含 1
# 研究 D（RR 2.00）在線性軸上，估計點左側長 = 估計 − 下限，右側長 = 上限 − 估計
assert (f(est[3] - lo[3], 2), f(hi[3] - est[3], 2)) == ('0.84', '1.46')
# 區間由 exp(ln RR ± 1.96×標準誤) 求得，所以在對數軸上左右等長（這個對稱只在區間這樣求得時成立）
assert np.allclose(np.log(est) - np.log(lo), np.log(hi) - np.log(est))
key_md = ('S3', 'MD')
mm = M[key_md]
assert [f(v, 2) for v in (mm['mu'], mm['lo'], mm['hi'])] == ['-1.68', '-2.67', '-0.70'] and mm['hi'] < 0   # 差值的無效線在 0，合併上限 < 0
say(f'[S3] RR 合併 {f(pooled_rr(m)[0], 2)} [{f(pooled_rr(m)[1], 2)}, {f(pooled_rr(m)[2], 2)}]（含 1）；研究 D 線性軸左 {f(est[3] - lo[3], 2)}、右 {f(hi[3] - est[3], 2)}，對數軸等長；'
    f'差值合併 {f(mm["mu"], 2)} [{f(mm["lo"], 2)}, {f(mm["hi"], 2)}]（上限 < 0）')

# ------------------------------------------------------------------ S4：異質性低 vs 高（圖 S4）
low, high = M[('S4', 'low')], M[('S4', 'high')]
assert [f(math.exp(v), 2) for v in arr('S4', 'low', 'analysis_value')] == ['0.68', '0.74', '0.70', '0.66', '0.76', '0.70']
assert [f(math.exp(v), 2) for v in arr('S4', 'high', 'analysis_value')] == ['0.41', '0.90', '0.58', '1.28', '0.45', '0.82']
assert (f(low['Q'], 2), low['df'], f(low['i2'], 1), f(low['tau2'], 3)) == ('0.36', 5, '0.0', '0.000')
assert low['tau2_raw'] < 0                                   # (a) 的 DL 原始 τ² 為負，截為 0
assert [f(v, 2) for v in pooled_rr(low)] == ['0.70', '0.63', '0.79']
assert (f(high['Q'], 2), high['df'], f(high['i2'], 1), f(high['tau2'], 3)) == ('35.43', 5, '85.9', '0.138')
assert f((35.43 - 5) / 35.43 * 100, 1) == '85.9'             # 用顯示的 Q=35.43 手算 I² 也是 85.9%
assert [f(v, 2) for v in pooled_rr(high)] == ['0.63', '0.56', '0.71']
# 圖說的警語：若直接拿顯示的兩位數風險比重算，Q 會略有不同（(b) 約 34.75）
y_round = np.log([float(f(math.exp(v), 2)) for v in arr('S4', 'high', 'analysis_value')])
q_round = meta(y_round, arr('S4', 'high', 'se'))['Q']
assert f(q_round, 2) == '34.75' and f(q_round, 2) != f(high['Q'], 2)
say(f'[S4] (a) Q={f(low["Q"], 2)}，I²={f(low["i2"], 1)}%，τ²={f(low["tau2"], 3)}，合併 {f(pooled_rr(low)[0], 2)}；'
    f'(b) Q={f(high["Q"], 2)}，I²={f(high["i2"], 1)}%，τ²(DL)={f(high["tau2"], 3)}，合併 {f(pooled_rr(high)[0], 2)}；用顯示的兩位數 RR 重算 (b) 的 Q={f(q_round, 2)}')

# ------------------------------------------------------------------ S5：固定 vs 隨機（DL）（圖 S5）
key = ('S5', 'main')
m = M[key]
assert (f(m['Q'], 2), m['df'], f(m['i2'], 1), f(m['tau2'], 3)) == ('16.05', 6, '62.6', '0.060')
assert math.floor(m['tau2'] * 1000) / 1000 == 0.059          # 實際 τ² 約 0.05965：顯示 0.060 是四捨五入，不是捨去（捨去會是 0.059）
fx = pooled_rr(m)
rd = (math.exp(m['mur']), math.exp(m['lor']), math.exp(m['hir']))
assert [f(v, 2) for v in fx] == ['0.75', '0.66', '0.85'] and [f(v, 2) for v in rd] == ['0.72', '0.56', '0.92']
wfix, wrnd = m['hi'] - m['lo'], m['hir'] - m['lor']          # 對數風險比尺度下的區間寬
assert (f(wfix, 3), f(wrnd, 3), f(wrnd / wfix, 1)) == ('0.255', '0.495', '1.9')   # 隨機效應區間寬是固定效應的約 1.9 倍（1.94 四捨五入）
assert [f(m['wpct'][i], 1) for i in (0, 1, 6)] == ['29.4', '42.4', '2.6']          # 固定效應：第 1、2、7 項
assert [f(m['wrpct'][i], 1) for i in (0, 1, 6)] == ['21.5', '22.9', '7.2']         # 隨機效應：第 1、2、7 項
assert int(np.argmin(m['wpct'])) == 6 and m['wrpct'][6] > m['wpct'][6]            # 第七項固定權重最小，隨機效應下相對權重變大
say(f'[S5] Q={f(m["Q"], 2)}，df={m["df"]}，I²={f(m["i2"], 1)}%，τ²(DL)={f(m["tau2"], 3)}（實際 {m["tau2"]:.5f}）；固定 {f(fx[0], 2)} [{f(fx[1], 2)}, {f(fx[2], 2)}] 寬 {f(wfix, 3)}；'
    f'隨機(DL) {f(rd[0], 2)} [{f(rd[1], 2)}, {f(rd[2], 2)}] 寬 {f(wrnd, 3)}（{f(wrnd / wfix, 2)} 倍）；第七項權重 {f(m["wpct"][6], 1)}%→{f(m["wrpct"][6], 1)}%')

# ------------------------------------------------------------------ S6：亞組（圖 S6）
key = ('S6', 'main')
m = M[key]
sub = np.array([r['subgroup'] for r in G[key]])
y, se = arr(*key, 'analysis_value'), arr(*key, 'se')
lo, hi = np.exp(study_ci(y, se)[0]), np.exp(study_ci(y, se)[1])
assert [f(v, 2) for v in lo] == ['0.37', '0.52', '0.36', '0.67', '0.83', '0.49']
assert [f(v, 2) for v in hi] == ['0.81', '0.94', '1.07', '1.35', '1.33', '1.58']
assert [f(v, 1) for v in m['wpct']] == ['12.9', '23.0', '6.6', '15.9', '35.9', '5.7']   # 方塊面積依占全部 6 項的固定效應權重
ma, mb = meta(y[sub == 'A'], se[sub == 'A']), meta(y[sub == 'B'], se[sub == 'B'])
assert [f(v, 2) for v in pooled_rr(ma)] == ['0.64', '0.51', '0.79'] and f(ma['i2'], 1) == '0.0' and ma['i2_raw'] < 0   # 亞組 A：Q<df，I² 取 0
assert [f(v, 2) for v in pooled_rr(mb)] == ['1.00', '0.83', '1.21']
assert [f(v, 2) for v in pooled_rr(m)] == ['0.83', '0.72', '0.95'] and pooled_rr(m)[2] < 1
# 亞組間差異：兩種算法（組間離差平方和 / 總 Q 減兩個組內 Q）結果相同
mus, ses = np.array([ma['mu'], mb['mu']]), np.array([ma['se'], mb['se']])
wg = 1 / ses**2
qb1 = float((wg * (mus - (wg * mus).sum() / wg.sum())**2).sum())
qb2 = m['Q'] - ma['Q'] - mb['Q']
assert abs(qb1 - qb2) < 1e-9
pb = math.erfc(math.sqrt(qb1 / 2))                           # 自由度 1 的卡方右尾機率 = erfc(√(Q/2))
assert (f(qb1, 2), f(pb, 3)) == ('9.68', '0.002')
say(f'[S6] 亞組 A {f(pooled_rr(ma)[0], 2)} [{f(pooled_rr(ma)[1], 2)}, {f(pooled_rr(ma)[2], 2)}]（I²={f(ma["i2"], 1)}%），亞組 B {f(pooled_rr(mb)[0], 2)} [{f(pooled_rr(mb)[1], 2)}, {f(pooled_rr(mb)[2], 2)}]，'
    f'全部 {f(pooled_rr(m)[0], 2)} [{f(pooled_rr(m)[1], 2)}, {f(pooled_rr(m)[2], 2)}]；亞組間 Q={f(qb1, 2)}（df=1，兩種算法相同），p={pb:.4f}→{f(pb, 3)}')

# ------------------------------------------------------------------ S7：方塊大小 ≠ 效果大小（圖 S7）
key = ('S7', 'main')
m = M[key]
y, se = arr(*key, 'analysis_value'), arr(*key, 'se')
est = np.exp(y)
lo, hi = np.exp(study_ci(y, se)[0]), np.exp(study_ci(y, se)[1])
assert [f(v, 2) for v in lo] == ['0.85', '0.12', '0.54', '0.33', '0.23']
assert [f(v, 2) for v in hi] == ['1.08', '1.03', '1.18', '1.16', '1.33']
assert [f(v, 1) for v in m['wpct']] == ['86.6', '1.0', '7.8', '3.0', '1.5']
assert int(np.argmax(m['wpct'])) == 0 and f(est[0], 2) == '0.96'                    # 權重最大的是「大樣本」，RR 0.96
assert int(np.argmin(est)) == 1 and f(est[1], 2) == '0.35'                          # RR 最小（離 1 最遠）的是「小樣本」
assert crosses(lo[1], hi[1], 1)                                                     # 其區間 [0.12, 1.03] 含 1
assert f(m['w'][0] / m['w'][1], 0) == '84'                                          # 兩者權重比 84.0 倍（面積∝權重是畫圖設計）
assert [f(v, 2) for v in pooled_rr(m)] == ['0.92', '0.82', '1.02'] and pooled_rr(m)[2] > 1   # 合併上限 1.02 > 1：菱形右端略過 1
say(f'[S7] 權重 {"／".join(f(v, 1) for v in m["wpct"])}（%）；最大權重研究 RR {f(est[0], 2)}，RR 最小研究 {f(est[1], 2)}（區間 [{f(lo[1], 2)}, {f(hi[1], 2)}] 含 1），'
    f'權重比 {f(m["w"][0] / m["w"][1], 1)} 倍；合併 {f(pooled_rr(m)[0], 2)} [{f(pooled_rr(m)[1], 2)}, {f(pooled_rr(m)[2], 2)}]（上限 > 1）')

# ------------------------------------------------------------------ S8：森林圖與漏斗圖（圖 S8）
key = ('S8', 'main')
m = M[key]
y, se = arr(*key, 'analysis_value'), arr(*key, 'se')
rng = np.random.default_rng(9)                                # 亂數種子 9：真實效應 ln RR = −0.25，y = −0.25 + 標準常態 × 標準誤
assert np.allclose(y, -0.25 + rng.normal(0, 1, 10) * se, atol=1e-9)
assert [f(v, 2) for v in np.exp(y)] == ['0.72', '0.80', '0.62', '0.87', '0.96', '0.71', '0.86', '0.83', '0.69', '0.58']
assert [f(v, 1) for v in m['wpct']] == ['27.1', '18.9', '13.9', '10.6', '8.4', '6.8', '5.1', '4.0', '3.0', '2.2']
assert [f(v, 2) for v in pooled_rr(m)] == ['0.76', '0.68', '0.84'] and f(m['i2'], 1) == '0.0' and m['i2_raw'] < 0
# 漏斗圖的灰虛線 = 合併估計 ± 1.96×標準誤；10 個研究點（含權重最大的、也是最靠近頂端的研究 1）都在虛線之內
inside = int((np.abs(y - m['mu']) <= Z * se).sum())
assert inside == 10 and len(y) == 10
say(f'[S8] 10 項（種子 9）合併 {f(pooled_rr(m)[0], 2)} [{f(pooled_rr(m)[1], 2)}, {f(pooled_rr(m)[2], 2)}]，I²={f(m["i2"], 1)}%；'
    f'落在「合併估計 ±1.96×標準誤」之內的點 {inside}／10（兩條虛線之間，含研究 1 本身）')

# ------------------------------------------------------------------ 交叉核對：statsmodels（選用）
try:
    import statsmodels
    from statsmodels.stats.meta_analysis import combine_effects
    HAVE_SM = True
except Exception:
    HAVE_SM = False
if HAVE_SM:
    for key in G:
        y, se = arr(*key, 'analysis_value'), arr(*key, 'se')
        m = M[key]
        dl = combine_effects(y, se**2, method_re='dl')           # DerSimonian–Laird
        pm = combine_effects(y, se**2)                           # 預設 method_re='iterated'：Paule–Mandel，不是 DL
        sf = dl.summary_frame()
        assert abs(sf.loc['fixed effect', 'eff'] - m['mu']) < 1e-8
        assert abs(dl.q - m['Q']) < 1e-8
        assert abs(dl.tau2 - m['tau2_raw']) < 1e-8               # statsmodels 的 DL τ² 不截為 0，所以和本程式的「原始值」比
        assert abs(max(0.0, dl.i2 * 100) - m['i2']) < 1e-6       # statsmodels 的 i2 可為負，截為 0 後比較
        if m['tau2_raw'] > 0:                                    # τ² > 0 時，隨機效應合併估計也要相同
            assert abs(sf.loc['random effect', 'eff'] - m['mur']) < 1e-6
    m5 = M[('S5', 'main')]
    pm5 = combine_effects(arr('S5', 'main', 'analysis_value'), arr('S5', 'main', 'se')**2)
    assert abs(pm5.tau2 - m5['tau2']) > 0.01                     # S5：PM 的 τ² 與 DL 明顯不同
    say(f'[statsmodels {statsmodels.__version__}] 10 個分析單位的固定效應合併值、Q、I²、τ²（method_re="dl"，DL 原始值不截斷）與本程式相符；'
        f'S5 的 τ²：DL={m5["tau2"]:.5f}，預設 Paule–Mandel={pm5.tau2:.5f}（不同方法，不要混用）')
else:
    say('[statsmodels] 未安裝，略過交叉核對（只做 numpy 重算）')

say('全部 assert 通過')
