from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.utils.paths import BACKUPS_DIR, CONFIGS_DIR, ensure_directories


class RollbackManager:
    def __init__(self) -> None:
        ensure_directories()

    def backup_profile(self, profile_filename: str) -> Path | None:
        src = CONFIGS_DIR / profile_filename
        if not src.exists():
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst = BACKUPS_DIR / f"{profile_filename}_{timestamp}.bak.json"
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        return dst

    def list_backups(self) -> list[str]:
        return sorted(
            [file.name for file in BACKUPS_DIR.glob("*.bak.json") if file.is_file()],
            reverse=True,
        )

    def restore_backup(self, backup_filename: str) -> Path | None:
        src = BACKUPS_DIR / backup_filename
        if not src.exists():
            return None

        parts = backup_filename.split("_")
        if len(parts) > 1:
            original = "_".join(parts[:-1])
        else:
            original = backup_filename.replace(".bak.json", "")

        if not original.endswith(".json"):
            original += ".json"

        dst = CONFIGS_DIR / original
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        return dst
