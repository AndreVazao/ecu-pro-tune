@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERRO] Executa install_ecu_pro_tune.bat primeiro.
    pause
    exit /b 1
)

.venv\Scripts\python.exe -m pip install pyinstaller
if errorlevel 1 goto :error

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --noconsole --name ECUProTune src\app\main.py
if errorlevel 1 goto :error

echo.
echo EXE criado em dist\ECUProTune\ECUProTune.exe
pause
exit /b 0

:error
echo.
echo [ERRO] Build falhou.
pause
exit /b 1
