@echo off
setlocal
title Pinterest Downloader CHK
cd /d "%~dp0.."

rem 2. OPEN the app if you already have Python. Not step 1.
rem cd to the repo root (parent of PARA WIN) so python finds pinterest_gui.py.
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
        echo Doble click en:
        echo "1. Instalar (si no tienes Python).exe"
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
