"""
No.6 WNNM デノイジング — numpy自己完結実装（発展・任意）
MATLAB版 WNNM_DeNoising.m の簡略Python移植

【注意】
- 256×256画像で数分かかります（ブルートフォースパッチ探索のため）
- BM3D版 denoise_bm3d.py が推奨です
- このファイルは学習目的のリファレンス実装です
"""
import numpy as np
from skimage.util import view_as_windows
import scipy.linalg


def extract_patches(img, patch_size=8, stride=1):
    """スライディングウィンドウでパッチを抽出"""
    patches = view_as_windows(img, (patch_size, patch_size), step=stride)
    h, w = patches.shape[:2]
    patches_flat = patches.reshape(-1, patch_size * patch_size)
    return patches_flat, h, w


def block_matching(patches, key_idx, n_similar=70):
    """類似パッチを距離で探索（ブルートフォース）"""
    key = patches[key_idx]
    dists = np.sum((patches - key) ** 2, axis=1)
    similar_idx = np.argsort(dists)[:n_similar]
    return similar_idx


def closed_wnnm(S, weights, c=2.0, n_sigma=0.01):
    """
    WNNM閉形式解: Y_hat = U * diag(wnnm_shrink(S)) * V^T
    weights[i] = c * sqrt(n) / (sigma[i] + eps)
    """
    # 重み付き閾値
    threshold = (weights ** 2) / (2 * n_sigma + 1e-8)
    S_hat = np.sign(S) * np.maximum(np.abs(S) - threshold, 0)
    return S_hat


def wnnm_denoise(noisy_img, noise_sigma=0.05, patch_size=8, n_similar=70,
                 outer_iter=3, inner_iter=3, c=2.0):
    """
    WNNM デノイジングのメインループ
    Args:
        noisy_img: [0,1]正規化ノイズ画像
        noise_sigma: ノイズ推定値
    Returns:
        denoised_img: デノイズ後の画像
    """
    h, w = noisy_img.shape
    denoised = noisy_img.copy()

    for outer in range(outer_iter):
        print(f"  Outer iteration {outer+1}/{outer_iter}...")
        patches, ph, pw = extract_patches(denoised, patch_size, stride=1)
        n_patches = len(patches)
        output_patches = np.zeros_like(patches)
        weight_map = np.zeros(n_patches)

        # 主要パッチのみ処理（全パッチはメモリ不足になるためサブサンプリング）
        step = max(1, patch_size // 2)
        key_indices = range(0, n_patches, step)

        for i, key_idx in enumerate(key_indices):
            similar_idx = block_matching(patches, key_idx, n_similar)
            Y = patches[similar_idx].T  # (patch_size^2, n_similar)

            # SVD分解
            try:
                U, S, Vt = scipy.linalg.svd(Y, full_matrices=False)
            except Exception:
                continue

            # WNNM重みの計算
            n = Y.shape[1]
            weights = c * np.sqrt(float(n)) / (S + 1e-8)

            # 重み付き閾値収縮
            for _ in range(inner_iter):
                S_hat = closed_wnnm(S, weights, c=c, n_sigma=noise_sigma)
                S = S_hat

            # 再構成
            Y_hat = U @ np.diag(S_hat) @ Vt
            output_patches[similar_idx] += Y_hat.T
            weight_map[similar_idx] += 1

        # 加重平均でパッチを統合
        weight_map = np.maximum(weight_map, 1)
        output_patches /= weight_map[:, np.newaxis]

        # パッチを画像に戻す（平均化）
        denoised_new = np.zeros_like(noisy_img)
        count_map = np.zeros_like(noisy_img)

        idx = 0
        for r in range(ph):
            for c_idx in range(pw):
                row = r
                col = c_idx
                patch = output_patches[idx].reshape(patch_size, patch_size)
                denoised_new[row:row+patch_size, col:col+patch_size] += patch
                count_map[row:row+patch_size, col:col+patch_size] += 1
                idx += 1

        count_map = np.maximum(count_map, 1)
        denoised = denoised_new / count_map

        # ノイジー画像とのブレンド（正則化）
        alpha = 0.5
        denoised = alpha * denoised + (1 - alpha) * noisy_img

    return np.clip(denoised, 0, 1)


if __name__ == "__main__":
    import skimage.io
    import skimage.metrics
    import matplotlib.pyplot as plt
    import japanize_matplotlib
    import time

    noisy_path = "data/noisy_0500.pgm"
    original_path = "data/original.pgm"

    An = skimage.io.imread(noisy_path).astype(float) / 255.0
    A  = skimage.io.imread(original_path).astype(float) / 255.0

    print("WNNM デノイジング開始（数分かかります）...")
    t0 = time.time()
    denoised = wnnm_denoise(An, noise_sigma=0.05)
    print(f"完了: {time.time()-t0:.1f}秒")

    psnr = skimage.metrics.peak_signal_noise_ratio(A, denoised, data_range=1.0)
    ssim = skimage.metrics.structural_similarity(A, denoised, data_range=1.0)
    psnr_noisy = skimage.metrics.peak_signal_noise_ratio(A, An, data_range=1.0)
    print(f"Noisy PSNR: {psnr_noisy:.2f} dB")
    print(f"WNNM  PSNR: {psnr:.2f} dB, SSIM: {ssim:.4f}")

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, im, title in zip(axes,
                              [A, An, denoised],
                              ['Original', f'Noisy ({psnr_noisy:.1f}dB)',
                               f'WNNM ({psnr:.1f}dB)']):
        ax.imshow(im, cmap='gray', vmin=0, vmax=1)
        ax.set_title(title)
        ax.axis('off')
    fig.tight_layout()
    fig.savefig('wnnm_result.png', dpi=150)
    plt.show()
