# AI PDF Rename Tool

## このツールについて / About

AI PDF Rename Toolは、元PDFを残したまま、今日の日付を付けたコピーを作る小さなデスクトップツールです。

AI PDF Rename Tool is a small desktop tool that keeps the original PDF and creates a copy with today's date in its filename.

元PDFを直接改名、移動、削除しません。PDF本文を読んで名前を決めるツールではありません。

It does not rename, move, or delete the original PDF. It does not read the PDF contents to decide the filename.

<img width="282" height="202" alt="image" src="https://github.com/user-attachments/assets/6aefa341-8cf5-4cda-a342-2517c08e6e05" />

## 現在できること / Current Features

- 複数のPDFをファイル選択画面で選べます。  
  Select multiple PDFs from a file dialog.
- 1件ずつ新しいコピー名を表示し、作成するか確認します。  
  Review each new copy name and approve it one file at a time.
- 元PDFと同じフォルダへ、`YYYYMMDD_元ファイル名.pdf` のコピーを作ります。  
  Create `YYYYMMDD_original-filename.pdf` in the same folder as the original PDF.
- 通常名がすでにある場合は、`_001`から`_999`までの空いている最小番号を提案します。  
  If that name already exists, suggest the smallest available number from `_001` to `_999`.
- 連番付きコピーも、確認画面で承認した場合だけ作ります。  
  Create a numbered copy only after confirmation.
- 成功、キャンセル、エラーの件数と対象ファイルを表示します。  
  Show the counts and files for successful, canceled, and failed operations.
- 1件のコピーに失敗しても、ほかに選んだPDFの処理を続けます。  
  Continue with the other selected PDFs when one copy fails.
- ライト・ダーク表示、アクセント色、4つの外観プリセット、標準・コンパクト表示を設定できます。  
  Choose light or dark appearance, an accent color, four visual presets, and standard or compact density.

## 処理例 / Example

実行日が2026年7月22日の場合：

If the tool is run on July 22, 2026:

```text
元PDF / Original PDF
sample.pdf

最初のコピー / First copy
20260722_sample.pdf

同名がある場合 / If the first name already exists
20260722_sample_001.pdf
```

`_001`が存在して`_002`が空いている場合は、`_002`を提案します。日付はPDFに書かれた日付ではなく、パソコンの実行日です。

If `_001` exists and `_002` is available, the tool suggests `_002`. The date is the computer's current date, not a date read from the PDF.

## 安全について / Safety

- 元PDFは元の名前と場所に残します。  
  The original PDF stays in its original location with its original name.
- 元PDFや既存コピーを上書きしないよう、空いている名前へ新しいコピーを作ります。  
  A new copy is created with an available name so the original and existing copies remain unchanged.
- 確認画面で「いいえ」を選ぶと、新しいコピーは作りません。  
  Choosing “No” in the confirmation dialog creates no new copy.
- コピーにはPython標準ライブラリの`shutil.copy2`を使い、内容と更新日時などを可能な範囲で保ちます。  
  Copies use Python's standard `shutil.copy2`, preserving content and timestamps where possible.
- 実行コードは外部AI、API、クラウドへ接続しません。  
  The application code does not connect to external AI services, APIs, or cloud services.
- 表示設定にはPDFの場所や内容を保存しません。  
  UI settings do not store PDF locations or contents.

安全性と操作を確認する手順は、[第三者受入仕様書 v1.5](THIRD_PARTY_ACCEPTANCE_TEST_V1_5.md)を参照してください。

See the [Third-Party Acceptance Test Specification v1.5](THIRD_PARTY_ACCEPTANCE_TEST_V1_5.md) for safety and operation checks.

## 現在できないこと / Current Limitations

- PDF本文を読みません。拡張子が`.pdf`でも、内容が本当にPDFかは検査しません。  
  The tool does not read PDF contents or verify that a `.pdf` file contains valid PDF data.
- OCRによる文字抽出は未実装です。  
  OCR text extraction is not implemented.
- AIによる会社名、日付、書類種別の抽出は未実装です。  
  AI extraction of company names, dates, and document types is not implemented.
- 請求書、見積書、納品書などの自動判定は未実装です。  
  Automatic classification of invoices, quotations, delivery notes, or other document types is not implemented.
- 保存先の変更はできません。コピーは元PDFと同じフォルダに作られます。  
  The output folder cannot be changed. Copies are created beside the original PDF.
- PDFページのプレビューはありません。確認画面に表示するのは新しいファイル名です。  
  There is no PDF page preview. The confirmation dialog shows only the new filename.
