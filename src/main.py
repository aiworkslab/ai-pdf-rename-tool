from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import os


# 日付を付けた新しいファイル名を作る
def create_new_file_name(file_name):
    today = datetime.now().strftime("%Y%m%d")
    return today + "_" + file_name


# 成功・キャンセル・エラーの結果を表示する
def show_result(
    success_count,
    cancel_count,
    error_count,
    success_files,
    cancel_files,
    error_files
):
    success_text = "\n".join(success_files) if success_files else "なし"
    cancel_text = "\n".join(cancel_files) if cancel_files else "なし"
    error_text = "\n".join(error_files) if error_files else "なし"

    messagebox.showinfo(
        "処理結果",
        f"成功：{success_count}件\n"
        f"{success_text}\n\n"
        f"キャンセル：{cancel_count}件\n"
        f"{cancel_text}\n\n"
        f"エラー：{error_count}件\n"
        f"{error_text}"
    )


# メインウィンドウを非表示
root = tk.Tk()
root.withdraw()

# PDF選択
# pdf_file = filedialog.askopenfilename(
#     title="PDFファイルを選択してください",
#     filetypes=[("PDFファイル", "*.pdf")]
# )

# PDF選択
pdf_files = filedialog.askopenfilenames(
    title="PDFファイルを選択してください",
    filetypes=[("PDFファイル", "*.pdf")]
)

# 結果表示
if pdf_files:
    
    success_count = 0
    cancel_count = 0
    error_count = 0

    success_files = []
    cancel_files = []
    error_files = []

    for pdf_file in pdf_files:
        print("選択したファイル:")
        print(pdf_file)
        
        file_name = os.path.basename(pdf_file)

        new_file_name = create_new_file_name(file_name)
        
        pdf_path = Path(pdf_file)
        new_file_path = pdf_path.parent / new_file_name

        print("\n変更前ファイル名:")
        print(file_name)

        print("\n変更後ファイル名:")
        print(new_file_name)

        if new_file_path.exists():
            messagebox.showerror(
                "エラー",
                "同じ名前のファイルが存在します。"
            )
            print("同じ名前のファイルが存在します。")
            error_count += 1
            error_files.append(file_name)
        else:

            answer = messagebox.askyesno(
                "確認",
                f"この名前でリネームしますか？\n\n{new_file_name}"
            )

            if answer:
                pdf_path.rename(new_file_path)
                print("リネームしました。")
                success_count += 1
                success_files.append(new_file_name)
                # messagebox.showinfo("完了",
                #                     "リネーム完了")
            else:
                print("リネームをキャンセルしました。")
                cancel_count += 1
                cancel_files.append(file_name)
                # messagebox.showinfo("キャンセル",
                #         "リネームをキャンセルしました。")
    
    show_result(
        success_count,
        cancel_count,
        error_count,
        success_files,
        cancel_files,
        error_files
    )

else:
    print("PDFが選択されませんでした。")
    messagebox.showinfo("未選択",
                        "PDFが選択されませんでした。")

# input("Press Enter to exit...")
