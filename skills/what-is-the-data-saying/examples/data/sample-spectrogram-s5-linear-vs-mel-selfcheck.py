#!/usr/bin/env python3
"""sample-spectrogram-s5-linear-vs-mel-selfcheck.py：圖 S5 自我檢查（梅爾換算與嘶聲位置）。
從對應 CSV 獨立重算（自寫週期型漢寧窗、迭代基 2 快速傅立葉轉換、分貝），與圖說寫死的預期值比對。
只需 Python 標準函式庫。CSV 為本 repo 縮小版：取樣率仍 16000 赫茲，只截取第 16000–28799 點（1.0–1.8 秒）、保留原取樣點編號。
用法：python3 sample-spectrogram-s5-linear-vs-mel-selfcheck.py   全部通過時結束碼為 0。數字為虛構，未核。"""

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


def mel(hz):
    return 2595 * math.log10(1 + hz / 700)

c = read_cols("sample-spectrogram-s5-linear-vs-mel.csv", ["sample", "x"], 12800, 16000)
x = c["x"]; fs, N, hop, first = 16000, 512, 128, 16000
chk("1000 赫茲＝1000.0 梅爾", r(mel(1000)) == 1000.0, r(mel(1000)))
chk("8000 赫茲＝2840.0 梅爾", r(mel(8000)) == 2840.0, r(mel(8000)))
chk("線性軸 1000 赫茲以下占高度 12.5%", r(1000 / (fs / 2) * 100) == 12.5)
chk("梅爾軸 1000 赫茲以下占高度 35.2%", r(mel(1000) / mel(fs / 2) * 100) == 35.2,
    r(mel(1000) / mel(fs / 2) * 100))
f, t, P = stft_power(x, fs, N, hop, first)
chk("窗數 97", len(t) == 97, len(t))
band = [k for k, fk in enumerate(f) if 5000 <= fk <= 7000]
inside = [i for i, ti in enumerate(t) if 1.25 < ti < 1.55]
outside = [i for i, ti in enumerate(t) if ti < 1.1 or ti > 1.7]
pin = mean([P[k][i] for k in band for i in inside])
pout = mean([P[k][i] for k in band for i in outside])
gap = 10 * math.log10(pin / pout)
chk("嘶聲：1.2–1.6 秒的 5000–7000 赫茲比其他時間亮 6 分貝以上（結構檢查）", gap > 6, "%.1f 分貝" % gap)
ks = [k for k, fk in enumerate(f) if fk < 300]
avg8 = [mean([P[k][i] for i in range(8)]) for k in ks]
f0 = f[ks[argmax(avg8)]]
chk("開頭 8 窗基頻 187.5 赫茲（理論 200，差不到兩格）",
    f0 == 187.5 and abs(f0 - 200) < 2 * fs / N, f0)
done()
