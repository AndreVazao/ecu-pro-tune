from __future__ import annotations

import math
import random
import tkinter as tk
from collections import deque

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, RIGHT, X, Y

from src.core.ecu_manager import ECUManager
from src.core.sound_manager import SoundManager
from src.tuning.tuning_panel import TuningPanel


class Dashboard(ttk.Frame):
    """Responsive, simulation-only ECU dashboard with lightweight Tk canvases."""

    BG = "#0b1118"
    PANEL = "#121c27"
    PANEL_ALT = "#172432"
    GRID = "#263746"
    TEXT = "#e7eef5"
    MUTED = "#8da1b3"
    BLUE = "#27a9e8"
    CYAN = "#47d7e8"
    GREEN = "#38d996"
    AMBER = "#f4b942"
    RED = "#f06b75"

    def __init__(self, parent, mode: str, logger) -> None:
        super().__init__(parent)
        self.mode = mode
        self.logger = logger
        self.sound = SoundManager("pro" if mode == "showcase" else "light")
        self.ecu = ECUManager()
        self.running = False
        self._after_id: str | None = None
        self._phase = 0.0
        self._values = {
            "rpm": 850.0,
            "load": 12.0,
            "boost": 0.0,
            "temp": 78.0,
            "lambda": 1.00,
            "speed": 0.0,
        }
        self._history = deque([0.0] * 90, maxlen=90)
        self.configure(style="TFrame")
        self.build()
        self.bind("<Destroy>", self._on_destroy, add="+")

    def build(self) -> None:
        self.header = ttk.Frame(self, padding=(18, 12))
        self.header.pack(fill=X)
        brand = ttk.Frame(self.header)
        brand.pack(side=LEFT)
        ttk.Label(
            brand, text="ECU", font=("Segoe UI", 22, "bold"),
            foreground=self.BLUE,
        ).pack(side=LEFT)
        ttk.Label(
            brand, text=" PRO TUNE", font=("Segoe UI", 22, "bold"),
            foreground=self.TEXT,
        ).pack(side=LEFT)
        ttk.Label(
            self.header, text="LIVE TELEMETRY  /  SAFE SIMULATION",
            font=("Segoe UI", 9, "bold"), foreground=self.MUTED,
        ).pack(side=RIGHT, pady=8)

        statusbar = ttk.Frame(self, padding=(18, 0, 18, 10))
        statusbar.pack(fill=X)
        self.status_var = tk.StringVar(value="SIMULATOR STANDBY")
        self.status_label = ttk.Label(
            statusbar, textvariable=self.status_var,
            font=("Segoe UI", 9, "bold"), foreground=self.AMBER,
        )
        self.status_label.pack(side=LEFT)
        ttk.Label(
            statusbar, text=f"PROFILE: {self.mode.upper()}",
            font=("Segoe UI", 9), foreground=self.MUTED,
        ).pack(side=RIGHT)

        self.metrics = ttk.Frame(self, padding=(14, 0, 14, 8))
        self.metrics.pack(fill=X)
        self.metric_vars: dict[str, tk.StringVar] = {}
        metric_specs = [
            ("ENGINE SPEED", "rpm", "0", "RPM", self.BLUE),
            ("BOOST PRESSURE", "boost", "0.00", "BAR", self.CYAN),
            ("ENGINE LOAD", "load", "0", "%", self.AMBER),
            ("COOLANT TEMP", "temp", "0", "°C", self.GREEN),
            ("LAMBDA", "lambda", "1.00", "λ", self.CYAN),
            ("SIM. OUTPUT", "power", "0", "HP", self.BLUE),
        ]
        for column, (caption, key, initial, unit, accent) in enumerate(metric_specs):
            self.metrics.columnconfigure(column, weight=1, uniform="metric")
            card = tk.Frame(
                self.metrics, bg=self.PANEL, highlightbackground=self.GRID,
                highlightthickness=1, bd=0,
            )
            card.grid(row=0, column=column, sticky="nsew", padx=4, pady=4)
            tk.Label(
                card, text=caption, bg=self.PANEL, fg=self.MUTED,
                font=("Segoe UI", 8, "bold"), anchor="w",
            ).pack(fill=X, padx=10, pady=(9, 2))
            variable = tk.StringVar(value=initial)
            self.metric_vars[key] = variable
            tk.Label(
                card, textvariable=variable, bg=self.PANEL, fg=accent,
                font=("Segoe UI", 19, "bold"), anchor="w",
            ).pack(fill=X, padx=10)
            tk.Label(
                card, text=unit, bg=self.PANEL, fg=self.MUTED,
                font=("Segoe UI", 8), anchor="w",
            ).pack(fill=X, padx=10, pady=(0, 9))

        body = ttk.Frame(self, padding=(18, 4, 18, 8))
        body.pack(fill=BOTH, expand=True)
        body.columnconfigure(0, weight=3, uniform="body")
        body.columnconfigure(1, weight=2, uniform="body")
        body.rowconfigure(0, weight=1)

        chart_panel = tk.Frame(body, bg=self.PANEL, highlightbackground=self.GRID, highlightthickness=1)
        chart_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        tk.Label(
            chart_panel, text="ENGINE TELEMETRY", bg=self.PANEL, fg=self.TEXT,
            font=("Segoe UI", 10, "bold"), anchor="w",
        ).pack(fill=X, padx=14, pady=(12, 0))
        tk.Label(
            chart_panel, text="RPM LOAD PROFILE  •  rolling 45 seconds",
            bg=self.PANEL, fg=self.MUTED, font=("Segoe UI", 8), anchor="w",
        ).pack(fill=X, padx=14, pady=(2, 8))
        self.chart = tk.Canvas(
            chart_panel, bg=self.PANEL, highlightthickness=0, height=230,
        )
        self.chart.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))
        self.chart.bind("<Configure>", lambda _event: self._draw_chart())

        side = tk.Frame(body, bg=self.PANEL, highlightbackground=self.GRID, highlightthickness=1)
        side.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        tk.Label(
            side, text="SYSTEM MONITOR", bg=self.PANEL, fg=self.TEXT,
            font=("Segoe UI", 10, "bold"), anchor="w",
        ).pack(fill=X, padx=14, pady=(12, 10))
        self._gauge_canvas = tk.Canvas(
            side, bg=self.PANEL, highlightthickness=0, height=170,
        )
        self._gauge_canvas.pack(fill=X, padx=8)
        self._gauge_canvas.bind("<Configure>", lambda _event: self._draw_gauges())
        self.health_var = tk.StringVar(value="ALL SYSTEMS NOMINAL")
        tk.Label(
            side, textvariable=self.health_var, bg=self.PANEL, fg=self.GREEN,
            font=("Segoe UI", 9, "bold"),
        ).pack(pady=(5, 2))
        tk.Label(
            side, text="Values are generated locally for demonstration.",
            bg=self.PANEL, fg=self.MUTED, font=("Segoe UI", 8),
            wraplength=260, justify="center",
        ).pack(padx=12, pady=(0, 12))

        footer = ttk.Frame(self, padding=(18, 8, 18, 14))
        footer.pack(fill=X)
        self.start_btn = ttk.Button(
            footer, text="START SIMULATION", bootstyle="success",
            command=self.toggle,
        )
        self.start_btn.pack(side=LEFT, padx=(0, 8))
        ttk.Button(
            footer, text="PROFILES / MAPS", bootstyle="info",
            command=self.open_tuning,
        ).pack(side=LEFT, padx=4)
        ttk.Label(
            footer,
            text="NO ECU FLASH  •  NO HARDWARE WRITE  •  SIMULATION ONLY",
            font=("Segoe UI", 8, "bold"), foreground=self.MUTED,
        ).pack(side=RIGHT, pady=8)
        self._draw_chart()
        self._draw_gauges()

    def toggle(self) -> None:
        self.running = not self.running
        if self.running:
            self.status_var.set("SIMULATOR RUNNING")
            self.status_label.configure(foreground=self.GREEN)
            self.start_btn.configure(text="STOP SIMULATION", bootstyle="danger")
            self.health_var.set("SIMULATION ACTIVE")
            self.sound.play_startup()
            self.tick()
        else:
            self.status_var.set("SIMULATOR STANDBY")
            self.status_label.configure(foreground=self.AMBER)
            self.start_btn.configure(text="START SIMULATION", bootstyle="success")
            self.health_var.set("ALL SYSTEMS NOMINAL")
            self.sound.play_shutdown()
            if self._after_id is not None:
                self.after_cancel(self._after_id)
                self._after_id = None

    def tick(self) -> None:
        if not self.running:
            return
        self._phase += 0.12
        rpm_target = 900 + (math.sin(self._phase) + 1) * 2650 + random.uniform(-180, 180)
        load_target = 12 + (math.sin(self._phase * 0.73 + 1) + 1) * 39
        for key, target, factor in (
            ("rpm", rpm_target, 0.28),
            ("load", load_target, 0.22),
        ):
            self._values[key] += (target - self._values[key]) * factor
        self._values["boost"] = max(0.0, self._values["load"] / 82 - 0.17)
        self._values["temp"] += (82 + self._values["load"] * 0.10 - self._values["temp"]) * 0.025
        self._values["lambda"] = 1.00 + random.uniform(-0.018, 0.018)
        self._values["speed"] = max(0, self._values["rpm"] * self._values["load"] / 10000)
        power = self._values["rpm"] * self._values["load"] / 1050
        self.metric_vars["rpm"].set(f"{self._values['rpm']:,.0f}")
        self.metric_vars["boost"].set(f"{self._values['boost']:.2f}")
        self.metric_vars["load"].set(f"{self._values['load']:.0f}")
        self.metric_vars["temp"].set(f"{self._values['temp']:.0f}")
        self.metric_vars["lambda"].set(f"{self._values['lambda']:.2f}")
        self.metric_vars["power"].set(f"{power:.0f}")
        self._history.append(self._values["rpm"])
        self._draw_chart()
        self._draw_gauges()
        self._after_id = self.after(400, self.tick)

    def _draw_chart(self) -> None:
        if not hasattr(self, "chart"):
            return
        canvas = self.chart
        canvas.delete("all")
        width = max(canvas.winfo_width(), 240)
        height = max(canvas.winfo_height(), 150)
        left, right, top, bottom = 42, width - 14, 14, height - 28
        plot_h = bottom - top
        for value in (0, 2000, 4000, 6000, 8000):
            y = bottom - value / 8000 * plot_h
            canvas.create_line(left, y, right, y, fill=self.GRID, dash=(2, 4))
            canvas.create_text(
                left - 8, y, text=str(value), fill=self.MUTED,
                anchor="e", font=("Segoe UI", 7),
            )
        points = list(self._history)
        if len(points) > 1:
            coords = []
            for index, value in enumerate(points):
                x = left + index / (len(points) - 1) * (right - left)
                y = bottom - min(value, 8000) / 8000 * plot_h
                coords.extend((x, y))
            canvas.create_line(*coords, fill=self.BLUE, width=2, smooth=True)
        canvas.create_text(
            right, height - 8, text="TIME →", fill=self.MUTED,
            anchor="e", font=("Segoe UI", 7),
        )

    def _draw_gauges(self) -> None:
        if not hasattr(self, "_gauge_canvas"):
            return
        canvas = self._gauge_canvas
        canvas.delete("all")
        width = max(canvas.winfo_width(), 220)
        center_y = 82
        radius = min(62, width / 3.3)
        for index, (label, value, maximum, color, unit) in enumerate((
            ("RPM", self._values["rpm"], 7000, self.BLUE, ""),
            ("BOOST", self._values["boost"], 2.0, self.CYAN, " bar"),
        )):
            center_x = width * (0.27 if index == 0 else 0.73)
            canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=135, extent=-270, style="arc", outline=self.GRID, width=9,
            )
            extent = -270 * min(max(value / maximum, 0), 1)
            canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=135, extent=extent, style="arc", outline=color, width=9,
            )
            canvas.create_text(
                center_x, center_y - 4, text=f"{value:.0f}" if index == 0 else f"{value:.2f}",
                fill=self.TEXT, font=("Segoe UI", 13, "bold"),
            )
            canvas.create_text(
                center_x, center_y + 17, text=unit or "rpm",
                fill=self.MUTED, font=("Segoe UI", 8),
            )
            canvas.create_text(
                center_x, center_y + radius + 17, text=label,
                fill=color, font=("Segoe UI", 8, "bold"),
            )

    def open_tuning(self) -> None:
        self._stop_simulation_for_navigation()
        for child in self.winfo_children():
            child.destroy()
        panel = TuningPanel(self, self.sound, self.logger)
        panel.pack(fill=BOTH, expand=True)
        ttk.Button(
            panel, text="← DASHBOARD", bootstyle="secondary",
            command=self.restore_dashboard,
        ).pack(anchor="w", padx=8, pady=6, before=panel.winfo_children()[0])

    def restore_dashboard(self) -> None:
        for child in self.winfo_children():
            child.destroy()
        self.running = False
        self.build()

    def _stop_simulation_for_navigation(self) -> None:
        self.running = False
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _on_destroy(self, event) -> None:
        if event.widget is self:
            self._stop_simulation_for_navigation()
