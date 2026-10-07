from __future__ import annotations

from collections import deque
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LiveGraph:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.x = deque(maxlen=120)
        self.y = deque(maxlen=120)
        self.figure = Figure(figsize=(7, 3.2), dpi=90)
        self.axis = self.figure.add_subplot(111)
        self.axis.set_facecolor("#101820")
        self.axis.tick_params(colors="#aab8c4")
        for spine in self.axis.spines.values():
            spine.set_color("#334452")
        self.axis.set_title("Telemetria / simulação", color="#8ed8ff")
        self.axis.set_xlabel("Amostra", color="#9aa9b8")
        self.axis.set_ylabel("Valor", color="#9aa9b8")
        self.line, = self.axis.plot([], [], linewidth=2)
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update(self, value: float) -> None:
        index = self.x[-1] + 1 if self.x else 0
        self.x.append(index)
        self.y.append(value)
        self.line.set_data(list(self.x), list(self.y))
        self.axis.relim()
        self.axis.autoscale_view()
        self.canvas.draw_idle()

    def clear(self) -> None:
        self.x.clear()
        self.y.clear()
        self.line.set_data([], [])
        self.canvas.draw_idle()
