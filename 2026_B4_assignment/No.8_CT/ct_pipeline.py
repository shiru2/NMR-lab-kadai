"""
No.8 CTフィルタード逆投影（Filtered Back-Projection）
C言語版 projection3.c / filter3.c / backprojection3.c の Python変換
scikit-image の radon / iradon を使用
"""
import numpy as np
import skimage.io
import skimage.transform
import matplotlib.pyplot as plt
import japanize_matplotlib


def load_dat(filepath: str, n_angles: int = 256, n_samples: int = 256) -> np.ndarray:
    """
    CT .dat ファイルを読み込んでサイノグラムに変換

    .dat フォーマット: 各投影角ごとに n_samples 行
    各行は "index value" のスペース区切り、投影間は空行で区切られる
    """
    sinogram = np.zeros((n_samples, n_angles))
    with open(filepath) as f:
        lines = [l.strip() for l in f if l.strip()]

    idx = 0
    for angle_idx in range(n_angles):
        for sample_idx in range(n_samples):
            if idx < len(lines):
                parts = lines[idx].split()
                if len(parts) >= 2:
                    sinogram[sample_idx, angle_idx] = float(parts[1])
                idx += 1

    return sinogram


# --- データ読み込み ---
dat_file = "data/Chest256.dat"
print(f"読み込み: {dat_file}")
sinogram = load_dat(dat_file, n_angles=256, n_samples=256)

# --- プロット: サイノグラム ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.imshow(sinogram, cmap='gray', aspect='auto',
          extent=[0, 180, sinogram.shape[0], 0])
ax.set_title("Sinogram (Radon transform)")
ax.set_xlabel("Projection angle [deg]")
ax.set_ylabel("Detector position")
plt.tight_layout()
plt.show()

# --- フィルタード逆投影（FBP）---
# MATLABのC版は sin(pi*v)/pi フィルタ（Shepp-Logan型）を使用
angles = np.linspace(0, 180, 256, endpoint=False)
reconstruction = skimage.transform.iradon(sinogram, theta=angles,
                                           filter_name='shepp-logan',
                                           interpolation='linear')

# --- プロット: 再構成画像 ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(sinogram, cmap='gray', aspect='auto')
axes[0].set_title("Sinogram")
axes[0].set_xlabel("Angle")
axes[1].imshow(reconstruction, cmap='gray')
axes[1].set_title("FBP Reconstruction")
axes[1].axis('off')
fig.tight_layout()
fig.savefig("ct_reconstruction.png", dpi=150)
plt.show()

# --- 保存 ---
normalized = reconstruction - reconstruction.min()
if normalized.max() > 0:
    normalized = normalized / normalized.max() * 255
skimage.io.imsave("ct_reconstructed.pgm", normalized.astype(np.uint8))
print("ct_reconstructed.pgm を保存しました")


# ============================================================
# 【オプション】順方向投影のデモ（ファントムから）
# ============================================================
print("\n--- 順方向投影デモ（Shepp-Loganファントム）---")
phantom = skimage.data.shepp_logan_phantom()
phantom_resized = skimage.transform.resize(phantom, (256, 256))

# Radon変換で順方向投影（サイノグラム生成）
sinogram_phantom = skimage.transform.radon(phantom_resized, theta=angles)
# IRadon変換で逆投影（再構成）
recon_phantom = skimage.transform.iradon(sinogram_phantom, theta=angles,
                                          filter_name='shepp-logan')

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(phantom_resized, cmap='gray')
axes[0].set_title("Original phantom")
axes[0].axis('off')
axes[1].imshow(sinogram_phantom, cmap='gray', aspect='auto')
axes[1].set_title("Sinogram (Radon transform)")
axes[1].set_xlabel("Angle [deg]")
axes[2].imshow(recon_phantom, cmap='gray')
axes[2].set_title("FBP Reconstruction")
axes[2].axis('off')
fig.tight_layout()
fig.savefig("ct_phantom_demo.png", dpi=150)
plt.show()
