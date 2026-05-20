"""
No.7 PSNR/SSIM バッチ計算とExcel出力
MATLAB版 PSNR_SSIM_test.m の Python変換
"""
import glob
import numpy as np
import skimage.io
import skimage.filters
import skimage.metrics
import matplotlib.pyplot as plt
import japanize_matplotlib
import openpyxl

from cal_psnrssim import cal_psnrssim_for_mr

# --- データ読み込み ---
image_files = sorted(glob.glob("data/MR_image/*.pgm"))
if not image_files:
    print("data/MR_image/*.pgm が見つかりません")
    exit()

print(f"{len(image_files)} 枚の画像を処理します")

psnr_list = []
ssim_list = []
names = []

for fpath in image_files:
    img = skimage.io.imread(fpath).astype(float) / 255.0
    # ガウスぼかし（MATLAB版と同じ σ=1）
    blurred = skimage.filters.gaussian(img, sigma=1)

    psnr, ssim = cal_psnrssim_for_mr(img, blurred)
    psnr_list.append(psnr)
    ssim_list.append(ssim)
    names.append(fpath.split("/")[-1])
    print(f"  {names[-1]}: PSNR={psnr:.2f}dB, SSIM={ssim:.4f}")

# --- Excel出力 ---
wb = openpyxl.Workbook()
ws_psnr = wb.active
ws_psnr.title = "PSNR"
ws_ssim = wb.create_sheet("SSIM")

ws_psnr.append(["Filename", "PSNR [dB]"])
ws_ssim.append(["Filename", "SSIM"])

for name, psnr, ssim in zip(names, psnr_list, ssim_list):
    ws_psnr.append([name, round(psnr, 4)])
    ws_ssim.append([name, round(ssim, 6)])

wb.save("PSNR_SSIM.xlsx")
print("PSNR_SSIM.xlsx を保存しました")

# --- 棒グラフ（双軸）---
x = np.arange(len(names))
fig, ax1 = plt.subplots(figsize=(max(8, len(names)*0.8), 5))

bars1 = ax1.bar(x - 0.2, psnr_list, width=0.4, label='PSNR [dB]', color='C0', alpha=0.8)
ax1.set_ylabel("PSNR [dB]", color='C0', fontsize=13)
ax1.tick_params(axis='y', labelcolor='C0')
ax1.set_ylim(20, 35)

ax2 = ax1.twinx()
bars2 = ax2.bar(x + 0.2, ssim_list, width=0.4, label='SSIM', color='C1', alpha=0.8)
ax2.set_ylabel("SSIM", color='C1', fontsize=13)
ax2.tick_params(axis='y', labelcolor='C1')
ax2.set_ylim(0.8, 1.0)

ax1.set_xticks(x)
ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
ax1.set_title("PSNR / SSIM (Gaussian blur σ=1)")

fig.legend(loc='upper right', bbox_to_anchor=(0.88, 0.88))
fig.tight_layout()
fig.savefig("PSNR_SSIM_chart.png", dpi=150)
plt.show()
