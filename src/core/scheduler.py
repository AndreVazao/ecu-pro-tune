from __future__ import annotations

import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Callable, Any

from src.core.logger import setup_logger
from src.utils.paths import SCHEDULE_FILE


class Scheduler(threading.Thread):
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
        if not SCHEDULE_FILE.exists():
            return []

        try:
            data = json.loads(SCHEDULE_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError("O ficheiro de agendamentos está ilegível.") from exc

        if not isinstance(data, list):
            raise ValueError("O ficheiro de agendamentos tem de conter uma lista.")

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

        return data

    @staticmethod
    def _write_schedule_file(data: list[dict[str, Any]]) -> None:
        SCHEDULE_FILE.parent.mkdir(parents=True, exist_ok=True)
        temporary = SCHEDULE_FILE.with_suffix(SCHEDULE_FILE.suffix + ".tmp")
        temporary.write_text(
            json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False),
            encoding="utf-8",
        )
        temporary.replace(SCHEDULE_FILE)

    def run(self) -> None:
        while not self._stop_event.is_set():
            try:
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
                # Keep the scheduler alive and leave malformed files untouched.
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

        data = Scheduler._read_schedule_file()
        data.append(
            {
                "profile": profile,
                "run_at": run_at_iso,
                "executed": False,
            }
        )
        Scheduler._write_schedule_file(data)
