"""
No.3 2D FFT（MRI k空間 ↔ 画像空間）
MATLAB版 FFT2D.m の Python変換
"""
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import scipy.io
import skimage.io

# --- パラメータ ---
input_filename = "mri128def.mat"  # または .pgm ファイル
flag = 0  # 0: FFT (画像→k空間),  1: IFFT (k空間→画像)

# --- データ読み込み ---
if input_filename.endswith(".mat"):
    data = scipy.io.loadmat(input_filename)
    keys = [k for k in data.keys() if not k.startswith("_")]
    print("利用可能なキー:", keys)
    Signal = data[keys[0]].astype(complex)
elif input_filename.endswith(".pgm"):
    img = skimage.io.imread(input_filename)
    Signal = img.astype(complex)
else:
    raise ValueError("対応形式: .mat または .pgm")

print(f"Signal shape: {Signal.shape}")

# --- 2D FFT / IFFT ---
if flag == 0:
    Output = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(Signal)))
    title_prefix = "2D FFT"
else:
    Output = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(Signal)))
    title_prefix = "2D IFFT"

# --- プロット ---
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 入力
axes[0].imshow(np.abs(Signal), cmap="gray")
axes[0].set_title("Input (magnitude)")
axes[0].axis("off")

# 出力（実部）
axes[1].imshow(Output.real, cmap="gray")
axes[1].set_title(f"{title_prefix} — Real")
axes[1].axis("off")

# 出力（対数スケール magnitude）
axes[2].imshow(np.log1p(np.abs(Output)), cmap="gray")
axes[2].set_title(f"{title_prefix} — log|magnitude|")
axes[2].axis("off")

fig.tight_layout()
fig.savefig("FFT2D_result.png", dpi=150)
plt.show()

# --- 保存 ---
output_filename = input_filename.replace(".mat", "_FFT2D.mat").replace(".pgm", "_FFT2D.mat")
scipy.io.savemat(output_filename, {"Signal": Output})
print(f"{output_filename} を保存しました")
