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

    assert "Generate Windows executable version metadata" in workflow
    assert "--version-file build/windows_version_info.txt" in workflow
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


def test_windows_ci_verifies_embedded_executable_file_and_product_versions() -> None:
    workflow = (ROOT / ".github" / "workflows" / "windows-ci.yml").read_text(
        encoding="utf-8"
    )

    assert "Verify Windows executable version metadata" in workflow
    assert '$expectedVersion = "$version.0"' in workflow
    assert "$versionInfo.FileVersion" in workflow
    assert "$versionInfo.ProductVersion" in workflow



def test_release_verifier_checks_manifest_hash_checksum_and_zip_layout() -> None:
    script = (ROOT / "scripts" / "verify_release.ps1").read_text(encoding="utf-8")

    assert "BUILD-MANIFEST.json" in script
    assert "SHA256SUMS.txt" in script
    assert "Get-FileHash" in script
    assert "archive_size_bytes" in script
    assert "windows_file_version" in script
    assert "ECUProTune/ECUProTune.exe" in script
    assert "ECUProTune/_internal/*" in script
    assert "zip.Dispose()" in script
    assert "actualHash -ne $manifest.sha256" in script


def test_windows_ci_runs_independent_release_verification_before_upload() -> None:
    workflow = (ROOT / ".github" / "workflows" / "windows-ci.yml").read_text(
        encoding="utf-8"
    )

    verify_position = workflow.index("Independently verify release archive")
    upload_position = workflow.index("Upload Windows build")

    assert "verify_release.ps1" in workflow
    assert verify_position < upload_position



def test_release_verifier_rejects_zip_slip_and_duplicate_entries() -> None:
    script = (ROOT / "scripts" / "verify_release.ps1").read_text(encoding="utf-8")

    assert 'StartsWith("/")' in script
    assert "entryName -match '(^|/)\\.\\.(/|$)'" in script
    assert "seenEntries.ContainsKey($entryName)" in script
    assert 'entryName -notlike "ECUProTune/*"' in script
    assert '$executableEntry.Length -le 0' in script
    assert '$internalFiles.Count -eq 0' in script



def test_windows_acceptance_recorder_captures_all_fourteen_cases() -> None:
    script = (ROOT / "scripts" / "record_windows_acceptance.ps1").read_text(
        encoding="utf-8"
    )
    plan = (ROOT / "docs" / "ACCEPTANCE_TEST_WINDOWS.md").read_text(
        encoding="utf-8"
    )

    assert script.count("@{ id = ") == 14
    assert "PASS" in script and "FAIL" in script and "SKIP" in script
    assert "overall_result = $overall" in script
    assert "recorded_at_utc" in script
    assert "os_build = $os.BuildNumber" in script
    assert "python_311 = $python311" in script
    assert "ECUProTune-Acceptance-$timestamp.json" in script
    assert "14." in plan



def test_windows_acceptance_recorder_uses_collision_resistant_report_names() -> None:
    script = (ROOT / "scripts" / "record_windows_acceptance.ps1").read_text(
        encoding="utf-8"
    )

    assert 'ToString("yyyyMMdd-HHmmss-fff")' in script
    assert "while (Test-Path -LiteralPath $reportPath)" in script
    assert "Set-Content -LiteralPath $reportPath" in script


def test_windows_acceptance_validator_checks_all_cases_and_recomputed_totals() -> None:
    script = (ROOT / "scripts" / "validate_windows_acceptance.ps1").read_text(
        encoding="utf-8"
    )

    assert "schema_version" in script
    assert "recorded_at_utc" in script
    assert "expectedCases.Count" in script
    assert "seenIds.ContainsKey($caseId)" in script
    assert "Os totais do" in script
    assert "expectedOverall" in script
    assert "RequirePass" in script
    assert 'exit 2' in script


def test_acceptance_documentation_explains_report_validation_gate() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    plan = (ROOT / "docs" / "ACCEPTANCE_TEST_WINDOWS.md").read_text(
        encoding="utf-8"
    )

    assert "validate_windows_acceptance.ps1" in readme
    assert "validate_windows_acceptance.ps1" in plan
    assert "-RequirePass" in plan



def test_windows_ci_executes_powerShell_acceptance_validator_integration_suite() -> None:
    workflow = (ROOT / ".github" / "workflows" / "windows-ci.yml").read_text(
        encoding="utf-8"
    )
    harness = ROOT / "tests" / "test_windows_acceptance_validator.ps1"
    harness_text = harness.read_text(encoding="utf-8")

    assert "Validate PowerShell scripts and acceptance report gate" in workflow
    assert "test_windows_acceptance_validator.ps1" in workflow
    assert harness.is_file()
    assert "Parser]::ParseFile" in harness_text
    assert "valid 14/14 report accepted" in harness_text
    assert "RequirePass" in harness_text
    assert "duplicate case IDs are rejected" in harness_text
    assert "inconsistent totals are rejected" in harness_text



def test_windows_installer_supports_noninteractive_ci_mode() -> None:
    installer = (ROOT / "install_ecu_pro_tune.bat").read_text(encoding="utf-8")

    assert 'if /I "%ECU_PRO_TUNE_CI%"=="1" goto :ffmpeg_skipped' in installer
    assert 'if /I "%ECU_PRO_TUNE_CI%"=="1" exit /b 0' in installer
    assert 'if /I "%ECU_PRO_TUNE_CI%"=="1" exit /b 1' in installer
    assert "winget install" in installer


def test_windows_ci_executes_clean_installer_and_checks_venv_imports() -> None:
    workflow = (ROOT / ".github" / "workflows" / "windows-ci.yml").read_text(
        encoding="utf-8"
    )

    assert "Smoke test Windows installer" in workflow
    assert "ECU_PRO_TUNE_CI: " in workflow
    assert "cmd /c install_ecu_pro_tune.bat" in workflow
    assert r".\.venv\Scripts\python.exe" in workflow
    assert "sys.version_info[:2] == (3, 11)" in workflow
    assert "Installed virtual environment smoke test: OK" in workflow



def test_release_readiness_gate_matches_report_version_and_runs_both_validators() -> None:
    script = (ROOT / "scripts" / "check_release_readiness.ps1").read_text(
        encoding="utf-8"
    )
    parser_harness = (ROOT / "tests" / "test_windows_acceptance_validator.ps1").read_text(
        encoding="utf-8"
    )

    assert "BUILD-MANIFEST.json" in script
    assert "application_version" in script
    assert "manifest.version" in script
    assert "verify_release.ps1" in script
    assert "validate_windows_acceptance.ps1" in script
    assert "-RequirePass" in script
    assert "RELEASE READY" in script
    assert "check_release_readiness.ps1" in parser_harness
