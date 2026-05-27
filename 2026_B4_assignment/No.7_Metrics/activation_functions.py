"""
No.7 活性化関数の可視化
MATLAB版 gragh_maker.m / Step.m / Sigmoid.m / ReLU.m の Python変換
"""
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib

# --- 活性化関数の定義 ---
def step(x):
    return np.where(x >= 0, 1.0, 0.0)

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)

# --- プロット ---
x = np.linspace(-6, 6, 1200)

fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(x, step(x),    label='Step',    linewidth=3, color='C0')
ax.plot(x, sigmoid(x), label='Sigmoid', linewidth=3, color='C1')
ax.plot(x, relu(x),    label='ReLU',    linewidth=3, color='C2')

# 軸線
ax.axhline(0, color='black', linewidth=0.8)
ax.axvline(0, color='black', linewidth=0.8)

ax.set_xlim(-6, 6)
ax.set_ylim(-0.5, 2)
ax.set_xlabel("x", fontsize=14)
ax.set_ylabel("y", fontsize=14)
ax.set_title("Activation Functions", fontsize=16)
ax.legend(fontsize=13)
ax.grid(True, alpha=0.4)

fig.tight_layout()
fig.savefig("activation_functions.png", dpi=150)
plt.show()
print("activation_functions.png を保存しました")
