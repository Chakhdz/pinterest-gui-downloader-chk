#!/usr/bin/env python3
"""
Pinterest Downloader - Interfaz gráfica tipo asistente (wizard)
Un paso a la vez: Link -> Carpeta -> Opciones -> Descargar -> Resultado.
Ventana que llama a la librería "pinterest-dl" (pip install pinterest-dl) por detrás.

Único archivo que hay que abrir: "PINDOWNLOADER.command" (o el .command que
tengas) o "python3 pinterest_gui.py". Esta ventana hace todo lo demás: instala
lo que falte, descarga, cuenta y renombra los archivos.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from urllib.parse import urlparse

# FROZEN = True cuando esto corre como .exe compilado con PyInstaller (en vez
# de "python3 pinterest_gui.py" normal). Importa para dos cosas:
#  1) __file__ dentro de un .exe apunta a una carpeta temporal de
#     descompresion, no a donde esta el .exe de verdad -> hay que usar
#     sys.executable para saber la carpeta real (donde el usuario espera
#     encontrar la carpeta "images" y el archivo de configuracion).
#  2) Un .exe empaquetado no trae un "python.exe" de proposito general
#     adentro: sys.executable ES el propio .exe, asi que "sys.executable -m
#     pinterest_dl.cli" no funciona. En su lugar el propio .exe se
#     relanza a si mismo con la bandera --pinterest-dl-cli (ver el bloque
#     __main__ al final del archivo).
FROZEN = getattr(sys, "frozen", False)
SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.executable if FROZEN else __file__))
DEFAULT_DEST = os.path.join(SCRIPT_DIR, "images")

# Fuente monoespaciada para la consola de detalles: "Menlo" solo existe en
# macOS. En Windows Tk no la tiene y cae en una fuente generica que puede
# verse mal, asi que se elige la fuente nativa segun el sistema operativo.
if sys.platform == "darwin":
    MONO_FONT = "Menlo"
elif sys.platform.startswith("win"):
    MONO_FONT = "Consolas"
else:
    MONO_FONT = "Monospace"


def pinterest_dl_base_cmd():
    """Comando base para invocar pinterest-dl como subproceso.

    En un .exe empaquetado no hay interprete "python" real por dentro, asi
    que en vez de "-m pinterest_dl.cli" se relanza el propio .exe con la
    bandera interna "--pinterest-dl-cli" (ver el bloque __main__)."""
    if FROZEN:
        return [sys.executable, "--pinterest-dl-cli"]
    return [sys.executable, "-m", "pinterest_dl.cli"]
CONFIG_PATH = os.path.join(SCRIPT_DIR, ".pindownloader_config.json")


def load_last_dest():
    """Recupera la ultima carpeta de destino usada (si sigue existiendo en disco)."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        path = data.get("last_dest")
        if path and os.path.isdir(path):
            return path
    except (OSError, ValueError):
        pass
    return None


def _read_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except (OSError, ValueError):
        pass
    return {}


def _write_config(data):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except OSError:
        pass


def load_lang():
    lang = _read_config().get("lang", "es")
    return lang if lang in ("es", "en") else "es"


def save_lang(lang):
    data = _read_config()
    data["lang"] = lang
    _write_config(data)


def save_last_dest(path):
    data = _read_config()
    data["last_dest"] = path
    _write_config(data)

# ---------- Paleta de colores (estilo Pinterest) ----------
RED = "#E60023"
RED_DARK = "#AD081B"
RED_SOFT = "#D98A93"  # rojo tenue, para confirmaciones (ej. carpeta ya elegida) sin gritar tanto como el rojo principal
RED_TINT_25 = "#F9BFC8"  # RED mezclado 25% sobre blanco, para fondos de confirmacion muy tenues
BG = "#F5F6F8"
CARD = "#FFFFFF"
TEXT = "#1A1A1A"
SUBTEXT = "#6B6B6B"
PLACEHOLDER = "#9A9A9A"
LINK_COLOR = "#1A73E8"  # azul tipico de link/URL, para distinguir el texto real del link pegado
BORDER = "#E1E1E1"
CONSOLE_BG = "#161616"
CONSOLE_FG = "#E8E8E8"
CONSOLE_ACCENT = "#FF6B81"

PROGRESS_STEP = 1.6  # % por tick (40ms) -> barrido completo 0-100 tarda ~2.5s minimo
TICK_MS = 40

LINK_PLACEHOLDER = "Pega un link de un tablero, sección o pin de Pinterest"
DEST_PLACEHOLDER = "Elige una carpeta"

