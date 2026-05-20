"""
No.3 2次元信号の抽出（中心部/周辺部マスク）
MATLAB版 extract.m の Python変換
FFT2D後のデータから中心部（低周波）または周辺部（高周波）を抽出する。
"""
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import scipy.io
import skimage.io

# --- パラメータ ---
flag = "A"      # "C" = 中心部抽出（低周波）, "A" = 周辺部抽出（高周波）
o_flag = "m"    # "m" = matファイル出力, "p" = pgmファイル出力
imgSize = 128   # 入力画像サイズ（imgSize x imgSize）
d = 120         # 抽出する正方形サイズ（d x d）

input_filename = "mri128def_FFT2D.mat"

# --- データ読み込み ---
data = scipy.io.loadmat(input_filename)
keys = [k for k in data.keys() if not k.startswith("_")]
Signal = data[keys[0]].astype(complex)
print(f"Signal shape: {Signal.shape}")

# --- マスク作成 ---
border = imgSize // 2 - d // 2  # 開始インデックス
mask = np.ones((imgSize, imgSize))

if flag == "C":
    # 中心部抽出: 中心d×dだけ残す
    mask[:] = 0
    mask[border:border + d, border:border + d] = 1
    output_base = input_filename.replace(".mat", "") + f"C{d}"
elif flag == "A":
    # 周辺部抽出: 中心d×dをカット
    mask[border:border + d, border:border + d] = 0
    output_base = input_filename.replace(".mat", "") + f"A{d}"
else:
    raise ValueError('flag は "C" または "A" にしてください')

# --- マスク適用 ---
Signal = Signal * mask

# --- 出力 ---
if o_flag == "m":
    # matファイル出力 + 1行目の実部・虚部をプロット
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(Signal[0, :].real, linewidth=1, label="real part")
    ax.plot(Signal[0, :].imag, linewidth=1, label="imaginary part")
    ax.set_xlabel("Data")
    ax.set_ylabel("Amp.")
    ax.set_title(output_base)
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(f"{output_base}.png", dpi=150)
    fig.savefig(f"{output_base}.eps", format="eps")
    plt.show()

    scipy.io.savemat(f"{output_base}.mat", {"Signal": Signal})
    print(f"{output_base}.mat を保存しました")

elif o_flag == "p":
    # pgm画像として保存
    Signal_abs = np.abs(Signal)
    max_val = Signal_abs.max()
    if max_val > 0:
        Signal_norm = Signal_abs / max_val * 255
    else:
        Signal_norm = Signal_abs
    Signal_uint8 = Signal_norm.astype(np.uint8)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(Signal_uint8, cmap="gray")
    ax.set_title(output_base)
    ax.axis("off")
    plt.show()

    skimage.io.imsave(f"{output_base}.pgm", Signal_uint8)
    print(f"{output_base}.pgm を保存しました")
else:
    raise ValueError('o_flag は "m" または "p" にしてください')
