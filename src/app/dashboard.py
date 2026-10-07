from __future__ import annotations
import random
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, X

from src.core.ecu_manager import ECUManager
from src.core.sound_manager import SoundManager
from src.tuning.tuning_panel import TuningPanel

class Dashboard(ttk.Frame):
    def __init__(self, parent, mode: str, logger) -> None:
        super().__init__(parent)
        self.mode = mode
        self.logger = logger
        self.sound = SoundManager("pro" if mode == "showcase" else "light")
        self.ecu = ECUManager()
        self.running = False
        self.build()

    def build(self) -> None:
        header = ttk.Frame(self, padding=(18, 14))
        header.pack(fill=X)
        ttk.Label(header, text="ECU PRO TUNE", font=("Segoe UI", 24, "bold"), bootstyle="info").pack(side=LEFT)
        ttk.Label(header, text=f"{self.mode.upper()} • SIMULAÇÃO SEGURA", bootstyle="secondary").pack(side="right")

        cards = ttk.Frame(self, padding=(18, 0))
        cards.pack(fill=X)
        self.status_var = tk.StringVar(value="OFFLINE")
        self.rpm_var = tk.StringVar(value="0")
        self.load_var = tk.StringVar(value="0 %")
        self.boost_var = tk.StringVar(value="0.00 bar")

        for caption, variable, style in [
            ("ECU", self.status_var, "success"),
            ("RPM", self.rpm_var, "info"),
            ("Carga", self.load_var, "warning"),
            ("Boost", self.boost_var, "primary"),
        ]:
            card = ttk.Labelframe(cards, text=caption, padding=12, bootstyle=style)
            card.pack(side=LEFT, fill=X, expand=True, padx=5)
            ttk.Label(card, textvariable=variable, font=("Segoe UI", 18, "bold")).pack()

        toolbar = ttk.Frame(self, padding=18)
        toolbar.pack(fill=X)
        self.start_btn = ttk.Button(toolbar, text="INICIAR", bootstyle="success", command=self.toggle)
        self.start_btn.pack(side=LEFT, padx=4)
        ttk.Button(toolbar, text="Perfil / Mapas", bootstyle="info", command=self.open_tuning).pack(side=LEFT, padx=4)

        self.content = ttk.Frame(self, padding=(18, 0))
        self.content.pack(fill=BOTH, expand=True)
        ttk.Label(self.content, text="Sistema pronto. Nenhuma ECU física é gravada por esta camada.", bootstyle="secondary").pack(pady=30)

    def toggle(self) -> None:
        self.running = not self.running
        if self.running:
            self.status_var.set("ONLINE")
            self.start_btn.configure(text="PARAR", bootstyle="danger")
            self.sound.play_startup()
            self.tick()
        else:
            self.status_var.set("OFFLINE")
            self.start_btn.configure(text="INICIAR", bootstyle="success")
            self.sound.play_shutdown()

    def tick(self) -> None:
        if not self.running:
            return
        rpm = random.randint(800, 6200)
        load = random.randint(10, 96)
        boost = max(0, load / 90 - 0.2)
        self.rpm_var.set(str(rpm))
        self.load_var.set(f"{load} %")
        self.boost_var.set(f"{boost:.2f} bar")
        self.after(500, self.tick)

    def open_tuning(self) -> None:
        for child in self.content.winfo_children():
            child.destroy()
        TuningPanel(self.content, self.sound, self.logger).pack(fill=BOTH, expand=True)
