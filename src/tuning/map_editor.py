from __future__ import annotations
import json
import tkinter as tk
from pathlib import Path
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, RIGHT, X, Y
from src.tuning.validators import clamp, validate_numeric_map

class MapEditor(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=10)
        self.values: list[float] = []
        self.entries: list[ttk.Entry] = []
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=X, pady=(0, 8))
        ttk.Button(toolbar, text="Novo", bootstyle="secondary", command=self.new_map).pack(side=LEFT, padx=3)
        ttk.Button(toolbar, text="Validar", bootstyle="warning", command=self.validate).pack(side=LEFT, padx=3)
        ttk.Button(toolbar, text="Aplicar limites", bootstyle="info", command=self.clamp_values).pack(side=LEFT, padx=3)
        self.status = ttk.Label(self, text="Mapa vazio.", bootstyle="secondary")
        self.status.pack(fill=X, pady=4)
        body = ttk.Frame(self)
        body.pack(fill=BOTH, expand=True)
        self.canvas = tk.Canvas(body, highlightthickness=0, bg="#111820")
        self.scroll = ttk.Scrollbar(body, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.new_map()

    def new_map(self, count: int = 32) -> None:
        for child in self.inner.winfo_children():
            child.destroy()
        self.entries.clear()
        self.values = [0.0] * count
        for index, value in enumerate(self.values):
            row = ttk.Frame(self.inner)
            row.pack(fill=X, pady=2)
            ttk.Label(row, text=f"{index:02d}", width=5).pack(side=LEFT)
            entry = ttk.Entry(row, width=18)
            entry.insert(0, str(value))
            entry.pack(side=LEFT)
            self.entries.append(entry)

    def read_values(self) -> list[float]:
        return [float(entry.get().replace(",", ".")) for entry in self.entries]

    def clamp_values(self) -> None:
        values = [clamp(v, -100.0, 100.0) for v in self.read_values()]
        for entry, value in zip(self.entries, values):
            entry.delete(0, "end")
            entry.insert(0, f"{value:.3f}")
        self.status.configure(text="Limites aplicados: -100 .. +100.")

    def validate(self) -> bool:
        try:
            ok, message = validate_numeric_map(self.read_values(), -100.0, 100.0)
        except ValueError:
            ok, message = False, "Existem valores não numéricos."
        self.status.configure(text=message)
        return ok

    def export_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"values": self.read_values()}, indent=2), encoding="utf-8")
        self.status.configure(text=f"Guardado: {path.name}")
