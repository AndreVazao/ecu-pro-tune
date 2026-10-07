@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================
echo        ECU PRO TUNE - INSTALLER
echo ============================================

where py >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado no PATH.
    echo Instala Python 3.12+ e ativa Add Python to PATH.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo [1/5] A criar ambiente virtual...
    py -3 -m venv .venv
    if errorlevel 1 goto :error
)

echo [2/5] A atualizar pip...
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto :error

echo [3/5] A instalar dependencias...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo [4/5] A validar Python e bibliotecas...
.venv\Scripts\python.exe -c "import numpy, matplotlib, ttkbootstrap, pydub, PIL, playsound; print('ECU PRO TUNE: dependencias OK')"
if errorlevel 1 goto :error

echo [5/5] A verificar FFmpeg...
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo [AVISO] FFmpeg nao encontrado. A aplicacao GUI continua funcional.
    echo O gerador de MP3 necessita de FFmpeg.
    where winget >nul 2>&1
    if not errorlevel 1 (
        echo A tentar instalar FFmpeg via winget...
        winget install --id Gyan.FFmpeg.Shared -e --accept-source-agreements --accept-package-agreements
    ) else (
        echo Winget nao disponivel. Instala FFmpeg manualmente para gerar MP3.
    )
) else (
    echo FFmpeg encontrado.
)

echo.
echo Instalacao concluida.
echo Arranque: .venv\Scripts\python.exe -m src.app.main
pause
exit /b 0

:error
echo.
echo [ERRO] A instalacao falhou.
pause
exit /b 1
