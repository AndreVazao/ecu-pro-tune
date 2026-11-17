@echo off
setlocal EnableExtensions
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERRO] Executa install_ecu_pro_tune.bat primeiro.
    goto :error
)

.venv\Scripts\python.exe -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 11) else 1)"
if errorlevel 1 (
    echo [ERRO] O ambiente virtual tem de usar Python 3.11.
    goto :error
)

echo [1/4] A validar dependencias...
.venv\Scripts\python.exe -m pip check
if errorlevel 1 goto :error

echo [2/4] A instalar PyInstaller...
.venv\Scripts\python.exe -m pip install --upgrade pyinstaller
if errorlevel 1 goto :error

echo [3/4] A preparar build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [4/4] A construir ECUProTune.exe...
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --windowed --name ECUProTune --paths . --add-data "configs;configs" --add-data "maps;maps" --collect-all ttkbootstrap --collect-all matplotlib src\app\main.py
if errorlevel 1 goto :error

if not exist "dist\ECUProTune\ECUProTune.exe" (
    echo [ERRO] O executavel esperado nao foi criado.
    goto :error
)

echo.
echo EXE criado em dist\ECUProTune\ECUProTune.exe
echo Mantem a pasta ECUProTune completa, incluindo _internal.
pause
exit /b 0

:error
echo.
echo [ERRO] Build falhou.
pause
exit /b 1
