"""
PSNR / SSIM 計算モジュール
MATLAB版 Cal_PSNRSSIM_forMR.m の Python移植

MRI画像では背景ピクセル（輝度が低い領域）を除外してから評価するのが一般的です。
"""
import numpy as np
import skimage.metrics


def cal_psnrssim_for_mr(ref: np.ndarray, test: np.ndarray,
                         threshold: float = 0.08) -> tuple[float, float]:
    """
    MRI画像用のPSNR/SSIM計算
    背景（最大輝度の threshold 倍以下のピクセル）を除外して計算

    Args:
        ref:  参照画像 (float, [0,1])
        test: 評価画像 (float, [0,1])
        threshold: 背景マスクの閾値（最大輝度に対する割合）

    Returns:
        (psnr, ssim)
    """
    # 背景マスク（参照画像の高輝度領域のみ評価）
    mask = ref > threshold * ref.max()

    # PSNR: マスク内ピクセルのMSEで計算
    mse = np.mean((ref[mask] - test[mask]) ** 2)
    if mse == 0:
        psnr = float('inf')
    else:
        psnr = 10 * np.log10(1.0 ** 2 / mse)

    # SSIM: 画像全体で計算（skimage実装を使用）
    ssim = skimage.metrics.structural_similarity(ref, test, data_range=1.0)

    return psnr, ssim
