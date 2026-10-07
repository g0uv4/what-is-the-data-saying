# 練習資料檢查程式：只讀取同資料夾內指定檔名 sample-pp-fictional.csv（不搜尋檔案），
# 用固定規則重算教學稿八張模擬圖的點，並檢查圖說裡寫的數字。
# 用法：在本檔所在資料夾執行 python3 sample-pp-selfcheck.py（需要 numpy 與 scipy）
# 資料為虛構，數字未核；檔頭以 # 開頭的說明行會略過。
import csv, os
import numpy as np
from scipy import stats

here = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(here, 'sample-pp-fictional.csv')
with open(csv_path, encoding='utf8') as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith('#')))
# 全檔 1000 列 = 20 + 100 + 200 + 100 + 200 + 200（兩樣本，A、B 各 100）+ 80 + 100
assert len(rows) == 1000, len(rows)
assert len({r['row_id'] for r in rows}) == 1000

def vals(ds, grp=''):
    return np.array([float(r['value']) for r in rows if r['dataset'] == ds and r['group'] == grp])

def pp_norm(x, standardize=True):
    """樣本對常態：橫軸＝常態 CDF 在排序值（可先標準化）的值，縱軸＝繪圖位置 (i−0.5)/n"""
    xs = np.sort(x); n = len(xs)
    z = (xs - xs.mean()) / xs.std(ddof=1) if standardize else xs
    return z, stats.norm.cdf(z), (np.arange(1, n + 1) - 0.5) / n

counts = {k: sum(1 for r in rows if r['dataset'] == k) for k in ['anatomy', 'good', 'heavy', 'loc', 'skew', 'two', 'resid', 'sm']}
print('OK 全檔 %d 列；各資料集列數：%s' % (len(rows), '、'.join('%s %d' % kv for kv in counts.items())))

# 1 座標系解剖圖：n=20，參考分布就是產生資料的 N(0,1)，不另標準化；圖上標出第 14 個排序值
z, X, Y = pp_norm(vals('anatomy'), standardize=False)
assert len(z) == 20 and round(z[13], 2) == 0.69 and round(X[13], 3) == 0.754 and round(Y[13], 3) == 0.675
print('anatomy：n=20；第 14 個排序值 z=%.2f，橫座標 Φ(z)=%.3f，縱座標 (14−0.5)/20=%.3f；全部點到對角線的最大垂直距離 %.3f' % (z[13], X[13], Y[13], np.abs(X - Y).max()))

# 2 近似常態：標準化後代入標準常態 CDF，最大垂直距離小於 0.07
z, X, Y = pp_norm(vals('good'))
assert len(z) == 100 and np.abs(X - Y).max() < 0.07
print('good：n=100；樣本平均 %.1f、標準差 %.1f；點到對角線的最大垂直距離 %.3f（小於 0.07）' % (vals('good').mean(), vals('good').std(ddof=1), np.abs(X - Y).max()))

# 3 厚尾（t 分布，自由度 2）：標準化後，橫軸 0.05 到 0.45 的點全在對角線下方，0.55 到 0.95 的點全在上方
x = vals('heavy'); z, X, Y = pp_norm(x)
lo = (X >= 0.05) & (X < 0.45); hi = (X >= 0.55) & (X < 0.95)
assert int(lo.sum()) == 81 and int((Y[lo] < X[lo]).sum()) == 81
assert int(hi.sum()) == 66 and int((Y[hi] > X[hi]).sum()) == 66
print('heavy：n=200；標準化後，橫軸 [0.05, 0.45) 的 %d 個點全在對角線下方，[0.55, 0.95) 的 %d 個點全在對角線上方' % (lo.sum(), hi.sum()))
# 不標準化（直接把 t 分布樣本代入標準常態 CDF）時方向相反：橫軸小於 0.5 的點幾乎都在線上方
zu, Xu, Yu = pp_norm(x, standardize=False)
lo_u = Xu < 0.5; hi_u = Xu > 0.5
assert int(lo_u.sum()) == 105 and int((Yu[lo_u] > Xu[lo_u]).sum()) == 104
assert int(hi_u.sum()) == 95 and int((Yu[hi_u] < Xu[hi_u]).sum()) == 88
print('heavy（不標準化）：橫軸小於 0.5 的 %d 個點中有 %d 個在線上方；大於 0.5 的 %d 個點中有 %d 個在線下方（方向與標準化後相反）' % (lo_u.sum(), (Yu[lo_u] > Xu[lo_u]).sum(), hi_u.sum(), (Yu[hi_u] < Xu[hi_u]).sum()))

