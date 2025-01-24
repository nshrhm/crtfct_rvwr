# 査読者証明書生成ツール

このツールは、学術会議（ICISIP 2025）の査読者に対する証明書をLaTeXを使用して自動生成するPythonスクリプトです。

## システム要件

- Python 3.x
- LaTeX（pdflatexコマンドが必要）
- 必要なLaTeXパッケージ:
  - geometry
  - tikz
  - mathpazo
  - graphicx

## 使用方法

```bash
python generate_certificates.py reviewer.csv certificate_review.tex [-d]
```

### オプション
- `reviewer.csv`: 査読者情報が記載されたCSVファイル（必須）
- `certificate_review.tex`: 証明書のLaTeXテンプレート（必須）
- `-d`, `--delete_tex`: 生成されたTeXファイルを削除する（オプション）

## ファイル構成

- `generate_certificates.py`: 証明書生成スクリプト
- `certificate_review.tex`: 証明書のLaTeXテンプレート
- `reviewer.csv`: 査読者情報ファイル
- `logo.png`: 証明書に使用するロゴ画像

## 入力ファイル（reviewer.csv）のフォーマット

CSVファイルには以下の列が必要です：

- `Name`: 査読者の名前
- `Number`: 査読した論文数

例：
```csv
Name,Number
John Doe,2
Jane Smith,1
```

## 出力

プログラムは各査読者に対して以下のファイルを生成します：

- `Certificate_of_reviewer_[名前].pdf`: 生成された証明書PDF
- `Certificate_of_reviewer_[名前].tex`: LaTeXソースファイル（-dオプションを使用しない場合）

## エラー処理

スクリプトは以下の状況で適切なエラーメッセージを表示します：

- 入力ファイル（CSVまたはTeX）が見つからない場合
- pdflatexコマンドが利用できない場合
- PDFファイルの生成に失敗した場合

## 証明書のカスタマイズ

証明書のデザインを変更する場合は、`certificate_review.tex`を編集してください。テンプレートでは以下のプレースホルダーが使用されています：

- `[Reviewer Name]`: 査読者の名前
- `[Number] papers`: 査読した論文数（自動的に単数形/複数形に調整されます）