from __future__ import annotations

import threading
import wave
from pathlib import Path
from typing import Literal

try:
    from playsound import playsound
except Exception:  # pragma: no cover
    playsound = None

try:
    import winsound
except ImportError:  # pragma: no cover
    winsound = None

from src.utils.paths import SOUNDS_V1_DIR, SOUNDS_V3_DIR

SoundMode = Literal["light", "pro"]


class SoundManager:
    """Non-blocking sound service with graceful fallback.

    Missing MP3 files, broken audio backends, or missing FFmpeg must never
    prevent the GUI from starting or operating. On Windows, a generated WAV
    fallback is used when an MP3 cannot be played.
    """

    def __init__(self, mode: SoundMode = "light") -> None:
        self.mode = mode
        self.enabled = True
        self._lock = threading.Lock()

    def set_mode(self, mode: SoundMode) -> None:
        self.mode = mode

    def set_enabled(self, enabled: bool) -> None:
        self.enabled = bool(enabled)

    def _base_dir(self) -> Path:
        return SOUNDS_V1_DIR if self.mode == "light" else SOUNDS_V3_DIR

    def _resolve(self, filename: str) -> Path:
        return self._base_dir() / filename

    def _fallback_wav(self, filename: str) -> Path:
        return self._base_dir() / (Path(filename).stem + "_fallback.wav")

    def _play_wav(self, path: Path) -> None:
        if winsound is None or not path.exists():
            return
        try:
            winsound.PlaySound(str(path), winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            return

    def play(self, filename: str) -> None:
        if not self.enabled:
            return
        path = self._resolve(filename)
        fallback = self._fallback_wav(filename)

        if playsound is not None and path.exists():
            def worker() -> None:
                try:
                    playsound(str(path), block=False)
                except Exception:
                    self._play_wav(fallback)
            threading.Thread(target=worker, daemon=True).start()
            return

        self._play_wav(fallback)

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


def generate_fallback_wavs() -> int:
    """Create tiny deterministic WAV cues using only the Python stdlib."""
    sounds = {
        "startup_fallback.wav": (660, 0.16),
        "load_profile_fallback.wav": (520, 0.12),
        "turbo_spool_fallback.wav": (880, 0.10),
        "engine_rev_fallback.wav": (1040, 0.18),
        "error_fallback.wav": (180, 0.20),
        "shutdown_fallback.wav": (330, 0.18),
    }
    created = 0
    for directory in (SOUNDS_V1_DIR, SOUNDS_V3_DIR):
        directory.mkdir(parents=True, exist_ok=True)
        for name, (frequency, seconds) in sounds.items():
            target = directory / name
            if target.exists():
                continue
            sample_rate = 22050
            amplitude = 10000
            count = int(sample_rate * seconds)
            import math
            with wave.open(str(target), "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(sample_rate)
                frames = bytearray()
                for index in range(count):
                    value = int(amplitude * math.sin(2 * math.pi * frequency * index / sample_rate))
                    frames.extend(value.to_bytes(2, "little", signed=True))
                wav.writeframes(frames)
            created += 1
    return created
