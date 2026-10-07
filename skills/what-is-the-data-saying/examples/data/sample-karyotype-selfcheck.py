# 練習資料檢查程式：只讀取同資料夾內指定檔名 sample-karyotype-fictional.csv（不搜尋檔案），
# 用 assert 檢查資料表的筆數、帶的排列規則，並重算教學稿九張模擬圖圖說裡寫的數字。
# 用法：在本檔所在資料夾執行 python3 sample-karyotype-selfcheck.py（只需要 Python 標準函式庫）
# 資料為虛構，數字未核；資料表檔頭以 # 開頭的說明行會略過。
import csv, os, math
from collections import Counter

here = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(here, 'sample-karyotype-fictional.csv')
with open(csv_path, encoding='utf8') as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith('#')))

# 全檔 1548 列 = 24 條染色體 + 320 個帶 + 5 個標註區間 + 631 個密度格 + 560 個關聯點 + 8 條連線
assert len(rows) == 1548, len(rows)
assert len({r['row_id'] for r in rows}) == 1548
cnt = Counter(r['record_type'] for r in rows)
assert cnt == {'chrom': 24, 'band': 320, 'interval': 5, 'density': 631, 'assoc': 560, 'link': 8}, cnt
print('OK 全檔 %d 列；各類列數：%s' % (len(rows), '、'.join('%s %d' % kv for kv in cnt.items())))

ORDER = [str(i) for i in range(1, 23)] + ['X', 'Y']
chrom = {r['chrom']: (int(r['end_bp']) / 1e6, int(r['value']) / 1e6) for r in rows if r['record_type'] == 'chrom'}   # 長度 Mb、著絲點位置 Mb
assert list(chrom) == ORDER
bands = {c: sorted([r for r in rows if r['record_type'] == 'band' and r['chrom'] == c], key=lambda r: int(r['start_bp'])) for c in ORDER}

# 1 帶要剛好鋪滿每條染色體（從 0 到長度、無縫隙無重疊），著絲點兩側各有一個 acen 帶，兩帶在著絲點位置相接
for c in ORDER:
    b = bands[c]; L, cen = chrom[c]
    assert int(b[0]['start_bp']) == 0 and int(b[-1]['end_bp']) == round(L * 1e6)
    assert all(int(b[i]['end_bp']) == int(b[i + 1]['start_bp']) for i in range(len(b) - 1))
    ac = [x for x in b if x['gstain'] == 'acen']
    assert len(ac) == 2 and ac[0]['name'] == 'p11' and ac[1]['name'] == 'q11'
    assert int(ac[0]['end_bp']) == int(ac[1]['start_bp']) == round(cen * 1e6)
st = Counter(r['gstain'] for c in ORDER for r in bands[c])
assert st == {'gneg': 69, 'gpos25': 46, 'gpos50': 50, 'gpos75': 63, 'gpos100': 33, 'acen': 48, 'stalk': 5, 'gvar': 6}, st
print('帶：24 條染色體共 %d 個帶，每條都從 0 鋪到全長；acen 帶 %d 個（每條 2 個）；stalk %d 個（13、14、15、21、22 號短臂各 1 個）；gvar %d 個（上述 5 條短臂各 1 個，加 Y 染色體長臂 1 個）；gneg %d、gpos25 %d、gpos50 %d、gpos75 %d、gpos100 %d' % (
    sum(len(bands[c]) for c in ORDER), st['acen'], st['stalk'], st['gvar'], st['gneg'], st['gpos25'], st['gpos50'], st['gpos75'], st['gpos100']))
assert {c for c in ORDER for r in bands[c] if r['gstain'] == 'stalk'} == {'13', '14', '15', '21', '22'}
assert {c for c in ORDER for r in bands[c] if r['gstain'] == 'gvar'} == {'13', '14', '15', '21', '22', 'Y'}

# 2 帶號規則：序號 i 由著絲點往外從 0 起算，帶號＝臂別＋（i÷3 取整數＋1）＋（i 除以 3 的餘數＋1）；往端粒方向帶號依序變大
def idx(name): return (int(name[1]) - 1) * 3 + (int(name[2]) - 1)
for c in ORDER:
    p = [r for r in bands[c] if r['name'][0] == 'p']       # 位置由端粒到著絲點
    q = [r for r in bands[c] if r['name'][0] == 'q']       # 位置由著絲點到端粒
    assert [idx(r['name']) for r in p] == list(range(len(p) - 1, -1, -1)), c
    assert [idx(r['name']) for r in q] == list(range(len(q))), c
