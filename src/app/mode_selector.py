from __future__ import annotations

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, X

class ModeSelector(ttk.Toplevel):
    def __init__(self, parent, on_select) -> None:
        super().__init__(parent)
        self.title("ECU Pro Tune — modo de operação")
        self.geometry("560x360")
        self.resizable(False, False)
        self.on_select = on_select

        ttk.Label(self, text="ECU PRO TUNE", font=("Segoe UI", 24, "bold"), bootstyle="info").pack(pady=(35, 5))
        ttk.Label(self, text="Escolhe o ambiente de trabalho", bootstyle="secondary").pack(pady=(0, 25))

        box = ttk.Frame(self, padding=20)
        box.pack(fill=BOTH, expand=True)

        ttk.Button(box, text="PERFORMANCE\nOperação rápida", bootstyle="primary", command=lambda: self.select("performance")).pack(fill=X, pady=8, ipady=12)
        ttk.Button(box, text="SHOWCASE\nApresentação visual", bootstyle="info", command=lambda: self.select("showcase")).pack(fill=X, pady=8, ipady=12)
        ttk.Button(box, text="Cancelar", bootstyle="secondary", command=self.destroy).pack(pady=18)

    def select(self, mode: str) -> None:
        self.on_select(mode)
        self.destroy()
