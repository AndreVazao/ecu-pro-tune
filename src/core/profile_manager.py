from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.utils.paths import PROFILES_DIR, CONFIGS_DIR, ensure_directories


class ProfileManager:
    def __init__(self, base_dir: Path | None = None) -> None:
        ensure_directories()
        self.base_dir = base_dir or PROFILES_DIR

    def list_saved_profiles(self) -> list[str]:
        return sorted(
            file.stem for file in self.base_dir.glob("*.json") if file.is_file()
        )

    def list_config_profiles(self) -> list[str]:
        return sorted(
            file.name for file in CONFIGS_DIR.glob("*.json") if file.is_file()
        )

    def save_profile(self, name: str, data: dict[str, Any]) -> Path:
        target = self.base_dir / f"{name}.json"
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return target

    def load_saved_profile(self, name: str) -> dict[str, Any] | None:
        target = self.base_dir / f"{name}.json"
        if not target.exists():
            return None
        return json.loads(target.read_text(encoding="utf-8"))

    def load_config_profile(self, filename: str) -> dict[str, Any] | None:
        target = CONFIGS_DIR / filename
        if not target.exists():
            return None
        return json.loads(target.read_text(encoding="utf-8"))
