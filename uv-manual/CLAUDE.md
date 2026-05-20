# uv-manual — Claude Code 設定

## プロジェクト概要
B4課題向け「仮想環境セットアップガイド」の LaTeX ソース。
uv を使った Python 仮想環境構築と JupyterLab 起動手順を解説する。
pLaTeX + dvipdfmx でコンパイル（wsl-manual と同じパイプライン）。

---

## 言語設定
- **日本語で回答すること**

---

## ファイル構成
```
uv-manual/
├── main.tex              # マスターファイル（パッケージ・スタイル定義）
├── latexmkrc             # latexmk 設定（pLaTeX + dvipdfmx）
├── jlisting.sty          # ローカル stub（apt 未収録）
├── CLAUDE.md             # このファイル
└── chapters/             # 本文 .tex ファイル
    ├── ch01_intro.tex        # はじめに
    ├── ch02_venv_concept.tex # 仮想環境の概念
    ├── ch03_uv.tex           # uv・pyproject.toml・uv.lock の詳細
    ├── ch04_install.tex      # uv のインストール
    ├── ch05_folder.tex       # フォルダ構成
    ├── ch06_copy.tex         # 共有フォルダからコピー
    ├── ch07_setup.tex        # uv sync で環境構築
    ├── ch08_jupyter.tex      # JupyterLab 起動・操作
    ├── ch09_errors.tex       # よくあるエラーと対処
    ├── ch10_tips.tex         # 補足知識
    ├── ch11_cheatsheet.tex   # チートシート
    └── ch12_research.tex     # 研究用途：uv init / activate / VS Code
```

---

## コンパイル方法

```bash
cd /home/shiru/2024/uv-manual
latexmk -f main.tex
```

途中でエラーが出て止まった場合はクリーンビルド：

```bash
cd /home/shiru/2024/uv-manual
latexmk -f -C && latexmk -f main.tex
```

相互参照（\ref）が解決されない場合は platex を手動で追加実行：

```bash
platex -synctex=1 -kanji=utf8 main.tex
dvipdfmx -o main.pdf main.dvi
```

PDF を開く：

```bash
open "$(wslpath -w /home/shiru/2024/uv-manual/main.pdf)"
```

---

## スタイル設定（main.tex と共通）
- ドキュメントクラス：`jsreport`（a4j, 12pt, openany）
- 余白：`top=20mm, bottom=20mm, left=20mm, right=20mm`
- コードブロック：`wslbox`（黒背景）/ `lstlisting[style=bash]`
- コールアウト：`notebox`（緑）/ `warnbox`（橙）/ `tipbox`（青）/ `dangerbox`（赤）
- インライン：`\cmd{xxx}`（\texttt）/ `\key{xxx}`（キーボードキー）

## 文字コードの注意
pLaTeX（kanji=utf8）では CJK 文字（日本語）は通るが、
以下の Unicode 文字はコンパイルエラーになるため使用禁止：

| 文字 | コードポイント | 代替 |
|------|--------------|------|
| ①②③④ | U+2460〜 | `(1)(2)(3)(4)` |
| →    | U+2192     | `$\rightarrow$` |
| …   | U+2026     | `\ldots` |

lstlisting 環境内の `├` `└` `─` `│` などボックス描画文字は問題なし。

---

## 表組みルール
- 短い表（5行以下）: `tabularx{\linewidth}{...X}` + `\begin{center}`
- 長い表: `longtable`

---

## git
- ブランチ: `main`（未設定の場合は `git init && git add -A && git commit` から）
- 除外推奨: `*.aux`, `*.log`, `*.pdf`, `*.dvi`, `*.synctex.gz`
