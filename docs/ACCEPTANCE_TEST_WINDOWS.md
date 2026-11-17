# Windows manual acceptance plan — ECU Pro Tune 0.1.0

## Purpose

This plan covers the user-machine checks that GitHub Actions cannot fully replace. The automated Windows CI validates imports, tests, Tk construction, packaging and a short executable startup. It does not validate prolonged interactive use on every Windows installation.

## Test environment

- Windows 10 or Windows 11, x64.
- Python 3.11 x64 and Python Launcher.
- ECU Pro Tune repository checkout or the versioned release ZIP.
- No ECU hardware connection is required. Keep all checks in simulation mode.
- FFmpeg may be absent; it is optional.

## Acceptance cases

1. **Clean installation**
   - Start without an existing .venv.
   - Run install_ecu_pro_tune.bat.
   - Expected: Python 3.11 virtual environment created, dependencies installed, pip check passes, application imports validate.

2. **Incompatible existing virtual environment**
   - Use an existing .venv created with a Python version other than 3.11.
   - Run the installer.
   - Expected: clear error; existing .venv is not deleted or overwritten.

3. **FFmpeg absent**
   - Ensure FFmpeg is not on PATH and answer N to the optional winget prompt.
   - Expected: installation completes; GUI and WAV fallback audio remain functional.

4. **Application launch and version**
   - Launch with .venv\Scripts\python.exe -m src.app.main.
   - Expected: main window opens and title shows ECU Pro Tune v0.1.0.

5. **Dashboard simulation**
   - Start and stop the dashboard simulation several times.
   - Expected: RPM, boost, load, temperature, lambda, gauges and graph update while running and stop cleanly.
   - Expected: no physical ECU connection or write operation is attempted.

6. **Navigation**
   - Navigate from dashboard to Profiles/Maps and return.
   - Expected: screens render, controls remain responsive, and no exception is shown.

7. **Profile and map validation**
   - Load the sample Stage 1 profile and inspect its map.
   - Try a valid numeric map value and an out-of-range value.
   - Expected: valid values are accepted; invalid values are rejected with a useful validation message.

8. **Backup and restore**
   - Create a profile backup, change the profile, then restore the backup.
   - Expected: restored JSON matches the backup content.

9. **Automated test launcher**
   - Run ecu_test.bat.
   - Expected: Python 3.11 check, pip check, compileall and pytest all pass.

10. **Local executable build**
    - Run build_exe.bat.
    - Expected: dist\ECUProTune\ECUProTune.exe and the versioned release ZIP are created.
    - Expected: unrelated content under dist is preserved.

11. **Executable file properties**
    - Run:
      
          (Get-Item .\dist\ECUProTune\ECUProTune.exe).VersionInfo | Format-List FileVersion,ProductVersion

    - Expected: FileVersion and ProductVersion both show 0.1.0.0.

12. **Release ZIP extraction**
    - Extract ECUProTune-Windows-Python311-v0.1.0.zip into a directory whose path contains spaces.
    - Launch ECUProTune\ECUProTune.exe from the extracted folder.
    - Expected: application opens with the _internal directory alongside the EXE.

13. **Release integrity**
    - Compare the ZIP hash with SHA256SUMS.txt and the sha256 field in BUILD-MANIFEST.json.
    - Expected: hashes match exactly.

14. **Safety boundary**
    - Confirm the application remains in simulation/visualization mode.
    - Expected: no ECU flash, physical write, or hardware programming control is present.

## Result recording

For each case, record PASS/FAIL, Windows edition/build, CPU architecture, Python version, date, and any error output. Do not mark the release as manually accepted until these checks have actually been run on a Windows user machine.