- PDF内の日付を使った命名、半角変換、処理履歴、保存ログ、処理途中の一括キャンセルは未実装です。  
  Naming from dates inside a PDF, half-width conversion, history, saved logs, and canceling the whole operation midway are not implemented.

## 起動方法 / How to Run

現在のソースコードはPython標準ライブラリだけで動きます。Python 3と`tkinter`が利用できる環境で、プロジェクトのフォルダから次を実行します。

The current source code uses only the Python standard library. In an environment with Python 3 and `tkinter`, run this command from the project folder:

```powershell
python -B src/main.py
```

小さなメイン画面が開きます。「PDFを選択」を押し、各PDFの新しいコピー名を確認してください。

A small main window opens. Select “PDFを選択” and review the new copy name for each PDF.

Windowsでは、外観設定を次の場所に保存します。

On Windows, appearance settings are stored at:

```text
%LOCALAPPDATA%\AIWorksLab\ai-pdf-rename-tool\ui_settings.json
```

## テスト / Testing

- [第三者受入仕様書 v1.5 / Third-Party Acceptance Test Specification v1.5](THIRD_PARTY_ACCEPTANCE_TEST_V1_5.md)
- [安全コピー出力 修正報告 / Safe Copy Output Report](PDF_SAFE_COPY_OUTPUT_REPORT.md)
- [確認付き連番コピー 修正報告 / Confirmed Sequence Copy Report](PDF_CONFIRMED_SEQUENCE_COPY_REPORT.md)
- [UIモダナイズ テスト報告 / UI Modernization Test Report](UI_MODERNIZATION_TEST_REPORT_20260718.md)

テストには架空PDFを使います。実在する会社名や個人情報は使いません。

Tests use fictional PDFs and no real company names or personal information.

## 今後の候補 / Future Ideas

次は将来の候補です。現在のバージョンには含まれません。

These are possible future additions. They are not included in the current version.

- OCRによる文字抽出 / OCR text extraction
- AIによる会社名、日付、書類種別の抽出 / AI extraction of company names, dates, and document types
- 請求書、見積書、納品書などの自動判定 / Automatic document-type classification
- 保存先の選択 / Output-folder selection
- PDFページのプレビュー / PDF page preview
- 配布しやすい実行形式 / Easier-to-distribute executable format

## 更新履歴 / Update History

### v1.5

- 日付付きの通常名がすでにある場合、連番付きコピー名を作成前に確認するようにしました。  
  Ask for confirmation before creating a numbered copy when the normal date-prefixed name already exists.
- `_001`～`_999`から、空いている最小番号を使うようにしました。  
  Use the smallest available number from `_001` to `_999`.
- 元PDF、通常名のコピー、既存の連番コピーを残します。  
  Keep the original PDF, the normal date-prefixed copy, and all existing numbered copies unchanged.
- 連番が`_999`まで埋まっている場合はエラーとして記録し、ほかのPDF処理を続けます。  
  Record an error when all numbers through `_999` are used, then continue processing other PDFs.

### v1.4

- 元PDFを直接改名せず、同じフォルダへ日付付きコピーを作る方式に変更しました。  
  Changed from directly renaming the original PDF to creating a date-prefixed copy in the same folder.
- PDF内容と更新日時などを可能な範囲でコピーするようにしました。  
  Preserve PDF content and timestamps where possible.
- 1件のコピーに失敗しても、ほかのPDF処理を続けるようにしました。  
  Continue processing other PDFs when one copy fails.
- 最終結果にエラー理由を表示するようにしました。  
  Show the error reason in the final result.

### v1.3

- プログラム全体の流れを`main`関数に整理しました。  
  Organized the program flow into a `main` function.

### v1.2

- PDF1件分の処理を関数に分けました。  
  Separated the processing of one PDF into a function.

### v1.1

- ファイル名作成と結果表示を関数に分けました。  
  Separated filename creation and result display into functions.

### v1.0

- 成功、キャンセル、エラーの対象ファイルを結果一覧に追加しました。  
  Added file lists for successful, canceled, and failed operations.

### v0.9

- 複数PDFの成功、キャンセル、エラー件数を表示するようにしました。  
  Added result counts for multiple PDFs.

### v0.8

- 複数PDFの選択と1件ずつの処理に対応しました。  
  Added multiple PDF selection and one-by-one processing.

### v0.7

- 同名ファイルの確認とエラー表示を追加しました。  
  Added duplicate filename checks and error messages.

### v0.6

- 今日の日付の自動取得と、処理前の確認画面を追加しました。  
  Added automatic current-date naming and a confirmation dialog before processing.
