from __future__ import annotations

import json
import threading
import time
from datetime import datetime
from typing import Callable

from src.utils.paths import SCHEDULE_FILE


class Scheduler(threading.Thread):
    def __init__(self, callback: Callable[[str], None]) -> None:
        super().__init__(daemon=True)
        self.callback = callback
        self._stop_event = threading.Event()

    def stop(self) -> None:
        self._stop_event.set()

    def run(self) -> None:
        while not self._stop_event.is_set():
            try:
                if SCHEDULE_FILE.exists():
                    data = json.loads(SCHEDULE_FILE.read_text(encoding="utf-8"))
                    now = datetime.now()
                    changed = False

                    for item in data:
                        if item.get("executed"):
                            continue

                        run_at = datetime.fromisoformat(item["run_at"])
                        if now >= run_at:
                            self.callback(item["profile"])
                            item["executed"] = True
                            changed = True

                    if changed:
                        SCHEDULE_FILE.write_text(
                            json.dumps(data, indent=2, ensure_ascii=False),
                            encoding="utf-8",
                        )
            except Exception:
                pass

            time.sleep(5)

    @staticmethod
    def add_schedule(profile: str, run_at_iso: str) -> None:
        data = []
        if SCHEDULE_FILE.exists():
            try:
                data = json.loads(SCHEDULE_FILE.read_text(encoding="utf-8"))
            except Exception:
                data = []

        data.append(
            {
                "profile": profile,
                "run_at": run_at_iso,
                "executed": False,
            }
        )
        SCHEDULE_FILE.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
                      )
