"""Tkinterアプリ用のローカル外観設定。主処理のデータは保存しない。"""

from copy import deepcopy
import json
import os
from pathlib import Path
import re
import tkinter as tk
from tkinter import messagebox, ttk


SCHEMA_VERSION = 1
APP_ID = "ai-pdf-rename-tool"
PRESETS = {
    "Classic": {"corner": 0, "padding": 7},
    "Fluent Soft": {"corner": 8, "padding": 8},
    "Expressive Rounded": {"corner": 14, "padding": 10},
    "Compact Professional": {"corner": 2, "padding": 5},
}
ACCENTS = {
    "青": "#2367A8", "緑": "#26734D", "紫": "#6750A4",
    "オレンジ": "#A64B00", "グレー": "#52677D",
    "現在のAI Works Labカラー": "#397DBB",
}
DEFAULT_SETTINGS = {
    "schema_version": SCHEMA_VERSION,
    "preset": "Fluent Soft",
    "appearance": "Windows設定に合わせる",
    "accent": "青",
    "custom_accent": "#2367A8",
    "density": "標準",
}


def settings_path():
    base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    return base / "AIWorksLab" / APP_ID / "ui_settings.json"


def validate_settings(value):
    if not isinstance(value, dict) or value.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("設定ファイルの形式またはバージョンが正しくありません。")
    result = deepcopy(DEFAULT_SETTINGS)
    if value.get("preset") not in PRESETS:
        raise ValueError("外観プリセットが不正です。")
    if value.get("appearance") not in ("Windows設定に合わせる", "ライト", "ダーク"):
        raise ValueError("表示モードが不正です。")
    if value.get("accent") not in (*ACCENTS.keys(), "カスタム"):
        raise ValueError("アクセントカラーが不正です。")
    if value.get("density") not in ("標準", "コンパクト"):
        raise ValueError("表示密度が不正です。")
    custom = value.get("custom_accent")
    if not isinstance(custom, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", custom):
        raise ValueError("カスタムカラーは #RRGGBB 形式で入力してください。")
    result.update(
        preset=value["preset"], appearance=value["appearance"], accent=value["accent"],
        custom_accent=custom.upper(), density=value["density"],
    )
    return result


def load_settings(path=None):
    target = Path(path) if path else settings_path()
    if not target.exists():
        return deepcopy(DEFAULT_SETTINGS), None
    try:
        return validate_settings(json.loads(target.read_text(encoding="utf-8"))), None
    except Exception as error:
        return deepcopy(DEFAULT_SETTINGS), (
            "外観設定を読み込めなかったため、初期設定で起動しました。\n"
            f"設定ファイルは削除していません。\n{error}"
        )


def save_settings(value, path=None):
    valid = validate_settings(value)
    target = Path(path) if path else settings_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp")
    temporary.write_text(json.dumps(valid, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, target)
    return target


def _luminance(color):
    rgb = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [part / 12.92 if part <= 0.04045 else ((part + 0.055) / 1.055) ** 2.4 for part in rgb]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(first, second):
    high, low = sorted((_luminance(first), _luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def readable_text_color(background):
    choices = [(contrast_ratio(background, color), color) for color in ("#FFFFFF", "#000000")]
    ratio, color = max(choices)
    if ratio < 4.5:
        raise ValueError("この色ではボタン文字を安全に読めません。")
    return color


def system_uses_dark_mode():
    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            return winreg.QueryValueEx(key, "AppsUseLightTheme")[0] == 0
    except Exception:
        return False


def build_tokens(settings):
    valid = validate_settings(settings)
    dark = valid["appearance"] == "ダーク" or (
        valid["appearance"] == "Windows設定に合わせる" and system_uses_dark_mode()
    )
    accent = valid["custom_accent"] if valid["accent"] == "カスタム" else ACCENTS[valid["accent"]]
    compact = valid["density"] == "コンパクト" or valid["preset"] == "Compact Professional"
    if dark:
        colors = dict(background="#151B23", surface="#1E2732", surface_alt="#283442", text="#F4F7FA", secondary="#C4CFDA", border="#536579", selection="#355675", disabled="#99A8B7")
    else:
        colors = dict(background="#F4F7FB", surface="#FFFFFF", surface_alt="#EEF3F8", text="#1B2938", secondary="#52677D", border="#C9D5E1", selection="#CFE3F7", disabled="#7A8794")
    colors.update(accent=accent, accent_text=readable_text_color(accent), padding=5 if compact else PRESETS[valid["preset"]]["padding"], font_size=9 if compact else 10)
    return colors


def apply_theme(root, settings):
    tokens = build_tokens(settings)
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    font = ("Segoe UI", tokens["font_size"])
    style.configure(".", background=tokens["background"], foreground=tokens["text"], font=font)
    style.configure("TFrame", background=tokens["background"])
    style.configure("Card.TFrame", background=tokens["surface"], bordercolor=tokens["border"], relief="solid")
    style.configure("TLabel", background=tokens["background"], foreground=tokens["text"])
    style.configure("Card.TLabel", background=tokens["surface"], foreground=tokens["text"])
    style.configure("Secondary.TLabel", background=tokens["background"], foreground=tokens["secondary"])
    style.configure("Title.TLabel", background=tokens["background"], foreground=tokens["text"], font=("Segoe UI", tokens["font_size"] + 7, "bold"))
    style.configure("TButton", background=tokens["surface_alt"], foreground=tokens["text"], bordercolor=tokens["border"], padding=(tokens["padding"] * 2, tokens["padding"]))
    style.map("TButton", background=[("active", tokens["selection"]), ("disabled", tokens["surface_alt"])], foreground=[("disabled", tokens["disabled"])])
    style.configure("Primary.TButton", background=tokens["accent"], foreground=tokens["accent_text"], bordercolor=tokens["accent"], padding=(tokens["padding"] * 2, tokens["padding"] + 1), font=("Segoe UI", tokens["font_size"], "bold"))
    style.map("Primary.TButton", background=[("active", tokens["accent"]), ("pressed", tokens["selection"])])
    style.configure("TEntry", fieldbackground=tokens["surface"], foreground=tokens["text"], bordercolor=tokens["border"], padding=tokens["padding"])
    style.configure("TCombobox", fieldbackground=tokens["surface"], foreground=tokens["text"], background=tokens["surface_alt"], bordercolor=tokens["border"], padding=tokens["padding"])
    style.map("TCombobox", fieldbackground=[("readonly", tokens["surface"])], foreground=[("readonly", tokens["text"])])
    style.configure("TLabelframe", background=tokens["surface"], foreground=tokens["text"], bordercolor=tokens["border"])
    style.configure("TLabelframe.Label", background=tokens["surface"], foreground=tokens["text"], font=("Segoe UI", tokens["font_size"], "bold"))
    root.configure(background=tokens["background"])
    _apply_native_colors(root, tokens)
    return tokens


def _apply_native_colors(widget, tokens):
    for child in widget.winfo_children():
        if isinstance(child, (tk.Listbox, tk.Text)):
            child.configure(background=tokens["surface"], foreground=tokens["text"], selectbackground=tokens["selection"], selectforeground=tokens["text"], highlightcolor=tokens["accent"], highlightbackground=tokens["border"], insertbackground=tokens["text"])
        elif isinstance(child, tk.Canvas):
            child.configure(background=tokens["surface"], highlightbackground=tokens["border"])
        _apply_native_colors(child, tokens)


def fit_window_to_screen(root, preferred_width, preferred_height, min_width=520, min_height=360):
    root.update_idletasks()
    available_width = root.winfo_screenwidth()
    available_height = root.winfo_screenheight()
    width = max(min_width, min(preferred_width, available_width - 40))
    height = max(min_height, min(preferred_height, available_height - 80))
    width = min(width, available_width)
    height = min(height, available_height)
    x = max(0, (available_width - width) // 2)
    y = max(0, (available_height - height) // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.minsize(min(min_width, available_width), min(min_height, available_height))


class UiSettingsDialog(tk.Toplevel):
    def __init__(self, parent, current, preview_callback):
        super().__init__(parent)
        self.title("表示設定")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        self.original = deepcopy(current)
        self.preview_callback = preview_callback
        self.result = None
        self.variables = {
            "preset": tk.StringVar(), "appearance": tk.StringVar(), "accent": tk.StringVar(),
            "custom_accent": tk.StringVar(), "density": tk.StringVar(),
        }
        frame = ttk.Frame(self, padding=16)
        frame.grid(sticky="nsew")
        ttk.Label(frame, text="見た目だけを変更します。ファイル処理には影響しません。", wraplength=430).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))
        fields = [
            ("外観プリセット", "preset", list(PRESETS)),
            ("表示モード", "appearance", ["Windows設定に合わせる", "ライト", "ダーク"]),
            ("アクセントカラー", "accent", [*ACCENTS, "カスタム"]),
            ("表示密度", "density", ["標準", "コンパクト"]),
        ]
        row = 1
        for label, key, values in fields:
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=4)
            combo = ttk.Combobox(frame, textvariable=self.variables[key], values=values, state="readonly", width=28)
            combo.grid(row=row, column=1, sticky="ew", pady=4)
            combo.bind("<MouseWheel>", lambda _event: "break")
            row += 1
        ttk.Label(frame, text="カスタムカラー").grid(row=row, column=0, sticky="w", padx=(0, 12), pady=4)
        ttk.Entry(frame, textvariable=self.variables["custom_accent"], width=30).grid(row=row, column=1, sticky="ew", pady=4)
        row += 1
        preview = ttk.Frame(frame, style="Card.TFrame", padding=10)
        preview.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(12, 8))
        ttk.Label(preview, text="プレビュー", style="Card.TLabel").pack(side="left")
        ttk.Button(preview, text="主要ボタン", style="Primary.TButton").pack(side="right")
        row += 1
        tools = ttk.Frame(frame)
        tools.grid(row=row, column=0, columnspan=2, sticky="ew", pady=4)
        ttk.Button(tools, text="プレビュー", command=self.preview).pack(side="left")
        ttk.Button(tools, text="初期設定に戻す", command=self.reset_defaults).pack(side="left", padx=8)
        ttk.Button(tools, text="キャンセル", command=self.cancel).pack(side="right")
        ttk.Button(tools, text="適用", style="Primary.TButton", command=self.apply).pack(side="right", padx=8)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.set_values(current)
        self.wait_visibility()
        self.focus_set()

    def set_values(self, values):
        for key, variable in self.variables.items():
            variable.set(values[key])

    def values(self):
        return validate_settings({"schema_version": SCHEMA_VERSION, **{key: variable.get() for key, variable in self.variables.items()}})

    def preview(self):
        try:
            self.preview_callback(self.values())
        except Exception as error:
            messagebox.showwarning("設定を確認してください", str(error), parent=self)

    def reset_defaults(self):
        self.set_values(DEFAULT_SETTINGS)
        self.preview()

    def apply(self):
        try:
            self.result = self.values()
            self.preview_callback(self.result)
        except Exception as error:
            messagebox.showwarning("設定を確認してください", str(error), parent=self)
            return
        self.destroy()

    def cancel(self):
        self.preview_callback(self.original)
        self.destroy()


def open_settings_dialog(parent, current, preview_callback):
    dialog = UiSettingsDialog(parent, current, preview_callback)
    parent.wait_window(dialog)
    return dialog.result
