from __future__ import annotations

import threading
from pathlib import Path
from typing import Literal

try:
    from playsound import playsound
except Exception:  # pragma: no cover
    playsound = None

from src.utils.paths import SOUNDS_V1_DIR, SOUNDS_V3_DIR


SoundMode = Literal["light", "pro"]


class SoundManager:
    def __init__(self, mode: SoundMode = "light") -> None:
        self.mode = mode

    def set_mode(self, mode: SoundMode) -> None:
        self.mode = mode

    def _base_dir(self) -> Path:
        return SOUNDS_V1_DIR if self.mode == "light" else SOUNDS_V3_DIR

    def _resolve(self, filename: str) -> Path:
        return self._base_dir() / filename

    def play(self, filename: str) -> None:
        if playsound is None:
            return

        path = self._resolve(filename)
        if not path.exists():
            return

        threading.Thread(target=playsound, args=(str(path),), daemon=True).start()

    def play_startup(self) -> None:
        self.play("startup.mp3")

    def play_profile_load(self) -> None:
        self.play("load_profile.mp3")

    def play_spool(self) -> None:
        self.play("turbo_spool.mp3")

    def play_success(self) -> None:
        self.play("engine_rev.mp3")

    def play_error(self) -> None:
        self.play("error.mp3")

    def play_shutdown(self) -> None:
        self.play("shutdown.mp3")