print('帶號：24 條染色體的 p 臂（由頂端端粒往下）帶號由大到小、到著絲點為 p11；q 臂（由著絲點往下）由 q11 依序變大，往端粒方向帶號都是變大')

# 3 第 7 號（單條帶號圖）與第 5 號（讀圖圖例、缺失／重複圖）
def frac(c): return chrom[c][1] / chrom[c][0]
assert [r['name'] for r in bands['7']] == ['p23','p22','p21','p13','p12','p11','q11','q12','q13','q21','q22','q23','q31','q32','q33','q41']
assert round(frac('7') * 100, 1) == 37.7
print('第 7 號：%d 個帶（p 臂 6 個含 p11，q 臂 10 個含 q11），頂端最外層 %s、底端最外層 %s；著絲點在全長 %.1f%% 處' % (len(bands['7']), bands['7'][0]['name'], bands['7'][-1]['name'], frac('7') * 100))
assert len(bands['5']) == 18 and round(frac('5') * 100, 1) == 26.9 and round(chrom['5'][0], 2) == 181.54
dark = [r['name'] for r in bands['5'] if r['gstain'] == 'gpos100' and r['name'][0] == 'q']; light = [r['name'] for r in bands['5'] if r['gstain'] == 'gneg' and r['name'][0] == 'q']
assert dark == ['q42'] and light[:2] == ['q22', 'q32'] and light[0] == 'q22'
print('第 5 號：%d 個帶，長度 %.2f Mb，著絲點在全長 %.1f%% 處；長臂 gpos100 的帶只有 %s；長臂第一個 gneg 帶是 %s（圖例拿它當淺色帶）' % (len(bands['5']), chrom['5'][0], frac('5') * 100, dark[0], light[0]))

# 4 缺失／重複圖：同一段（第 5 號 q21–q23）
iv = {r['name']: r for r in rows if r['record_type'] == 'interval' and r['dataset'] == 'cnv'}
s0, e0 = int(iv['缺失']['start_bp']) / 1e6, int(iv['缺失']['end_bp']) / 1e6
assert (iv['缺失']['start_bp'], iv['缺失']['end_bp']) == (iv['重複']['start_bp'], iv['重複']['end_bp'])
sel = [r for r in bands['5'] if r['name'] in ('q21', 'q22', 'q23')]
assert int(sel[0]['start_bp']) / 1e6 == s0 and int(sel[-1]['end_bp']) / 1e6 == e0
assert int(iv['缺失']['value']) == 2 - 1 and int(iv['重複']['value']) == 2 + 1
seg = e0 - s0; L5 = chrom['5'][0]
assert round(seg, 2) == 25.27 and round(L5 - seg, 2) == 156.27 and round(L5 + seg, 2) == 206.81
print('缺失／重複：第 5 號 q21、q22、q23 三個帶，%.2f 到 %.2f Mb，長度 %.2f Mb；缺失後該段拷貝數 %s（2−1）、重複後 %s（2+1）；若依比例，缺失那一條約 %.2f Mb、重複那一條約 %.2f Mb' % (s0, e0, seg, iv['缺失']['value'], iv['重複']['value'], L5 - seg, L5 + seg))

# 5 區間 A、B、C（示意圖對照照片式核型）：A 在短臂，B、C 在長臂
reg = {r['name']: (int(r['start_bp']) / 1e6, int(r['end_bp']) / 1e6) for r in rows if r['record_type'] == 'interval' and r['dataset'] == 'regions'}
assert reg == {'A': (20.0, 35.0), 'B': (100.0, 118.0), 'C': (140.0, 165.0)}
cen5 = chrom['5'][1]
assert reg['A'][1] < cen5 < reg['B'][0] and reg['C'][1] < L5
print('區間：A %g–%g Mb（在第 5 號短臂，著絲點 %.1f Mb 之前）、B %g–%g Mb、C %g–%g Mb（B、C 在長臂，且 C 的終點小於全長 %.2f Mb）' % (*reg['A'], cen5, *reg['B'], *reg['C'], L5))

