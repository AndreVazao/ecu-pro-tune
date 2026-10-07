@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERRO] Ambiente virtual inexistente.
    echo Executa install_ecu_pro_tune.bat primeiro.
    pause
    exit /b 1
)

.venv\Scripts\python.exe -m compileall -q src
if errorlevel 1 goto :fail

.venv\Scripts\python.exe -m pytest -q tests
if errorlevel 1 goto :fail

echo.
echo ECU PRO TUNE TESTS: PASS
pause
exit /b 0

:fail
echo.
echo ECU PRO TUNE TESTS: FAIL
pause
exit /b 1
