import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

import pytest

import src.core.logger as logger_module
import src.core.scheduler as scheduler_module
from src.core.logger import setup_logger
from src.core.scheduler import Scheduler


def test_add_schedule_appends_valid_entries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    schedule_file = tmp_path / "runtime" / "schedules.json"
    monkeypatch.setattr(scheduler_module, "SCHEDULE_FILE", schedule_file)

    Scheduler.add_schedule("stage1.json", datetime.now().isoformat())
    Scheduler.add_schedule("daily setup", (datetime.now() + timedelta(hours=1)).isoformat())

    data = json.loads(schedule_file.read_text(encoding="utf-8"))
    assert len(data) == 2
    assert data[0]["profile"] == "stage1.json"
    assert data[0]["executed"] is False
    assert data[1]["profile"] == "daily setup"


@pytest.mark.parametrize(
    ("profile", "run_at"),
    [
        ("", datetime.now().isoformat()),
        ("../outside.json", datetime.now().isoformat()),
        (r"..\outside.json", datetime.now().isoformat()),
        ("stage1.json", "not-a-date"),
    ],
)
def test_add_schedule_rejects_invalid_input(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    profile: str,
    run_at: str,
) -> None:
    monkeypatch.setattr(
        scheduler_module, "SCHEDULE_FILE", tmp_path / "schedules.json"
    )

    with pytest.raises(ValueError):
        Scheduler.add_schedule(profile, run_at)


def test_add_schedule_preserves_corrupt_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    schedule_file = tmp_path / "schedules.json"
    original = "{ this is not valid JSON"
    schedule_file.write_text(original, encoding="utf-8")
    monkeypatch.setattr(scheduler_module, "SCHEDULE_FILE", schedule_file)

    with pytest.raises(ValueError, match="ilegível"):
        Scheduler.add_schedule("stage1.json", datetime.now().isoformat())

    assert schedule_file.read_text(encoding="utf-8") == original


def test_scheduler_executes_due_items_once_and_keeps_future_items(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    schedule_file = tmp_path / "schedules.json"
    now = datetime.now()
    schedule_file.write_text(
        json.dumps(
            [
                {
                    "profile": "due.json",
                    "run_at": (now - timedelta(minutes=1)).isoformat(),
                    "executed": False,
                },
                {
                    "profile": "future.json",
                    "run_at": (now + timedelta(days=1)).isoformat(),
                    "executed": False,
                },
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(scheduler_module, "SCHEDULE_FILE", schedule_file)
    executed: list[str] = []
    scheduler: Scheduler

    def callback(profile: str) -> None:
        executed.append(profile)
        scheduler.stop()

    scheduler = Scheduler(callback)
    scheduler.run()

    data = json.loads(schedule_file.read_text(encoding="utf-8"))
    assert executed == ["due.json"]
    assert data[0]["executed"] is True
    assert data[1]["executed"] is False


def test_scheduler_logs_callback_failure_and_keeps_schedule_pending(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    schedule_file = tmp_path / "schedules.json"
    schedule_file.write_text(
        json.dumps(
            [
                {
                    "profile": "retry.json",
                    "run_at": (datetime.now() - timedelta(minutes=1)).isoformat(),
                    "executed": False,
                }
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(scheduler_module, "SCHEDULE_FILE", schedule_file)
    logger = logging.getLogger("ecu-scheduler-callback-test")
    caplog.set_level(logging.ERROR, logger=logger.name)
    scheduler: Scheduler

    def callback(_profile: str) -> None:
        scheduler.stop()
        raise RuntimeError("temporary callback failure")

    scheduler = Scheduler(callback, logger=logger)
    scheduler.run()

    data = json.loads(schedule_file.read_text(encoding="utf-8"))
    assert data[0]["executed"] is False
    assert any(
        "retry.json" in record.getMessage()
        and "novamente tentado" in record.getMessage()
        and record.exc_info is not None
        for record in caplog.records
    )


def test_scheduler_logs_invalid_storage_and_preserves_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    schedule_file = tmp_path / "schedules.json"
    original = "{ malformed scheduler JSON"
    schedule_file.write_text(original, encoding="utf-8")
    monkeypatch.setattr(scheduler_module, "SCHEDULE_FILE", schedule_file)
    logger = logging.getLogger("ecu-scheduler-storage-test")
    caplog.set_level(logging.ERROR, logger=logger.name)
    scheduler = Scheduler(lambda _profile: None, logger=logger)

    class StopOnWait:
        def is_set(self) -> bool:
            return False

        def set(self) -> None:
            pass

        def wait(self, _timeout: float) -> bool:
            return True

    scheduler._stop_event = StopOnWait()  # type: ignore[assignment]
    scheduler.run()

    assert schedule_file.read_text(encoding="utf-8") == original
    assert any(
        "ficheiro de agendamentos" in record.getMessage()
        and record.exc_info is not None
        for record in caplog.records
    )


def test_logger_writes_utf8_records_and_can_be_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    log_file = tmp_path / "logs" / "ecu.log"
    log_file.parent.mkdir(parents=True)
    monkeypatch.setattr(logger_module, "LOG_FILE", log_file)
    logger = setup_logger(f"ecu-pro-tune-test-{tmp_path.name}")

    try:
        logger.info("integration log entry: ação concluída")
        for handler in logger.handlers:
            handler.flush()

        content = log_file.read_text(encoding="utf-8")
        assert "INFO" in content
        assert "integration log entry: ação concluída" in content
    finally:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
            handler.close()
