@echo off
setlocal
title Generando PINDOWNLOADER.exe
cd /d "%~dp0"

echo ============================================================
echo   Generador del ejecutable de Pinterest Downloader (Windows)
echo ============================================================
echo.
echo Este script se ejecuta UNA SOLA VEZ (o cuando quieras actualizar
echo la app) y deja un archivo PINDOWNLOADER.exe en esta carpeta.
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
    --name PINDOWNLOADER ^
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
echo [3/3] Copiando PINDOWNLOADER.exe a esta carpeta...
copy /y "dist\PINDOWNLOADER.exe" "PINDOWNLOADER.exe" >nul

echo.
echo ============================================================
echo   Listo. Ya puedes usar PINDOWNLOADER.exe (doble click).
echo   Puedes borrar las carpetas "build" y "dist" y el archivo
echo   PINDOWNLOADER.spec si quieres dejar la carpeta mas limpia.
echo ============================================================
echo.
pause
