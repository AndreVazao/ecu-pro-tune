from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from src.utils.paths import BACKUPS_DIR, CONFIGS_DIR, ensure_directories


_BACKUP_PATTERN = re.compile(
    r"^(?P<profile>.+\\.json)_(?P<date>\\d{8})_(?P<time>\\d{6})\\.bak\\.json$"
)


class RollbackManager:
    def __init__(self) -> None:
        ensure_directories()

    @staticmethod
    def _safe_config_filename(filename: str) -> bool:
        return (
            isinstance(filename, str)
            and Path(filename).name == filename
            and "/" not in filename
            and "\\\\" not in filename
            and filename.endswith(".json")
        )

    def backup_profile(self, profile_filename: str) -> Path | None:
        if not self._safe_config_filename(profile_filename):
            raise ValueError("Nome de perfil inválido.")
        src = CONFIGS_DIR / profile_filename
        if not src.is_file():
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst = BACKUPS_DIR / f"{profile_filename}_{timestamp}.bak.json"
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
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
            or "\\\\" in backup_filename
        ):
            raise ValueError("Nome de backup inválido.")

        match = _BACKUP_PATTERN.fullmatch(backup_filename)
        if match is None:
            raise ValueError("Formato de backup inválido.")

        src = BACKUPS_DIR / backup_filename
        if not src.is_file():
            return None

        dst = CONFIGS_DIR / match.group("profile")
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        return dst
