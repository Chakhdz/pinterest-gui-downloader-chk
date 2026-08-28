# Pinterest Downloader CHK — Version Windows

Los nombres de archivo SON los pasos.

1. Si no tienes Python: doble click **`1. Instalar (si no tienes Python).bat`**
2. El programa es **`Pinterest Downloader CHK.exe`**
3. Reconstruir solo si ya tienes Python: **`3. Reconstruir (solo si ya tienes Python).bat`**

Mac: carpeta **`PARA MAC`**, doble click `1. Abrir Pinterest Downloader CHK.command`.

## 1. Instalar (sin Python)

`1. Instalar (si no tienes Python).bat` NO necesita Python. Abre `Pinterest Downloader CHK.exe` que ya esta en esta carpeta.

Si Windows Defender/SmartScreen se queja ("Windows protegio tu PC"): "Mas informacion" y luego "Ejecutar de todas formas".

## 2. El programa

`Pinterest Downloader CHK.exe` es la app. Doble click en ese archivo, o usa el bat del paso 1.

## 3. Reconstruir (solo si ya tienes Python)

`3. Reconstruir (solo si ya tienes Python).bat` NO es el paso 1. Necesita Python. Genera de nuevo `Pinterest Downloader CHK.exe` en esta carpeta.

1. Instala Python 3 (ver Requisito) si no lo tienes.
2. Doble click en **`3. Reconstruir (solo si ya tienes Python).bat`**.
3. Cuando termine, usa de nuevo el **`.exe`** o el bat **`1.`**.
4. (Opcional) borra `build`, `dist` y el `.spec` en la raiz del repo.

## Requisito para el 3: Python instalado

1. https://www.python.org/downloads/windows/ (Python 3.9 o mas nueva).
2. Marca **"Add python.exe to PATH"**.
3. Deja las opciones por defecto (incluye Tkinter).

El .exe del paso 2 ya trae todo empaquetado.

## Si algo no abre

- Sin Python: usa **`1. Instalar (si no tienes Python).bat`** o **`Pinterest Downloader CHK.exe`**.
- A mano, en la raiz del repo (padre de `PARA WIN`):

      python pinterest_gui.py
