from __future__ import annotations

import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4

from src.core.logger import setup_logger
from src.utils.json_utils import strict_json_loads
from src.utils.paths import SCHEDULE_FILE


class Scheduler(threading.Thread):
    """Persistent local scheduler; callbacks run in simulation-only application context."""

    _file_lock = threading.RLock()

    def __init__(
        self,
        callback: Callable[[str], None],
        logger: logging.Logger | None = None,
    ) -> None:
        super().__init__(daemon=True)
        self.callback = callback
        self.logger = logger or setup_logger("ecu_scheduler")
        self._stop_event = threading.Event()

    def stop(self) -> None:
        self._stop_event.set()

    @staticmethod
    def _validate_profile_name(profile: str) -> None:
        if (
            not isinstance(profile, str)
            or not profile.strip()
            or Path(profile).name != profile
            or "/" in profile
            or "\\" in profile
        ):
            raise ValueError("Nome de perfil agendado inválido.")

    @staticmethod
    def _read_schedule_file() -> list[dict[str, Any]]:
        with Scheduler._file_lock:
            if not SCHEDULE_FILE.exists():
                return []

            try:
                data = strict_json_loads(SCHEDULE_FILE.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                raise ValueError("O ficheiro de agendamentos está ilegível.") from exc

            if not isinstance(data, list):
                raise ValueError("O ficheiro de agendamentos tem de conter uma lista.")

            seen_ids: set[str] = set()
            for item in data:
                if not isinstance(item, dict):
                    raise ValueError("Existe uma entrada de agendamento inválida.")
                if not isinstance(item.get("profile"), str):
                    raise ValueError("Um agendamento não contém um perfil válido.")
                Scheduler._validate_profile_name(item["profile"])
                if not isinstance(item.get("run_at"), str):
                    raise ValueError("Um agendamento não contém uma data válida.")
                try:
                    datetime.fromisoformat(item["run_at"])
                except ValueError as exc:
                    raise ValueError("Um agendamento contém uma data inválida.") from exc
                if not isinstance(item.get("executed"), bool):
                    raise ValueError("O estado de execução do agendamento é inválido.")
                schedule_id = item.get("id")
                if schedule_id is not None:
                    if not isinstance(schedule_id, str) or not schedule_id.strip():
                        raise ValueError("O identificador do agendamento é inválido.")
                    if schedule_id in seen_ids:
                        raise ValueError("Existem identificadores de agendamento duplicados.")
                    seen_ids.add(schedule_id)

            return data

    @staticmethod
    def _write_schedule_file(data: list[dict[str, Any]]) -> None:
        with Scheduler._file_lock:
            SCHEDULE_FILE.parent.mkdir(parents=True, exist_ok=True)
            temporary = SCHEDULE_FILE.with_suffix(SCHEDULE_FILE.suffix + ".tmp")
            temporary.write_text(
                json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False),
                encoding="utf-8",
            )
            temporary.replace(SCHEDULE_FILE)

    @staticmethod
    def list_schedules() -> list[dict[str, Any]]:
        """Return a safe snapshot; legacy records receive stable-in-snapshot IDs."""
        with Scheduler._file_lock:
            data = Scheduler._read_schedule_file()
            result: list[dict[str, Any]] = []
            for index, item in enumerate(data):
                entry = dict(item)
                entry["id"] = item.get("id") or f"legacy:{index}"
                result.append(entry)
            return result

    @staticmethod
    def cancel_schedule(schedule_id: str) -> bool:
        """Cancel one pending entry without rewriting unrelated schedule records."""
        if not isinstance(schedule_id, str) or not schedule_id:
            raise ValueError("Identificador do agendamento inválido.")

        with Scheduler._file_lock:
            data = Scheduler._read_schedule_file()
            for index, item in enumerate(data):
                current_id = item.get("id") or f"legacy:{index}"
                if current_id == schedule_id:
                    if item["executed"]:
                        return False
                    del data[index]
                    Scheduler._write_schedule_file(data)
                    return True
        return False

    def run(self) -> None:
        while not self._stop_event.is_set():
            try:
                with self._file_lock:
                    data = self._read_schedule_file()
                    changed = False

                    for item in data:
                        if item["executed"]:
                            continue

                        run_at = datetime.fromisoformat(item["run_at"])
                        now = datetime.now(run_at.tzinfo) if run_at.tzinfo else datetime.now()
                        if now < run_at:
                            continue

                        try:
                            self.callback(item["profile"])
                        except Exception:
                            self.logger.exception(
                                "Agendamento do perfil %s falhou; continua pendente "
                                "e será novamente tentado.",
                                item["profile"],
                            )
                            continue

                        item["executed"] = True
                        changed = True

                    if changed:
                        self._write_schedule_file(data)
            except (OSError, ValueError, TypeError):
                self.logger.exception(
                    "Scheduler não conseguiu processar o ficheiro de agendamentos; "
                    "os dados existentes foram preservados."
                )

            if self._stop_event.wait(5):
                break

    @staticmethod
    def add_schedule(profile: str, run_at_iso: str) -> None:
        Scheduler._validate_profile_name(profile)
        if not isinstance(run_at_iso, str):
            raise ValueError("Data de agendamento inválida.")
        try:
            datetime.fromisoformat(run_at_iso)
        except ValueError as exc:
            raise ValueError("Data de agendamento inválida.") from exc

        with Scheduler._file_lock:
            data = Scheduler._read_schedule_file()
            data.append(
                {
                    "id": str(uuid4()),
                    "profile": profile,
                    "run_at": run_at_iso,
                    "executed": False,
                }
            )
            Scheduler._write_schedule_file(data)
