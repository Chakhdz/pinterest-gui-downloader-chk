# Pinterest Downloader CHK — Version Windows

Los nombres de archivo SON los pasos. Windows Explorer los ordena por numero.

1. Si no tienes Python: doble click **`1. Instalar (si no tienes Python).exe`**
2. Si ya tienes Python: doble click **`2. Ejecutable - Pinterest Downloader CHK.bat`**
3. Solo si ya tienes Python y quieres reconstruir: **`3. Reconstruir (solo si ya tienes Python).bat`**

Mac: carpeta **`PARA MAC`**, doble click `1. Abrir Pinterest Downloader CHK.command`.

## 1. El .exe (sin Python)

`1. Instalar (si no tienes Python).exe` ya viene en esta carpeta. Doble click. No hace falta Python ni Releases.

Si Windows Defender/SmartScreen se queja ("Windows protegio tu PC"): "Mas informacion" y luego "Ejecutar de todas formas".

## 2. El .bat (si ya tienes Python)

`2. Ejecutable - Pinterest Downloader CHK.bat` abre la app con Python. Si Python falta, te dice que uses el paso 1.

## 3. Reconstruir (solo si ya tienes Python)

`3. Reconstruir (solo si ya tienes Python).bat` NO es el paso 1. Necesita Python. Genera de nuevo el .exe y lo deja como `1. Instalar (si no tienes Python).exe`.

1. Instala Python 3 (ver Requisito) si no lo tienes.
2. Doble click en **`3. Reconstruir (solo si ya tienes Python).bat`**.
3. Cuando termine, usa de nuevo el archivo **`1.`**.
4. (Opcional) borra `build`, `dist` y el `.spec` en la raiz del repo.

## Requisito para el .bat 2 y el 3: Python instalado

1. https://www.python.org/downloads/windows/ (Python 3.9 o mas nueva).
2. Marca **"Add python.exe to PATH"**.
3. Deja las opciones por defecto (incluye Tkinter).

El .exe del paso 1 ya trae todo empaquetado.

## Primera vez

Si la app pide `pinterest-dl`:
- En el **`.bat` 2**: click "Instalar pinterest-dl" una vez.
- En el **`.exe` 1**: no deberia aparecer. Si aparece, corre el **3** una vez (necesita Python).

## Si algo no abre

- Sin Python: usa **`1. Instalar (si no tienes Python).exe`**.
- A mano, en la raiz del repo (padre de `PARA WIN`):

      python pinterest_gui.py
