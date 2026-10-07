from __future__ import annotations
import random
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, RIGHT, X

from src.core.ecu_manager import ECUManager
from src.core.profile_manager import ProfileManager
from src.core.rollback_manager import RollbackManager
from src.tuning.live_graphs import LiveGraph
from src.tuning.map_editor import MapEditor
from src.utils.paths import MAPS_DIR

class TuningPanel(ttk.Frame):
    def __init__(self, parent, sound_manager, log) -> None:
        super().__init__(parent, padding=10)
        self.sound = sound_manager
        self.log = log
        self.ecu = ECUManager()
        self.profiles = ProfileManager()
        self.rollback = RollbackManager()
        self.selected_profile = tk.StringVar()
        self.build()

    def build(self) -> None:
        top = ttk.Frame(self)
        top.pack(fill=X, pady=(0, 8))
        ttk.Label(top, text="Perfil", bootstyle="secondary").pack(side=LEFT, padx=(0, 6))
        self.combo = ttk.Combobox(top, textvariable=self.selected_profile, state="readonly")
        self.combo.pack(side=LEFT, fill=X, expand=True)
        ttk.Button(top, text="Atualizar", bootstyle="secondary", command=self.refresh_profiles).pack(side=LEFT, padx=5)
        ttk.Button(top, text="Carregar", bootstyle="info", command=self.load_profile).pack(side=LEFT, padx=5)
        ttk.Button(top, text="Backup", bootstyle="warning", command=self.backup_profile).pack(side=LEFT, padx=5)

        splitter = ttk.Panedwindow(self, orient="horizontal")
        splitter.pack(fill=BOTH, expand=True)
        left = ttk.Frame(splitter, padding=6)
        right = ttk.Frame(splitter, padding=6)
        splitter.add(left, weight=1)
        splitter.add(right, weight=2)

        self.map_editor = MapEditor(left)
        self.map_editor.pack(fill=BOTH, expand=True)
        self.graph = LiveGraph(right)
        self.refresh_profiles()

    def refresh_profiles(self) -> None:
        profiles = self.profiles.list_config_profiles()
        self.combo["values"] = profiles
        if profiles and not self.selected_profile.get():
            self.selected_profile.set(profiles[0])

    def load_profile(self) -> None:
        name = self.selected_profile.get()
        if not name:
            return
        try:
            self.ecu.load_profile(name)
            arrays = self.ecu.list_numeric_arrays(name)
            self.log.info("Perfil carregado: %s", name)
            self.sound.play_profile_load()
            if arrays:
                first = next(iter(arrays.values()))
                self.map_editor.new_map(len(first))
                for entry, value in zip(self.map_editor.entries, first):
                    entry.delete(0, "end")
                    entry.insert(0, str(value))
            for _ in range(12):
                self.graph.update(random.uniform(0, 100))
        except Exception as exc:
            self.log.exception("Erro a carregar perfil: %s", exc)
            self.sound.play_error()

    def backup_profile(self) -> None:
        name = self.selected_profile.get()
        if not name:
            return
        target = self.rollback.backup_profile(name)
        if target:
            self.log.info("Backup criado: %s", target)

    def save_map(self) -> None:
        if not self.map_editor.validate():
            return
        path = MAPS_DIR / "edited_map.json"
        self.map_editor.export_json(path)
        self.log.info("Mapa guardado: %s", path)
