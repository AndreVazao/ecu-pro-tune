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

The Windows CI runs the same packaging script and independently checks the archive hash before uploading the artifact.

## Distribution scope

This is a portable onedir package, not an MSI installer. It requires no FFmpeg for the GUI or WAV fallback sounds. Do not describe it as an ECU flashing tool: the application remains in simulation/visualization mode and has no physical ECU write path.