I18N = {
    "es": {
        "link_ph": LINK_PLACEHOLDER,
        "dest_ph": DEST_PLACEHOLDER,
        "ask_what": "¿Qué quieres descargar?",
        "next": "Siguiente  →",
        "back": "←  Atrás",
        "ask_where": "¿Dónde guardamos las imágenes?",
        "use_images": "Usar la carpeta “images” dentro de esta app",
        "missing_link_t": "Falta el link",
        "missing_link": "Pega un link de Pinterest primero.",
        "review_link": "Revisa el link",
        "continue_anyway": "\n\n¿Quieres continuar de todas formas?",
        "missing_folder_t": "Falta la carpeta",
        "missing_folder": "Elige una carpeta primero.",
        "options": "Opciones (opcional)",
        "max_images": "CANTIDAD MÁXIMA DE IMÁGENES",
        "max_hint": "Sin límite fijo: puedes subirlo si el tablero es grande. Números muy altos tardan más.",
        "include_video": "Incluir videos",
        "rename_board": "Nombrar archivos con el nombre del board",
        "cookies_off": "Cookies (tableros privados)  ▸",
        "cookies_on": "Cookies (tableros privados)  ▾",
        "cookies_help": "Sirve para descargar tableros o pines privados/secretos. Primero inicia sesión una vez\nen Terminal con: pinterest-dl login --from-browser -o cookies.json\ny luego selecciona aquí ese archivo cookies.json.",
        "choose": "Elegir...",
        "download": "Descargar",
        "downloading": "Descargando...",
        "preparing": "Preparando...",
        "details_off": "Ver detalles ▸",
        "details_on": "Ocultar detalles ▾",
        "cancel": "Cancelar",
        "done": "¡Listo!",
        "problem": "Hubo un problema",
        "more": "Descargar algo más",
        "open_folder": "Abrir carpeta de destino",
        "install_btn": "Instalar pinterest-dl",
        "dep_missing": "Falta instalar la librería 'pinterest-dl' para poder descargar.",
        "dep_exe": "Falta 'pinterest-dl' en este .exe. Vuelve a generarlo con build_windows_exe.bat, o usa PINDOWNLOADER.bat en su lugar.",
        "installing": "Instalando pinterest-dl...",
        "install_fail": "No se pudo instalar. Prueba en Terminal: python3 -m pip install --upgrade pinterest-dl",
        "dep_need_t": "Falta dependencia",
        "dep_need": "Instala primero 'pinterest-dl' (banner amarillo arriba de la ventana).",
        "filetypes_all": "Todos",
        "not_pinterest": "Ese link no parece ser de Pinterest. Revisa que lo hayas copiado completo (sin texto extra al inicio).",
        "pin_it": "Link corto de pin detectado (se resolverá al descargar).",
        "not_link": "Esto no parece un link de Pinterest.",
        "no_user": "No se reconoce un usuario, tablero, sección o pin en ese link.",
        "no_search": "Pinterest no permite descargar búsquedas ni categorías, solo tableros, secciones y pines.",
        "pin_fmt": "Pin detectado: {id}",
        "user_fmt": "Usuario: {name} (sin conexión no puedo confirmar que exista)",
        "board_fmt": "Tablero: {name}",
        "section_fmt": "Sección: {name}",
        "dl_pct": "Descargando... {pct}%",
        "result_ok": "{count} archivo{plural} descargado{plural} en:\n{dest}",
        "result_prefix": "\n\nNombrados con el prefijo: {slug}_...",
        "result_fail": "No se pudo completar la descarga. Revisa el link o abre 'Ver detalles' en el paso anterior para ver el mensaje de error.\n\nCódigo de salida: {code}",
        "lang_btn": "EN",
    },
    "en": {
        "link_ph": "Paste a Pinterest board, section, or pin link",
        "dest_ph": "Choose a folder",
        "ask_what": "What do you want to download?",
        "next": "Next  →",
        "back": "←  Back",
        "ask_where": "Where should we save the images?",
        "use_images": "Use the “images” folder inside this app",
        "missing_link_t": "Link missing",
        "missing_link": "Paste a Pinterest link first.",
        "review_link": "Check the link",
        "continue_anyway": "\n\nContinue anyway?",
        "missing_folder_t": "Folder missing",
        "missing_folder": "Choose a folder first.",
        "options": "Options (optional)",
        "max_images": "MAXIMUM NUMBER OF IMAGES",
        "max_hint": "No hard cap: raise it if the board is large. Very high numbers take longer.",
        "include_video": "Include videos",
        "rename_board": "Name files with the board name",
        "cookies_off": "Cookies (private boards)  ▸",
        "cookies_on": "Cookies (private boards)  ▾",
        "cookies_help": "Needed for private or secret boards and pins. Sign in once\nin Terminal with: pinterest-dl login --from-browser -o cookies.json\nthen pick that cookies.json file here.",
        "choose": "Browse...",
        "download": "Download",
        "downloading": "Downloading...",
        "preparing": "Preparing...",
        "details_off": "Show details ▸",
        "details_on": "Hide details ▾",
        "cancel": "Cancel",
        "done": "Done!",
        "problem": "Something went wrong",
        "more": "Download something else",
        "open_folder": "Open destination folder",
        "install_btn": "Install pinterest-dl",
        "dep_missing": "Install the 'pinterest-dl' library to download.",
        "dep_exe": "'pinterest-dl' is missing from this .exe. Rebuild with build_windows_exe.bat, or use PINDOWNLOADER.bat.",
        "installing": "Installing pinterest-dl...",
        "install_fail": "Install failed. Try in Terminal: python3 -m pip install --upgrade pinterest-dl",
        "dep_need_t": "Missing dependency",
        "dep_need": "Install 'pinterest-dl' first (yellow banner at the top).",
        "filetypes_all": "All",
        "not_pinterest": "That does not look like a Pinterest link. Copy the full URL (no extra text at the start).",
        "pin_it": "Short pin link detected (it will resolve when downloading).",
        "not_link": "This does not look like a Pinterest link.",
        "no_user": "No user, board, section, or pin found in that link.",
        "no_search": "Pinterest searches and categories cannot be downloaded — only boards, sections, and pins.",
        "pin_fmt": "Pin found: {id}",
        "user_fmt": "User: {name} (offline, cannot confirm they exist)",
        "board_fmt": "Board: {name}",
        "section_fmt": "Section: {name}",
        "dl_pct": "Downloading... {pct}%",
        "result_ok": "{count} file{plural} downloaded to:\n{dest}",
        "result_prefix": "\n\nNamed with prefix: {slug}_...",
        "result_fail": "Download did not finish. Check the link or open 'Show details' on the previous step for the error.\n\nExit code: {code}",
        "lang_btn": "ES",
    },
}


def has_pinterest_dl():
    # find_spec es mas confiable que un import directo en general, pero con
    # el import-hook especial que usa PyInstaller para empaquetar un .exe a
    # veces da falsos negativos. Un intento de import de verdad funciona en
    # ambos casos (script normal y .exe congelado).
    if importlib.util.find_spec("pinterest_dl") is not None:
        return True
    try:
        import pinterest_dl  # noqa: F401
        return True
    except ImportError:
        return False


def slugify(text):
    text = re.sub(r"[^\w\-]+", "_", text, flags=re.UNICODE).strip("_")
    return re.sub(r"_+", "_", text) or "pinterest"


def board_name_from_link(link):
    """Deriva un nombre corto (para prefijar archivos) a partir del link/usuario pegado."""
    link = link.strip()
    if "://" in link:
        parsed = urlparse(link)
        parts = [p for p in parsed.path.split("/") if p]
    else:
        parts = [p for p in link.split("/") if p]
    if not parts:
        return "pinterest"
    if len(parts) >= 2:
        name = "_".join(parts[:2])
    else:
        name = parts[0]
    return slugify(name)


def short_path(path, max_len=48):
    if len(path) <= max_len:
        return path
    return "..." + path[-(max_len - 3):]


def prettify_slug(slug):
    """Convierte un slug de URL (ej. 'food-recipes') en un nombre legible ('Food Recipes')."""
    return slug.replace("-", " ").replace("_", " ").strip().title() or slug


SLUG_RE = re.compile(r"^[A-Za-z0-9_\-]{1,60}$")


