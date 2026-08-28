@echo off
setlocal
title Pinterest Downloader CHK
cd /d "%~dp0"

rem OPEN the app (double-click this file). Not the installer.
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
        echo Instala Python 3 desde https://www.python.org/downloads/windows/
        echo IMPORTANTE: en el instalador marca la casilla "Add python.exe to PATH".
        echo.
        echo Or run "Install Pinterest Downloader CHK.bat" once to generate
        echo "Pinterest Downloader CHK.exe", then open that .exe.
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