# 4 位置未對齊：樣本取自平均 1.3，卻拿 N(0,1) 當參考，不標準化
x = vals('loc'); z, X, Y = pp_norm(x, standardize=False)
y_half = float(np.interp(0.5, X, Y))
assert round(y_half, 2) == 0.08 and int((Y < X).sum()) == 100
print('loc：n=100；樣本平均 %.2f；全部 %d 個點都在對角線下方；橫軸 0.5 處縱軸約 %.2f（沒有通過 (0.5, 0.5)）' % (x.mean(), (Y < X).sum(), y_half))

# 5 右偏（對數常態）：P–P 圖中段在線上方，Q–Q 圖右尾上翹
x = vals('skew'); z, X, Y = pp_norm(x)
d = Y - X; m = (X >= 0.3) & (X < 0.85)
assert int(m.sum()) == 111 and int((d[m] > 0).sum()) == 111
assert round(float(d.max()), 3) == 0.171 and round(float(X[d.argmax()]), 2) == 0.43
qq_theory_max = stats.norm.ppf(Y).max()
assert round(float(z.max()), 2) == 6.19 and round(float(qq_theory_max), 2) == 2.81
print('skew：n=200；橫軸 [0.3, 0.85) 的 %d 個點全在對角線上方；最大垂直距離 %.3f（橫軸 %.2f 處）；Q–Q 圖最右邊的點：樣本標準化值 %.2f，對應的理論分位數只有 %.2f' % (m.sum(), d.max(), X[d.argmax()], z.max(), qq_theory_max))

# 6 兩樣本：z 取兩批合併後的排序值（共 200 個點），橫軸 A 的經驗 CDF，縱軸 B 的經驗 CDF；
#    橫軸小於 0.4 的 79 個點全在對角線上方；橫軸大於 0.6 的 82 個點中，81 個在下方、1 個剛好在線上
A = vals('two', 'A'); B = vals('two', 'B'); assert len(A) == len(B) == 100
zz = np.sort(np.concatenate([A, B]))
FA = np.searchsorted(np.sort(A), zz, side='right') / 100; FB = np.searchsorted(np.sort(B), zz, side='right') / 100
lo = FA < 0.4; hi = FA > 0.6
assert int(lo.sum()) == 79 and int((FB[lo] > FA[lo]).sum()) == 79
assert int(hi.sum()) == 82 and int((FB[hi] < FA[hi]).sum()) == 81
assert round(float(np.interp(0.5, FA, FB)), 2) == 0.52
on_line = int((FB[hi] == FA[hi]).sum())      # 橫軸大於 0.6 的點中，縱軸剛好等於橫軸的個數
assert on_line == 1
print('two：每批 n=100；平均數 A %.2f、B %.2f；標準差 A %.2f、B %.2f；橫軸小於 0.4 的 %d 個點全在線上方；橫軸大於 0.6 的 %d 個點中有 %d 個在線下方、%d 個剛好在線上；橫軸 0.5 處縱軸約 %.2f' % (
    A.mean(), B.mean(), A.std(ddof=1), B.std(ddof=1), lo.sum(), hi.sum(), (FB[hi] < FA[hi]).sum(), on_line, np.interp(0.5, FA, FB)))

# 7 迴歸殘差：最小平方直線的殘差，標準化後做常態 P–P
xv = vals('resid'); yv = np.array([float(r['value2']) for r in rows if r['dataset'] == 'resid'])
b1, b0 = np.polyfit(xv, yv, 1); res = yv - (b0 + b1 * xv)
z, X, Y = pp_norm(res)
assert len(res) == 80 and np.abs(X - Y).max() < 0.1
print('resid：n=80；配出的直線 y=%.2f+%.2fx；殘差標準差 %.2f；點到對角線的最大垂直距離 %.3f（小於 0.1）' % (b0, b1, res.std(ddof=1), np.abs(X - Y).max()))

# 8 statsmodels 等價公式：橫軸＝繪圖位置 i/(n+1)，縱軸＝擬合常態（最大概似估計）CDF 在排序值的值
x = np.sort(vals('sm')); n = len(x)
mu, sd = stats.norm.fit(x)
px = np.arange(1, n + 1) / (n + 1); py = stats.norm.cdf(x, mu, sd)
mid = (px >= 0.45) & (px < 0.85)
assert n == 100 and int(mid.sum()) == 40 and int((py[mid] < px[mid]).sum()) == 40 and round(float(np.abs(px - py).max()), 3) == 0.125
print('sm：n=100；擬合常態平均 %.2f、標準差 %.2f；橫軸 [0.45, 0.85) 的 %d 個點全在對角線下方（縱軸小於橫軸）；最大垂直距離 %.3f' % (mu, sd, mid.sum(), np.abs(px - py).max()))
