# 練習資料檢查程式：檢查同資料夾的虛構練習資料檔（筆數、範圍、欄位關係），並輸出分位數配對供畫 QQ 圖練習
# 用法：在本檔所在資料夾執行 python3 加本檔名（需要 numpy 與 scipy）
import csv
import numpy as np
from scipy import stats

csv_path = 'sample-qq-fictional.csv'
rows = list(csv.DictReader(l for l in open(csv_path, encoding='utf8') if not l.startswith('#')))
assert len(rows) == 220, len(rows)
assert len({r['row_id'] for r in rows}) == 220
a = np.array([float(r['value']) for r in rows if r['group'] == 'A'])
b = np.array([float(r['value']) for r in rows if r['group'] == 'B'])
p = np.array([float(r['pvalue_sim']) for r in rows])
assert len(a) == 120 and len(b) == 100
assert ((p > 0) & (p <= 1)).all()

# 1) 組 A 對常態的理論分位數：用 (i - 0.5) / n 當累積比例
sa = np.sort(a)
tq = stats.norm.ppf((np.arange(1, len(sa) + 1) - 0.5) / len(sa))
r_a = np.corrcoef(tq, sa)[0, 1]
# 2) 組 B 對常態：右偏，預期相關係數較低，且最大值遠高於四分位參考線
sb = np.sort(b)
tb = stats.norm.ppf((np.arange(1, len(sb) + 1) - 0.5) / len(sb))
r_b = np.corrcoef(tb, sb)[0, 1]
# 通過第一與第三四分位數的參考線
def qline(t, s):
    xq = stats.norm.ppf([.25, .75]); yq = np.quantile(s, [.25, .75])
    k = (yq[1] - yq[0]) / (xq[1] - xq[0]); return k, yq[0] - k * xq[0]
ka, ba = qline(tq, sa); kb, bb = qline(tb, sb)
gap_a = sa[-1] - (ka * tq[-1] + ba); gap_b = sb[-1] - (kb * tb[-1] + bb)
assert r_a > r_b and gap_b > gap_a
# 3) 兩組樣本互比：筆數不同，各取相同的累積比例（0.05 到 0.95，共 19 點）
probs = np.linspace(.05, .95, 19)
qa, qb = np.quantile(a, probs), np.quantile(b, probs)
# 4) 觀察對期望 −log10 p 值（虛構 p 值）
o = np.sort(-np.log10(p)); e = -np.log10((np.arange(1, len(p) + 1) - 0.5) / len(p))[::-1]
print('OK 筆數', len(rows), '| A 組', len(a), 'B 組', len(b))
print('A 組（近似常態）對常態的相關係數 %.4f；最大值離四分位參考線 %.2f' % (r_a, gap_a))
print('B 組（右偏）對常態的相關係數 %.4f；最大值離四分位參考線 %.2f' % (r_b, gap_b))
print('兩組互比的 19 組分位數配對：第 1 組 (%.2f, %.2f)，第 10 組 (%.2f, %.2f)，第 19 組 (%.2f, %.2f)' % (qa[0], qb[0], qa[9], qb[9], qa[18], qb[18]))
print('觀察 −log10(p) 最大 %.2f，期望最大 %.2f；p 值小於 0.001 的筆數 %d' % (o[-1], e[-1], int((p < 0.001).sum())))
