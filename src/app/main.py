from __future__ import annotations

import tkinter as tk
import ttkbootstrap as ttk

from src.app.dashboard import Dashboard
from src.app.gui_theme import AppTheme
from src.app.mode_selector import ModeSelector
from src.core.logger import setup_logger
from src.core.scheduler import Scheduler
from src.utils.paths import ensure_directories
from src.version import __version__


class ECUProTuneApp:
    def __init__(self) -> None:
        ensure_directories()
        self.logger = setup_logger()
        self.root = ttk.Window(themename="darkly")
        self.root.title(f"ECU Pro Tune v{__version__}")
        self.root.geometry("1400x860")
        self.root.minsize(1100, 700)
        AppTheme(self.root).configure()
        self.dashboard = None
        self.scheduler = Scheduler(self._run_scheduled_profile, self.logger)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def run(self) -> None:
        self.scheduler.start()
        try:
            self.show_mode_selector()
            self.root.mainloop()
        finally:
            self._stop_scheduler()

    def show_mode_selector(self) -> None:
        ModeSelector(self.root, self.set_mode)

    def set_mode(self, mode: str) -> None:
        self.logger.info("Modo selecionado: %s", mode)
        if self.dashboard is not None:
            self.dashboard.destroy()
        self.dashboard = Dashboard(self.root, mode, self.logger, self.scheduler)
        self.dashboard.pack(fill=tk.BOTH, expand=True)

    def _run_scheduled_profile(self, profile: str) -> None:
        self.logger.info(
            "Agendamento simulado concluído para %s; nenhuma ação de hardware executada.",
            profile,
        )

    def _stop_scheduler(self) -> None:
        if self.scheduler.is_alive():
            self.scheduler.stop()
            self.scheduler.join(timeout=2)
            if self.scheduler.is_alive():
                self.logger.warning("Scheduler não terminou dentro do período de shutdown.")

    def close(self) -> None:
        self._stop_scheduler()
        self.root.destroy()


def main() -> None:
    ECUProTuneApp().run()


if __name__ == "__main__":
    main()
