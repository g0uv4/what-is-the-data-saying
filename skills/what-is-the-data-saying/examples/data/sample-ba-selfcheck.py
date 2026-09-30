# 練習資料檢查程式：讀取同資料夾內指定檔名 sample-ba-fictional.csv（不搜尋檔案），檢查筆數與欄位，並算出平均差與一致性界限
# 用法：在本檔所在資料夾執行 python3 sample-ba-selfcheck.py（需要 numpy）
# 差值方向一律是「方法 B 減方法 A」；檔頭以 # 開頭的說明行會略過
import csv, os
import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(here, 'sample-ba-fictional.csv')
with open(csv_path, encoding='utf8') as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith('#')))
assert len(rows) == 220, len(rows)
assert len({r['row_id'] for r in rows}) == 220

def summary(name):
    a = np.array([float(r['method_a']) for r in rows if r['dataset'] == name])
    b = np.array([float(r['method_b']) for r in rows if r['dataset'] == name])
    d = b - a                      # 方法 B 減方法 A
    m = (a + b) / 2                # 兩方法的平均值
    md, sd = d.mean(), d.std(ddof=1)
    return a, b, d, m, md, sd, md + 1.96 * sd, md - 1.96 * sd

ga, gb, gd, gm, gmd, gsd, gup, glo = summary('good')
fa, fb, fd, fm, fmd, fsd, fup, flo = summary('fan')
assert len(ga) == 100 and len(fa) == 120

# 良好一致的例子：平均差小，落在界限外的點很少（約 5%，不是 0）
g_out = int(((gd > gup) | (gd < glo)).sum())
# 各自的 95% 信賴區間（近似式：平均差的標準誤 = s/sqrt(n)，界限的標準誤約 sqrt(3 s^2 / n)；這裡用 1.984 當自由度 99 的 t 臨界值）
t99 = 1.984
se_m = gsd / np.sqrt(len(gd)); se_l = np.sqrt(3 * gsd ** 2 / len(gd))
# 扇形例子：平均值較小的一半與較大的一半，比較差值標準差
order = np.argsort(fm); lo_half, hi_half = fd[order[:60]], fd[order[60:]]
ratio = hi_half.std(ddof=1) / lo_half.std(ddof=1)
assert ratio > 1.5
# 百分比差異 = 差值 ÷ 兩方法平均 × 100，散布不再隨平均值變寬
pct = fd / fm * 100
p_lo, p_hi = pct[order[:60]].std(ddof=1), pct[order[60:]].std(ddof=1)
assert 0.7 < p_hi / p_lo < 1.3
# 假設的可接受範圍 ±8（示範用，非臨床標準）
inside = (gup + t99 * se_l < 8) and (glo - t99 * se_l > -8)

print('OK 筆數', len(rows), '| good', len(ga), 'fan', len(fa), '（差值方向：方法 B 減方法 A）')
print('good：平均差 %.3f，差值標準差 %.3f，一致性界限 %.3f 與 %.3f，界限外 %d 點' % (gmd, gsd, gup, glo, g_out))
print('good：平均差的 95%% 信賴區間 %.3f 到 %.3f；上界的信賴區間 %.3f 到 %.3f；下界的信賴區間 %.3f 到 %.3f' % (gmd - t99 * se_m, gmd + t99 * se_m, gup - t99 * se_l, gup + t99 * se_l, glo - t99 * se_l, glo + t99 * se_l))
print('good：界限連同信賴區間是否都在假設的可接受範圍 ±8 內：%s（範圍是假設，非臨床標準）' % ('是' if inside else '否'))
print('fan：平均差 %.3f，差值標準差 %.3f，一致性界限 %.3f 與 %.3f' % (fmd, fsd, fup, flo))
print('fan：平均值較小一半的差值標準差 %.3f，較大一半 %.3f，比值 %.2f（扇形）' % (lo_half.std(ddof=1), hi_half.std(ddof=1), ratio))
print('fan：改看百分比差異，兩半標準差 %.2f 與 %.2f 個百分點（大致相等）' % (p_lo, p_hi))
