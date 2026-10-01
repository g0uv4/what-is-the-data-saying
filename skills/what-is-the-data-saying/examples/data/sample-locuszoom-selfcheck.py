# 練習資料檢查程式：讀取同資料夾內指定檔名 sample-locuszoom-fictional.csv（不搜尋檔案），
# 檢查筆數、欄位、指標變異是否為各區間最顯著的點，並數出各顏色等級與超過顯著門檻的點數。
# 用法：在本檔所在資料夾執行 python3 sample-locuszoom-selfcheck.py（需要 numpy）
# 檔頭以 # 開頭的說明行會略過；資料為虛構，數字未核。
import csv, os
import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(here, 'sample-locuszoom-fictional.csv')
with open(csv_path, encoding='utf8') as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith('#')))
# 全檔 2306 列 = 1760 個全基因組背景點 + 四段區間的變異點（114 + 121 + 127 + 117 = 479）
#              + 11 筆基因軌（3 + 3 + 3 + 2）+ 56 個重組率示意取樣點
assert len(rows) == 2306, len(rows)
assert len({r['row_id'] for r in rows}) == 2306
THR = -np.log10(5e-8)            # 全基因組顯著門檻 5×10^-8，換算約 7.30

def region(name):
    v = [r for r in rows if r['dataset'] == name and r['record_type'] == 'variant']
    p = np.array([int(r['position_bp']) / 1e6 for r in v])
    y = np.array([float(r['neg_log10_p']) for r in v])
    r2 = np.array([float(r['ld_r2_to_index']) for r in v])
    band = np.array([r['ld_band'] for r in v])
    idx = np.array([int(r['is_index']) for r in v])
    return p, y, r2, band, idx

genome = [r for r in rows if r['dataset'] == 'genome']
chroms = sorted({int(r['chrom']) for r in genome})
assert len(genome) == 1760 and chroms == list(range(1, 23))   # 22 條染色體各 80 個背景點
assert all(sum(1 for r in genome if int(r['chrom']) == c) == 80 for c in chroms)

print('OK 全檔 %d 列；全基因組背景點 %d 個（染色體 %d 條，各 80 個）；基因軌 %d 筆；重組率示意取樣點 %d 個' % (
    len(rows), len(genome), len(chroms),
    sum(1 for r in rows if r['record_type'] == 'gene'), sum(1 for r in rows if r['record_type'] == 'recomb')))

for name in ['single', 'following', 'second', 'readcolors']:
    p, y, r2, band, idx = region(name)
    assert idx.sum() == 1                                   # 每段只有一個指標變異
    iy = y[idx == 1][0]
    others = y[idx == 0]
    assert iy > others.max()                                # 指標變異必須是該段最顯著（最高）的點
    n_over = int((y > THR).sum())
    cnt = {k: int((band == k).sum()) for k in ['紅', '橙', '綠', '淺藍', '深藍']}
    print('%s：%d 個點；指標變異在 %.3f Mb、高度 %.1f；其餘點最高 %.3f（低於指標變異）；超過顯著門檻 %d 點；顏色等級 紅 %d、橙 %d、綠 %d、淺藍 %d、深藍 %d' % (
        name, len(y), p[idx == 1][0], iy, others.max(), n_over, cnt['紅'], cnt['橙'], cnt['綠'], cnt['淺藍'], cnt['深藍']))
    # 顏色等級與 r² 數值一致：紅 r²≥0.8，橙 0.6 到 0.8，綠 0.4 到 0.6，淺藍 0.2 到 0.4，深藍小於 0.2
    assert ((band == '紅') == ((r2 >= 0.8) & (idx == 0))).all()
    assert ((band == '深藍') == (r2 < 0.2)).all()

# 第二個峰（second 區間，約 45.38 到 45.48 Mb，r² 小於 0.35 且高度大於 5）：14 個點，最高 8.4，低於指標變異的 9.0
p, y, r2, band, idx = region('second')
m = (p > 45.38) & (p < 45.48) & (r2 < 0.35) & (y > 5)
assert int(m.sum()) == 14 and abs(y[m].max() - 8.4) < 1e-9 and y[m].max() < y[idx == 1][0]
print('second：第二個峰共 %d 個點，r² 都小於 0.35（深藍 %d、淺藍 %d），最高 %.1f，仍高於顯著門檻但低於指標變異；需條件分析確認，不能直接說獨立' % (
    int(m.sum()), int((band[m] == '深藍').sum()), int((band[m] == '淺藍').sum()), y[m].max()))

# readcolors 區間：補了 3 個高處的深藍點（高度 7.0、7.6、8.1），其中 2 個高於顯著門檻 7.30
p, y, r2, band, idx = region('readcolors')
hb = (band == '深藍') & (y > 5)
assert int(hb.sum()) == 3 and int((y[hb] > THR).sum()) == 2
print('readcolors：高處的深藍點 %d 個（高度 %s），其中 %d 個高於顯著門檻' % (
    int(hb.sum()), '、'.join('%.1f' % v for v in sorted(y[hb])), int((y[hb] > THR).sum())))

# 重組率示意曲線：最高處約在 45.48 Mb，不在關聯峰位置（single 區間的指標變異在 45.235 Mb）
rc = [r for r in rows if r['record_type'] == 'recomb']
rx = np.array([int(r['position_bp']) / 1e6 for r in rc]); ry = np.array([float(r['recomb_rate_schematic']) for r in rc])
print('recomb：最高 %.2f 在 %.2f Mb（示意曲線，非真實資料）' % (ry.max(), rx[ry.argmax()]))
