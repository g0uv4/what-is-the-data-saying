#!/usr/bin/env python3
"""sample-spectrogram-s7-spectrum-vs-spectrogram-selfcheck.py：圖 S7 自我檢查（頻譜相同、頻譜圖不同）。
從對應 CSV 獨立重算（自寫週期型漢寧窗、迭代基 2 快速傅立葉轉換、分貝），與圖說寫死的預期值比對。
只需 Python 標準函式庫。CSV 為本 repo 縮小版：整段以 FFT 截掉 2000 赫茲以上後重取樣為 4000 赫茲（每 2 點留 1 點）。
用法：python3 sample-spectrogram-s7-spectrum-vs-spectrogram-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

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


c = read_cols("sample-spectrogram-s7-spectrum-vs-spectrogram.csv",
              ["sample", "signal_a", "signal_b"], 8000, 0)
fs, N, hop, first = 4000, 256, 64, 0
fa, ta, PA = stft_power(c["signal_a"], fs, N, hop, first)
fb, tb, PB = stft_power(c["signal_b"], fs, N, hop, first)
chk("窗數 122", len(ta) == 122, len(ta))
avgA = [mean(PA[k]) for k in range(len(fa))]
avgB = [mean(PB[k]) for k in range(len(fb))]
ref = max(max(avgA), max(avgB))
SA = [10 * math.log10(v / ref) for v in avgA]
SB = [10 * math.log10(v / ref) for v in avgB]
k4, k12 = near(fa, 400), near(fa, 1200)
chk("平均頻譜 400 赫茲相差 0.0 分貝", r(abs(SA[k4] - SB[k4])) == 0.0, r(abs(SA[k4] - SB[k4])))
chk("平均頻譜 1200 赫茲相差 0.0 分貝", r(abs(SA[k12] - SB[k12])) == 0.0, r(abs(SA[k12] - SB[k12])))
early = [i for i, ti in enumerate(ta) if ti < 0.9]
late = [i for i, ti in enumerate(ta) if ti > 1.1]
a4e, a4l = mean([PA[k4][i] for i in early]), mean([PA[k4][i] for i in late])
a12e, a12l = mean([PA[k12][i] for i in early]), mean([PA[k12][i] for i in late])
chk("訊號甲：前段 400 赫茲亮、後段 1200 赫茲亮（頻譜圖看得出先後）",
    a4e > 1000 * a4l and a12l > 1000 * a12e)
b4e, b4l = mean([PB[k4][i] for i in early]), mean([PB[k4][i] for i in late])
b12e, b12l = mean([PB[k12][i] for i in early]), mean([PB[k12][i] for i in late])
chk("訊號乙：兩條從頭到尾同時存在",
    b4e > 0.5 * b4l and b4l > 0.5 * b4e and b12e > 0.5 * b12l and b12l > 0.5 * b12e)
done()
