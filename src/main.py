from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import os


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

        today = datetime.now().strftime("%Y%m%d")
        new_file_name = today + "_" + file_name
        
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
        else:

            answer = messagebox.askyesno(
                "確認",
                f"この名前でリネームしますか？\n\n{new_file_name}"
            )

            if answer:
                pdf_path.rename(new_file_path)
                print("リネームしました。")
                success_count += 1
                # messagebox.showinfo("完了",
                #                     "リネーム完了")
            else:
                print("リネームをキャンセルしました。")
                cancel_count += 1
                # messagebox.showinfo("キャンセル",
                #         "リネームをキャンセルしました。")
    
    messagebox.showinfo(
        "処理結果",
        f"成功：{success_count}件\n"
        f"キャンセル：{cancel_count}件\n"
        f"エラー：{error_count}件"
    )

else:
    print("PDFが選択されませんでした。")
    messagebox.showinfo("未選択",
                        "PDFが選択されませんでした。")

# input("Press Enter to exit...")