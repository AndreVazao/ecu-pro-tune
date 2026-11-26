# Changelog

All notable changes to ECU Pro Tune are recorded here.

## Unreleased

### Dashboard
- Plot RPM and engine load as separate, explicitly scaled series (RPM left axis, load percentage right axis).
- Correct the rolling history label to a 36-second nominal window (90 samples at 400 ms) and expose the sampling cadence.

## 0.1.0 — 2026-11-17

### Added
- Desktop GUI with Performance and Showcase modes.
- Advanced simulation dashboard with RPM, boost, load, coolant temperature, lambda and simulated output metrics.
- Rolling RPM graph, RPM/boost gauges and local system monitor.
- Profile and map management, numeric map editor, validation and graph visualization.
- Profile backup and rollback services.
- Persistent scheduler with validated JSON storage and cancelable shutdown.
- Sound manager with MP3 support when available and WAV fallback cues.
- Versioned Windows onedir packaging with release manifest and SHA-256 checksum.
- Windows executable FileVersion/ProductVersion metadata generated from VERSION.
- Windows CI for tests, Tk construction, PyInstaller, executable startup, version metadata, release packaging and checksum verification.

### Validation
- Windows / Python 3.11 CI.
- 42 automated tests passed in the latest PR validation.
- PyInstaller executable built and started successfully in the CI smoke test.
- Release ZIP created and SHA-256 verified by CI.

### Limitations
- Simulation and visualization only.
- No physical ECU telemetry, flashing driver, ECU write path or hardware programming.
- Manual acceptance testing on a user Windows machine remains outstanding.
- FFmpeg is optional and not required for GUI startup or WAV fallback audio.
