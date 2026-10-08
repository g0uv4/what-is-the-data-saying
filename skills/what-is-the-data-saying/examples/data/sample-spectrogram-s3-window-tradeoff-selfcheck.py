#!/usr/bin/env python3
"""sample-spectrogram-s3-window-tradeoff-selfcheck.py：圖 S3 自我檢查（三種窗長的凹陷分貝）。
從對應 CSV 獨立重算（自寫週期型漢寧窗、迭代基 2 快速傅立葉轉換、分貝），與圖說寫死的預期值比對。
只需 Python 標準函式庫。CSV 為本 repo 縮小版：取樣率仍 8000 赫茲，只截取第 0–11263 點（0–1.408 秒）。
用法：python3 sample-spectrogram-s3-window-tradeoff-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STATUS = "虛構資料，數字未核"
RESULTS = []

def chk(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS" if cond else "FAIL") + "｜" + name + (("｜" + str(info)) if info != "" else ""))

def hann(N):
    # 週期型漢寧窗：0.5 − 0.5 × cos(2πn ÷ N)
    return [0.5 - 0.5 * math.cos(2 * math.pi * n / N) for n in range(N)]

def fft(a):
    """迭代基 2 快速傅立葉轉換（時間抽樣、位元反轉）。"""
    n = len(a)
    a = [complex(v) for v in a]
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        half = length // 2
        ang = -2 * math.pi / length
        for i in range(0, n, length):
            for k in range(half):
                wr = math.cos(ang * k)
                wi = math.sin(ang * k)
                u = a[i + k]
                v = a[i + k + half]
                t = complex(wr * v.real - wi * v.imag, wr * v.imag + wi * v.real)
                a[i + k] = u + t
                a[i + k + half] = u - t
        length *= 2
    return a

def stft_power(x, fs, N, hop, first_sample=0):
    w = hann(N)
    nfr = 1 + (len(x) - N) // hop
    nbin = N // 2 + 1
    P = [[0.0] * nfr for _ in range(nbin)]
    for i in range(nfr):
        frame = [x[i * hop + n] * w[n] for n in range(N)]
        X = fft(frame)
        for k in range(nbin):
            P[k][i] = X[k].real ** 2 + X[k].imag ** 2
    f = [k * fs / N for k in range(nbin)]
    t = [(first_sample + i * hop + N / 2) / fs for i in range(nfr)]
    return f, t, P

def to_db(P, ref, floor):
    return [[max(10 * math.log10(max(p, 1e-30) / ref), floor) for p in row] for row in P]

def r(x, n=1):
    return float(round(x, n)) + 0.0

def near(arr, v):
    best, bd = 0, abs(arr[0] - v)
    for i, a in enumerate(arr):
        d = abs(a - v)
        if d < bd:
            bd, best = d, i
    return best

def mean(xs):
    return sum(xs) / len(xs)

def median(xs):
    ys = sorted(xs)
    n = len(ys)
    m = n // 2
    return ys[m] if n % 2 else 0.5 * (ys[m - 1] + ys[m])

def argmax(xs):
    k, m = 0, xs[0]
    for i, v in enumerate(xs):
        if v > m:
            k, m = i, v
    return k

def pmax(P):
    m = P[0][0]
    for row in P:
        for v in row:
            if v > m:
                m = v
    return m

def done():
    n = len(RESULTS); bad = n - sum(RESULTS)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}（{n - bad} 項通過、{bad} 項失敗）")
    sys.exit(0 if bad == 0 else 1)

def read_cols(fn, header, n_rows, first_sample, status_col=False):
    with open(os.path.join(HERE, fn), encoding="utf-8", newline="") as fh:
        first = fh.readline()
        chk("第一行標示虛構資料", first.startswith("# " + STATUS), first.strip()[:40])
        reader = csv.DictReader(fh)
        got_head = list(reader.fieldnames)
        chk("欄名", got_head == list(header), got_head)
        rows = list(reader)
    chk("%d 列" % n_rows, len(rows) == n_rows, len(rows))
    samples = [int(r["sample"]) for r in rows]
    chk("sample 欄從 %d 連續編號" % first_sample,
        samples == list(range(first_sample, first_sample + n_rows)))
    if status_col:
        chk("每列 data_status 都是「" + STATUS + "」",
            all(r["data_status"] == STATUS for r in rows))
    cols = {k: [float(r[k]) for r in rows] for k in header if k not in ("data_status", "sample")}
    cols["sample"] = samples
    return cols


def slice_max(arr, k):
    lo = max(k - 1, 0)
    return max(arr[lo:k + 2])

c = read_cols("sample-spectrogram-s3-window-tradeoff.csv", ["sample", "x"], 11264, 0)
x = c["x"]; fs = 8000; fa, fb = 1000, 1060; c1, c2 = 1.00, 1.02
for N, want_nfr, want_tdip, want_cdip, want_tok, want_cok, want_bins, want_ts in [
    (64, 701, 0.0, 61.6, False, True, [1000.0, 1000.0], [1.0, 1.02]),
    (512, 85, 29.0, 0.0, True, False, [1000.0, 1062.5], [0.992, 1.024]),
    (4096, 8, 76.4, 0.0, True, False, [1000.0, 1060.546875], [1.024, 1.024]),
]:
    hop = N // 4
    f, t, P = stft_power(x, fs, N, hop, 0)
    chk("窗長 %d：窗數 %d" % (N, want_nfr), len(t) == want_nfr, len(t))
    sel = [i for i, ti in enumerate(t) if ti > 0.2 + N / fs / 2 and ti < 0.8 - N / fs / 2]
    if not sel:
        sel = [i for i, ti in enumerate(t) if ti < 0.9]
    spec = [10 * math.log10(mean([P[k][i] for i in sel])) for k in range(len(f))]
    ka, kb, km = near(f, fa), near(f, fb), near(f, (fa + fb) / 2)
    pk = min(slice_max(spec, ka), slice_max(spec, kb))
    band = [k for k, fk in enumerate(f) if 2000 <= fk <= 4000]
    e = [10 * math.log10(sum(P[k][i] for k in band)) for i in range(len(t))]
    ja, jb, jm = near(t, c1), near(t, c2), near(t, (c1 + c2) / 2)
    epk = min(slice_max(e, ja), slice_max(e, jb))
    tdip, cdip = r(pk - spec[km]), r(epk - e[jm])
    tok = bool(pk - spec[km] >= 3)
    cok = bool(epk - e[jm] >= 3) and ja != jb
    chk("窗長 %d：兩音凹陷 %s 分貝" % (N, want_tdip), tdip == want_tdip, tdip)
    chk("窗長 %d：敲擊凹陷 %s 分貝" % (N, want_cdip), cdip == want_cdip, cdip)
    chk("窗長 %d：兩音%s、敲擊%s" % (N, "分得開" if want_tok else "分不開", "分得開" if want_cok else "分不開"),
        tok == want_tok and cok == want_cok, (tok, cok))
    chk("窗長 %d：兩音最近頻率格 %s" % (N, want_bins), [f[ka], f[kb]] == want_bins, [f[ka], f[kb]])
    chk("窗長 %d：兩次敲擊最近窗中心 %s" % (N, want_ts), [r(t[ja], 3), r(t[jb], 3)] == want_ts,
        [r(t[ja], 3), r(t[jb], 3)])
done()