def classify_link(raw, lang="es"):
    """Revisa el link pegado y devuelve (status, mensaje).
    status es "invalid", "uncertain" o "valid":
      - "valid": vino con https://pinterest.com/... (o pin.it), confianza alta.
      - "uncertain": no trae protocolo, es una sola palabra suelta (forma
        corta de usuario). Formalmente parece valido pero NO hay forma de
        verificar contra Pinterest sin conexion, asi que no se marca como
        confirmado del todo (antes esto se marcaba "valid" a ciegas, y
        cualquier texto sin espacios/simbolos raros -osea, texto random
        tambien- pasaba como "confirmado". Bug reportado.)
      - "invalid": no parece nada de lo anterior (texto con espacios, otro
        dominio, simbolos raros, etc.)
    El mensaje describe que se detecto (tablero / seccion / pin) para
    confirmarle al usuario que se copio bien."""
    link = raw.strip()

    if "://" in link:
        parsed = urlparse(link)
        host = parsed.netloc.lower()
        is_pin_it = host == "pin.it" or host.endswith(".pin.it")
        is_pinterest = is_pin_it or host.endswith("pinterest.com") or host.endswith("pinterest.co.uk")
        if not is_pinterest:
            return "invalid", I18N[lang]["not_pinterest"]
        if is_pin_it:
            return "valid", I18N[lang]["pin_it"]
        parts = [p for p in parsed.path.split("/") if p]
        confidence = "valid"
    else:
        # Sin protocolo (sin "https://") no hay dominio que revisar, asi que
        # es mucho mas facil confundir texto random con un usuario/tablero.
        # Se rechaza de una vez si tiene espacios, puntos (pinta de otro
        # dominio/archivo), arrobas, o simbolos que un usuario de Pinterest
        # nunca tendria.
        if not link or " " in link or "." in link or "@" in link:
            return "invalid", I18N[lang]["not_link"]
        parts = [p for p in link.split("/") if p]
        if not parts or not all(SLUG_RE.match(p) for p in parts):
            return "invalid", I18N[lang]["not_link"]
        # Pasa el formato, pero sigue siendo una adivinanza sin conexion:
        # "uncertain" si es una sola palabra (podria ser cualquier texto
        # random que por casualidad no tiene espacios ni simbolos).
        confidence = "uncertain" if len(parts) == 1 else "valid"

    parts = [p for p in parts if p.lower() not in ("boards", "_saved", "_created", "pins")]

    if not parts:
        return "invalid", I18N[lang]["no_user"]

    if parts[0].lower() in ("search", "categories", "topics"):
        return "invalid", I18N[lang]["no_search"]

    if parts[0].lower() == "pin" and len(parts) >= 2:
        return "valid", I18N[lang]["pin_fmt"].format(id=parts[1])
    if len(parts) == 1:
        return confidence, I18N[lang]["user_fmt"].format(name=parts[0])
    if len(parts) == 2:
        return "valid", I18N[lang]["board_fmt"].format(name=prettify_slug(parts[1]))
    return "valid", I18N[lang]["section_fmt"].format(name=prettify_slug(parts[2]))


def rounded_rect(canvas, x1, y1, x2, y2, radius=14, **kwargs):
    """Dibuja un rectangulo con esquinas redondeadas en un Canvas (Tkinter no trae esto de fabrica)."""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def make_step_indicator(parent, current, total=4, width=240, height=30):
    """Stepper (indicador de progreso). La linea es el "track" que conecta
    los marcadores ("step markers"). Los pasos intermedios son circulos:
    rojo = donde estas, gris relleno = ya pasaste, gris hueco = te falta.
    El ultimo marcador es un rombo (el "hito"/meta final): gris hasta que
    llegas al ultimo paso, rojo cuando lo alcanzas."""
    canvas = tk.Canvas(parent, width=width, height=height, bg=BG, highlightthickness=0)
    y = height / 2
    margin = 16
    span = width - margin * 2
    xs = [margin + span * i / (total - 1) for i in range(total)]

    canvas.create_line(xs[0], y, xs[-1], y, fill="#D5D7DA", width=2)

    for i, x in enumerate(xs):
        step_num = i + 1
        is_goal = step_num == total
        if is_goal:
            r = 8
            color = RED if current >= total else "#9AA0A6"
            canvas.create_polygon(x, y - r, x + r, y, x, y + r, x - r, y, fill=color, outline=color)
        elif step_num == current:
            r = 6
            canvas.create_oval(x - r, y - r, x + r, y + r, fill=RED, outline=RED)
        elif step_num < current:
            r = 6
            canvas.create_oval(x - r, y - r, x + r, y + r, fill="#9AA0A6", outline="")
        else:
            r = 6
            canvas.create_oval(x - r, y - r, x + r, y + r, fill=BG, outline="#C7C9CC", width=2)
    return canvas


def make_rounded_entry(parent, placeholder, width=440, height=54, radius=16):
    """Campo de texto con fondo redondeado.

    OJO: el Entry NO va incrustado dentro del Canvas (canvas.create_window).
    Ese patron tiene un bug conocido de refresco en Tk/macOS: el widget
    incrustado se queda "en blanco" tras perder el foco y solo se repinta
    cuando la app pierde y recupera el foco del sistema (justo lo que se
    reporto). En vez de eso, el Canvas solo dibuja el fondo redondeado y el
    Entry va superpuesto encima con .place(), como widget normal e
    independiente: mucho mas estable.
    """
    wrap = tk.Frame(parent, bg=BG, width=width, height=height)
    wrap.pack_propagate(False)

    canvas = tk.Canvas(wrap, width=width, height=height, bg=BG, highlightthickness=0)
    canvas.place(x=0, y=0, width=width, height=height)
    rounded_rect(canvas, 2, 2, width - 2, height - 2, radius=radius, fill="white", outline=BORDER, width=1)

    entry = PlaceholderEntry(
        wrap, placeholder, relief="flat", bd=0, highlightthickness=0, bg="white", justify="center",
    )
    entry.place(x=16, y=10, width=width - 32, height=height - 20)
    return wrap, entry


def make_folder_button(parent, on_click, width=280, height=120, radius=18):
    """Tarjeta grande y clickeable con icono de carpeta para elegir la
    carpeta con un solo click (reemplaza el boton chico + label separado que
    habia antes, que no seguia el mismo estilo centrado del paso 1)."""
    wrap = tk.Frame(parent, bg=BG, width=width, height=height)
    wrap.pack_propagate(False)

    canvas = tk.Canvas(wrap, width=width, height=height, bg=BG, highlightthickness=0, cursor="hand2")
    canvas.place(x=0, y=0, width=width, height=height)
    bg_id = rounded_rect(canvas, 2, 2, width - 2, height - 2, radius=radius, fill="white", outline=BORDER, width=1)

    # Icono y texto centrados como un solo bloque (antes quedaba mucho mas
    # espacio abajo que arriba, descompensado).
    icon_id = canvas.create_text(width / 2, height / 2 - 14, text="📁", font=("Helvetica", 34))
    text_id = canvas.create_text(width / 2, height / 2 + 20, text=DEST_PLACEHOLDER, fill=PLACEHOLDER,
                                  font=("Helvetica", 14), width=width - 40, justify="center")

    canvas.bind("<Button-1>", lambda e: on_click())
    return wrap, canvas, icon_id, text_id, bg_id


class PlaceholderEntry(tk.Entry):
    """Entry con texto de ejemplo en gris que se borra solo al hacer click
    DENTRO del campo o al escribir.

    Usa una StringVar en vez de borrar/insertar texto a mano (mas robusto:
    evita que la bandera interna "_showing_placeholder" se desincronice del
    contenido real si dos eventos llegan casi al mismo tiempo, que era una
    fuente posible del bug reportado de "se borra/no se restablece solo")."""

    def __init__(self, master, placeholder, **kwargs):
        kwargs.setdefault("relief", "solid")
        kwargs.setdefault("bd", 1)
        kwargs.setdefault("highlightthickness", 0)
        kwargs.setdefault("bg", "white")
        kwargs.setdefault("font", ("Helvetica", 15))
        self._base_font = kwargs["font"]
        self.placeholder = placeholder
        self.var = tk.StringVar()
        kwargs["textvariable"] = self.var
        super().__init__(master, **kwargs)
        self._showing_placeholder = False
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        self._set_placeholder()

    def _set_placeholder(self):
        self.var.set(self.placeholder)
        self.configure(fg=PLACEHOLDER, font=self._base_font)
        self._showing_placeholder = True

    def refresh_style(self):
        """Si hay texto real (no el placeholder) lo pinta como link: azul y subrayado."""
        if self._showing_placeholder:
            return
        if self.var.get():
            self.configure(fg=LINK_COLOR, font=self._base_font + ("underline",))
        else:
            self.configure(fg=TEXT, font=self._base_font)

    def _on_focus_in(self, _event=None):
        # Solo se dispara cuando ESTE widget recibe el foco de verdad (click
        # adentro o Tab), nunca por clicks en otros widgets de la ventana.
        if self._showing_placeholder:
            self.var.set("")
            self._showing_placeholder = False
        self.refresh_style()

    def _on_focus_out(self, _event=None):
        if not self.var.get():
            self._set_placeholder()
        else:
            self.refresh_style()

    def value(self):
        return "" if self._showing_placeholder else self.var.get().strip()


class PinterestGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pinterest GUI Downloader")
        self._center_window(600, 600)
        self.resizable(False, False)
        self.configure(bg=BG)

        self.lang = load_lang()
        self.process = None
        self.dest_dir = None
        self._progress_value = 0.0
        self._progress_target = 0.0
        self._ticking = False
        self._process_done = False
        self._process_code = None

        self._setup_style()
        self._build_header()
        self._build_dep_banner()
        self._check_dependency()  # se empaqueta ANTES del contenedor para que quede arriba

        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.steps = {}
        self._build_step_link()
        self._build_step_dest()
        self._build_step_options()
        self._build_step_download()
        self._build_step_result()

        self._show_step("link")
        self._apply_lang()

        self.credit_label = tk.Label(
            self,
            text="Engine: limkokhole/pinterest-downloader (MIT). Viewer: CHK.",
            bg=BG, fg="#888888", font=("Helvetica", 10),
        )
        self.credit_label.pack(side="bottom", pady=(0, 10))


    def t(self, key):
        return I18N[self.lang][key]

    def _toggle_lang(self):
        self.lang = "en" if self.lang == "es" else "es"
        save_lang(self.lang)
        self._apply_lang()

    def _apply_lang(self):
        s = I18N[self.lang]
        self.lang_btn.configure(text=s["lang_btn"])
        self.link_title.configure(text=s["ask_what"])
        self.link_entry.placeholder = s["link_ph"]
        if self.link_entry._showing_placeholder:
            self.link_entry._set_placeholder()
        self.link_next_btn.configure(text=s["next"])
        self.dest_title.configure(text=s["ask_where"])
        if not self.dest_dir:
            self.dest_canvas.itemconfigure(self.dest_text_id, text=s["dest_ph"], fill=PLACEHOLDER)
        self.use_default_chk.configure(text=s["use_images"])
        self.dest_back_btn.configure(text=s["back"])
        self.dest_next_btn.configure(text=s["next"])
        self.opt_title.configure(text=s["options"])
        self.max_label.configure(text=s["max_images"])
        self.max_hint.configure(text=s["max_hint"])
        self.video_chk.configure(text=s["include_video"])
        self.rename_chk.configure(text=s["rename_board"])
        self.cookies_toggle_btn.configure(text=s["cookies_on"] if self._cookies_visible else s["cookies_off"])
        self.cookies_help.configure(text=s["cookies_help"])
        self.cookies_pick_btn.configure(text=s["choose"])
        self.opt_dl_btn.configure(text=s["download"])
        self.opt_back_btn.configure(text=s["back"])
        self.download_title.configure(text=s["downloading"])
        self.download_status.configure(text=s["preparing"])
        self.details_toggle_btn.configure(text=s["details_on"] if self._details_visible else s["details_off"])
        self.cancel_btn.configure(text=s["cancel"])
        self.result_title.configure(text=s["done"])
        self.more_btn.configure(text=s["more"])
        self.open_folder_btn.configure(text=s["open_folder"])
        self.dep_install_btn.configure(text=s["install_btn"])
        if self.dep_banner.winfo_ismapped():
            if FROZEN:
                self.dep_label.configure(text=s["dep_exe"])
            else:
                self.dep_label.configure(text=s["dep_missing"])
        value = self.link_entry.value()
        if value:
            status, message = classify_link(value, self.lang)
            if status == "valid":
                self.link_feedback.configure(text="✓  " + message)
            elif status == "uncertain":
                self.link_feedback.configure(text="?  " + message)
            else:
                self.link_feedback.configure(text="⚠  " + message)

    def _center_window(self, width, height):
        """Coloca la ventana centrada en la pantalla (por defecto Tk la abre
        arriba a la izquierda)."""
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    # ---------- Estilo ----------
    def _setup_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(".", background=BG, foreground=TEXT, font=("Helvetica", 14))
        style.configure("Card.TLabel", background=CARD, foreground=TEXT)
        style.configure("Bg.TLabel", background=BG, foreground=TEXT)
        style.configure("Sub.TLabel", background=BG, foreground=SUBTEXT, font=("Helvetica", 13))
        style.configure("Step.TLabel", background=BG, foreground=RED, font=("Helvetica", 13, "bold"))
        style.configure("Title.TLabel", background=BG, foreground=TEXT, font=("Helvetica", 23, "bold"))
        # Version mas chica para el titulo de error en el resultado: no debe
        # competir en tamaño con la confirmacion de exito ("¡Listo!").
        style.configure("ErrorTitle.TLabel", background=BG, foreground="#B54708", font=("Helvetica", 17, "bold"))
        style.configure("FieldLabel.TLabel", background=BG, foreground=SUBTEXT,
                         font=("Helvetica", 13, "bold"))

        style.configure("TCheckbutton", background=BG, foreground=TEXT)
        style.map("TCheckbutton", background=[("active", BG)])

        # Version mas tenue del checkbox, para opciones secundarias (ej. "usar
        # la carpeta por defecto") que no deben competir visualmente con la
        # accion principal del paso.
        style.configure("Sub.TCheckbutton", background=BG, foreground=SUBTEXT, font=("Helvetica", 12))
        style.map("Sub.TCheckbutton", background=[("active", BG)], foreground=[("active", SUBTEXT)])

        style.configure(
            "Primary.TButton",
            background=RED, foreground="white",
            font=("Helvetica", 15, "bold"), padding=(20, 13), borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("disabled", "#B9BCC0"), ("active", RED_DARK)],
            foreground=[("disabled", "#FFFFFF")],
        )

        style.configure(
            "Secondary.TButton",
            background="#EDEEF1", foreground=TEXT, padding=(18, 12), borderwidth=0,
        )
        style.map("Secondary.TButton", background=[("active", "#DEDFE3"), ("disabled", "#F5F5F5")])

        style.configure(
            "Link.TButton",
            background=BG, foreground=RED, font=("Helvetica", 13, "bold"), borderwidth=0, padding=(3, 3),
        )
        style.map("Link.TButton", foreground=[("active", RED_DARK)])

        style.configure(
            "Gray.Horizontal.TProgressbar",
            troughcolor="#E1E1E1", background="#9AA0A6",
            bordercolor="#E1E1E1", lightcolor="#9AA0A6", darkcolor="#9AA0A6", thickness=16,
        )
        style.configure(
            "Red.Horizontal.TProgressbar",
            troughcolor="#E1E1E1", background=RED,
            bordercolor="#E1E1E1", lightcolor=RED, darkcolor=RED, thickness=16,
        )

    # ---------- Header ----------
    def _build_header(self):
        header = tk.Frame(self, bg=RED, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        row = tk.Frame(header, bg=RED)
        row.pack(pady=12)  # sin side="left": pack centra horizontalmente por defecto

        # Icono temporal: insignia blanca con "P" en rojo (evita el pin de color
        # sobre fondo rojo, que se pierde). Facil de sustituir despues por un
        # archivo propio (recomendado: PNG cuadrado, fondo transparente, 256x256px).
        icon = tk.Canvas(row, width=36, height=36, bg=RED, highlightthickness=0)
        icon.pack(side="left", padx=(0, 10))
        icon.create_oval(1, 1, 35, 35, fill="white", outline="")
        icon.create_text(18, 19, text="P", fill=RED, font=("Helvetica", 21, "bold"))

        tk.Label(row, text="Pinterest GUI Downloader", bg=RED, fg="white",
                 font=("Helvetica", 21, "bold")).pack(side="left")

        self.lang_btn = tk.Label(
            header, text=I18N[self.lang]["lang_btn"], bg="white", fg=RED,
            font=("Helvetica", 11, "bold"), padx=10, pady=3, cursor="hand2",
        )
        self.lang_btn.place(relx=1.0, x=-14, y=20, anchor="ne")
        self.lang_btn.bind("<Button-1>", lambda e: self._toggle_lang())

    def _build_dep_banner(self):
        self.dep_banner = tk.Frame(self, bg="#FFF4E5")
        self.dep_label = tk.Label(self.dep_banner, text="", bg="#FFF4E5", fg="#8A5A00",
                                   font=("Helvetica", 13), anchor="w")
        self.dep_label.pack(side="left", padx=14, pady=8, fill="x", expand=True)
        self.dep_install_btn = ttk.Button(self.dep_banner, text=I18N[self.lang]["install_btn"],
                                           style="Secondary.TButton", command=self._install_dependency)
        self.dep_install_btn.pack(side="right", padx=10, pady=6)
        # No se empaqueta hasta que haga falta (ver _check_dependency).

    # ---------- Navegacion entre pasos ----------
    def _show_step(self, name):
        for frame in self.steps.values():
            frame.grid_remove()
        self.steps[name].grid(row=0, column=0, sticky="nsew")
        if name == "download":
            self._begin_download()

    # ---------- Paso 1: Link ----------
    def _build_step_link(self):
        frame = tk.Frame(self.container, bg=BG)
        self.steps["link"] = frame

        body = tk.Frame(frame, bg=BG)
        body.pack(fill="both", expand=True)

        # Frame centrado en ambos ejes dentro de la ventana (pack(expand=True)
        # sin fill ni side reparte el espacio sobrante arriba/abajo/lados).
        center_col = tk.Frame(body, bg=BG)
        center_col.pack(expand=True)

        make_step_indicator(center_col, current=1, total=4).pack(pady=(0, 18))
        self.link_title = ttk.Label(center_col, text=I18N[self.lang]["ask_what"], style="Title.TLabel")
        self.link_title.pack(pady=(0, 24))

        field_canvas, self.link_entry = make_rounded_entry(center_col, I18N[self.lang]["link_ph"], width=440, height=54)
        field_canvas.pack()
        self.link_entry.bind("<KeyRelease>", self._on_link_changed)
        self.link_entry.bind("<<Paste>>", lambda e: self.after(10, self._on_link_changed))
        # OJO: sin focus_set() aca. Si el campo arranca con el foco puesto, el
        # placeholder se borra apenas la ventana recibe el primer click en
        # CUALQUIER parte (no solo al clickar dentro del campo). Debe quedar
        # sin foco hasta que el usuario clickee el campo a proposito.

        self.link_feedback = tk.Label(center_col, text="", bg=BG, font=("Helvetica", 19, "bold"),
                                       wraplength=440, justify="center")
        self.link_feedback.pack(pady=(14, 0))

        # El boton "Siguiente" va agrupado aqui mismo, justo debajo del campo,
        # en vez de una barra de navegacion separada pegada al fondo de la
        # ventana (quedaba muy lejos del campo).
        self.link_next_btn = ttk.Button(center_col, text=I18N[self.lang]["next"], style="Primary.TButton",
                                         command=self._go_to_dest, state="disabled")
        self.link_next_btn.pack(pady=(22, 0))

    def _on_link_changed(self, _event=None):
        self.link_entry.refresh_style()
        value = self.link_entry.value()
        self.link_next_btn.configure(state="normal" if value else "disabled")
        if not value:
            self.link_feedback.configure(text="")
            return
        status, message = classify_link(value, self.lang)
        if status == "valid":
            self.link_feedback.configure(text="✓  " + message, fg=RED, font=("Helvetica", 19, "bold"))
        elif status == "uncertain":
            self.link_feedback.configure(text="?  " + message, fg="#6B6B6B", font=("Helvetica", 19, "bold"))
        else:
            # Mismo color naranja, pero 1.5x mas chico que los otros mensajes
            # (19 / 1.5 ≈ 13): el texto de "link invalido" no debe pesar tanto
            # visualmente como una confirmacion.
            self.link_feedback.configure(text="⚠  " + message, fg="#B54708", font=("Helvetica", 13, "bold"))

    def _go_to_dest(self):
        value = self.link_entry.value()
        if not value:
            messagebox.showwarning(I18N[self.lang]["missing_link_t"], I18N[self.lang]["missing_link"])
            return
        status, message = classify_link(value, self.lang)
        if status == "invalid":
            proceed = messagebox.askyesno(
                I18N[self.lang]["review_link"],
                message + I18N[self.lang]["continue_anyway"],
            )
            if not proceed:
                return
        self._show_step("dest")

    # ---------- Paso 2: Carpeta de destino ----------
    def _build_step_dest(self):
        frame = tk.Frame(self.container, bg=BG)
        self.steps["dest"] = frame

        body = tk.Frame(frame, bg=BG)
        body.pack(fill="both", expand=True)

        # Misma composicion centrada que el paso 1 (pack(expand=True) sin
        # fill/side reparte el espacio sobrante y centra en ambos ejes).
        center_col = tk.Frame(body, bg=BG)
        center_col.pack(expand=True)

        make_step_indicator(center_col, current=2, total=4).pack(pady=(0, 18))
        self.dest_title = ttk.Label(center_col, text=I18N[self.lang]["ask_where"], style="Title.TLabel")
        self.dest_title.pack(pady=(0, 24))

        # Tarjeta grande con icono en vez del boton chico + label "CARPETA DE
        # DESTINO" de antes; la instruccion va dentro de la propia tarjeta.
        self.dest_wrap, self.dest_canvas, self.dest_icon_id, self.dest_text_id, self.dest_bg_id = make_folder_button(
            center_col, self._choose_dest, width=280, height=120,
        )
        self.dest_wrap.pack()

        # Checkbox tenue que sirve como override: si se marca, se usa la
        # carpeta "images" de la app y la tarjeta de arriba queda deshabilitada.
        self.use_default_var = tk.BooleanVar(value=False)
        self.use_default_chk = ttk.Checkbutton(
            center_col, text=I18N[self.lang]["use_images"],
            variable=self.use_default_var, style="Sub.TCheckbutton",
            command=self._toggle_default_dest,
        )
        self.use_default_chk.pack(pady=(14, 0))

        # Botones agrupados y centrados debajo del contenido, igual que el
        # paso 1 (antes iban en una barra separada pegada al fondo, partida
        # en dos extremos, y no correspondia con la composicion del paso 1).
        btn_row = tk.Frame(center_col, bg=BG)
        btn_row.pack(pady=(26, 0))
        self.dest_back_btn = ttk.Button(btn_row, text=I18N[self.lang]["back"], style="Secondary.TButton",
                   command=lambda: self._show_step("link"))
        self.dest_back_btn.pack(side="left", padx=(0, 10))
        self.dest_next_btn = ttk.Button(btn_row, text=I18N[self.lang]["next"], style="Primary.TButton",
                                         command=self._go_to_options, state="disabled")
        self.dest_next_btn.pack(side="left")

        # Si ya se habia usado la app antes, reconoce la carpeta anterior y la
        # deja preseleccionada (o marca el checkbox si esa carpeta era la de
        # "images" por defecto), en vez de pedirla de cero cada vez.
        last_dest = load_last_dest()
        if last_dest:
            if os.path.normpath(last_dest) == os.path.normpath(DEFAULT_DEST):
                self.use_default_var.set(True)
                self._toggle_default_dest()
            else:
                self._set_dest(last_dest)

    def _choose_dest(self):
        if self.use_default_var.get():
            return  # la tarjeta queda "apagada" mientras el checkbox tenga el control
        initial = self.dest_dir or load_last_dest() or SCRIPT_DIR
        path = filedialog.askdirectory(initialdir=initial)
        if path:
            self._set_dest(path)

    def _toggle_default_dest(self):
        if self.use_default_var.get():
            os.makedirs(DEFAULT_DEST, exist_ok=True)
            self._set_dest(DEFAULT_DEST)
            self.dest_canvas.configure(cursor="arrow")
            self.dest_canvas.itemconfigure(self.dest_icon_id, fill="#C7C9CC")
        else:
            self.dest_canvas.configure(cursor="hand2")
            self.dest_canvas.itemconfigure(self.dest_icon_id, fill=TEXT)
            self.dest_canvas.itemconfigure(self.dest_bg_id, fill="white")
            self.dest_dir = None
            self.dest_canvas.itemconfigure(self.dest_text_id, text=I18N[self.lang]["dest_ph"], fill=PLACEHOLDER)
            self.dest_next_btn.configure(state="disabled")

    def _set_dest(self, path):
        self.dest_dir = path
        self.dest_canvas.itemconfigure(self.dest_text_id, text=short_path(path, max_len=30), fill=TEXT)
        self.dest_canvas.itemconfigure(self.dest_icon_id, fill=RED_SOFT)
        # Fondo de la tarjeta con un tinte rojo tenue (25%) para confirmar de
        # un vistazo que la carpeta ya quedo seleccionada.
        self.dest_canvas.itemconfigure(self.dest_bg_id, fill=RED_TINT_25)
        self.dest_next_btn.configure(state="normal")
        save_last_dest(path)

    def _go_to_options(self):
        if not self.dest_dir:
            messagebox.showwarning(I18N[self.lang]["missing_folder_t"], I18N[self.lang]["missing_folder"])
            return
        self._show_step("options")

    # ---------- Paso 3: Opciones ----------
    def _build_step_options(self):
        frame = tk.Frame(self.container, bg=BG)
        self.steps["options"] = frame

        body = tk.Frame(frame, bg=BG)
        body.pack(fill="both", expand=True, padx=36, pady=30)

        make_step_indicator(body, current=3, total=4).pack(anchor="w", pady=(0, 10))
        self.opt_title = ttk.Label(body, text=I18N[self.lang]["options"], style="Title.TLabel")
        self.opt_title.pack(anchor="w", pady=(4, 16))

        row1 = tk.Frame(body, bg=BG)
        row1.pack(fill="x", pady=(0, 4))
        self.max_label = ttk.Label(row1, text=I18N[self.lang]["max_images"], style="FieldLabel.TLabel")
        self.max_label.pack(anchor="w")
        num_row = tk.Frame(row1, bg=BG)
        num_row.pack(anchor="w", pady=(4, 0))
        self.num_var = tk.StringVar(value="500")
        tk.Entry(num_row, textvariable=self.num_var, width=8, relief="flat", bd=0,
                 highlightthickness=1, highlightbackground=BORDER, highlightcolor=BORDER,
                 font=("Helvetica", 15)).pack(side="left", ipady=6)
        self.max_hint = ttk.Label(row1, text=I18N[self.lang]["max_hint"], style="Sub.TLabel",
                  wraplength=500, justify="left")
        self.max_hint.pack(anchor="w", pady=(4, 0))

        opts = tk.Frame(body, bg=BG)
        opts.pack(fill="x", pady=(16, 4), anchor="w")
        self.video = tk.BooleanVar()
        self.video_chk = ttk.Checkbutton(opts, text=I18N[self.lang]["include_video"], variable=self.video)
        self.video_chk.pack(anchor="w", pady=2)
        self.rename_board = tk.BooleanVar(value=True)
        self.rename_chk = ttk.Checkbutton(opts, text=I18N[self.lang]["rename_board"],
                         variable=self.rename_board)
        self.rename_chk.pack(anchor="w", pady=2)

        self.cookies_toggle_btn = ttk.Button(body, text=I18N[self.lang]["cookies_off"],
                                              style="Link.TButton", command=self._toggle_cookies)
        self.cookies_toggle_btn.pack(anchor="w", pady=(14, 0))

        self.cookies_frame = tk.Frame(body, bg=BG)
        self.cookies_help = ttk.Label(self.cookies_frame,
                  text=I18N[self.lang]["cookies_help"],
                  style="Sub.TLabel", justify="left")
        self.cookies_help.pack(anchor="w", pady=(6, 4))
        cookie_row = tk.Frame(self.cookies_frame, bg=BG)
        cookie_row.pack(fill="x")
        self.cookies_var = tk.StringVar()
        tk.Entry(cookie_row, textvariable=self.cookies_var, relief="flat", bd=0,
                 highlightthickness=1, highlightbackground=BORDER, highlightcolor=BORDER,
                 font=("Helvetica", 15)).pack(side="left", fill="x", expand=True, ipady=6)
        self.cookies_pick_btn = ttk.Button(cookie_row, text=I18N[self.lang]["choose"], style="Secondary.TButton",
                   command=self._choose_cookies)
        self.cookies_pick_btn.pack(side="left", padx=(8, 0))
        self._cookies_visible = False

        nav = tk.Frame(frame, bg=BG)
        nav.pack(fill="x", padx=36, pady=(0, 30), side="bottom")
        self.opt_dl_btn = ttk.Button(nav, text=I18N[self.lang]["download"], style="Primary.TButton",
                   command=self._go_to_download)
        self.opt_dl_btn.pack(side="right")
        self.opt_back_btn = ttk.Button(nav, text=I18N[self.lang]["back"], style="Secondary.TButton",
                   command=lambda: self._show_step("dest"))
        self.opt_back_btn.pack(side="left")

    def _toggle_cookies(self):
        if self._cookies_visible:
            self.cookies_frame.pack_forget()
            self.cookies_toggle_btn.configure(text=I18N[self.lang]["cookies_off"])
        else:
            self.cookies_frame.pack(fill="x", pady=(0, 4), anchor="w")
            self.cookies_toggle_btn.configure(text=I18N[self.lang]["cookies_on"])
        self._cookies_visible = not self._cookies_visible

    def _choose_cookies(self):
        path = filedialog.askopenfilename(initialdir=SCRIPT_DIR, filetypes=[("JSON", "*.json"), (I18N[self.lang]["filetypes_all"], "*.*")])
        if path:
            self.cookies_var.set(path)

    def _go_to_download(self):
        if not has_pinterest_dl():
            messagebox.showerror(I18N[self.lang]["dep_need_t"], I18N[self.lang]["dep_need"])
            return
        self._show_step("download")

    # ---------- Paso 4: Descargando ----------
    def _build_step_download(self):
        frame = tk.Frame(self.container, bg=BG)
        self.steps["download"] = frame

        body = tk.Frame(frame, bg=BG)
        body.pack(fill="both", expand=True, padx=36, pady=40)

        make_step_indicator(body, current=4, total=4).pack(anchor="w", pady=(0, 10))
        self.download_title = ttk.Label(body, text=I18N[self.lang]["downloading"], style="Title.TLabel")
        self.download_title.pack(anchor="w", pady=(4, 30))

        self.progress = ttk.Progressbar(
            body, style="Gray.Horizontal.TProgressbar",
            orient="horizontal", mode="determinate", maximum=100, value=0,
        )
        self.progress.pack(fill="x", ipady=2)

        self.download_status = ttk.Label(body, text=I18N[self.lang]["preparing"], style="Sub.TLabel")
        self.download_status.pack(anchor="w", pady=(10, 0))

        self.details_toggle_btn = ttk.Button(body, text=I18N[self.lang]["details_off"], style="Link.TButton",
                                              command=self._toggle_details)
        self.details_toggle_btn.pack(anchor="w", pady=(16, 0))

        self.details_frame = tk.Frame(body, bg=BG)
        self.output = tk.Text(self.details_frame, wrap="word", state="disabled", bg=CONSOLE_BG, fg=CONSOLE_FG,
                               insertbackground=CONSOLE_FG, relief="flat", padx=10, pady=8, height=8,
                               font=(MONO_FONT, 13))
        self.output.tag_configure("accent", foreground=CONSOLE_ACCENT)
        self.output.tag_configure("ok", foreground="#7CE38B")
        out_scroll = ttk.Scrollbar(self.details_frame, command=self.output.yview)
        self.output.configure(yscrollcommand=out_scroll.set)
        self.output.pack(side="left", fill="both", expand=True)
        out_scroll.pack(side="right", fill="y")
        self._details_visible = False

        nav = tk.Frame(frame, bg=BG)
        nav.pack(fill="x", padx=36, pady=(0, 30), side="bottom")
        self.cancel_btn = ttk.Button(nav, text=I18N[self.lang]["cancel"], style="Secondary.TButton",
                                      command=self._cancel_download)
        self.cancel_btn.pack(side="left")

    def _toggle_details(self):
        if self._details_visible:
            self.details_frame.pack_forget()
            self.details_toggle_btn.configure(text=I18N[self.lang]["details_off"])
        else:
            self.details_frame.pack(fill="both", expand=True, pady=(8, 0))
            self.details_toggle_btn.configure(text=I18N[self.lang]["details_on"])
        self._details_visible = not self._details_visible

    # ---------- Paso 5: Resultado ----------
    def _build_step_result(self):
        frame = tk.Frame(self.container, bg=BG)
        self.steps["result"] = frame

        body = tk.Frame(frame, bg=BG)
        body.pack(fill="both", expand=True, padx=36, pady=40)

        self.result_title = ttk.Label(body, text=I18N[self.lang]["done"], style="Title.TLabel")
        self.result_title.pack(anchor="w", pady=(10, 10))
        self.result_detail = ttk.Label(body, text="", style="Bg.TLabel", font=("Helvetica", 15),
                                        wraplength=500, justify="left")
        self.result_detail.pack(anchor="w")

        nav = tk.Frame(frame, bg=BG)
        nav.pack(fill="x", padx=36, pady=(0, 30), side="bottom")
        self.more_btn = ttk.Button(nav, text=I18N[self.lang]["more"], style="Secondary.TButton",
                   command=self._reset_to_link)
        self.more_btn.pack(side="left")
        self.open_folder_btn = ttk.Button(nav, text=I18N[self.lang]["open_folder"], style="Primary.TButton",
                                           command=self._open_dest_folder)
        self.open_folder_btn.pack(side="right")

    def _reset_to_link(self):
        self.link_entry._set_placeholder()
        self._refresh_link_button()
        self._show_step("link")

    def _open_dest_folder(self):
        dest = self.dest_dir or DEFAULT_DEST
        os.makedirs(dest, exist_ok=True)
        if sys.platform == "darwin":
            subprocess.run(["open", dest])
        elif sys.platform.startswith("win"):
            os.startfile(dest)  # noqa
        else:
            subprocess.run(["xdg-open", dest])

    # ---------- Dependencia (pinterest-dl) ----------
    def _check_dependency(self):
        if not has_pinterest_dl():
            if FROZEN:
                # Un .exe empaquetado no trae pip de verdad adentro: no se
                # puede "instalar" nada en caliente. pinterest-dl debio
                # quedar incluido al generar el .exe (build_windows_exe.bat).
                self.dep_install_btn.pack_forget()
                self.dep_label.configure(text=I18N[self.lang]["dep_exe"])
            else:
                self.dep_label.configure(text=I18N[self.lang]["dep_missing"])
            self.dep_banner.pack(fill="x")

    def _install_dependency(self):
        self.dep_install_btn.configure(state="disabled")
        self.dep_label.configure(text=I18N[self.lang]["installing"])
        thread = threading.Thread(target=self._run_install, daemon=True)
        thread.start()

    def _run_install(self):
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "pinterest-dl"]
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            proc.communicate()
            ok = proc.returncode == 0 and has_pinterest_dl()
        except Exception:
            ok = False
        self.after(0, self._on_install_finished, ok)

    def _on_install_finished(self, ok):
        if ok:
            self.dep_banner.pack_forget()
        else:
            self.dep_label.configure(text=I18N[self.lang]["install_fail"])
            self.dep_install_btn.configure(state="normal")

    # ---------- Descarga ----------
    def _append(self, text, tag=None):
        self.output.configure(state="normal")
        self.output.insert("end", text, tag) if tag else self.output.insert("end", text)
        self.output.see("end")
        self.output.configure(state="disabled")

    def _begin_download(self):
        link = self.link_entry.value()
        dest = self.dest_dir or DEFAULT_DEST
        os.makedirs(dest, exist_ok=True)

        self._pre_existing_files = set(os.listdir(dest))
        self._board_slug = board_name_from_link(link)
        self._dest_dir = dest

        cmd = pinterest_dl_base_cmd() + ["scrape", link, "-o", dest]
        num = self.num_var.get().strip()
        if num:
            cmd += ["-n", num]
        cookies = self.cookies_var.get().strip()
        if cookies:
            cmd += ["-c", cookies]
        if self.video.get():
            cmd.append("--video")

        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")
        self._append(f"$ {' '.join(cmd)}\n\n", "accent")

        self.download_title.configure(text=I18N[self.lang]["downloading"])
        self.download_status.configure(text=I18N[self.lang]["preparing"])
        self.cancel_btn.configure(state="normal")

        self._progress_value = 0.0
        self._progress_target = 0.0
        self._process_done = False
        self._process_code = None
        self.progress.configure(style="Gray.Horizontal.TProgressbar", value=0)

        self._ticking = True
        self.after(TICK_MS, self._tick_progress)

        thread = threading.Thread(target=self._run_process, args=(cmd,), daemon=True)
        thread.start()

    def _handle_output_line(self, text):
        self._append(text + "\n")
        match = re.search(r"(\d{1,3})\s*%", text)
        if match:
            percent = min(99, max(0, int(match.group(1))))
            self._progress_target = max(self._progress_target, float(percent))
            self.download_status.configure(text=I18N[self.lang]["dl_pct"].format(pct=int(self._progress_target)))

    def _run_process(self, cmd):
        try:
            env = dict(os.environ)
            env["PYTHONIOENCODING"] = "utf8"
            env["PYTHONUNBUFFERED"] = "1"
            popen_kwargs = {}
            if sys.platform.startswith("win"):
                # Evita que aparezca (aunque sea un instante) una ventana de
                # consola negra al lanzar el subproceso en Windows.
                popen_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
            self.process = subprocess.Popen(
                cmd, cwd=SCRIPT_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, env=env, **popen_kwargs,
            )
            # Se lee caracter a caracter y se separa por \r ademas de \n, porque
            # las barras de progreso (tqdm) de pinterest-dl actualizan con \r.
            buf = ""
            while True:
                chunk = self.process.stdout.read(256)
                if not chunk:
                    break
                buf += chunk
                while True:
                    m = re.search(r"[\r\n]", buf)
                    if not m:
                        break
                    line, buf = buf[: m.start()], buf[m.end():]
                    if line.strip():
                        self.after(0, self._handle_output_line, line)
            if buf.strip():
                self.after(0, self._handle_output_line, buf)
            self.process.wait()
            code = self.process.returncode
        except Exception as e:
            self.after(0, self._append, f"\n[Error] {e}\n")
            code = -1

        self.after(0, self._mark_process_done, code)

    def _mark_process_done(self, code):
        self._process_done = True
        self._process_code = code
        if code == 0:
            self._progress_target = 100.0
        # si code != 0, el tick detecta el error y termina de inmediato

    def _tick_progress(self):
        if not self._ticking:
            return
        if self._progress_value < self._progress_target:
            self._progress_value = min(self._progress_target, self._progress_value + PROGRESS_STEP)
            self.progress.configure(value=self._progress_value)

        if self._process_done:
            if self._process_code == 0:
                if self._progress_value >= 100:
                    self._ticking = False
                    self.progress.configure(style="Red.Horizontal.TProgressbar", value=100)
                    self._finish(self._process_code)
                    return
            else:
                self._ticking = False
                self._finish(self._process_code)
                return

        self.after(TICK_MS, self._tick_progress)

    def _rename_new_files(self):
        dest = self._dest_dir
        try:
            current_files = os.listdir(dest)
        except OSError:
            return 0
        new_files = [f for f in current_files if f not in self._pre_existing_files]
        new_files = [f for f in new_files if os.path.isfile(os.path.join(dest, f))]

        if self.rename_board.get():
            prefix = self._board_slug + "_"
            for fname in new_files:
                if fname.startswith(prefix):
                    continue
                src = os.path.join(dest, fname)
                new_name = prefix + fname
                dst = os.path.join(dest, new_name)
                counter = 1
                base, ext = os.path.splitext(new_name)
                while os.path.exists(dst):
                    dst = os.path.join(dest, f"{base}_{counter}{ext}")
                    counter += 1
                try:
                    os.rename(src, dst)
                except OSError:
                    pass
        return len(new_files)

    def _finish(self, code):
        self.process = None
        self.cancel_btn.configure(state="disabled")
        if code == 0:
            count = self._rename_new_files()
            self._append(f"\n[OK] Proceso terminado. {count} archivo(s) nuevo(s).\n", "ok")
            self.result_title.configure(text=I18N[self.lang]["done"], style="Title.TLabel")
            plural = "s" if count != 1 else ""
            detail = I18N[self.lang]["result_ok"].format(count=count, plural=plural, dest=self._dest_dir)
            if self.rename_board.get() and count:
                detail += I18N[self.lang]["result_prefix"].format(slug=self._board_slug)
            self.result_detail.configure(text=detail)
            self.open_folder_btn.configure(state="normal")
        else:
            self._append(f"\n[i] Proceso termino con codigo {code}.\n")
            self.result_title.configure(text=I18N[self.lang]["problem"], style="ErrorTitle.TLabel")
            self.result_detail.configure(text=I18N[self.lang]["result_fail"].format(code=code))
            self.open_folder_btn.configure(state="disabled")
        self._show_step("result")

    def _cancel_download(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self._append("\n[!] Cancelado por el usuario.\n")
        self._ticking = False
        self.progress.configure(style="Gray.Horizontal.TProgressbar", value=0)
        self.cancel_btn.configure(state="disabled")
        self._show_step("options")


if __name__ == "__main__":
    if FROZEN and len(sys.argv) > 1 and sys.argv[1] == "--pinterest-dl-cli":
        # El propio .exe se relanzo a si mismo con esta bandera interna (ver
        # pinterest_dl_base_cmd): en vez de abrir la ventana, actua como el
        # comando "pinterest-dl" de verdad. Necesario porque un .exe de
        # PyInstaller no trae un interprete "python" utilizable por fuera.
        sys.argv = ["pinterest-dl"] + sys.argv[2:]
        from pinterest_dl.cli import main as _pinterest_dl_main
        _pinterest_dl_main()
        sys.exit(0)

    app = PinterestGUI()
    app.mainloop()
