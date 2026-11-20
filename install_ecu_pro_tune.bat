@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================
echo        ECU PRO TUNE - INSTALLER
echo ============================================
echo.

where py >nul 2>&1
if errorlevel 1 goto :python_missing

py -3.11 --version >nul 2>&1
if errorlevel 1 goto :python311_missing

if exist ".venv\Scripts\python.exe" (
    echo [1/6] A validar ambiente virtual existente...
    .venv\Scripts\python.exe -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 11) else 1)"
    if errorlevel 1 goto :venv_incompatible
) else (
    echo [1/6] A criar ambiente virtual Python 3.11...
    py -3.11 -m venv .venv
    if errorlevel 1 goto :error
)

echo [2/6] A atualizar ferramentas pip...
.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
if errorlevel 1 goto :error

echo [3/6] A instalar dependencias...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo [4/6] A verificar consistencia das dependencias...
.venv\Scripts\python.exe -m pip check
if errorlevel 1 goto :error

echo [5/6] A validar imports da aplicacao...
.venv\Scripts\python.exe -c "import numpy, matplotlib, ttkbootstrap, pydub, PIL, playsound; from src.core.sound_manager import SoundManager; from src.app.dashboard import Dashboard; print('ECU PRO TUNE: dependencias e imports OK')"
if errorlevel 1 goto :error

echo [6/6] A verificar FFmpeg opcional...
where ffmpeg >nul 2>&1
if not errorlevel 1 goto :ffmpeg_found

echo [AVISO] FFmpeg nao encontrado.
echo A aplicacao GUI e os sons WAV de fallback continuam funcionais.
echo FFmpeg so e necessario para fluxos opcionais de conversao/geracao MP3.
if /I "%ECU_PRO_TUNE_CI%"=="1" goto :ffmpeg_skipped

where winget >nul 2>&1
if errorlevel 1 goto :ffmpeg_manual

set "INSTALL_FFMPEG=N"
set /p "INSTALL_FFMPEG=Queres tentar instalar FFmpeg com winget? (S/N): "
if /I not "%INSTALL_FFMPEG%"=="S" goto :ffmpeg_skipped

echo A instalar FFmpeg...
winget install --id Gyan.FFmpeg.Shared -e --accept-source-agreements --accept-package-agreements
if errorlevel 1 (
    echo [AVISO] A instalacao de FFmpeg falhou. A GUI continua funcional.
) else (
    echo FFmpeg instalado. Abre uma nova consola para atualizar o PATH.
)
goto :finished

:ffmpeg_found
echo FFmpeg encontrado.
goto :finished

:ffmpeg_manual
echo Winget nao disponivel. Podes instalar FFmpeg manualmente mais tarde.
goto :finished

:ffmpeg_skipped
echo Instalacao opcional de FFmpeg ignorada.
goto :finished

:python_missing
echo [ERRO] Python Launcher (py) nao encontrado.
echo Instala Python 3.11 e ativa a opcao Python Launcher.
goto :error

:python311_missing
echo [ERRO] Python 3.11 nao encontrado pelo launcher py.
echo Instala Python 3.11. Esta versao e a validada pelo projeto e pelo CI.
goto :error

:venv_incompatible
echo [ERRO] O ambiente .venv existente nao usa Python 3.11.
echo Renomeia ou remove manualmente a pasta .venv e volta a executar este instalador.
goto :error

:finished
echo.
echo Instalacao concluida.
echo Arranque: .venv\Scripts\python.exe -m src.app.main
echo Testes:   ecu_test.bat
if /I "%ECU_PRO_TUNE_CI%"=="1" exit /b 0
pause
exit /b 0

:error
echo.
echo [ERRO] A instalacao nao foi concluida.
if /I "%ECU_PRO_TUNE_CI%"=="1" exit /b 1
pause
exit /b 1
