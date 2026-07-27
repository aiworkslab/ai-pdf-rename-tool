from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil

from ui_settings import (
    apply_theme,
    fit_window_to_screen,
    load_settings,
    open_settings_dialog,
    save_settings,
)


# 日付を付けた新しいファイル名を作る
def create_new_file_name(file_name):
    today = datetime.now().strftime("%Y%m%d")
    return today + "_" + file_name


# 同名コピーがある場合に、001～999の最小の空き番号を探す
def find_available_sequence_path(base_path):
    for sequence in range(1, 1000):
        candidate = base_path.with_name(
            f"{base_path.stem}_{sequence:03d}{base_path.suffix}"
        )
        if not candidate.exists():
            return candidate
    return None


# PDFファイルを1件処理し、結果と記録するファイル名を返す
def process_pdf_file(pdf_file):
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
        sequence_path = find_available_sequence_path(new_file_path)
        if sequence_path is None:
            error_message = "連番が999に達したため、新しいコピーを作成できません。"
            messagebox.showerror("エラー", error_message)
            print(error_message)
            return "error", f"{file_name}: {error_message}"

        sequence_file_name = sequence_path.name
        answer = messagebox.askyesno(
            "同名ファイルがあります",
            "同じ名前のコピーが既にあります。\n"
            "次の連番付きコピーを作成しますか？\n\n"
            f"{sequence_file_name}"
        )
        if not answer:
            print("連番付きコピーの作成をキャンセルしました。")
            return "cancel", file_name
        new_file_path = sequence_path
        new_file_name = sequence_file_name

    else:
        answer = messagebox.askyesno(
            "確認",
            f"元のPDFを残して、この名前のコピーを作成しますか？\n\n{new_file_name}"
        )

    if answer:
        try:
            # copy2はPDF内容に加え、更新日時などの情報も可能な範囲でコピーします。
            shutil.copy2(pdf_path, new_file_path)
        except Exception as error:
            error_message = f"コピーに失敗しました: {error}"
            messagebox.showerror("エラー", error_message)
            print(error_message)
            return "error", f"{file_name}: {error_message}"

        print("元のPDFを残して、新しい名前のコピーを作成しました。")
        # messagebox.showinfo("完了",
        #                     "コピー完了")
        return "success", new_file_name

    print("コピー作成をキャンセルしました。")
    # messagebox.showinfo("キャンセル",
    #         "リネームをキャンセルしました。")
    return "cancel", file_name


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


def run_dialog_only():
    # メインウィンドウを非表示
    root = tk.Tk()
    root.withdraw()

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
            result, recorded_file_name = process_pdf_file(pdf_file)

            if result == "success":
                success_count += 1
                success_files.append(recorded_file_name)
            elif result == "cancel":
                cancel_count += 1
                cancel_files.append(recorded_file_name)
            elif result == "error":
                error_count += 1
                error_files.append(recorded_file_name)

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


class PdfRenameApp(tk.Tk):
    """既存の安全コピー処理を操作する、小さなメイン画面。"""

    def __init__(self):
        super().__init__()
        self.title("AI PDF Rename Tool")
        self.ui_settings, warning = load_settings()
        self.status_var = tk.StringVar(value="PDFを選択してください。")
        self.result_var = tk.StringVar(value="まだ処理していません。")
        self._build_ui()
        self.apply_ui_settings(self.ui_settings)
        fit_window_to_screen(self, 720, 500, 560, 400)
        if warning:
            self.after(0, lambda: messagebox.showwarning("表示設定", warning, parent=self))

    def _build_ui(self):
        page = ttk.Frame(self, padding=18)
        page.pack(fill="both", expand=True)
        page.columnconfigure(0, weight=1)
        page.rowconfigure(4, weight=1)

        header = ttk.Frame(page)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="AI PDF Rename Tool", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        self.settings_button = ttk.Button(header, text="設定", command=self.open_ui_settings)
        self.settings_button.grid(row=0, column=1, sticky="e")

        ttk.Label(
            page,
            text="元のPDFを残したまま、今日の日付を付けたコピーを安全に作成します。",
            style="Secondary.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 16))

        action = ttk.Frame(page, style="Card.TFrame", padding=16)
        action.grid(row=2, column=0, sticky="ew")
        action.columnconfigure(0, weight=1)
        ttk.Label(action, text="1. PDFを選ぶ  2. 新しい名前を確認する  3. 承認したPDFだけコピーする", style="Card.TLabel", wraplength=580).grid(row=0, column=0, sticky="w")
        self.select_button = ttk.Button(action, text="PDFを選択", style="Primary.TButton", command=self.select_and_process)
        self.select_button.grid(row=1, column=0, sticky="w", pady=(12, 0))

        ttk.Label(page, textvariable=self.status_var, style="Secondary.TLabel").grid(row=3, column=0, sticky="ew", pady=(12, 8))
        result_frame = ttk.LabelFrame(page, text="処理結果", padding=10)
        result_frame.grid(row=4, column=0, sticky="nsew")
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        self.result_text = tk.Text(result_frame, height=10, wrap="word", state="disabled", relief="flat")
        self.result_text.grid(row=0, column=0, sticky="nsew")
        ttk.Button(page, text="終了", command=self.destroy).grid(row=5, column=0, sticky="e", pady=(12, 0))
        self.show_result_text(self.result_var.get())

    def apply_ui_settings(self, settings):
        apply_theme(self, settings)

    def open_ui_settings(self):
        selected = open_settings_dialog(self, self.ui_settings, self.apply_ui_settings)
        if selected is None:
            return
        try:
            save_settings(selected)
            self.ui_settings = selected
            self.apply_ui_settings(selected)
        except Exception as error:
            self.apply_ui_settings(self.ui_settings)
            messagebox.showerror("表示設定", f"設定を保存できませんでした。\n{error}", parent=self)

    def show_result_text(self, text):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", text)
        self.result_text.configure(state="disabled")

    def select_and_process(self):
        pdf_files = filedialog.askopenfilenames(
            parent=self,
            title="PDFファイルを選択してください",
            filetypes=[("PDFファイル", "*.pdf")],
        )
        if not pdf_files:
            self.status_var.set("PDFは選択されませんでした。")
            return

        self.select_button.state(["disabled"])
        self.settings_button.state(["disabled"])
        self.status_var.set(f"{len(pdf_files)}件を順番に確認しています…")
        self.update_idletasks()
        success_files, cancel_files, error_files = [], [], []
        try:
            for pdf_file in pdf_files:
                result, recorded = process_pdf_file(pdf_file)
                {"success": success_files, "cancel": cancel_files, "error": error_files}[result].append(recorded)
            text = (
                f"成功: {len(success_files)}件\n" + ("\n".join(success_files) or "なし")
                + f"\n\nキャンセル: {len(cancel_files)}件\n" + ("\n".join(cancel_files) or "なし")
                + f"\n\nエラー: {len(error_files)}件\n" + ("\n".join(error_files) or "なし")
            )
            self.show_result_text(text)
            self.status_var.set("処理が完了しました。元のPDFは変更していません。")
            show_result(len(success_files), len(cancel_files), len(error_files), success_files, cancel_files, error_files)
        finally:
            self.select_button.state(["!disabled"])
            self.settings_button.state(["!disabled"])


def main():
    app = PdfRenameApp()
    app.mainloop()

if __name__ == "__main__":
    main()
