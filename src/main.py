from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import os


# メインウィンドウを非表示
root = tk.Tk()
root.withdraw()

# PDF選択
pdf_file = filedialog.askopenfilename(
    title="PDFファイルを選択してください",
    filetypes=[("PDFファイル", "*.pdf")]
)

# 結果表示
if pdf_file:
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

    answer = input(f"この名前でリネームしますか？ y/n: ")

    if answer == "y":
        pdf_path.rename(new_file_path)
        print("\nリネーム完了:")
        print(new_file_name)
    else:
        print("\nリネームをキャンセルしました。")

else:
    print("PDFが選択されませんでした。")

input("Press Enter to exit...")