# 6 核型條數：22 對常染色體各兩條，加 X、Y 各一條＝46；23 對（含 XX）＝46；21 號兩份與三份對應 46 與 47
n_male = 2 * 22 + 1 + 1; n_female = 2 * 22 + 2
assert n_male == n_female == 46 and 2 * 23 == 46
assert 46 + (3 - 2) == 47
print('條數：男性示意 22×2＋X＋Y＝%d；女性示意 22×2＋XX＝%d（23 對）；21 號由 2 份變 3 份，整套由 46 變 %d' % (n_male, n_female, 46 + 1))

# 7 著絲點類型圖（總長 120 單位，著絲點帶各 1 單位）：長臂÷短臂
def qp(f, total=120.0): return (total - total * f - 1.0) / (total * f - 1.0)
assert [round(qp(f), 2) for f in (0.5, 0.33, 0.13)] == [1.0, 2.06, 7.08]
print('著絲點類型：著絲點在全長 50%%、33%%、13%% 處時，長臂÷短臂＝%.1f、%.1f、%.1f' % (qp(0.5), qp(0.33), qp(0.13)))

# 8 密度軌（橫向全基因體圖）：每 5 Mb 一格，24 條染色體共 631 格，值在 0.05 到 1 之間
dens = [r for r in rows if r['record_type'] == 'density']
for c in ORDER:
    assert sum(1 for r in dens if r['chrom'] == c) == math.ceil(chrom[c][0] / 5), c
vals = [float(r['value']) for r in dens]
assert min(vals) == 0.05 and max(vals) < 1.0 and sum(1 for v in vals if v == 0.05) == 6
print('密度：%d 格；最小 %.2f（有 %d 格剛好在下限 0.05），最大 %.3f（沒有任何一格達到上限 1），平均 %.3f' % (len(vals), min(vals), sum(1 for v in vals if v == 0.05), max(vals), sum(vals) / len(vals)))

# 9 曼哈頓圖（相近圖種對照）：門檻 5×10^-8，−log10(p)≈7.30
THR = -math.log10(5e-8)
asc = [(r['chrom'], int(r['start_bp']) / 1e6, float(r['value'])) for r in rows if r['record_type'] == 'assoc']
percnt = Counter(c for c, _, _ in asc)
assert len(asc) == 560 and all(percnt[c] == 25 for c in ORDER[:22] if c not in ('6', '12')) and percnt['6'] == 31 and percnt['12'] == 29
assert 'X' not in percnt and 'Y' not in percnt
above = [(c, p, v) for c, p, v in asc if v >= THR]
assert len(above) == 8 and Counter(c for c, _, _ in above) == {'6': 5, '12': 3}
assert all(30.5 <= p <= 31.3 for c, p, v in above if c == '6') and all(61.6 <= p <= 62.3 for c, p, v in above if c == '12')
other_max = max(v for c, p, v in asc if c not in ('6', '12'))
assert round(other_max, 3) == 3.283 and other_max < THR
print('曼哈頓：%d 個點（第 6 號 31 個、第 12 號 29 個、其餘 1–22 號各 25 個，X、Y 沒有點）；高於門檻 %.2f 的共 %d 個，第 6 號 5 個（位置 30.6–31.2 Mb）、第 12 號 3 個（位置 61.7–62.3 Mb），其餘染色體 0 個；其餘染色體最高只有 %.3f' % (len(asc), THR, len(above), other_max))

# 10 環狀圖的連線與長度比例圖
lk = [r for r in rows if r['record_type'] == 'link']
assert len(lk) == 8 and all(r['chrom'] != r['chrom2'] for r in lk)
assert all(int(r['start_bp']) / 1e6 <= chrom[r['chrom']][0] and int(r['start2_bp']) / 1e6 <= chrom[r['chrom2']][0] for r in lk)
r21, r6 = chrom['21'][0] / chrom['1'][0], chrom['6'][0] / chrom['1'][0]
assert round(r21, 3) == 0.188 and round(r6, 3) == 0.686
print('連線 %d 條，每條連到不同的兩條染色體；21 號長度約為 1 號的 %.1f%%、6 號約為 1 號的 %.1f%%' % (len(lk), r21 * 100, r6 * 100))
print('全部檢查通過')
