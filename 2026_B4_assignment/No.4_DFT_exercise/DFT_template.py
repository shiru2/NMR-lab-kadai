"""
No.4 DFT手動実装（演習テンプレート）
ここを自分で実装してください！

DFTの定義式:
  G[k] = sum_{n=0}^{N-1} g[n] * exp(-2*pi*j * k*n / N)
  ただし k = 0, 1, ..., N-1
"""
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import scipy.io

# --- パラメータ ---
m = 1024    # 入力データ点数
dx = 0.025  # サンプリング間隔
N = 256     # DFT出力点数
Dx = 0.1   # 周波数分解能

# --- データ読み込み ---
# No.2で生成した kukei_DW17.mat を使用
data = scipy.io.loadmat("../No.2_FFT1D/kukei_DW17.mat")
keys = [k for k in data.keys() if not k.startswith("_")]
signal = data[keys[0]].flatten().real  # 実部のみ使用
# N点だけ使う
g = signal[:N]

# ============================================================
# TODO: ここにDFTを実装してください
# ============================================================
re = np.zeros(N)
im = np.zeros(N)

for k in range(N):
    for n in range(N):
        # TODO: re[k] と im[k] に DFT の実部・虚部を計算してください
        # ヒント: cos() が実部、sin() が虚部に対応します
        pass  # ← この行を置き換えてください

G = re + 1j * im
# ============================================================

# --- プロット ---
fig, axes = plt.subplots(2, 1, figsize=(10, 6))
freq = np.arange(N) * Dx
axes[0].plot(freq, re, label="Real")
axes[0].set_title("DFT — Real part")
axes[0].set_xlabel("Frequency")
axes[0].legend()
axes[0].grid(True)

axes[1].plot(freq, im, label="Imaginary", color="orange")
axes[1].set_title("DFT — Imaginary part")
axes[1].set_xlabel("Frequency")
axes[1].legend()
axes[1].grid(True)

fig.tight_layout()
plt.show()

# --- np.fft.fft との比較 ---
G_ref = np.fft.fft(g)
print(f"np.fft との最大誤差（実部）: {np.max(np.abs(re - G_ref.real)):.2e}")
print(f"np.fft との最大誤差（虚部）: {np.max(np.abs(im - G_ref.imag)):.2e}")
