# Windows release packaging

## Version

The current application version is stored in VERSION and exposed through src.version. Update both together when preparing a new release; the automated test verifies they match.

## Build

1. Use the validated Python 3.11 environment.
2. Run build_exe.bat, or build the PyInstaller onedir package through Windows CI.
3. The release packager reads VERSION, validates ECUProTune.exe, creates a versioned ZIP and writes a manifest and SHA-256 checksum.

The output directory contains:

- ECUProTune-Windows-Python311-v0.1.0.zip
- BUILD-MANIFEST.json
- SHA256SUMS.txt

The ZIP includes the full ECUProTune onedir directory. Extract the archive without separating ECUProTune.exe from its _internal folder.

## Verify integrity

In PowerShell, from the repository root:

    Get-FileHash .\release\ECUProTune-Windows-Python311-v0.1.0.zip -Algorithm SHA256

Compare the result with SHA256SUMS.txt and the sha256 field in BUILD-MANIFEST.json.

The Windows CI runs the same packaging script, independently checks the archive hash, and reads the executable VersionInfo to assert FileVersion and ProductVersion match VERSION before uploading the artifact.

## Distribution scope

This is a portable onedir package, not an MSI installer. It requires no FFmpeg for the GUI or WAV fallback sounds. Do not describe it as an ECU flashing tool: the application remains in simulation/visualization mode and has no physical ECU write path.


## Independent package verification

After generating or extracting the release output directory, run:

    powershell -NoProfile -ExecutionPolicy Bypass -File scripts\verify_release.ps1 -ReleaseDirectory release

The verifier checks the product/version/platform metadata, expected ZIP filename, archive size, SHA-256 in both the manifest and checksum file, and the required onedir executable plus _internal contents inside the ZIP. It also rejects absolute paths, parent-directory traversal, entries outside ECUProTune/, and duplicate ZIP entries before the archive is trusted. Windows CI runs this independent verifier before uploading the artifact.

The verifier is intended for a release output directory containing the ZIP, BUILD-MANIFEST.json and SHA256SUMS.txt. It does not replace the manual GUI acceptance plan.
