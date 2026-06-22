## Update History

v1.2

- Refactored single PDF processing into a function
- Separated PDF processing from result counting
- Improved code maintainability without changing existing behavior

- PDF1件分の処理を関数化
- PDF処理と結果集計の役割を分離
- 既存機能を変えずにコードを保守しやすく改善

v1.1

- Refactored filename creation process
- Refactored result display process
- Improved code readability without changing existing behavior

- ファイル名作成処理を関数化
- 処理結果表示を関数化
- 既存機能を変えずにコードを読みやすく整理

v1.0

- Added result file list display
- Show successful, canceled, and error file names
- Improved final result message after PDF rename processing

- リネーム結果ファイル一覧表示を追加
- 成功・キャンセル・エラーになったファイル名を表示
- PDFリネーム後の処理結果を分かりやすく改善

v0.9

- Added rename result summary
- Count successful, canceled, and error results
- Show final result message after processing multiple PDF files

- リネーム結果サマリー追加
- 成功・キャンセル・エラー件数を集計
- 複数PDF処理後に最終結果を表示

v0.8

- Added multiple PDF selection support
- Process selected PDF files one by one

- 複数PDF選択機能追加
- 選択したPDFを1つずつ処理

### v0.7
### English

- Added duplicate filename check
- Show error message when filename already exists

- 同名ファイルチェック機能追加
- 同名ファイル存在時のエラーメッセージ追加

### v0.6

- Date auto acquisition
- Rename confirmation dialog
- Rename completion dialog

- 日付自動取得
- リネーム確認ダイアログ
- リネーム完了ダイアログ

# AI PDF Rename Tool

業務用PDFを自動で整理・リネームするためのツールです。

This tool helps rename and organize business PDF documents.

## 目的

請求書・見積書・納品書などのPDFファイルを、分かりやすい名前に自動整理することを目的としています。

## 対応予定

- PDFファイルのリネーム
- 請求書・見積書・納品書への対応
- OCRによる文字抽出
- AIによる会社名・日付・書類種別の抽出
- EXE配布

## 開発状況

現在開発中です。
まずは小さく動く版を作成し、少しずつ機能を追加していきます。

## Features

- Select a PDF file with a file dialog
- Automatically add today's date (YYYYMMDD)
- Preview the new filename before renaming
- Confirmation dialog before rename
- Completion message after rename
- Simple and beginner-friendly Python code

## 機能

- PDFファイルをダイアログで選択
- 今日の日付（YYYYMMDD）を自動取得
- リネーム後のファイル名を事前確認
- リネーム前に確認ダイアログを表示
- リネーム完了メッセージを表示
- Python初心者でも理解しやすい構成

<img width="282" height="202" alt="image" src="https://github.com/user-attachments/assets/6aefa341-8cf5-4cda-a342-2517c08e6e05" />
