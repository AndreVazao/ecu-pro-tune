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
