"""
No.6 ガウスノイズ付加
MATLAB版 AddNoise.m の Python変換
"""
import numpy as np
import skimage.io
import skimage.util
import matplotlib.pyplot as plt
import japanize_matplotlib

# --- パラメータ ---
noise_sigma = 0.05  # ノイズ標準偏差（[0,1]正規化画像に対して）
input_path = "data/original.pgm"

# --- 画像読み込み ---
img = skimage.io.imread(input_path)
# [0, 1] に正規化
A = img.astype(float) / 255.0

# --- ガウスノイズ付加 ---
rng = np.random.default_rng(seed=0)
noise = rng.normal(0, noise_sigma, A.shape)
An = A + noise
An_clipped = np.clip(An, 0, 1)

# --- プロット ---
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(A, cmap='gray', vmin=0, vmax=1)
axes[0].set_title('Original')
axes[0].axis('off')
axes[1].imshow(An_clipped, cmap='gray', vmin=0, vmax=1)
axes[1].set_title(f'Noisy (σ={noise_sigma})')
axes[1].axis('off')
axes[2].imshow(noise, cmap='bwr', vmin=-3*noise_sigma, vmax=3*noise_sigma)
axes[2].set_title('Noise component')
axes[2].axis('off')
fig.tight_layout()
fig.savefig('noisy_image.png', dpi=150)
plt.show()

# --- 保存 ---
sigma_tag = f"{int(noise_sigma*1000):04d}"
out_path = f"data/noisy_{sigma_tag}.pgm"
skimage.io.imsave(out_path, (An_clipped * 255).astype(np.uint8))
print(f"{out_path} を保存しました")
