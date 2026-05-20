"""
No.1 平滑化（3点移動平均）
MATLAB版 heikatsu.m の Python変換
Signal.mat を読み込み、3点移動平均で平滑化して保存する。
"""
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import scipy.io

# --- パラメータ ---
dt = 0.02       # サンプリング間隔 [s]
DNUM = 1024     # データ点数

# --- データ読み込み ---
data = scipy.io.loadmat("Signal.mat")
Signal = data["Signal"].flatten()

# --- 3点移動平均による平滑化 ---
hSignal = np.zeros(DNUM)
hSignal[0] = Signal[0]           # 端点はそのまま
hSignal[DNUM - 1] = Signal[DNUM - 1]
for i in range(1, DNUM - 1):
    hSignal[i] = (Signal[i - 1] + Signal[i] + Signal[i + 1]) / 3

# --- プロット（元信号と平滑化信号を重ねて表示）---
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(Signal, "--b", linewidth=0.8, label="元信号")
ax.plot(hSignal, "-r", linewidth=1.0, label="平滑化")

# x軸を時間表記に変換
tLabel = [5, 10, 15, 20, 25]
numLabel = [t / dt for t in tLabel]
ax.set_xticks(numLabel)
ax.set_xticklabels(tLabel)
ax.set_xlabel("time [sec]")
ax.set_ylabel("Amp.")
ax.set_title("The smoothed signal")
ax.legend()
ax.grid(True)
fig.tight_layout()
fig.savefig("SmoothedSignal.png", dpi=150)
fig.savefig("SmoothedSignal.eps", format="eps")
plt.show()

# --- 保存 ---
scipy.io.savemat("hsignal.mat", {"hSignal": hSignal})
print("hsignal.mat を保存しました")
