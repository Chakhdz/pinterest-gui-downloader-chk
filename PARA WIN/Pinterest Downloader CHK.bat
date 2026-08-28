@echo off
setlocal
title Pinterest Downloader CHK
cd /d "%~dp0.."

rem OPEN the app (double-click this file). Not the installer.
rem cd to the repo root (parent of PARA WIN) so python finds pinterest_gui.py.
rem Busca un Python que funcione: primero "python", si no existe intenta
rem con el lanzador "py" que instala el instalador oficial de python.org.
where python >nul 2>nul
if %errorlevel%==0 (
    set "PYCMD=python"
) else (
    where py >nul 2>nul
    if %errorlevel%==0 (
        set "PYCMD=py"
    ) else (
        echo No se encontro Python instalado.
        echo.
        echo Without Python, download the Release exe:
        echo https://github.com/Chakhdz/pinterest-gui-downloader-chk/releases/tag/v1.0.0
        echo.
        echo Con Python: instala Python 3 desde https://www.python.org/downloads/windows/
        echo IMPORTANTE: en el instalador marca la casilla "Add python.exe to PATH".
        echo.
        echo Then double-click "Pinterest Downloader CHK.bat" to OPEN.
        echo "Install Pinterest Downloader CHK.bat" is the installer, run once.
        echo.
        pause
        exit /b 1
    )
)

%PYCMD% pinterest_gui.py
if errorlevel 1 (
    echo.
    echo Hubo un error al iniciar Pinterest Downloader CHK ^(ver arriba^).
    pause
)
