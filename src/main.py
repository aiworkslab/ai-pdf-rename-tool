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
    print("\nファイル名だけ:")
    print(file_name)
else:
    print("PDFが選択されませんでした。")

input("Press Enter to exit...")