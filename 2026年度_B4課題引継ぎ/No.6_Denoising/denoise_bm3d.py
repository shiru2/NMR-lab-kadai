"""
No.6 BM3D デノイジング
MATLAB版 Denoise.m (mode=1) の Python変換
"""
import numpy as np
import bm3d
import skimage.io
import skimage.metrics
import matplotlib.pyplot as plt
import japanize_matplotlib

# --- パラメータ ---
noise_sigma = 0.05   # ノイズ推定値（[0,1]スケール）
noisy_path = "data/noisy_0500.pgm"   # add_noise.py で生成したファイル
original_path = "data/original.pgm"  # 参照用

# --- 画像読み込み ---
An = skimage.io.imread(noisy_path).astype(float) / 255.0
A  = skimage.io.imread(original_path).astype(float) / 255.0

# --- BM3D デノイジング ---
# MATLABでは BM3D(1, single(An), 255*noiseSigma/sqrt(2))
# Python bm3d パッケージでは sigma_psd を [0,1] スケールで指定
sigma_psd = noise_sigma / np.sqrt(2)  # MATLABのsqrt(2)補正と同じ
denoised = bm3d.bm3d(An, sigma_psd=sigma_psd)

# --- 品質評価 ---
psnr = skimage.metrics.peak_signal_noise_ratio(A, denoised, data_range=1.0)
ssim = skimage.metrics.structural_similarity(A, denoised, data_range=1.0)
psnr_noisy = skimage.metrics.peak_signal_noise_ratio(A, An, data_range=1.0)
print(f"Noisy PSNR:    {psnr_noisy:.2f} dB")
print(f"BM3D PSNR:     {psnr:.2f} dB")
print(f"BM3D SSIM:     {ssim:.4f}")

# --- プロット ---
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(A, cmap='gray', vmin=0, vmax=1)
axes[0].set_title('Original')
axes[0].axis('off')
axes[1].imshow(An, cmap='gray', vmin=0, vmax=1)
axes[1].set_title(f'Noisy (PSNR={psnr_noisy:.1f}dB)')
axes[1].axis('off')
axes[2].imshow(np.clip(denoised, 0, 1), cmap='gray', vmin=0, vmax=1)
axes[2].set_title(f'BM3D (PSNR={psnr:.1f}dB, SSIM={ssim:.3f})')
axes[2].axis('off')
fig.tight_layout()
fig.savefig('bm3d_result.png', dpi=150)
plt.show()

# --- 保存 ---
skimage.io.imsave('data/denoised_bm3d.pgm', (np.clip(denoised, 0, 1) * 255).astype(np.uint8))
print("data/denoised_bm3d.pgm を保存しました")
