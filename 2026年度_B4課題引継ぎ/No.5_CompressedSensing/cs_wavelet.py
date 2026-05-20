"""
No.5 圧縮センシング — Wavelet版
MATLAB版 cs_wavelet.m の Python変換
pywavelets (pywt) を使用
"""
import numpy as np
import pywt
import scipy.io
import skimage.io
import skimage.metrics
import matplotlib.pyplot as plt
import japanize_matplotlib

# --- パラメータ ---
J = 3           # ウェーブレット分解レベル
wavelet = 'db3' # ウェーブレットの種類（Daubechies 3次）
rate = 0.05     # サンプリング率（5%）
T = 0.2         # 初期閾値
step = 40       # 閾値を下げるステップ数
iter_per_step = 1  # 各ステップの反復回数

# --- 画像読み込み ---
img = skimage.io.imread("data/MRI05.pgm").astype(float) / 255.0
n = img.shape[0]
print(f"画像サイズ: {img.shape}")

# --- アンダーサンプリングマスク読み込み ---
mask = skimage.io.imread("data/mask_1d_rand40.tiff").astype(bool)
if mask.shape != img.shape:
    mask = mask[:n, :n]
print(f"サンプリング率: {mask.mean()*100:.1f}%")

# --- 観測データ生成（k空間の部分サンプリング）---
Kfull = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(img)))
Kobs = Kfull * mask  # マスクされていない成分のみ保持

# --- ウェーブレット係数のヘルパー関数 ---
def apply_threshold(coeffs, threshold):
    """ウェーブレット係数にハード閾値を適用"""
    new_coeffs = [coeffs[0]]  # スケーリング係数はそのまま
    for detail in coeffs[1:]:
        new_detail = tuple(
            c * (np.abs(c) >= threshold) for c in detail
        )
        new_coeffs.append(new_detail)
    return new_coeffs

# --- 圧縮センシング再構成（反復ウェーブレット収縮）---
sk = np.zeros_like(img)  # 再構成画像の初期値

for s in range(step):
    for _ in range(iter_per_step):
        # 1. 順ウェーブレット変換
        coeffs = pywt.wavedec2(sk, wavelet, level=J, mode='periodization')

        # 2. ハード閾値処理
        coeffs = apply_threshold(coeffs, T)

        # 3. 逆ウェーブレット変換
        sk = pywt.waverec2(coeffs, wavelet, mode='periodization')

        # 4. k空間でデータ整合性を強制（観測値で置換）
        Krec = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(sk)))
        Krec[mask] = Kobs[mask]  # サンプリング済み点を元データで置換
        sk = np.real(np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(Krec))))

    # 閾値を段階的に下げる
    T *= 0.9

    if (s + 1) % 10 == 0:
        psnr = skimage.metrics.peak_signal_noise_ratio(img, sk, data_range=1.0)
        print(f"Step {s+1}/{step}: T={T:.4f}, PSNR={psnr:.2f} dB")

# --- 結果表示 ---
psnr_final = skimage.metrics.peak_signal_noise_ratio(img, sk, data_range=1.0)
ssim_final = skimage.metrics.structural_similarity(img, sk, data_range=1.0)
print(f"\n最終結果: PSNR={psnr_final:.2f} dB, SSIM={ssim_final:.4f}")

# ゼロ充填再構成（比較用）
sk_zerofill = np.real(np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(Kobs))))
psnr_zf = skimage.metrics.peak_signal_noise_ratio(img, sk_zerofill, data_range=1.0)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(img, cmap='gray', vmin=0, vmax=1)
axes[0].set_title('Original')
axes[0].axis('off')
axes[1].imshow(np.clip(sk_zerofill, 0, 1), cmap='gray', vmin=0, vmax=1)
axes[1].set_title(f'Zero-fill (PSNR={psnr_zf:.1f}dB)')
axes[1].axis('off')
axes[2].imshow(np.clip(sk, 0, 1), cmap='gray', vmin=0, vmax=1)
axes[2].set_title(f'Wavelet CS (PSNR={psnr_final:.1f}dB)')
axes[2].axis('off')
fig.tight_layout()
fig.savefig('cs_wavelet_result.png', dpi=150)
plt.show()
