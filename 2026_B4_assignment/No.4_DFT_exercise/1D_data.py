"""
No.4 1次元データモデル生成
MATLAB版 1D_data.m の Python変換
区分的に定義された関数 g(x) を生成し、DFT演習の入力データを作成する。
"""
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import scipy.io

# --- パラメータ ---
m = 1024      # データ点数
dx = 0.025    # データ間隔

# --- 中心化されたx座標 ---
x = (np.arange(m) - m / 2) * dx

# --- g(x) のモデル定義（区分関数）---
Signal = np.zeros(m)
for i in range(m):
    xi = x[i]
    if ((-6.0 <= xi < -3.5) or (0.2 <= xi < 2.0) or (2.5 <= xi <= 6.0)):
        Signal[i] = 0.1
    elif -3.5 <= xi < -2.0:
        Signal[i] = 0.7
    elif -2.0 <= xi < 0:
        Signal[i] = 0.8
    elif 0 <= xi < 0.2:
        Signal[i] = 0.5
    elif 2.0 <= xi < 2.5:
        Signal[i] = 0.2
    elif abs(xi) > 6.0:
        Signal[i] = 0.0

# --- プロット ---
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, Signal, linewidth=1.5)
ax.set_xlabel("x [cm]")
ax.set_ylabel("g(x)")
ax.set_title("1D Data Model")
ax.grid(True)
fig.tight_layout()

filename_base = f"m{m}dx{dx * 1000:.0f}"
fig.savefig(f"{filename_base}.png", dpi=150)
fig.savefig(f"{filename_base}.eps", format="eps")
plt.show()

# --- 保存 ---
scipy.io.savemat(f"{filename_base}.mat", {"Signal": Signal})
print(f"{filename_base}.mat を保存しました")
