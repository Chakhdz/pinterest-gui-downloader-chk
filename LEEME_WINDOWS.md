# Pinterest Downloader — Version Windows

Hay dos formas de usar la app en Windows. Elige una.

## Opcion A — Ejecutable de verdad (PINDOWNLOADER.exe)

Esto genera un solo archivo .exe que puedes usar (o mandarle a alguien mas
en la misma carpeta) sin escribir nada en una terminal despues.

**Importante:** el .exe hay que generarlo UNA VEZ en una PC con Windows (no
se puede generar un .exe de Windows desde Mac/Linux, ni yo puedo generarlo
por ti sin una maquina Windows a la mano). El proceso es automatico, solo
toma un par de minutos:

1. Instala Python 3 (ver "Requisito" mas abajo) si no lo tienes.
2. Haz doble click en **`build_windows_exe.bat`**. Va a instalar lo que
   falte y generar el archivo.
3. Cuando termine, va a quedar **`PINDOWNLOADER.exe`** en esta misma
   carpeta. Ese es el ejecutable final: doble click para abrir la app,
   ya no depende de que build_windows_exe.bat se vuelva a correr.
4. (Opcional) borra las carpetas `build`, `dist` y el archivo
   `PINDOWNLOADER.spec` que quedan del proceso; no se necesitan para usar
   el .exe.

Si Windows Defender/SmartScreen se queja la primera vez que abres el .exe
("Windows protegio tu PC"), es normal en ejecutables nuevos sin firma
digital: dale a "Mas informacion" y luego "Ejecutar de todas formas".

## Opcion B — Sin generar .exe (mas simple, requiere Python instalado)

Doble click en **`PINDOWNLOADER.bat`**. Abre la app directo usando Python,
sin pasos extra. Es la opcion mas facil si no te interesa tener un .exe
para compartir.

## Requisito para ambas opciones: tener Python instalado

1. Ve a https://www.python.org/downloads/windows/ y descarga el instalador
   de Python 3 (version 3.9 o mas nueva).
2. Al ejecutar el instalador, **marca la casilla "Add python.exe to PATH"**
   antes de darle a Install. Si no la marcas, Windows no va a encontrar el
   comando `python` despues.
3. Deja las opciones por defecto (el instalador oficial ya incluye Tkinter,
   que es lo que usa la ventana de la app).

Nota: una vez que generas `PINDOWNLOADER.exe` (Opcion A), ese .exe ya trae
todo empaquetado — Python solo hace falta para generarlo, no para usarlo
despues.

## Primera vez usando la app

Si es la primera vez, la app puede mostrar un aviso amarillo arriba
pidiendo instalar `pinterest-dl`:
- En **PINDOWNLOADER.bat**: dale click a "Instalar pinterest-dl" y espera
  a que termine (una sola vez).
- En **PINDOWNLOADER.exe**: no deberia aparecer (ya viene incluido), pero
  si aparece, vuelve a generar el .exe con `build_windows_exe.bat`.

## Si algo no abre

- Si aparece "No se encontro Python instalado", revisa el paso de
  Requisito de arriba (falta marcar "Add python.exe to PATH").
- Tambien puedes abrir la app a mano: abre "Simbolo del sistema" (cmd) en
  esta carpeta y escribe:

      python pinterest_gui.py

## Notas

- Todo lo demas (elegir carpeta, pegar el link, opciones, cookies para
  tableros privados) funciona igual que en Mac.
- "Abrir carpeta de destino" al terminar usa el explorador de archivos de
  Windows automaticamente.
