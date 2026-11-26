from __future__ import annotations

from src.app.dashboard import Dashboard


def test_dashboard_history_window_matches_sample_count_and_interval() -> None:
    assert Dashboard.SAMPLE_INTERVAL_MS == 400
    assert Dashboard.HISTORY_SAMPLES == 90
    assert Dashboard.HISTORY_WINDOW_SECONDS == 36


def test_dashboard_rpm_and_load_use_explicit_independent_scales() -> None:
    assert Dashboard.RPM_CHART_MAX == 8000
    assert Dashboard.HISTORY_WINDOW_SECONDS == (
        Dashboard.HISTORY_SAMPLES * Dashboard.SAMPLE_INTERVAL_MS / 1000
    )
