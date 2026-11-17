from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_windows_installer_pins_validated_python_and_checks_dependencies() -> None:
    installer = (ROOT / "install_ecu_pro_tune.bat").read_text(encoding="utf-8")

    assert "py -3.11" in installer
    assert "python.exe -m pip check" in installer
    assert "python.exe -m pip install -r requirements.txt" in installer
    assert ":venv_incompatible" in installer


def test_installer_never_installs_ffmpeg_without_user_confirmation() -> None:
    installer = (ROOT / "install_ecu_pro_tune.bat").read_text(encoding="utf-8")

    assert 'set "INSTALL_FFMPEG=N"' in installer
    assert 'if /I not "%INSTALL_FFMPEG%"=="S" goto :ffmpeg_skipped' in installer
    assert "winget install --id Gyan.FFmpeg.Shared" in installer


def test_windows_build_includes_runtime_data_and_collects_gui_resources() -> None:
    build_script = (ROOT / "build_exe.bat").read_text(encoding="utf-8")

    assert '--add-data "configs;configs"' in build_script
    assert '--add-data "maps;maps"' in build_script
    assert "--collect-all ttkbootstrap" in build_script
    assert "--collect-all matplotlib" in build_script
    assert "scripts\\generate_windows_version_info.py" in build_script
    assert "--version-file build\\windows_version_info.txt" in build_script
    assert r"dist\ECUProTune\ECUProTune.exe" in build_script
    assert 'if exist dist rmdir /s /q dist' not in build_script
    assert 'if exist build rmdir /s /q build' not in build_script


def test_windows_test_launcher_checks_environment_and_runs_pip_check() -> None:
    test_script = (ROOT / "ecu_test.bat").read_text(encoding="utf-8")

    assert "sys.version_info[:2] == (3, 11)" in test_script
    assert "python.exe -m pip check" in test_script
    assert "python.exe -m compileall -q src tests" in test_script
    assert "python.exe -m pytest -q tests" in test_script
