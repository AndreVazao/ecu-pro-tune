@echo off
setlocal EnableExtensions
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERRO] Ambiente virtual inexistente.
    echo Executa install_ecu_pro_tune.bat primeiro.
    goto :fail
)

.venv\Scripts\python.exe -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 11) else 1)"
if errorlevel 1 (
    echo [ERRO] O ambiente virtual tem de usar Python 3.11.
    goto :fail
)

echo [1/3] A verificar dependencias...
.venv\Scripts\python.exe -m pip check
if errorlevel 1 goto :fail

echo [2/3] A compilar modulos...
.venv\Scripts\python.exe -m compileall -q src tests
if errorlevel 1 goto :fail

echo [3/3] A executar testes...
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
