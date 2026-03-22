from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
APP_DIR = SRC_DIR / "app"
CORE_DIR = SRC_DIR / "core"
TUNING_DIR = SRC_DIR / "tuning"
UTILS_DIR = SRC_DIR / "utils"
GENERATORS_DIR = SRC_DIR / "generators"

ASSETS_DIR = PROJECT_ROOT / "assets"
DOCS_DIR = PROJECT_ROOT / "docs"
CONFIGS_DIR = PROJECT_ROOT / "configs"
MAPS_DIR = PROJECT_ROOT / "maps"
TESTS_DIR = PROJECT_ROOT / "tests"

SOUNDS_V1_DIR = ASSETS_DIR / "sounds_v1"
SOUNDS_V3_DIR = ASSETS_DIR / "sounds_v3"
ICONS_DIR = ASSETS_DIR / "icons"
THEMES_DIR = ASSETS_DIR / "themes"

BACKUPS_DIR = PROJECT_ROOT / "backups"
RUNTIME_DIR = PROJECT_ROOT / "runtime"
PROFILES_DIR = PROJECT_ROOT / "runtime" / "profiles"

AUTH_FILE = PROJECT_ROOT / "auth.json"
SCHEDULE_FILE = PROJECT_ROOT / "schedules.json"
LOG_FILE = PROJECT_ROOT / "runtime" / "ecu_pro_tune.log"


def ensure_directories() -> None:
    dirs = [
        ASSETS_DIR,
        DOCS_DIR,
        CONFIGS_DIR,
        MAPS_DIR,
        TESTS_DIR,
        SOUNDS_V1_DIR,
        SOUNDS_V3_DIR,
        ICONS_DIR,
        THEMES_DIR,
        BACKUPS_DIR,
        RUNTIME_DIR,
        PROFILES_DIR,
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)


def getenv_path(name: str, default: Path) -> Path:
    value = os.getenv(name)
    return Path(value).expanduser().resolve() if value else default.resolve()
