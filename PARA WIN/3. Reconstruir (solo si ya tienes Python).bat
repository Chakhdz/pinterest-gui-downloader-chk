@echo off
setlocal EnableDelayedExpansion
title Reconstruir Pinterest Downloader CHK
cd /d "%~dp0.."

echo ============================================================
echo   3. RECONSTRUIR. Solo si YA tienes Python.
echo   Si no tienes Python, cierra esto y abre
echo   "1. Instalar (si no tienes Python).bat"
echo ============================================================
echo.
echo Este script se ejecuta UNA SOLA VEZ (o cuando quieras
echo actualizar). Genera de nuevo el .exe en PARA WIN.
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
        echo Si no tienes Python, doble click en
        echo "1. Instalar (si no tienes Python).bat"
        echo.
        pause
        exit /b 1
    )
)

echo [1/3] Instalando/actualizando pyinstaller, pillow y pinterest-dl...
%PYCMD% -m pip install --upgrade pip pyinstaller pillow pinterest-dl
if errorlevel 1 (
    echo.
    echo Fallo la instalacion de dependencias. Revisa tu conexion a internet.
    pause
    exit /b 1
)

set "ICON_ARGS="
if exist icon.png (
    echo Convirtiendo icon.png a icon.ico...
    %PYCMD% -c "from PIL import Image; im=Image.open('icon.png').convert('RGBA'); im.save('icon.ico', format='ICO', sizes=[(256,256),(128,128),(64,64),(48,48),(32,32),(16,16)])"
    if exist icon.ico set "ICON_ARGS=--icon icon.ico"
)

echo.
echo [2/3] Generando el ejecutable (puede tardar 1-2 minutos)...
%PYCMD% -m PyInstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "Pinterest Downloader CHK" ^
    %ICON_ARGS% ^
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
echo [3/3] Copiando el .exe a "PARA WIN\Pinterest Downloader CHK.exe"...
copy /y "dist\Pinterest Downloader CHK.exe" "PARA WIN\Pinterest Downloader CHK.exe" >nul

echo.
echo ============================================================
echo   Listo. Para ABRIR: doble click
echo   "1. Instalar (si no tienes Python).bat"
echo   o "Pinterest Downloader CHK.exe"
echo   Puedes borrar las carpetas "build" y "dist" (compiler junk)
echo   y el .spec / icon.ico en la raiz del repo.
echo ============================================================
echo.
pause
