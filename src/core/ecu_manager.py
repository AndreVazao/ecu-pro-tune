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
        if (
            not isinstance(profile_filename, str)
            or Path(profile_filename).name != profile_filename
            or "/" in profile_filename
            or "\\\\" in profile_filename
            or not profile_filename.endswith(".json")
        ):
            raise ValueError("Nome de perfil inválido.")

        profile_path = CONFIGS_DIR / profile_filename
        if not profile_path.is_file():
            raise FileNotFoundError(f"Perfil não encontrado: {profile_path}")

        self.logger.info("Loading profile: %s", profile_path)
        data = json.loads(profile_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("O perfil não contém um objeto JSON.")
        return data

    @staticmethod
    def _map_path(filename: str) -> Path | None:
        if (
            not isinstance(filename, str)
            or Path(filename).name != filename
            or "/" in filename
            or "\\\\" in filename
            or not filename.endswith(".json")
        ):
            return None
        candidate = (MAPS_DIR / filename).resolve()
        try:
            candidate.relative_to(MAPS_DIR.resolve())
        except ValueError:
            return None
        return candidate

    def validate_profile_maps(self, profile_data: dict[str, Any]) -> list[str]:
        missing: list[str] = []
        for key, value in profile_data.items():
            if key == "Profile_Name":
                continue
            if isinstance(value, str) and value.endswith(".json"):
                map_path = self._map_path(value)
                if map_path is None:
                    missing.append(f"Referência de mapa inválida: {value}")
                elif not map_path.is_file():
                    missing.append(str(map_path))
        return missing

    def apply_profile(self, profile_filename: str) -> tuple[bool, list[str]]:
        profile = self.load_profile(profile_filename)
        missing = self.validate_profile_maps(profile)
        if missing:
            self.logger.error(
                "Missing or invalid maps for profile %s: %s",
                profile_filename,
                missing,
            )
            return False, missing
        self.logger.info("Profile applied successfully: %s", profile_filename)
        return True, []

    def list_numeric_arrays(self, profile_filename: str) -> dict[str, list[float]]:
        profile = self.load_profile(profile_filename)
        arrays: dict[str, list[float]] = {}

        for key, value in profile.items():
            if (
                isinstance(value, list)
                and value
                and all(
                    isinstance(item, (int, float))
                    and not isinstance(item, bool)
                    for item in value
                )
            ):
                arrays[key] = value

        if arrays:
            return arrays

        for key, value in profile.items():
            if key == "Profile_Name" or not isinstance(value, str):
                continue
            if not value.endswith(".json"):
                continue
            map_path = self._map_path(value)
            if map_path is None or not map_path.is_file():
                continue
            try:
                map_data = json.loads(map_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                self.logger.exception("Could not read map: %s", map_path)
                continue
            if not isinstance(map_data, dict):
                continue
            for map_key, map_values in map_data.items():
                if (
                    isinstance(map_values, list)
                    and map_values
                    and all(
                        isinstance(item, (int, float))
                        and not isinstance(item, bool)
                        for item in map_values
                    )
                ):
                    arrays[f"{value}:{map_key}"] = map_values

        return arrays
