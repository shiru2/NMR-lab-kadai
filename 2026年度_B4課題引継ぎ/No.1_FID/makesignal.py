"""
No.1 FID信号生成とガウスノイズ付加
MATLAB版 makesignal.m の Python変換
"""
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import scipy.io

# --- パラメータ ---
a1, a2 = 1.0, 1.0       # 振幅
t1_1, t1_2 = 2.0, 0.5   # 緩和時間 [s]
dt = 0.02                # サンプリング間隔 [s]
sigma = 0.03             # ガウスノイズ標準偏差
DNUM = 1024              # データ点数

# --- FID信号生成 ---
t = np.arange(DNUM) * dt
Signal = np.zeros(DNUM)

for k in range(DNUM):
    v1 = -t[k] / t1_1
    v2 = -t[k] / t1_2
    # e^(-50) 以下は 0 とする（MATLABと同じ打ち切り）
    s1 = a1 * np.exp(v1) if v1 > -50 else 0.0
    s2 = a2 * np.exp(v2) if v2 > -50 else 0.0
    Signal[k] = s1 + s2

# --- Box-Muller法によるガウスノイズ付加 ---
# MATLABと同じアルゴリズムを使用（教育目的）
rng = np.random.default_rng(seed=42)
u1 = rng.uniform(0, 1, DNUM)
u2 = rng.uniform(0, 1, DNUM)
noise = sigma * np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
Signal = Signal + noise

# --- プロット ---
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(t, Signal, linewidth=0.8)
ax.set_xlabel("Time [s]")
ax.set_ylabel("Signal Intensity")
ax.set_title("FID Signal with Gaussian Noise")
ax.grid(True)
fig.tight_layout()
fig.savefig("NoisySignal.png", dpi=150)
fig.savefig("NoisySignal.eps", format="eps")
plt.show()

# --- データ保存（MATLABと互換）---
scipy.io.savemat("Signal.mat", {"Signal": Signal})
print("Signal.mat を保存しました")
