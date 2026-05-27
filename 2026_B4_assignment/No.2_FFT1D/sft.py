"""
No.2 信号シフト（循環シフト）
MATLAB版 sft.m の Python変換
FFT後のデータを循環シフトし、実部・虚部をプロットして保存する。
"""
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import scipy.io

# --- パラメータ ---
DNUM = 1024     # データ点数
DW = 65         # データ幅（元の矩形パルス幅）
DS = 600        # シフト量

input_filename = f"kukei_DW{DW}_FFT.mat"

# --- データ読み込み ---
data = scipy.io.loadmat(input_filename)
keys = [k for k in data.keys() if not k.startswith("_")]
Signal = data[keys[0]].flatten().astype(complex)

# --- 循環シフト ---
DS_mod = DS % DNUM  # シフト量がデータ点数を超える場合の対処
Signal = np.roll(Signal, DS_mod)

output_base = input_filename.replace(".mat", "") + f"sft{DS_mod}"

# --- プロット ---
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(Signal.real, linewidth=1, label="real part")
ax.plot(Signal.imag, linewidth=1, label="imaginary part")
ax.set_xlim(0, DNUM)
ax.set_xlabel("Data")
ax.set_ylabel("Amplitude")
ax.set_title(output_base)
ax.legend()
ax.grid(True)
fig.tight_layout()
fig.savefig(f"{output_base}.png", dpi=150)
fig.savefig(f"{output_base}.eps", format="eps")
plt.show()

# --- 保存 ---
scipy.io.savemat(f"{output_base}.mat", {"Signal": Signal})
print(f"{output_base}.mat を保存しました")
