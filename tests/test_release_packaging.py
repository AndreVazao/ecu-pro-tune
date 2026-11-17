from pathlib import Path

from src.version import __version__


ROOT = Path(__file__).resolve().parents[1]


def test_application_version_matches_version_file() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    assert version == __version__
    assert version == "0.1.0"


def test_release_packager_creates_archive_manifest_and_checksum() -> None:
    script = (ROOT / "scripts" / "package_release.ps1").read_text(encoding="utf-8")

    assert "Compress-Archive" in script
    assert '$internalDirectory = Join-Path $source "_internal"' in script
    assert "Get-FileHash" in script
    assert "BUILD-MANIFEST.json" in script
    assert "SHA256SUMS.txt" in script
    assert "ECUProTune-Windows-Python311-v$version.zip" in script
    assert "verifiedHash -ne $sha256" in script


def test_windows_ci_packages_and_uploads_release_directory() -> None:
    workflow = (ROOT / ".github" / "workflows" / "windows-ci.yml").read_text(
        encoding="utf-8"
    )

    assert "Package Windows release" in workflow
    assert "package_release.ps1" in workflow
    assert "path: release/" in workflow
    assert "BUILD-MANIFEST.json" in workflow
    assert "SHA256" in workflow


def test_main_window_displays_application_version() -> None:
    main = (ROOT / "src" / "app" / "main.py").read_text(encoding="utf-8")

    assert "from src.version import __version__" in main
    assert 'self.root.title(f"ECU Pro Tune v{__version__}")' in main



def test_local_build_invokes_release_packager_without_broad_cleanup() -> None:
    build_script = (ROOT / "build_exe.bat").read_text(encoding="utf-8")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    assert "scripts\\package_release.ps1" in build_script
    assert 'if exist "dist\\ECUProTune" rmdir /s /q "dist\\ECUProTune"' in build_script
    assert 'if exist dist rmdir /s /q dist' not in build_script
    assert "release/" in gitignore


def test_release_documentation_exists() -> None:
    guide = ROOT / "docs" / "RELEASE_PACKAGING.md"

    assert guide.is_file()
    assert "SHA256SUMS.txt" in guide.read_text(encoding="utf-8")



def test_windows_version_generator_writes_valid_pyinstaller_resource(tmp_path: Path) -> None:
    import subprocess
    import sys

    output = tmp_path / "windows_version_info.txt"
    script = ROOT / "scripts" / "generate_windows_version_info.py"
    result = subprocess.run(
        [sys.executable, str(script), "--output", str(output)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    generated = output.read_text(encoding="utf-8")
    assert "filevers=(0, 1, 0, 0)" in generated
    assert "prodvers=(0, 1, 0, 0)" in generated
    assert "StringStruct('FileVersion', '0.1.0.0')" in generated
    compile(generated, str(output), "exec")


def test_release_manifest_includes_windows_file_version() -> None:
    script = (ROOT / "scripts" / "package_release.ps1").read_text(encoding="utf-8")

    assert 'windows_file_version = "$version.0"' in script
