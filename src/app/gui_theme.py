from __future__ import annotations

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

STYLE_NAME = "darkly"

class AppTheme:
    def __init__(self, root: ttk.Window) -> None:
        self.root = root
        self.style = ttk.Style(theme=STYLE_NAME)

    def configure(self) -> None:
        self.style.configure("ECU.TFrame", background="#111820")
        self.style.configure("ECU.Card.TFrame", background="#18232e")
        self.style.configure("ECU.Title.TLabel", font=("Segoe UI", 22, "bold"), foreground="#8ed8ff")
        self.style.configure("ECU.Subtitle.TLabel", font=("Segoe UI", 10), foreground="#9aa9b8")
        self.style.configure("ECU.Value.TLabel", font=("Segoe UI", 18, "bold"), foreground="#e8f5ff")
        self.style.configure("ECU.Status.TLabel", font=("Segoe UI", 10, "bold"), foreground="#71e7a1")
        self.style.configure("ECU.Warning.TLabel", font=("Segoe UI", 10, "bold"), foreground="#ffd166")
