# NMRlab B4課題 2026年度 Python版

MATLABとPythonの両方で演習できます。どちらを使うかは自由です。

## セットアップ

**macOS / Linux:**
```bash
# uvのインストール（未インストールの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存パッケージのインストール
cd 2026年度_B4課題引継ぎ
uv sync

# Jupyter Lab の起動
uv run jupyter lab
```

**Windows 10/11（PowerShell）:**
```powershell
# uvのインストール（未インストールの場合）
powershell -ExecutionPolicy BypassExecutionPolicy `
  -c "irm https://astral.sh/uv/install.ps1 | iex"

# 依存パッケージのインストール
cd 2026年度_B4課題引継ぎ
uv sync

# Jupyter Lab の起動
uv run jupyter lab
```

### VS Code で使う場合

`uv sync` 後、ノートブックを開いてカーネルを `.venv` に切り替えてください。

1. ノートブック右上の「カーネル選択」をクリック
2. **Python Environments** → `.venv (Python 3.12)` を選択

## 演習一覧

| No. | テーマ | 主なライブラリ |
|-----|--------|----------------|
| No.1 | FID信号生成とノイズ付加 | numpy, matplotlib |
| No.2 | 矩形パルスと1D FFT | numpy, scipy |
| No.3 | 2D FFT（MRI k空間） | numpy, scikit-image |
| No.4 | DFT手動実装（演習） | numpy |
| No.5 | 圧縮センシング（Wavelet / TV） | pywt, scikit-image |
| No.6 | 画像デノイジング（BM3D / WNNM） | bm3d, scikit-image |
| No.7 | 活性化関数とPSNR/SSIM | matplotlib, openpyxl |
| No.8 | CTフィルタード逆投影 | scikit-image |

## MATLABとのデータ互換

`scipy.io.loadmat` / `scipy.io.savemat` を使って `.mat` ファイルを相互に読み書きできます。
MATLABで生成したデータをPythonで読む、逆もOKです。

## 注意事項

- **No.4** は空白セルに自分でコードを書く演習形式です
- **No.5** のCurvelet CS は Python対応ライブラリが存在しないため、同等のTV-CSで代替しています
- **No.6** のWNNM版はオプション（発展課題）です。256×256画像で数分かかります
