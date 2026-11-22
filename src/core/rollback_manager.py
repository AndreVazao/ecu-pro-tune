from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from src.utils.paths import BACKUPS_DIR, CONFIGS_DIR, ensure_directories


_BACKUP_PATTERN = re.compile(
    r"^(?P<profile>.+\.json)_(?P<date>\d{8})_(?P<time>\d{6})(?:_(?P<sequence>\d{3}))?\.bak\.json$"
)


def _reject_nonstandard_json_constant(value: str) -> None:
    raise ValueError(f"Valor JSON não permitido: {value}")


class RollbackManager:
    def __init__(self) -> None:
        ensure_directories()

    @staticmethod
    def _safe_config_filename(filename: str) -> bool:
        return (
            isinstance(filename, str)
            and Path(filename).name == filename
            and "/" not in filename
            and "\\" not in filename
            and filename.endswith(".json")
        )

    @staticmethod
    def _next_backup_path(profile_filename: str, timestamp: str) -> Path:
        first = BACKUPS_DIR / f"{profile_filename}_{timestamp}.bak.json"
        if not first.exists():
            return first

        for sequence in range(1, 1000):
            candidate = BACKUPS_DIR / f"{profile_filename}_{timestamp}_{sequence:03d}.bak.json"
            if not candidate.exists():
                return candidate

        raise RuntimeError("Limite de backups no mesmo segundo excedido.")

    def backup_profile(self, profile_filename: str) -> Path | None:
        if not self._safe_config_filename(profile_filename):
            raise ValueError("Nome de perfil inválido.")
        src = CONFIGS_DIR / profile_filename
        if not src.is_file():
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst = self._next_backup_path(profile_filename, timestamp)
        temporary = dst.with_suffix(dst.suffix + ".tmp")
        try:
            temporary.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            temporary.replace(dst)
        finally:
            if temporary.exists():
                temporary.unlink()
        return dst

    def list_backups(self) -> list[str]:
        return sorted(
            (
                file.name
                for file in BACKUPS_DIR.glob("*.bak.json")
                if file.is_file() and _BACKUP_PATTERN.fullmatch(file.name)
            ),
            reverse=True,
        )

    def restore_backup(self, backup_filename: str) -> Path | None:
        if (
            not isinstance(backup_filename, str)
            or Path(backup_filename).name != backup_filename
            or "/" in backup_filename
            or "\\" in backup_filename
        ):
            raise ValueError("Nome de backup inválido.")

        match = _BACKUP_PATTERN.fullmatch(backup_filename)
        if match is None:
            raise ValueError("Formato de backup inválido.")

        src = BACKUPS_DIR / backup_filename
        if not src.is_file():
            return None

        try:
            backup_text = src.read_text(encoding="utf-8")
            restored_data = json.loads(
                backup_text,
                parse_constant=_reject_nonstandard_json_constant,
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            raise ValueError("O backup não contém JSON válido.") from exc
        if not isinstance(restored_data, dict):
            raise ValueError("O backup não contém um objeto JSON.")

        dst = CONFIGS_DIR / match.group("profile")
        temporary = dst.with_suffix(dst.suffix + ".restore.tmp")
        try:
            temporary.write_text(
                backup_text,
                encoding="utf-8",
            )
            temporary.replace(dst)
        finally:
            if temporary.exists():
                temporary.unlink()
        return dst
