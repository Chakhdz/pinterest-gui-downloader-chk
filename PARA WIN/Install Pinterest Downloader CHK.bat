@echo off
setlocal
title Installing Pinterest Downloader CHK
cd /d "%~dp0.."

echo ============================================================
echo   This file INSTALLS. Run it ONCE.
echo   To OPEN the app afterwards, double-click
echo   "PARA WIN\Pinterest Downloader CHK.exe" - not this bat.
echo ============================================================
echo.
echo Este instalador se ejecuta UNA SOLA VEZ (o cuando quieras
echo actualizar la app). Genera "Pinterest Downloader CHK.exe"
echo en la carpeta PARA WIN. Despues de instalar, abre ESE .exe.
echo Requiere conexion a internet (descarga pyinstaller y pinterest-dl).
echo.

where python >nul 2>nul
if %errorlevel%==0 (
    set "PYCMD=python"
) else (
    where py >nul 2>nul
    if %errorlevel%==0 (
        set "PYCMD=py"
    ) else (
        echo No se encontro Python instalado.
        echo Instala Python 3 desde https://www.python.org/downloads/windows/
        echo IMPORTANTE: marca "Add python.exe to PATH" en el instalador.
        echo.
        pause
        exit /b 1
    )
)

echo [1/3] Instalando/actualizando pyinstaller y pinterest-dl...
%PYCMD% -m pip install --upgrade pip pyinstaller pinterest-dl
if errorlevel 1 (
    echo.
    echo Fallo la instalacion de dependencias. Revisa tu conexion a internet.
    pause
    exit /b 1
)

echo.
echo [2/3] Generando el ejecutable (puede tardar 1-2 minutos)...
%PYCMD% -m PyInstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "Pinterest Downloader CHK" ^
    --collect-all pinterest_dl ^
    --collect-all m3u8 ^
    pinterest_gui.py
if errorlevel 1 (
    echo.
    echo Fallo la generacion del .exe. Revisa el mensaje de error de arriba.
    pause
    exit /b 1
)

echo.
echo [3/3] Copiando "Pinterest Downloader CHK.exe" a "PARA WIN"...
copy /y "dist\Pinterest Downloader CHK.exe" "PARA WIN\Pinterest Downloader CHK.exe" >nul

echo.
echo ============================================================
echo   Listo. To OPEN the app, double-click
echo   "PARA WIN\Pinterest Downloader CHK.exe" - not this installer.
echo   Puedes borrar las carpetas "build" y "dist" (compiler junk,
echo   not the app) y el .spec si quieres dejar la carpeta mas limpia.
echo ============================================================
echo.
pause
