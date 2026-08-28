# Pinterest Downloader CHK — Version Windows

This folder is **`PARA WIN`**. Mac users: open **`PARA MAC`**.

**Without Python:** download the Release exe https://github.com/Chakhdz/pinterest-gui-downloader-chk/releases/tag/v1.0.0

**With Python:** double-click `Pinterest Downloader CHK.bat` to **OPEN** the app.

`Install Pinterest Downloader CHK.bat` is the **installer** — run once.

Hay dos formas de usar la app en Windows. Elige una. Primero **abrir**; el instalador va despues.

## Abrir la app (doble click)

**Si ya tienes `Pinterest Downloader CHK.exe`:** doble click en **ese** archivo. Ese es el programa. No abras el instalador.

**Si ya tienes Python y todavia no hay .exe:** doble click en **`Pinterest Downloader CHK.bat`**. Abre la app directo usando Python, sin pasos extra. Si Python falta, el .bat te lo dice.

## Instalar una vez (genera el .exe)

`Install Pinterest Downloader CHK.bat` es el **INSTALADOR**, no la app. Se corre UNA VEZ en una PC con Windows (no se puede generar un .exe de Windows desde Mac/Linux). El proceso es automatico, solo toma un par de minutos:

1. Instala Python 3 (ver "Requisito" mas abajo) si no lo tienes.
2. Haz doble click en **`Install Pinterest Downloader CHK.bat`**. Va a instalar lo que
   falte y generar el archivo.
3. Cuando termine, va a quedar **`Pinterest Downloader CHK.exe`** en esta misma
   carpeta. Ese es el ejecutable final: doble click para **abrir** la app.
   Ya no depende de que el instalador se vuelva a correr.
4. (Opcional) borra las carpetas `build` y `dist` (basura del compilador
   en la raiz del repo, no son la app) y el `.spec` que quedan del proceso;
   no se necesitan para usar el .exe.

Si Windows Defender/SmartScreen se queja la primera vez que abres el .exe
("Windows protegio tu PC"), es normal en ejecutables nuevos sin firma
digital: dale a "Mas informacion" y luego "Ejecutar de todas formas".

## Requisito para instalar (y para el .bat): tener Python instalado

1. Ve a https://www.python.org/downloads/windows/ y descarga el instalador
   de Python 3 (version 3.9 o mas nueva).
2. Al ejecutar el instalador, **marca la casilla "Add python.exe to PATH"**
   antes de darle a Install. Si no la marcas, Windows no va a encontrar el
   comando `python` despues.
3. Deja las opciones por defecto (el instalador oficial ya incluye Tkinter,
   que es lo que usa la ventana de la app).

Nota: una vez que generas `Pinterest Downloader CHK.exe`, ese .exe ya trae
todo empaquetado — Python solo hace falta para generarlo, no para usarlo
despues.

## Primera vez usando la app

Si es la primera vez, la app puede mostrar un aviso amarillo arriba
pidiendo instalar `pinterest-dl`:
- En **`Pinterest Downloader CHK.bat`**: dale click a "Instalar pinterest-dl" y espera
  a que termine (una sola vez).
- En **`Pinterest Downloader CHK.exe`**: no deberia aparecer (ya viene incluido), pero
  si aparece, vuelve a correr **una vez** `Install Pinterest Downloader CHK.bat`.

## Si algo no abre

- Si aparece "No se encontro Python instalado", descarga el exe de
  [Releases v1.0.0](https://github.com/Chakhdz/pinterest-gui-downloader-chk/releases/tag/v1.0.0),
  o revisa el paso de Requisito de arriba (falta marcar "Add python.exe to PATH").
- Tambien puedes abrir la app a mano: abre "Simbolo del sistema" (cmd) en
  la raiz del repo (la carpeta padre de `PARA WIN`) y escribe:

      python pinterest_gui.py

## Notas

- Todo lo demas (elegir carpeta, pegar el link, opciones, cookies para
  tableros privados) funciona igual que en Mac.
- "Abrir carpeta de destino" al terminar usa el explorador de archivos de
  Windows automaticamente.
