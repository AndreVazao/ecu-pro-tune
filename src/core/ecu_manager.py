from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.core.logger import setup_logger
from src.utils.paths import CONFIGS_DIR, MAPS_DIR


logger = setup_logger("ecu_manager")


class ECUManager:
    def __init__(self) -> None:
        self.logger = logger

    def load_profile(self, profile_filename: str) -> dict[str, Any]:
        profile_path = CONFIGS_DIR / profile_filename
        if not profile_path.exists():
            raise FileNotFoundError(f"Perfil não encontrado: {profile_path}")

        self.logger.info("Loading profile: %s", profile_path)
        return json.loads(profile_path.read_text(encoding="utf-8"))

    def validate_profile_maps(self, profile_data: dict[str, Any]) -> list[str]:
        missing: list[str] = []

        for key, value in profile_data.items():
            if key == "Profile_Name":
                continue

            if isinstance(value, str) and value.endswith(".json"):
                map_path = MAPS_DIR / value
                if not map_path.exists():
                    missing.append(str(map_path))

        return missing

    def apply_profile(self, profile_filename: str) -> tuple[bool, list[str]]:
        profile = self.load_profile(profile_filename)
        missing = self.validate_profile_maps(profile)

        if missing:
            self.logger.error("Missing maps for profile %s: %s", profile_filename, missing)
            return False, missing

        self.logger.info("Profile applied successfully: %s", profile_filename)
        return True, []

    def list_numeric_arrays(self, profile_filename: str) -> dict[str, list[float]]:
        profile = self.load_profile(profile_filename)
        arrays: dict[str, list[float]] = {}

        for key, value in profile.items():
            if isinstance(value, list) and all(isinstance(x, (int, float)) for x in value):
                arrays[key] = value

        if arrays:
            return arrays

        for key, value in profile.items():
            if key == "Profile_Name":
                continue
            if isinstance(value, str) and value.endswith(".json"):
                map_path = MAPS_DIR / value
                if not map_path.exists():
                    continue
                try:
                    map_data = json.loads(map_path.read_text(encoding="utf-8"))
                    for mk, mv in map_data.items():
                        if isinstance(mv, list) and all(isinstance(x, (int, float)) for x in mv):
                            arrays[f"{value}:{mk}"] = mv
                except Exception:
                    continue

        return arrays
