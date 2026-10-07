from __future__ import annotations
import tkinter as tk
import ttkbootstrap as ttk

from src.app.dashboard import Dashboard
from src.app.gui_theme import AppTheme
from src.app.mode_selector import ModeSelector
from src.core.logger import setup_logger
from src.utils.paths import ensure_directories

class ECUProTuneApp:
    def __init__(self) -> None:
        ensure_directories()
        self.logger = setup_logger()
        self.root = ttk.Window(themename="darkly")
        self.root.title("ECU Pro Tune")
        self.root.geometry("1400x860")
        self.root.minsize(1100, 700)
        AppTheme(self.root).configure()
        self.dashboard = None

    def run(self) -> None:
        self.show_mode_selector()
        self.root.mainloop()

    def show_mode_selector(self) -> None:
        ModeSelector(self.root, self.set_mode)

    def set_mode(self, mode: str) -> None:
        self.logger.info("Modo selecionado: %s", mode)
        if self.dashboard is not None:
            self.dashboard.destroy()
        self.dashboard = Dashboard(self.root, mode, self.logger)
        self.dashboard.pack(fill=tk.BOTH, expand=True)

def main() -> None:
    ECUProTuneApp().run()

if __name__ == "__main__":
    main()
