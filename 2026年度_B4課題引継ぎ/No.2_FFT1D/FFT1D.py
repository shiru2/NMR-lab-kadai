"""
No.2 1D FFT / IFFT
MATLAB版 FFT.m の Python変換
"""
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import scipy.io
import sys

# --- パラメータ ---
input_filename = "kukei_DW17.mat"  # 読み込む .mat ファイル
flag = 0  # 0: FFT,  1: IFFT

# --- データ読み込み ---
data = scipy.io.loadmat(input_filename)
# .mat ファイルのキー名を確認
keys = [k for k in data.keys() if not k.startswith("_")]
Signal = data[keys[0]].flatten().astype(complex)

# --- FFT / IFFT ---
if flag == 0:
    Output = np.fft.fftshift(np.fft.fft(np.fft.fftshift(Signal)))
    output_filename = input_filename.replace(".mat", "_FFT.mat")
    title_prefix = "FFT"
else:
    Output = np.fft.fftshift(np.fft.ifft(np.fft.fftshift(Signal)))
    output_filename = input_filename.replace(".mat", "_IFFT.mat")
    title_prefix = "IFFT"

# --- プロット ---
fig, axes = plt.subplots(2, 1, figsize=(10, 6))
axes[0].plot(Output.real, linewidth=1, label="Real")
axes[0].set_title(f"{title_prefix} — Real part")
axes[0].set_xlabel("Frequency index")
axes[0].legend()
axes[0].grid(True)

axes[1].plot(Output.imag, linewidth=1, label="Imaginary", color="orange")
axes[1].set_title(f"{title_prefix} — Imaginary part")
axes[1].set_xlabel("Frequency index")
axes[1].legend()
axes[1].grid(True)

fig.tight_layout()
fig.savefig(output_filename.replace(".mat", ".png"), dpi=150)
plt.show()

# --- 保存 ---
scipy.io.savemat(output_filename, {"Signal": Output})
print(f"{output_filename} を保存しました")
