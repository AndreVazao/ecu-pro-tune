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

echo [1/5] A validar dependencias...
.venv\Scripts\python.exe -m pip check
if errorlevel 1 goto :error

echo [2/5] A instalar PyInstaller...
.venv\Scripts\python.exe -m pip install --upgrade pyinstaller
if errorlevel 1 goto :error

echo [3/5] A preparar build...
if exist "build\ECUProTune" rmdir /s /q "build\ECUProTune"
if exist "dist\ECUProTune" rmdir /s /q "dist\ECUProTune"

echo [4/6] A gerar metadados de versao Windows...
.venv\Scripts\python.exe scripts\generate_windows_version_info.py
if errorlevel 1 goto :error

echo [5/6] A construir ECUProTune.exe...
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --windowed --name ECUProTune --version-file build\windows_version_info.txt --paths . --add-data "configs;configs" --add-data "maps;maps" --collect-all ttkbootstrap --collect-all matplotlib src\app\main.py
if errorlevel 1 goto :error

if not exist "dist\ECUProTune\ECUProTune.exe" (
    echo [ERRO] O executavel esperado nao foi criado.
    goto :error
)

echo.
echo [6/6] A empacotar release e SHA-256...
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\package_release.ps1 -SourceDirectory dist\ECUProTune -OutputDirectory release
if errorlevel 1 goto :error

echo EXE criado em dist\ECUProTune\ECUProTune.exe
echo Pacote versionado e manifesto criados em release\
echo Mantem a pasta ECUProTune completa, incluindo _internal.
pause
exit /b 0

:error
echo.
echo [ERRO] Build falhou.
pause
exit /b 1
