# sample-ma-selfcheck.py：sample-ma-fictional.csv 的簡單自檢（筆數、範圍、欄位關係）
# 用法：python3 sample-ma-selfcheck.py
import csv, math
rows = list(csv.DictReader(l for l in open('sample-ma-fictional.csv', encoding='utf8') if not l.startswith('#')))
assert len(rows) == 3000, len(rows)
bm = [float(r['base_mean']) for r in rows]
a = [float(r['a_log2_mean']) for r in rows]
m = [float(r['m_log2fc']) for r in rows]
ms = [float(r['m_log2fc_shrunk']) for r in rows]
padj = [float(r['padj']) for r in rows]
assert 1 <= min(bm) and max(bm) <= 100000
assert all(abs(x - math.log2(y + 1)) < 0.01 for x, y in zip(a, bm))
assert all(0 <= p <= 1 for p in padj)
assert all(abs(s) <= abs(x) + 1e-9 for s, x in zip(ms, m))
assert len({r['gene_id'] for r in rows}) == 3000
print('OK 筆數', len(rows), '| base_mean', min(bm), '~', max(bm), '| M', min(m), '~', max(m),
      '| padj<0.05 筆數', sum(p < 0.05 for p in padj))
