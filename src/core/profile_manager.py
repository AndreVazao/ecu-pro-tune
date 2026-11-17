from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.utils.paths import PROFILES_DIR, CONFIGS_DIR, ensure_directories


class ProfileManager:
    def __init__(self, base_dir: Path | None = None) -> None:
        ensure_directories()
        self.base_dir = Path(base_dir) if base_dir is not None else PROFILES_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _profile_path(name: str, base_dir: Path) -> Path:
        if not isinstance(name, str):
            raise ValueError("Nome de perfil inválido.")
        cleaned = name.strip()
        if (
            not cleaned
            or cleaned in {".", ".."}
            or Path(cleaned).name != cleaned
            or "/" in cleaned
            or "\\\\" in cleaned
            or cleaned.endswith(".json")
        ):
            raise ValueError("Nome de perfil inválido.")
        return base_dir / f"{cleaned}.json"

    def list_saved_profiles(self) -> list[str]:
        return sorted(
            file.stem for file in self.base_dir.glob("*.json") if file.is_file()
        )

    def list_config_profiles(self) -> list[str]:
        return sorted(
            file.name for file in CONFIGS_DIR.glob("*.json") if file.is_file()
        )

    def save_profile(self, name: str, data: dict[str, Any]) -> Path:
        if not isinstance(data, dict):
            raise TypeError("Os dados do perfil têm de ser um objeto.")
        target = self._profile_path(name, self.base_dir)
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_text(
            json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False),
            encoding="utf-8",
        )
        temporary.replace(target)
        return target

    def load_saved_profile(self, name: str) -> dict[str, Any] | None:
        target = self._profile_path(name, self.base_dir)
        if not target.exists():
            return None
        data = json.loads(target.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("O ficheiro de perfil não contém um objeto JSON.")
        return data

    def load_config_profile(self, filename: str) -> dict[str, Any] | None:
        if (
            not isinstance(filename, str)
            or Path(filename).name != filename
            or "/" in filename
            or "\\\\" in filename
            or not filename.endswith(".json")
        ):
            raise ValueError("Nome de configuração inválido.")
        target = CONFIGS_DIR / filename
        if not target.exists():
            return None
        data = json.loads(target.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("A configuração não contém um objeto JSON.")
        return data
