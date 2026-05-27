"""
No.5 圧縮センシング — TV（Total Variation）版
MATLABのcurvelet版の代替実装

【なぜcurvelet版でないか】
MATLAB版 cs_curvelet.m はGabriel Peyreの独自ツールボックスを使用しており、
Python対応のpipパッケージが存在しません。
同じ「圧縮センシング再構成」という目的をTotal Variation正則化で達成します。

TV-CSは実際のMRI再構成研究でも広く使われているアルゴリズムです。
"""
import numpy as np
import skimage.io
import skimage.metrics
import skimage.restoration
import matplotlib.pyplot as plt
import japanize_matplotlib

# --- パラメータ ---
step = 50        # 反復ステップ数
lam = 0.02       # TV正則化の強さ（大きいほど平滑化が強い）
tv_iter = 10     # 各ステップのTV収縮反復数

# --- 画像読み込み ---
img = skimage.io.imread("data/MRI05.pgm").astype(float) / 255.0
n = img.shape[0]

# --- アンダーサンプリングマスク ---
mask = skimage.io.imread("data/mask_1d_rand40.tiff").astype(bool)
if mask.shape != img.shape:
    mask = mask[:n, :n]

# --- 観測データ生成 ---
Kfull = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(img)))
Kobs = Kfull * mask

# --- FISTA + TV再構成 ---
sk = np.zeros_like(img)

for s in range(step):
    # 1. データ整合性ステップ（観測k空間値で置換）
    Krec = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(sk)))
    Krec[mask] = Kobs[mask]
    sk = np.real(np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(Krec))))

    # 2. TV収縮ステップ（Chambolle法）
    sk = skimage.restoration.denoise_tv_chambolle(sk, weight=lam, max_num_iter=tv_iter)

    if (s + 1) % 10 == 0:
        psnr = skimage.metrics.peak_signal_noise_ratio(img, sk, data_range=1.0)
        print(f"Step {s+1}/{step}: PSNR={psnr:.2f} dB")

# --- 結果 ---
psnr_final = skimage.metrics.peak_signal_noise_ratio(img, sk, data_range=1.0)
ssim_final = skimage.metrics.structural_similarity(img, sk, data_range=1.0)
print(f"\n最終結果: PSNR={psnr_final:.2f} dB, SSIM={ssim_final:.4f}")

# ゼロ充填比較
sk_zf = np.real(np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(Kobs))))
psnr_zf = skimage.metrics.peak_signal_noise_ratio(img, sk_zf, data_range=1.0)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(img, cmap='gray', vmin=0, vmax=1)
axes[0].set_title('Original')
axes[0].axis('off')
axes[1].imshow(np.clip(sk_zf, 0, 1), cmap='gray', vmin=0, vmax=1)
axes[1].set_title(f'Zero-fill (PSNR={psnr_zf:.1f}dB)')
axes[1].axis('off')
axes[2].imshow(np.clip(sk, 0, 1), cmap='gray', vmin=0, vmax=1)
axes[2].set_title(f'TV-CS (PSNR={psnr_final:.1f}dB)')
axes[2].axis('off')
fig.tight_layout()
fig.savefig('cs_tv_result.png', dpi=150)
plt.show()
