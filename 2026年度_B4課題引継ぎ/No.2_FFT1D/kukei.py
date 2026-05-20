"""
No.2 矩形パルス生成
MATLAB版 kukei.m の Python変換
"""
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import scipy.io

# --- パラメータ ---
DNUM = 1024
DW_list = [17, 33, 65]  # 課題で使用する3種のデータ幅

for DW in DW_list:
    # --- 矩形パルス生成 ---
    Signal = np.zeros(DNUM, dtype=complex)
    d1 = DNUM // 2 - DW // 2
    d2 = DNUM // 2 + (DW + 1) // 2
    Signal[d1:d2] = 1.0

    # --- プロット ---
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(Signal.real, linewidth=1, label="real part")
    ax.plot(Signal.imag, linewidth=1, label="imaginary part")
    ax.set_xlim(0, DNUM)
    ax.set_title(f"kukei{DW}")
    ax.set_xlabel("Data")
    ax.set_ylabel("Amplitude")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(f"kukei_DW{DW}.png", dpi=150)
    fig.savefig(f"kukei_DW{DW}.eps", format="eps")
    plt.show()

    # --- 保存 ---
    scipy.io.savemat(f"kukei_DW{DW}.mat", {"Signal": Signal})
    print(f"kukei_DW{DW}.mat を保存しました")
