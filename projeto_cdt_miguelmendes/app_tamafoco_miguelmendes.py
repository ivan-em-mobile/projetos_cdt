"""
Tamagotchi da Produtividade

Versão ampliada do projeto original, mantendo a ideia e as funções existentes.
As novas funções foram organizadas em abas e em blocos comentados para facilitar
a identificação e futuras alterações por estudantes iniciantes.
"""

# =============================================================================
# BLOCO 1 — IMPORTAÇÕES
# =============================================================================
import json
import os
import subprocess
import sys
import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import messagebox, ttk

try:
    from PIL import Image, ImageDraw, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

try:
    import pygetwindow as gw
    PYGETWINDOW_AVAILABLE = True
except ImportError:
    PYGETWINDOW_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


# =============================================================================
# BLOCO 2 — CONFIGURAÇÕES DE ATIVIDADE, PONTOS E NÍVEIS
# =============================================================================
DISTRACTION_KEYWORDS = ["instagram", "tiktok", "whatsapp", "youtube"]
PRODUCTIVE_KEYWORDS = ["visual studio code", "vscode", "github desktop", "github"]

PRODUCTIVE_PROCESS_NAMES = ["github desktop", "githubdesktop", "code", "code - insiders"]
DISTRACTION_PROCESS_NAMES = ["whatsapp", "tiktok", "instagram", "youtube"]

POLL_INTERVAL_MS = 3000
TICK_SECONDS = POLL_INTERVAL_MS / 1000
DECAY_PER_TICK = 0.5
BOOST_PRODUCTIVE = 2.5
PENALTY_DISTRACTION = 4.0

XP_PER_PRODUCTIVE_TICK = 10
POINTS_PER_PRODUCTIVE_TICK = 2
CRITICAL_HAPPINESS = 15
FOCUS_BREAK_MINUTES = 25

def base_dir():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def resource_path(*parts):
    return os.path.join(base_dir(), *parts)


def state_path():
    if getattr(sys, "frozen", False):
        appdata = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
        folder = os.path.join(appdata, "TamagotchiProdutividade")
        os.makedirs(folder, exist_ok=True)
        return os.path.join(folder, "tamagotchi_state.json")
    return os.path.join(base_dir(), "tamagotchi_state.json")


STATE_FILE = state_path()


def xp_needed_for_level(level):
    """Aumenta levemente a dificuldade a cada nível."""
    return 100 + ((level - 1) * 25)


# =============================================================================
# BLOCO 3 — CATÁLOGOS DE MASCOTES, ACESSÓRIOS, PRÊMIOS E CONQUISTAS
# =============================================================================
PETS = {
    "tradicional": {"name": "Tradicional", "icon": "🐣", "unlock": "Inicial"},
    "gato": {"name": "Gato", "icon": "🐱", "unlock": "Nível 2"},
    "cachorro": {"name": "Cachorro", "icon": "🐶", "unlock": "Nível 3"},
    "coelho": {"name": "Coelho", "icon": "🐰", "unlock": "Nível 4"},
    "raposa": {"name": "Raposa", "icon": "🦊", "unlock": "Loja"},
    "panda": {"name": "Panda", "icon": "🐼", "unlock": "Loja"},
}

ACCESSORIES = {
    "nenhum": {"name": "Sem acessório", "icon": "—"},
    "oculos": {"name": "Óculos", "icon": "👓"},
    "bone": {"name": "Boné", "icon": "🧢"},
    "laco": {"name": "Laço", "icon": "🎀"},
    "coroa": {"name": "Coroa", "icon": "👑"},
}

REWARDS = [
    {"id": "acc_oculos", "name": "Óculos do mascote", "cost": 80, "level": 1,
     "type": "accessory", "value": "oculos", "status": "disponivel"},
    {"id": "acc_bone", "name": "Boné do mascote", "cost": 120, "level": 2,
     "type": "accessory", "value": "bone", "status": "disponivel"},
    {"id": "acc_laco", "name": "Laço do mascote", "cost": 140, "level": 2,
     "type": "accessory", "value": "laco", "status": "disponivel"},
    {"id": "acc_coroa", "name": "Coroa do mascote", "cost": 250, "level": 4,
     "type": "accessory", "value": "coroa", "status": "disponivel"},
    {"id": "pet_raposa", "name": "Mascote Raposa", "cost": 350, "level": 5,
     "type": "pet", "value": "raposa", "status": "disponivel"},
    {"id": "pet_panda", "name": "Mascote Panda", "cost": 450, "level": 7,
     "type": "pet", "value": "panda", "status": "disponivel"},
    {"id": "gift_xbox", "name": "Cartão Xbox", "cost": 1000, "level": 10,
     "type": "external", "value": "xbox", "status": "em_breve"},
    {"id": "gift_psn", "name": "Cartão PlayStation", "cost": 1000, "level": 10,
     "type": "external", "value": "psn", "status": "em_breve"},
    {"id": "gift_centauro", "name": "Cartão Centauro", "cost": 1000, "level": 10,
     "type": "external", "value": "centauro", "status": "em_breve"},
    {"id": "gift_microsoft", "name": "Cartão Microsoft", "cost": 1000, "level": 10,
     "type": "external", "value": "microsoft", "status": "em_breve"},
    {"id": "gift_roblox", "name": "Cartão Roblox", "cost": 1000, "level": 10,
     "type": "external", "value": "roblox", "status": "em_breve"},
    {"id": "brinde_fisico", "name": "Brinde físico", "cost": 700, "level": 8,
     "type": "external", "value": "brinde", "status": "em_breve"},
]

ACHIEVEMENTS = [
    {"id": "first_focus", "name": "Primeiro foco", "description": "Complete sua primeira atividade produtiva.", "points": 20},
    {"id": "level_2", "name": "Subindo de nível", "description": "Alcance o nível 2.", "points": 30},
    {"id": "one_hour", "name": "Uma hora produtiva", "description": "Acumule 60 minutos de foco.", "points": 60},
    {"id": "goal_done", "name": "Meta cumprida", "description": "Complete uma meta diária de foco.", "points": 50},
    {"id": "streak_3", "name": "Sequência de 3 dias", "description": "Tenha atividade produtiva por 3 dias seguidos.", "points": 80},
    {"id": "first_reward", "name": "Primeiro resgate", "description": "Resgate sua primeira recompensa.", "points": 25},
    {"id": "collector", "name": "Colecionador", "description": "Desbloqueie 3 acessórios.", "points": 100},
]


# =============================================================================
# BLOCO 4 — PALETA VISUAL E FONTES
# =============================================================================
THEMES = {
    # Cores suaves e cartões brancos inspirados na organização do Microsoft Rewards.
    "claro": {
        "bg": "#f4f7fb", "card": "#ffffff", "card_border": "#dce4ef",
        "screen": "#e8f3ff", "screen_dark": "#d9eafc", "outline": "#162b47",
        "text": "#18263a", "text_muted": "#61748d", "cream": "#ffffff",
        "primary": "#0867d8", "primary_dark": "#074fa6", "primary_light": "#e6f1ff",
        "cyan": "#0867d8", "yellow": "#efb92d", "track": "#e9eef5",
        "success": "#138a5c", "warning": "#a36d00", "danger": "#c2354b",
        "warning_bg": "#fff5d8", "warning_fg": "#805600",
    },
    "escuro": {
        "bg": "#111827", "card": "#1f2b3d", "card_border": "#33465e",
        "screen": "#173251", "screen_dark": "#111f34", "outline": "#081525",
        "text": "#f5f8fc", "text_muted": "#b3c3d6", "cream": "#ffffff",
        "primary": "#1163c4", "primary_dark": "#0c4d9e", "primary_light": "#304660",
        "cyan": "#8bc4ff", "yellow": "#ffc94c", "track": "#334155",
        "success": "#59d3a5", "warning": "#f6c453", "danger": "#ff8091",
        "warning_bg": "#42371f", "warning_fg": "#ffdb80",
    },
}
COLORS = THEMES["claro"].copy()
ASSET_DIR = resource_path("assets")

MOOD_COLORS = {
    # O mascote mantém a identidade branca e azul, mudando os detalhes pelo humor.
    "euforico": {"body": "#f9f8de", "light": "#52cfff", "aura": "#fff06a"},
    "feliz": {"body": "#f9f8de", "light": "#61d8ff", "aura": "#7de9ff"},
    "neutro": {"body": "#eef7ea", "light": "#5ab9f6", "aura": "#4d9fda"},
    "triste": {"body": "#c9d9e4", "light": "#6d93bd", "aura": "#294f7d"},
    "doente": {"body": "#d8c6d1", "light": "#bd6c87", "aura": "#6e2949"},
    "irritado": {"body": "#f1d8ce", "light": "#ff7990", "aura": "#9a294a"},
}

# Segoe UI oferece leitura limpa e combina com a nova interface tridimensional.
FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 15, "bold")
FONT_STATUS = (FONT_FAMILY, 13, "bold")
FONT_SUB = (FONT_FAMILY, 9)
FONT_SMALL = (FONT_FAMILY, 8)
FONT_BTN = (FONT_FAMILY, 9, "bold")


# =============================================================================
# BLOCO 5 — DETECÇÃO DA JANELA E DO PROCESSO ATIVO
# =============================================================================
def get_active_window_title():
    if PYGETWINDOW_AVAILABLE:
        try:
            window = gw.getActiveWindow()
            if window and window.title:
                return window.title
        except Exception:
            pass

    try:
        if sys.platform == "darwin":
            script = ('tell application "System Events" to get name of first '
                      'application process whose frontmost is true')
            return subprocess.check_output(["osascript", "-e", script]).decode().strip()
        if sys.platform.startswith("linux"):
            return subprocess.check_output(
                ["xdotool", "getactivewindow", "getwindowname"]
            ).decode().strip()
    except Exception:
        return None
    return None


def get_active_process_name():
    if not PSUTIL_AVAILABLE:
        return None
    try:
        if sys.platform == "win32":
            import ctypes
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            pid = ctypes.c_ulong()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            return psutil.Process(pid.value).name().lower()
        if sys.platform == "darwin":
            script = ('tell application "System Events" to get name of first '
                      'application process whose frontmost is true')
            return subprocess.check_output(["osascript", "-e", script]).decode().strip().lower()
        if sys.platform.startswith("linux"):
            pid = int(subprocess.check_output(
                ["xdotool", "getactivewindow", "getwindowpid"]
            ).decode().strip())
            return psutil.Process(pid).name().lower()
    except Exception:
        return None
    return None


def classify_activity(title, process_name):
    title_lower = (title or "").lower()
    process_lower = (process_name or "").lower()

    if any(word in title_lower for word in DISTRACTION_KEYWORDS):
        return "distracao", title or "aplicativo de distração"
    if any(word in title_lower for word in PRODUCTIVE_KEYWORDS):
        return "produtivo", title or "aplicativo produtivo"
    if any(word in process_lower for word in DISTRACTION_PROCESS_NAMES):
        return "distracao", title or process_name or "aplicativo de distração"
    if any(word in process_lower for word in PRODUCTIVE_PROCESS_NAMES):
        return "produtivo", title or process_name or "aplicativo produtivo"
    return "neutro", title or "sem atividade identificada"


# =============================================================================
# BLOCO 6 — NOTIFICAÇÕES
# =============================================================================
def try_send_notification(title, message):
    if not PLYER_AVAILABLE:
        return False, "Instale a biblioteca com: pip install plyer"
    try:
        notification.notify(title=title, message=message,
                            app_name="Tamagotchi de Produtividade", timeout=8)
        return True, None
    except Exception as error:
        return False, f"{type(error).__name__}: {error}"


def platform_notification_tips():
    if sys.platform == "darwin":
        return "Ative as notificações do Terminal/Python nos Ajustes do Sistema."
    if sys.platform == "win32":
        return "Ative as notificações e desative a Assistência de Foco do Windows."
    return "No Linux, instale o pacote notify-send (libnotify-bin)."


# =============================================================================
# BLOCO 7 — ESTADO PADRÃO E PERSISTÊNCIA EM JSON
# =============================================================================
def default_state():
    return {
        "happiness": 70, "xp": 0, "level": 1, "points": 0,
        "name": "", "appearance": "tradicional", "accessory": "nenhum",
        "owner_name": "", "owner_nickname": "", "owner_age": "",
        "unlocked_pets": ["tradicional"], "unlocked_accessories": ["nenhum"],
        "redeemed_rewards": [], "achievements": [], "point_history": [],
        "time_history": {}, "daily_goal_minutes": 30,
        "goal_reward_dates": [], "streak": 0, "last_productive_date": "",
        "total_productive_seconds": 0,
        "floating_x": None, "floating_y": None,
        "theme": "claro",
    }


def load_state():
    """Lê o arquivo antigo e completa automaticamente os novos campos."""
    state = default_state()
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                saved = json.load(file)
            for key in state:
                if key in saved:
                    state[key] = saved[key]
        except (OSError, json.JSONDecodeError):
            pass
    return state


def write_state(state):
    try:
        directory = os.path.dirname(STATE_FILE) or "."
        os.makedirs(directory, exist_ok=True)
        state["updated"] = datetime.now().isoformat()
        with open(STATE_FILE, "w", encoding="utf-8") as file:
            json.dump(state, file, ensure_ascii=False, indent=2)
    except OSError:
        pass


# =============================================================================
# BLOCO 8 — COMPONENTES VISUAIS REUTILIZÁVEIS
# =============================================================================
def rounded_rect_points(x1, y1, x2, y2, radius):
    radius = max(1, min(radius, (x2 - x1) / 2, (y2 - y1) / 2))
    return [x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
            x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
            x1, y2 - radius, x1, y1 + radius, x1, y1]


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, bg=None, fg="#ffffff",
                 hover_bg=None, width=140, height=34, font=FONT_BTN, parent_bg=None):
        bg = bg or COLORS["primary"]
        parent_color = parent_bg if parent_bg is not None else parent["bg"]
        super().__init__(parent, width=width, height=height, bg=parent_color,
                         highlightthickness=0)
        self.command = command
        self.bg_color = bg
        self.hover_bg = hover_bg or bg
        self.fg = fg
        self.font = font
        self.button_width = width
        self.button_height = height
        self.text = text
        self.text_id = None
        self._render(bg)
        if command:
            self.configure(cursor="hand2")
            self.bind("<Button-1>", lambda _event: self.command())
            self.bind("<Enter>", lambda _event: self._render(self.hover_bg))
            self.bind("<Leave>", lambda _event: self._render(self.bg_color))

    def _render(self, color):
        self.delete("all")
        radius = self.button_height / 2
        # Sombra inferior cria profundidade; o brilho superior dá acabamento 3D.
        self.create_polygon(
            rounded_rect_points(2, 5, self.button_width - 2,
                                self.button_height - 1, radius),
            smooth=True, fill=COLORS["outline"], outline=""
        )
        self.create_polygon(
            rounded_rect_points(1, 1, self.button_width - 3,
                                self.button_height - 5, radius),
            smooth=True, fill=color, outline=COLORS["cyan"], width=1
        )
        self.create_line(12, 5, self.button_width - 14, 5,
                         fill="#8deeff", width=1)
        self.text_id = self.create_text(
            self.button_width / 2 - 1, self.button_height / 2 - 2,
            text=self.text, fill=self.fg, font=self.font
        )

    def set_text(self, text):
        self.text = text
        self._render(self.bg_color)


class RoundedBar(tk.Canvas):
    def __init__(self, parent, width, height, track_color, fill_color,
                 bg, text_fg="#ffffff"):
        super().__init__(parent, width=width, height=height, bg=bg,
                         highlightthickness=0)
        self.bar_width = width
        self.bar_height = height
        self.fill_color = fill_color
        self.text_fg = text_fg
        self.track_color = track_color
        self.create_polygon(
            rounded_rect_points(1, 1, width - 1, height - 1, height / 2),
            smooth=True, fill=track_color, outline="#2a69a7", width=1
        )
        self.fill_id = None
        self.text_id = self.create_text(width / 2, height / 2, text="",
                                        font=FONT_SMALL, fill=text_fg)

    def set(self, fraction, text="", fill_color=None):
        fraction = max(0.0, min(1.0, fraction))
        if self.fill_id is not None:
            self.delete(self.fill_id)
        final_width = 1 + (self.bar_width - 2) * fraction
        self.fill_id = None
        if final_width > 5:
            self.fill_id = self.create_polygon(
                rounded_rect_points(3, 3, final_width,
                                    self.bar_height - 3, self.bar_height / 2),
                smooth=True, fill=fill_color or self.fill_color, outline=""
            )
        self.itemconfig(self.text_id, text=text)
        self.tag_raise(self.text_id)


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def seconds_to_text(seconds):
    minutes = int(seconds // 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes:02d}min" if hours else f"{minutes} min"


def blend_color(color_a, color_b, amount):
    """Mistura duas cores hexadecimais para criar gradientes e volume."""
    amount = max(0.0, min(1.0, amount))
    first = tuple(int(color_a[index:index + 2], 16) for index in (1, 3, 5))
    second = tuple(int(color_b[index:index + 2], 16) for index in (1, 3, 5))
    mixed = tuple(round(a + (b - a) * amount) for a, b in zip(first, second))
    return "#{:02x}{:02x}{:02x}".format(*mixed)


class SmoothCanvas:
    """Canvas transparente em alta resolução usado para remover serrilhados."""
    def __init__(self, width, height, scale=4):
        self.scale = scale
        self.image = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)

    def _coords(self, values):
        return tuple(round(value * self.scale) for value in values)

    def _width(self, value):
        return max(1, round(value * self.scale))

    def create_oval(self, x1, y1, x2, y2, fill="", outline="", width=1, **_kwargs):
        self.draw.ellipse(
            self._coords((x1, y1, x2, y2)),
            fill=fill or None, outline=outline or None,
            width=self._width(width) if outline else 1,
        )

    def create_polygon(self, coordinates, fill="", outline="", width=1, **_kwargs):
        points = [
            (round(coordinates[index] * self.scale), round(coordinates[index + 1] * self.scale))
            for index in range(0, len(coordinates), 2)
        ]
        self.draw.polygon(points, fill=fill or None, outline=outline or None)
        if outline and width > 1:
            self.draw.line(points + [points[0]], fill=outline,
                           width=self._width(width), joint="curve")

    def create_line(self, *coordinates, fill="", width=1, **_kwargs):
        self.draw.line(self._coords(coordinates), fill=fill or None,
                       width=self._width(width), joint="curve")

    def create_arc(self, x1, y1, x2, y2, start=0, extent=90,
                   style="arc", fill="", outline="", width=1, **_kwargs):
        box = self._coords((x1, y1, x2, y2))
        end = start + extent
        if style == "pieslice":
            self.draw.pieslice(box, start=start, end=end, fill=fill or None,
                               outline=outline or None, width=self._width(width))
        else:
            self.draw.arc(box, start=start, end=end, fill=outline or fill,
                          width=self._width(width))

    def photo(self, width, height):
        resized = self.image.resize((width, height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized)


# =============================================================================
# BLOCO 9 — JANELA PRINCIPAL E NAVEGAÇÃO POR ABAS
# =============================================================================
class Tamagotchi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TAMAGOTCHI • Productivity Quest")
        self.geometry("940x840")
        self.minsize(860, 760)
        self.configure(bg=COLORS["bg"])

        self.state_data = load_state()
        # Mantém a escolha do usuário em futuras inicializações.
        self.theme_name = self.state_data.get("theme", "claro")
        if self.theme_name not in THEMES:
            self.theme_name = "claro"
        COLORS.update(THEMES[self.theme_name])
        self.configure(bg=COLORS["bg"])
        self.catalog_images = {}
        self.load_catalog_images()
        self.notified_critical = False
        self.break_notified = False
        self.continuous_focus_seconds = 0
        self.last_category = "neutro"
        self.speech_text = "Vamos manter o foco hoje?"

        # Variáveis usadas pelo modo flutuante do mascote.
        self.floating_window = None
        self.floating_canvas = None
        self.floating_drag_x = 0
        self.floating_drag_y = 0
        self.floating_transparent_color = "#010203"

        self.setup_styles()
        self.create_tabs()

        # Detecta o clique no botão de minimizar da janela principal.
        self.bind("<Unmap>", self.on_root_unmap)
        self.protocol("WM_DELETE_WINDOW", self.close_app)

        if not self.state_data["owner_name"]:
            self.after(200, lambda: self.ask_profile_setup(first_time=True))

        self.refresh_all()
        self.after(300, self.start_polling)

    # -------------------------------------------------------------------------
    # CÉLULA 9.1 — Estilo das abas
    # -------------------------------------------------------------------------
    def setup_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TNotebook", background=COLORS["bg"], borderwidth=0,
                        tabmargins=(4, 4, 4, 0))
        style.configure("TNotebook.Tab", font=(FONT_FAMILY, 9, "bold"),
                        padding=(17, 11), background=COLORS["card"],
                        foreground=COLORS["text_muted"], borderwidth=0)
        style.map(
            "TNotebook.Tab",
            background=[("selected", COLORS["primary_light"]), ("active", COLORS["primary_light"])],
            foreground=[("selected", COLORS["primary"]), ("active", COLORS["primary"])]
        )

    def build_brand_header(self):
        """Cabeçalho simples: marca à esquerda e seletor de tema à direita."""
        self.brand_header = tk.Frame(self, bg=COLORS["bg"])
        self.brand_header.pack(fill="x", padx=22, pady=(18, 8))
        title = tk.Frame(self.brand_header, bg=COLORS["bg"])
        title.pack(side="left")
        tk.Label(title, text="Tamagotchi", font=(FONT_FAMILY, 21, "bold"),
                 fg=COLORS["text"], bg=COLORS["bg"]).pack(anchor="w")
        tk.Label(title, text="Seu foco também merece recompensas",
                 font=FONT_SUB, fg=COLORS["text_muted"], bg=COLORS["bg"]).pack(anchor="w")
        next_theme = "escuro" if self.theme_name == "claro" else "claro"
        label = "☾  Modo escuro" if next_theme == "escuro" else "☀  Modo claro"
        tk.Button(self.brand_header, text=label, command=self.toggle_theme,
                  bg=COLORS["card"], fg=COLORS["text"], font=FONT_BTN,
                  activebackground=COLORS["primary_light"],
                  activeforeground=COLORS["text"], relief="flat", bd=0,
                  highlightbackground=COLORS["card_border"], cursor="hand2",
                  padx=15, pady=9).pack(side="right", pady=5)

    def toggle_theme(self):
        """Reconstrói as telas mantendo a aba atual e os dados do perfil."""
        selected_tab = self.notebook.index(self.notebook.select())
        self.theme_name = "escuro" if self.theme_name == "claro" else "claro"
        self.state_data["theme"] = self.theme_name
        COLORS.update(THEMES[self.theme_name])
        self.configure(bg=COLORS["bg"])
        self.notebook.destroy()
        self.brand_header.destroy()
        self.setup_styles()
        self.create_tabs()
        self.notebook.select(selected_tab)
        self.save_and_refresh()

    def load_catalog_images(self):
        """Reduz as artes de alta resolução com antialiasing para a interface."""
        for category, keys in (
            ("pets", PETS), ("accessories", ACCESSORIES),
            ("rewards", {reward["id"]: reward for reward in REWARDS}),
        ):
            for key in keys:
                path = os.path.join(ASSET_DIR, category, f"{key}.png")
                try:
                    if PIL_AVAILABLE:
                        source = Image.open(path).convert("RGBA")
                        source = source.resize((150, 94), Image.Resampling.LANCZOS)
                        image = ImageTk.PhotoImage(source)
                    else:
                        # A aplicação continua abrindo; o README orienta instalar Pillow.
                        source = tk.PhotoImage(file=path)
                        factor = max(1, round(source.width() / 150))
                        image = source.subsample(factor, factor)
                    self.catalog_images[(category, key)] = image
                except (tk.TclError, OSError):
                    self.catalog_images[(category, key)] = None

    # -------------------------------------------------------------------------
    # CÉLULA 9.2 — Criação das seis abas
    # -------------------------------------------------------------------------
    def create_tabs(self):
        self.build_brand_header()
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=14, pady=(4, 14))

        self.home_tab = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.progress_tab = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.rewards_tab = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.custom_tab = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.time_tab = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.achievements_tab = tk.Frame(self.notebook, bg=COLORS["bg"])

        self.notebook.add(self.home_tab, text="Início")
        self.notebook.add(self.progress_tab, text="Progresso")
        self.notebook.add(self.rewards_tab, text="Recompensas")
        self.notebook.add(self.custom_tab, text="Personalizar")
        self.notebook.add(self.time_tab, text="Tempo")
        self.notebook.add(self.achievements_tab, text="Conquistas")

        self.build_home_tab()
        self.build_progress_tab()
        self.build_rewards_tab()
        self.build_custom_tab()
        self.build_time_tab()
        self.build_achievements_tab()

        # A rolagem funciona mesmo quando o ponteiro está sobre imagens,
        # textos ou botões dos catálogos de recompensas e personalização.
        self.bind_all("<MouseWheel>", self.scroll_active_catalog)
        self.bind_all("<Button-4>", self.scroll_active_catalog)
        self.bind_all("<Button-5>", self.scroll_active_catalog)

    def scroll_active_catalog(self, event):
        """Rola o catálogo visível com a roda do mouse em qualquer sistema."""
        try:
            selected_tab = self.notebook.index(self.notebook.select())
        except tk.TclError:
            return None

        # Índices definidos em create_tabs: Recompensas = 2, Personalizar = 3.
        canvas = {2: self.rewards_scroll, 3: self.custom_scroll}.get(selected_tab)
        if canvas is None:
            return None

        if getattr(event, "num", None) == 4:       # Linux: roda para cima.
            direction = -1
        elif getattr(event, "num", None) == 5:     # Linux: roda para baixo.
            direction = 1
        else:                                      # Windows e macOS.
            delta = getattr(event, "delta", 0)
            if not delta:
                return None
            direction = -1 if delta > 0 else 1

        canvas.yview_scroll(direction, "units")
        return "break"

    # =========================================================================
    # BLOCO 10 — ABA INÍCIO: TELA ORIGINAL DO MASCOTE
    # =========================================================================
    def build_home_tab(self):
        card = tk.Frame(self.home_tab, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=3)
        card.pack(fill="both", expand=True, padx=76, pady=14)

        header = tk.Frame(card, bg=COLORS["card"])
        header.pack(fill="x", pady=(16, 2))

        self.badge_level = RoundedButton(
            header, text="⭐ Nível 1", bg=COLORS["primary_light"],
            fg=COLORS["text"], width=120, height=30,
            parent_bg=COLORS["card"]
        )
        self.badge_level.pack(side="left", padx=(24, 6))

        self.badge_points = RoundedButton(
            header, text="◆ 0 pontos", bg=COLORS["primary_light"], fg=COLORS["cyan"],
            width=140, height=30, parent_bg=COLORS["card"]
        )
        self.badge_points.pack(side="right", padx=(6, 24))

        self.label_name = tk.Label(card, text="Tama", font=FONT_TITLE,
                                   fg=COLORS["text"], bg=COLORS["card"])
        self.label_name.pack(pady=(4, 0))

        self.canvas = tk.Canvas(card, width=560, height=270, bg=COLORS["screen"],
                                highlightbackground=COLORS["cyan"], highlightthickness=2)
        self.canvas.pack(pady=(2, 0))

        self.label_status = tk.Label(card, text="Iniciando...", font=FONT_STATUS,
                                     fg=COLORS["text"], bg=COLORS["card"])
        self.label_status.pack()
        self.label_app = tk.Label(card, text="", font=FONT_SUB,
                                  fg=COLORS["text_muted"], bg=COLORS["card"],
                                  wraplength=520)
        self.label_app.pack(pady=(2, 8))

        row = tk.Frame(card, bg=COLORS["card"])
        row.pack(pady=(0, 10))
        RoundedButton(row, "🔍 Diagnosticar", self.show_diagnostics,
                      bg=COLORS["primary_light"], fg=COLORS["text"], hover_bg=COLORS["primary_dark"],
                      width=150, height=32, parent_bg=COLORS["card"]).pack(side="left", padx=5)
        RoundedButton(row, "🔔 Testar notificação", self.test_notification,
                      bg=COLORS["primary_light"], fg=COLORS["text"], hover_bg=COLORS["primary_dark"],
                      width=170, height=32, parent_bg=COLORS["card"]).pack(side="left", padx=5)
        RoundedButton(row, "✏️ Editar perfil", self.ask_profile_setup,
                      width=145, height=32, parent_bg=COLORS["card"]).pack(side="left", padx=5)
        RoundedButton(row, "🐣 Modo flutuante", self.enter_floating_mode,
                      bg=COLORS["primary_light"], fg=COLORS["cyan"], hover_bg=COLORS["primary_dark"],
                      width=155, height=32, parent_bg=COLORS["card"]).pack(side="left", padx=5)

        tk.Label(card, text="FELICIDADE", font=(FONT_FAMILY, 8, "bold"),
                 fg=COLORS["text_muted"], bg=COLORS["card"]).pack(pady=(4, 2))
        self.bar_happiness = RoundedBar(card, 500, 24, COLORS["track"],
                                        COLORS["success"], COLORS["card"])
        self.bar_happiness.pack(pady=(0, 10))

        tk.Label(card, text="EXPERIÊNCIA", font=(FONT_FAMILY, 8, "bold"),
                 fg=COLORS["text_muted"], bg=COLORS["card"]).pack(pady=(0, 2))
        self.bar_xp = RoundedBar(card, 500, 16, COLORS["primary_light"],
                                 COLORS["primary"], COLORS["card"], COLORS["text"])
        self.bar_xp.pack()
        self.label_xp = tk.Label(card, text="", font=FONT_SMALL,
                                 fg=COLORS["text_muted"], bg=COLORS["card"])
        self.label_xp.pack(pady=(3, 10))

    # =========================================================================
    # BLOCO 11 — ABA PROGRESSO: PONTOS, NÍVEIS, META E SEQUÊNCIA
    # =========================================================================
    def build_progress_tab(self):
        header = tk.Frame(self.progress_tab, bg=COLORS["bg"])
        header.pack(fill="x", padx=22, pady=(22, 12))
        tk.Label(header, text="Seu progresso", font=(FONT_FAMILY, 18, "bold"),
                 fg=COLORS["text"], bg=COLORS["bg"]).pack(anchor="w")
        tk.Label(header, text="Acompanhe pontos, nível, foco e sequência diária.",
                 font=FONT_SUB, fg=COLORS["text_muted"], bg=COLORS["bg"]).pack(anchor="w")

        stats = tk.Frame(self.progress_tab, bg=COLORS["bg"])
        stats.pack(fill="x", padx=18)
        self.progress_cards = {}
        for column, (key, title) in enumerate([
            ("level", "NÍVEL"), ("points", "PONTOS"),
            ("focus", "FOCO TOTAL"), ("streak", "SEQUÊNCIA")
        ]):
            card = tk.Frame(stats, bg=COLORS["card"], highlightbackground=COLORS["card_border"],
                            highlightthickness=2, width=180, height=100)
            card.grid(row=0, column=column, padx=5, sticky="nsew")
            card.grid_propagate(False)
            stats.grid_columnconfigure(column, weight=1)
            tk.Label(card, text=title, font=(FONT_FAMILY, 8, "bold"),
                     fg=COLORS["text_muted"], bg=COLORS["card"]).pack(pady=(18, 5))
            value = tk.Label(card, text="—", font=(FONT_FAMILY, 17, "bold"),
                             fg=COLORS["cyan"], bg=COLORS["card"])
            value.pack()
            self.progress_cards[key] = value

        level_card = tk.Frame(self.progress_tab, bg=COLORS["card"],
                              highlightbackground=COLORS["card_border"], highlightthickness=2)
        level_card.pack(fill="x", padx=23, pady=14)
        tk.Label(level_card, text="PROGRESSO PARA O PRÓXIMO NÍVEL",
                 font=(FONT_FAMILY, 9, "bold"), fg=COLORS["text"],
                 bg=COLORS["card"]).pack(anchor="w", padx=18, pady=(16, 6))
        self.progress_level_bar = RoundedBar(level_card, 720, 24, COLORS["track"],
                                             COLORS["primary"], COLORS["card"])
        self.progress_level_bar.pack(pady=(0, 16))

        goal_card = tk.Frame(self.progress_tab, bg=COLORS["card"],
                             highlightbackground=COLORS["card_border"], highlightthickness=2)
        goal_card.pack(fill="x", padx=23)
        self.goal_title = tk.Label(goal_card, text="META DE HOJE", font=(FONT_FAMILY, 10, "bold"),
                                   fg=COLORS["text"], bg=COLORS["card"])
        self.goal_title.pack(anchor="w", padx=18, pady=(16, 6))
        self.progress_goal_bar = RoundedBar(goal_card, 720, 24, COLORS["track"],
                                            COLORS["success"], COLORS["card"])
        self.progress_goal_bar.pack(pady=(0, 10))
        self.goal_hint = tk.Label(goal_card, text="", font=FONT_SUB,
                                  fg=COLORS["text_muted"], bg=COLORS["card"])
        self.goal_hint.pack(anchor="w", padx=18, pady=(0, 16))

    # =========================================================================
    # BLOCO 12 — ABA RECOMPENSAS: LOJA E RESGATES
    # =========================================================================
    def build_rewards_tab(self):
        top = tk.Frame(self.rewards_tab, bg=COLORS["bg"])
        top.pack(fill="x", padx=22, pady=(20, 8))
        tk.Label(top, text="Resgatar recompensas", font=(FONT_FAMILY, 18, "bold"),
                 fg=COLORS["text"], bg=COLORS["bg"]).pack(side="left")
        self.rewards_points_label = tk.Label(
            top, text="◆ 0 pontos", font=(FONT_FAMILY, 11, "bold"),
            fg=COLORS["primary"], bg=COLORS["primary_light"], padx=14, pady=7
        )
        self.rewards_points_label.pack(side="right")

        tk.Label(self.rewards_tab,
                 text="Ganhe pontos com foco e escolha seus itens favoritos. Cartões presente são prévias de futuras parcerias.",
                 font=FONT_SUB, fg=COLORS["text_muted"], bg=COLORS["bg"]).pack(anchor="w", padx=23)

        # Rolagem mantém todo o catálogo acessível, inclusive em telas menores.
        container = tk.Frame(self.rewards_tab, bg=COLORS["bg"])
        container.pack(fill="both", expand=True, padx=18, pady=12)
        self.rewards_scroll = tk.Canvas(container, bg=COLORS["bg"],
                                        highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical",
                                  command=self.rewards_scroll.yview)
        self.rewards_scroll.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.rewards_scroll.pack(side="left", fill="both", expand=True)
        self.rewards_list = tk.Frame(self.rewards_scroll, bg=COLORS["bg"])
        self.rewards_window = self.rewards_scroll.create_window(
            (0, 0), window=self.rewards_list, anchor="nw"
        )
        self.rewards_list.bind(
            "<Configure>", lambda _event: self.rewards_scroll.configure(
                scrollregion=self.rewards_scroll.bbox("all")
            )
        )
        self.rewards_scroll.bind(
            "<Configure>", lambda event: self.rewards_scroll.itemconfigure(
                self.rewards_window, width=event.width
            )
        )

    def refresh_rewards_tab(self):
        scroll_position = self.rewards_scroll.yview()[0]
        clear_frame(self.rewards_list)
        self.rewards_points_label.config(text=f"◆ {self.state_data['points']} pontos")

        for index, reward in enumerate(REWARDS):
            row, column = divmod(index, 2)
            card = tk.Frame(self.rewards_list, bg=COLORS["card"],
                            highlightbackground=COLORS["card_border"], highlightthickness=1,
                            width=385, height=145)
            card.grid(row=row, column=column, padx=6, pady=6, sticky="nsew")
            card.grid_propagate(False)
            self.rewards_list.grid_columnconfigure(column, weight=1)

            image = self.catalog_images.get(("rewards", reward["id"]))
            if image:
                tk.Label(card, image=image, bg=COLORS["card"]).pack(side="left", padx=(10, 8))
            details = tk.Frame(card, bg=COLORS["card"])
            details.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=9)
            tk.Label(details, text=reward["name"], font=(FONT_FAMILY, 10, "bold"),
                     fg=COLORS["text"], bg=COLORS["card"],
                     wraplength=190, justify="left").pack(anchor="w")
            tk.Label(details, text=f"◆ {reward['cost']} pontos · Nível {reward['level']}",
                     font=FONT_SUB, fg=COLORS["text_muted"], bg=COLORS["card"]).pack(anchor="w", pady=(3, 5))

            owned = reward["id"] in self.state_data["redeemed_rewards"]
            if reward["status"] == "em_breve":
                text, color = "Em breve", COLORS["primary_light"]
            elif owned:
                text, color = "Resgatado", COLORS["primary_light"]
            elif self.state_data["level"] < reward["level"]:
                text, color = "Nível bloqueado", COLORS["primary_light"]
            else:
                text, color = "Resgatar", COLORS["primary"]

            button = tk.Button(
                details, text=text, font=FONT_BTN, bg=color,
                fg="#ffffff" if text == "Resgatar" else COLORS["text"],
                activebackground=COLORS["primary_dark"], activeforeground="#ffffff",
                bd=0, padx=12, pady=5, cursor="hand2",
                command=lambda selected=reward: self.redeem_reward(selected)
            )
            button.pack(anchor="w")
            if reward["status"] == "em_breve" or owned:
                button.config(state="disabled", disabledforeground=COLORS["text_muted"])
        self.rewards_scroll.update_idletasks()
        self.rewards_scroll.yview_moveto(scroll_position)

    # =========================================================================
    # BLOCO 13 — ABA PERSONALIZAÇÃO: MASCOTES E ACESSÓRIOS
    # =========================================================================
    def build_custom_tab(self):
        # Toda a página fica dentro de um Canvas para permanecer acessível em
        # notebooks e janelas menores, mesmo com várias imagens no catálogo.
        self._custom_signature = None
        container = tk.Frame(self.custom_tab, bg=COLORS["bg"])
        container.pack(fill="both", expand=True)

        self.custom_scroll = tk.Canvas(
            container, bg=COLORS["bg"], highlightthickness=0, bd=0
        )
        custom_scrollbar = ttk.Scrollbar(
            container, orient="vertical", command=self.custom_scroll.yview
        )
        self.custom_scroll.configure(yscrollcommand=custom_scrollbar.set)
        custom_scrollbar.pack(side="right", fill="y")
        self.custom_scroll.pack(side="left", fill="both", expand=True)

        self.custom_content = tk.Frame(self.custom_scroll, bg=COLORS["bg"])
        self.custom_window = self.custom_scroll.create_window(
            (0, 0), window=self.custom_content, anchor="nw"
        )
        self.custom_content.bind(
            "<Configure>", lambda _event: self.custom_scroll.configure(
                scrollregion=self.custom_scroll.bbox("all")
            )
        )
        self.custom_scroll.bind(
            "<Configure>", lambda event: self.custom_scroll.itemconfigure(
                self.custom_window, width=event.width
            )
        )

        tk.Label(self.custom_content, text="Personalize seu mascote",
                 font=(FONT_FAMILY, 18, "bold"), fg=COLORS["text"],
                 bg=COLORS["bg"]).pack(anchor="w", padx=23, pady=(22, 2))
        self.custom_status = tk.Label(self.custom_content, text="", font=FONT_SUB,
                                      fg=COLORS["text_muted"], bg=COLORS["bg"])
        self.custom_status.pack(anchor="w", padx=23, pady=(0, 12))

        self.pet_choices = tk.LabelFrame(
            self.custom_content, text="  MASCOTES  ", font=(FONT_FAMILY, 9, "bold"),
            fg=COLORS["text"], bg=COLORS["card"], bd=1, relief="solid",
            highlightbackground=COLORS["card_border"], padx=12, pady=12
        )
        self.pet_choices.pack(fill="x", padx=23, pady=(0, 14))

        self.accessory_choices = tk.LabelFrame(
            self.custom_content, text="  ACESSÓRIOS  ", font=(FONT_FAMILY, 9, "bold"),
            fg=COLORS["text"], bg=COLORS["card"], bd=1, relief="solid",
            highlightbackground=COLORS["card_border"], padx=12, pady=12
        )
        self.accessory_choices.pack(fill="x", padx=23)

        tk.Label(self.custom_content,
                 text="Dica: novos mascotes são liberados por nível ou pela Central de recompensas.",
                 font=FONT_SUB, fg=COLORS["text_muted"], bg=COLORS["bg"]).pack(anchor="w", padx=24, pady=14)

    def refresh_custom_tab(self):
        self.unlock_level_pets()
        current_pet = PETS[self.state_data["appearance"]]["name"]
        current_accessory = ACCESSORIES[self.state_data["accessory"]]["name"]
        self.custom_status.config(text=f"Em uso: {current_pet} • {current_accessory}")

        # O monitor atualiza o app periodicamente. Só reconstruímos os cartões
        # quando algo visual realmente muda, evitando saltos durante a rolagem.
        signature = (
            self.theme_name,
            self.state_data["appearance"],
            self.state_data["accessory"],
            tuple(self.state_data["unlocked_pets"]),
            tuple(self.state_data["unlocked_accessories"]),
            self.state_data["level"],
        )
        if signature == self._custom_signature:
            return

        scroll_position = self.custom_scroll.yview()[0]
        clear_frame(self.pet_choices)
        clear_frame(self.accessory_choices)

        for index, (pet_id, pet) in enumerate(PETS.items()):
            unlocked = pet_id in self.state_data["unlocked_pets"]
            selected = pet_id == self.state_data["appearance"]
            text = pet["name"]
            if not unlocked:
                text += f" · {pet['unlock']}"
            button = tk.Button(
                self.pet_choices, text=text, width=20,
                image=self.catalog_images.get(("pets", pet_id)), compound="top",
                font=FONT_BTN, bd=1, relief="solid", cursor="hand2",
                bg=COLORS["primary_light"] if selected else COLORS["card"],
                fg=COLORS["primary"] if selected else COLORS["text"],
                activebackground=COLORS["primary_light"],
                command=lambda selected_id=pet_id: self.select_pet(selected_id)
            )
            button.grid(row=index // 3, column=index % 3, padx=6, pady=6, sticky="nsew")
            self.pet_choices.grid_columnconfigure(index % 3, weight=1)

        for index, (accessory_id, accessory) in enumerate(ACCESSORIES.items()):
            unlocked = accessory_id in self.state_data["unlocked_accessories"]
            selected = accessory_id == self.state_data["accessory"]
            text = accessory["name"]
            if not unlocked:
                text += " · Loja"
            button = tk.Button(
                self.accessory_choices, text=text, width=20,
                image=self.catalog_images.get(("accessories", accessory_id)), compound="top",
                font=FONT_BTN, bd=1, relief="solid", cursor="hand2",
                bg=COLORS["primary_light"] if selected else COLORS["card"],
                fg=COLORS["primary"] if selected else COLORS["text"],
                activebackground=COLORS["primary_light"],
                command=lambda selected_id=accessory_id: self.select_accessory(selected_id)
            )
            button.grid(row=index // 3, column=index % 3, padx=6, pady=6, sticky="nsew")
            self.accessory_choices.grid_columnconfigure(index % 3, weight=1)

        self._custom_signature = signature
        self.custom_scroll.update_idletasks()
        self.custom_scroll.configure(scrollregion=self.custom_scroll.bbox("all"))
        self.custom_scroll.yview_moveto(scroll_position)

    # =========================================================================
    # BLOCO 14 — ABA TEMPO: USO DIÁRIO, SEMANAL, MENSAL E META
    # =========================================================================
    def build_time_tab(self):
        tk.Label(self.time_tab, text="Tempo e bem-estar",
                 font=(FONT_FAMILY, 18, "bold"), fg=COLORS["text"],
                 bg=COLORS["bg"]).pack(anchor="w", padx=23, pady=(22, 2))
        tk.Label(self.time_tab,
                 text="O aplicativo registra o tempo por categoria e lembra você de fazer pausas.",
                 font=FONT_SUB, fg=COLORS["text_muted"], bg=COLORS["bg"]).pack(anchor="w", padx=23)

        summary = tk.Frame(self.time_tab, bg=COLORS["bg"])
        summary.pack(fill="x", padx=18, pady=14)
        self.time_labels = {}
        for column, (key, title) in enumerate([
            ("today", "FOCO HOJE"), ("week", "FOCO NA SEMANA"), ("month", "FOCO NO MÊS")
        ]):
            card = tk.Frame(summary, bg=COLORS["card"],
                            highlightbackground=COLORS["card_border"], highlightthickness=2,
                            width=240, height=95)
            card.grid(row=0, column=column, padx=5, sticky="nsew")
            card.grid_propagate(False)
            summary.grid_columnconfigure(column, weight=1)
            tk.Label(card, text=title, font=(FONT_FAMILY, 8, "bold"),
                     fg=COLORS["text_muted"], bg=COLORS["card"]).pack(pady=(17, 4))
            label = tk.Label(card, text="0 min", font=(FONT_FAMILY, 16, "bold"),
                             fg=COLORS["cyan"], bg=COLORS["card"])
            label.pack()
            self.time_labels[key] = label

        goal = tk.Frame(self.time_tab, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=2)
        goal.pack(fill="x", padx=23, pady=(0, 14))
        tk.Label(goal, text="META DIÁRIA DE FOCO", font=(FONT_FAMILY, 9, "bold"),
                 fg=COLORS["text"], bg=COLORS["card"]).pack(anchor="w", padx=18, pady=(15, 4))
        row = tk.Frame(goal, bg=COLORS["card"])
        row.pack(anchor="w", padx=18, pady=(0, 15))
        self.goal_entry = tk.Entry(row, width=8, font=(FONT_FAMILY, 10), justify="center")
        self.goal_entry.pack(side="left", ipady=5)
        tk.Label(row, text="minutos por dia", font=FONT_SUB,
                 fg=COLORS["text_muted"], bg=COLORS["card"]).pack(side="left", padx=8)
        tk.Button(row, text="Salvar meta", command=self.save_daily_goal,
                  font=FONT_BTN, bg=COLORS["primary"], fg="#ffffff", bd=0,
                  padx=16, pady=6, cursor="hand2").pack(side="left", padx=8)

        details = tk.Frame(self.time_tab, bg=COLORS["card"],
                           highlightbackground=COLORS["card_border"], highlightthickness=2)
        details.pack(fill="both", expand=True, padx=23, pady=(0, 18))
        tk.Label(details, text="RESUMO DE HOJE", font=(FONT_FAMILY, 9, "bold"),
                 fg=COLORS["text"], bg=COLORS["card"]).pack(anchor="w", padx=18, pady=(15, 7))
        self.today_details = tk.Label(details, text="", font=(FONT_FAMILY, 10),
                                      fg=COLORS["text"], bg=COLORS["card"], justify="left")
        self.today_details.pack(anchor="w", padx=18)
        tk.Label(details,
                 text=f"Uma pausa amigável será sugerida após {FOCUS_BREAK_MINUTES} minutos seguidos de foco.",
                 font=FONT_SUB, fg=COLORS["text_muted"], bg=COLORS["card"]).pack(anchor="w", padx=18, pady=14)

    # =========================================================================
    # BLOCO 15 — ABA CONQUISTAS: MEDALHAS E RECOMPENSAS
    # =========================================================================
    def build_achievements_tab(self):
        tk.Label(self.achievements_tab, text="Conquistas",
                 font=(FONT_FAMILY, 18, "bold"), fg=COLORS["text"],
                 bg=COLORS["bg"]).pack(anchor="w", padx=23, pady=(22, 2))
        self.achievement_summary = tk.Label(self.achievements_tab, text="",
                                            font=FONT_SUB, fg=COLORS["text_muted"],
                                            bg=COLORS["bg"])
        self.achievement_summary.pack(anchor="w", padx=23, pady=(0, 10))
        self.achievement_list = tk.Frame(self.achievements_tab, bg=COLORS["bg"])
        self.achievement_list.pack(fill="both", expand=True, padx=18, pady=4)

    def refresh_achievements_tab(self):
        clear_frame(self.achievement_list)
        unlocked = self.state_data["achievements"]
        self.achievement_summary.config(
            text=f"{len(unlocked)} de {len(ACHIEVEMENTS)} conquistas desbloqueadas"
        )
        for index, achievement in enumerate(ACHIEVEMENTS):
            achieved = achievement["id"] in unlocked
            card = tk.Frame(self.achievement_list,
                            bg=COLORS["card"] if achieved else COLORS["screen_dark"],
                            highlightbackground=COLORS["success"] if achieved else COLORS["card_border"],
                            highlightthickness=2 if achieved else 1, height=72)
            card.pack(fill="x", padx=5, pady=5)
            card.pack_propagate(False)
            tk.Label(card, text="🏆" if achieved else "🔒", font=("Segoe UI Emoji", 22),
                     bg=card["bg"]).pack(side="left", padx=15)
            texts = tk.Frame(card, bg=card["bg"])
            texts.pack(side="left", fill="y", pady=11)
            tk.Label(texts, text=achievement["name"], font=(FONT_FAMILY, 10, "bold"),
                     fg=COLORS["text"], bg=card["bg"]).pack(anchor="w")
            tk.Label(texts, text=achievement["description"], font=FONT_SUB,
                     fg=COLORS["text_muted"], bg=card["bg"]).pack(anchor="w")
            tk.Label(card, text=f"+{achievement['points']} pontos",
                     font=(FONT_FAMILY, 9, "bold"),
                     fg=COLORS["success"] if achieved else COLORS["text_muted"],
                     bg=card["bg"]).pack(side="right", padx=16)

    # =========================================================================
    # BLOCO 16 — MODO FLUTUANTE, TRANSPARENTE E ARRASTÁVEL
    # =========================================================================
    def on_root_unmap(self, event):
        """Transforma o mascote em flutuante ao minimizar a janela principal."""
        if event.widget == self:
            # O pequeno atraso permite que o sistema termine a minimização.
            self.after(150, self.check_if_minimized)

    def check_if_minimized(self):
        """Confirma que a janela foi minimizada antes de ativar o pet."""
        try:
            if self.state() == "iconic":
                self.enter_floating_mode()
        except tk.TclError:
            pass

    def enter_floating_mode(self):
        """Esconde o painel completo e mostra somente o pet na área de trabalho."""
        if self.floating_window is not None:
            try:
                if self.floating_window.winfo_exists():
                    self.floating_window.deiconify()
                    self.floating_window.lift()
                    self.draw_floating_pet()
                    self.withdraw()
                    return
            except tk.TclError:
                self.floating_window = None
                self.floating_canvas = None

        # Retira a janela principal da tela e da barra de tarefas.
        self.withdraw()

        floating = tk.Toplevel(self)
        self.floating_window = floating
        floating.title("Mascote flutuante")
        floating.overrideredirect(True)       # Remove barra, moldura e botões.
        floating.configure(bg=self.floating_transparent_color)
        floating.attributes("-topmost", True)  # Mantém o pet sobre outros apps.

        # No Windows, esta cor desaparece completamente e somente o pet fica visível.
        try:
            floating.wm_attributes("-transparentcolor", self.floating_transparent_color)
        except tk.TclError:
            # Alternativa para sistemas que não oferecem transparentcolor.
            try:
                floating.attributes("-alpha", 0.98)
            except tk.TclError:
                pass

        # Evita criar um segundo botão do aplicativo na barra de tarefas do Windows.
        try:
            floating.wm_attributes("-toolwindow", True)
        except tk.TclError:
            pass

        size = 210
        saved_x = self.state_data.get("floating_x")
        saved_y = self.state_data.get("floating_y")
        if saved_x is None or saved_y is None:
            saved_x = max(10, self.winfo_screenwidth() - size - 35)
            saved_y = max(10, self.winfo_screenheight() - size - 75)
        floating.geometry(f"{size}x{size}+{int(saved_x)}+{int(saved_y)}")

        self.floating_canvas = tk.Canvas(
            floating, width=size, height=size,
            bg=self.floating_transparent_color,
            highlightthickness=0, bd=0
        )
        self.floating_canvas.pack(fill="both", expand=True)

        # Clique e arraste move o pet pela tela.
        self.floating_canvas.bind("<ButtonPress-1>", self.start_floating_drag)
        self.floating_canvas.bind("<B1-Motion>", self.move_floating_pet)
        self.floating_canvas.bind("<ButtonRelease-1>", self.finish_floating_drag)

        # Duplo clique restaura o aplicativo completo.
        self.floating_canvas.bind("<Double-Button-1>", self.restore_main_window)

        # Menu simples no botão direito, sem adicionar caixas visíveis ao pet.
        self.floating_menu = tk.Menu(floating, tearoff=0)
        self.floating_menu.add_command(label="Abrir aplicativo", command=self.restore_main_window)
        self.floating_menu.add_separator()
        self.floating_menu.add_command(label="Fechar aplicativo", command=self.close_app)
        self.floating_canvas.bind("<Button-3>", self.show_floating_menu)

        self.draw_floating_pet()
        floating.lift()

    def start_floating_drag(self, event):
        """Guarda o ponto exato em que o usuário segurou o mascote."""
        if self.floating_window is None:
            return
        self.floating_drag_x = event.x_root - self.floating_window.winfo_x()
        self.floating_drag_y = event.y_root - self.floating_window.winfo_y()

    def move_floating_pet(self, event):
        """Move a janela transparente junto com o ponteiro do mouse."""
        if self.floating_window is None:
            return
        new_x = event.x_root - self.floating_drag_x
        new_y = event.y_root - self.floating_drag_y
        self.floating_window.geometry(f"+{new_x}+{new_y}")

    def finish_floating_drag(self, _event=None):
        """Salva a posição escolhida para a próxima vez que o modo for aberto."""
        if self.floating_window is None:
            return
        try:
            self.state_data["floating_x"] = self.floating_window.winfo_x()
            self.state_data["floating_y"] = self.floating_window.winfo_y()
            write_state(self.state_data)
        except tk.TclError:
            pass

    def show_floating_menu(self, event):
        try:
            self.floating_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.floating_menu.grab_release()

    def restore_main_window(self, _event=None):
        """Esconde o pet flutuante e devolve o painel completo à tela."""
        if self.floating_window is not None:
            try:
                self.floating_window.withdraw()
            except tk.TclError:
                pass
        self.deiconify()
        self.lift()
        self.focus_force()

    def close_app(self):
        """Fecha corretamente tanto o modo completo quanto o flutuante."""
        write_state(self.state_data)
        if self.floating_window is not None:
            try:
                self.floating_window.destroy()
            except tk.TclError:
                pass
        self.destroy()

    def floating_activity_mood(self):
        """Escolhe a expressão usando o app aberto, e não apenas a felicidade."""
        if self.state_data["happiness"] <= CRITICAL_HAPPINESS:
            return "doente"
        if self.last_category == "produtivo":
            return "euforico"
        if self.last_category == "distracao":
            return "irritado"
        return "neutro"

    # O desenho anterior foi substituído pelo personagem tridimensional abaixo.

    # =========================================================================
    # BLOCO 17 — DESENHO E HUMOR DO MASCOTE NA JANELA PRINCIPAL
    # =========================================================================
    def current_mood(self):
        happiness = self.state_data["happiness"]
        if happiness >= 85:
            return "euforico"
        if happiness >= 60:
            return "feliz"
        if happiness >= 40:
            return "neutro"
        if happiness >= 25:
            return "triste"
        if happiness >= 15:
            return "irritado"
        return "doente"

    # A janela principal e o modo flutuante usam o mesmo desenho 3D.

    # =========================================================================
    # BLOCO 18 — MASCOTE COM VOLUME, LUZ E SOMBRA 3D
    # =========================================================================
    def draw_3d_pet(self, canvas, cx, cy, radius=68, mood=None, floating=False):
        """Desenha um mascote suave e tridimensional sem usar imagens pixeladas."""
        mood = mood or self.current_mood()
        colors = MOOD_COLORS[mood]
        appearance = self.state_data["appearance"]
        accessory = self.state_data["accessory"]
        scale = radius / 68
        dark = COLORS["outline"]

        def oval(x1, y1, x2, y2, fill, outline="", width=1):
            return canvas.create_oval(
                cx + x1 * scale, cy + y1 * scale,
                cx + x2 * scale, cy + y2 * scale,
                fill=fill, outline=outline, width=width
            )

        def polygon(points, fill, outline="", width=1, smooth=True):
            coordinates = []
            for x, y in points:
                coordinates.extend([cx + x * scale, cy + y * scale])
            return canvas.create_polygon(
                coordinates, fill=fill, outline=outline,
                width=width, smooth=smooth
            )

        # Sombra projetada reforça que o mascote está apoiado sobre a tela.
        if not floating:
            oval(-62, 60, 62, 82, "#03132c")
            oval(-47, 63, 47, 75, "#0a2447")

        # Orelhas são desenhadas antes do corpo para ficarem em segundo plano.
        if appearance in ("gato", "raposa"):
            ear = "#f49a55" if appearance == "raposa" else colors["light"]
            ear_shadow = blend_color(ear, dark, 0.35)
            polygon([(-53, -36), (-55, -94), (-15, -58)], ear_shadow, dark, 3)
            polygon([(53, -36), (55, -94), (15, -58)], ear_shadow, dark, 3)
            polygon([(-47, -43), (-49, -80), (-25, -57)],
                    blend_color(ear, "#ffffff", 0.35))
            polygon([(47, -43), (49, -80), (25, -57)],
                    blend_color(ear, "#ffffff", 0.35))
        elif appearance == "coelho":
            oval(-43, -118, -10, -31, blend_color(colors["body"], dark, 0.25), dark, 3)
            oval(10, -118, 43, -31, blend_color(colors["body"], dark, 0.25), dark, 3)
            oval(-36, -108, -17, -43, "#a9ddff")
            oval(17, -108, 36, -43, "#a9ddff")
            oval(-31, -101, -23, -62, "#e7f8ff")
            oval(23, -101, 31, -62, "#e7f8ff")
        elif appearance in ("cachorro", "panda"):
            ear = "#14213b" if appearance == "panda" else colors["light"]
            oval(-86, -54, -40, 17, blend_color(ear, dark, 0.35), dark, 3)
            oval(40, -54, 86, 17, blend_color(ear, dark, 0.35), dark, 3)
            oval(-78, -45, -47, 5, blend_color(ear, "#ffffff", 0.2))
            oval(47, -45, 78, 5, blend_color(ear, "#ffffff", 0.2))

        # Pequenos braços e pés acrescentam profundidade ao personagem.
        limb = blend_color(colors["body"], dark, 0.18)
        oval(-77, 8, -48, 52, limb, dark, 2)
        oval(48, 8, 77, 52, limb, dark, 2)
        oval(-47, 49, -7, 78, limb, dark, 2)
        oval(7, 49, 47, 78, limb, dark, 2)

        # Corpo principal: contorno, sombra inferior, cor e reflexos.
        body = COLORS["cream"] if appearance == "panda" else colors["body"]
        body_shadow = blend_color(body, dark, 0.28)
        oval(-69, -72, 69, 72, body_shadow, dark, 4)
        oval(-64, -68, 64, 65, body, "", 0)
        canvas.create_arc(
            cx - 64 * scale, cy - 68 * scale,
            cx + 64 * scale, cy + 65 * scale,
            start=180, extent=180, style="pieslice",
            fill=blend_color(body, colors["light"], 0.28), outline=""
        )
        oval(-45, -55, 17, -12, blend_color(body, "#ffffff", 0.58))
        oval(-37, -48, -9, -27, "#ffffff")

        # Manchas azuis suaves preservam a identidade do ovo original.
        spot = colors["light"]
        spot_light = blend_color(spot, "#ffffff", 0.35)
        for x1, y1, x2, y2 in [
            (-39, -60, -4, -35), (26, -48, 52, -17),
            (-58, 3, -34, 35), (31, 29, 56, 53), (-23, 45, 11, 66),
        ]:
            oval(x1, y1, x2, y2, spot)
            oval(x1 + 4, y1 + 3, x1 + (x2 - x1) * 0.55,
                 y1 + (y2 - y1) * 0.5, spot_light)

        if appearance == "panda":
            oval(-44, -29, -9, 8, "#17223b")
            oval(9, -29, 44, 8, "#17223b")

        # Expressões com curvas suaves e brilho nos olhos.
        if mood == "doente":
            for eye_x in (-28, 28):
                canvas.create_line(cx + (eye_x - 8) * scale, cy - 19 * scale,
                                   cx + (eye_x + 8) * scale, cy - 3 * scale,
                                   fill=dark, width=max(3, round(4 * scale)))
                canvas.create_line(cx + (eye_x + 8) * scale, cy - 19 * scale,
                                   cx + (eye_x - 8) * scale, cy - 3 * scale,
                                   fill=dark, width=max(3, round(4 * scale)))
        elif mood == "euforico":
            canvas.create_arc(cx - 40 * scale, cy - 28 * scale,
                              cx - 10 * scale, cy - 2 * scale,
                              start=5, extent=170, style="arc", outline=dark,
                              width=max(3, round(4 * scale)))
            canvas.create_arc(cx + 10 * scale, cy - 28 * scale,
                              cx + 40 * scale, cy - 2 * scale,
                              start=5, extent=170, style="arc", outline=dark,
                              width=max(3, round(4 * scale)))
        else:
            for eye_x in (-27, 27):
                oval(eye_x - 9, -24, eye_x + 9, -3, dark)
                oval(eye_x - 4, -21, eye_x + 2, -14, "#ffffff")
            if mood == "irritado":
                canvas.create_line(cx - 42 * scale, cy - 34 * scale,
                                   cx - 15 * scale, cy - 27 * scale,
                                   fill=COLORS["danger"], width=max(3, round(4 * scale)))
                canvas.create_line(cx + 15 * scale, cy - 27 * scale,
                                   cx + 42 * scale, cy - 34 * scale,
                                   fill=COLORS["danger"], width=max(3, round(4 * scale)))

        # Bochechas ajudam a expressão a ficar viva e tridimensional.
        cheek = "#ff9eb1" if mood in ("feliz", "euforico") else "#9bbbd1"
        oval(-51, 5, -31, 17, cheek)
        oval(31, 5, 51, 17, cheek)
        oval(-47, 6, -39, 10, blend_color(cheek, "#ffffff", 0.55))
        oval(39, 6, 47, 10, blend_color(cheek, "#ffffff", 0.55))

        # Nariz aparece somente nos animais escolhidos na personalização.
        if appearance != "tradicional":
            polygon([(-6, -2), (6, -2), (0, 6)], "#243047", dark, 1)

        if mood in ("feliz", "euforico"):
            canvas.create_arc(cx - 20 * scale, cy + 4 * scale,
                              cx + 20 * scale, cy + 32 * scale,
                              start=180, extent=180, style="pieslice",
                              fill="#ef6179", outline=dark, width=2)
            oval(-8, 18, 8, 28, "#ffb4bf")
        elif mood in ("triste", "irritado", "doente"):
            canvas.create_arc(cx - 20 * scale, cy + 13 * scale,
                              cx + 20 * scale, cy + 39 * scale,
                              start=0, extent=180, style="arc", outline=dark,
                              width=max(3, round(3 * scale)))
        else:
            canvas.create_line(cx - 13 * scale, cy + 18 * scale,
                               cx + 13 * scale, cy + 18 * scale,
                               fill=dark, width=max(3, round(3 * scale)), smooth=True)

        # Acessórios com sombra e brilho, coerentes com o novo acabamento 3D.
        if accessory == "oculos":
            for left, right in [(-51, -7), (7, 51)]:
                canvas.create_oval(cx + left * scale, cy - 31 * scale,
                                   cx + right * scale, cy + 3 * scale,
                                   outline="#18243b", width=max(3, round(4 * scale)))
            canvas.create_line(cx - 7 * scale, cy - 15 * scale,
                               cx + 7 * scale, cy - 15 * scale,
                               fill="#18243b", width=max(3, round(4 * scale)))
        elif accessory == "bone":
            oval(-50, -91, 50, -46, COLORS["primary_dark"], dark, 3)
            oval(-46, -88, 46, -52, COLORS["primary"])
            oval(-18, -82, 25, -68, "#78c7ff")
            oval(25, -65, 78, -50, COLORS["primary_dark"], dark, 2)
        elif accessory == "laco":
            polygon([(-13, -59), (-60, -86), (-53, -42), (-12, -52)],
                    COLORS["danger"], dark, 2)
            polygon([(-13, -59), (31, -86), (26, -42), (-12, -52)],
                    COLORS["danger"], dark, 2)
            oval(-25, -70, -4, -47, "#c92d63", dark, 2)
            oval(-20, -65, -10, -55, "#ffb2c2")
        elif accessory == "coroa":
            polygon([(-43, -64), (-38, -105), (-15, -83), (0, -112),
                     (16, -83), (40, -105), (43, -64)],
                    COLORS["yellow"], "#9d6c00", 3)
            oval(-27, -91, -17, -80, "#ffffff")

    def render_smooth_pet(self, width, height, radius, mood, floating=True):
        """Renderiza o pet em 4x e reduz com LANCZOS para ficar bem definido."""
        if not PIL_AVAILABLE:
            return None
        surface = SmoothCanvas(width, height, scale=4)
        self.draw_3d_pet(
            surface, width / 2, height / 2 + 3, radius=radius,
            mood=mood, floating=floating,
        )
        return surface.photo(width, height)

    def draw_floating_pet(self):
        """Mostra apenas o mascote 3D, transparente e sem caixa ao redor."""
        if self.floating_canvas is None:
            return
        try:
            if not self.floating_canvas.winfo_exists():
                return
        except tk.TclError:
            return
        self.floating_canvas.delete("all")
        mood = self.floating_activity_mood()
        photo = self.render_smooth_pet(210, 210, 66, mood, floating=True)
        if photo:
            self.floating_pet_photo = photo
            self.floating_canvas.create_image(105, 105, image=photo)
        else:
            self.draw_3d_pet(
                self.floating_canvas, 105, 108, radius=68,
                mood=mood, floating=True
            )

    def draw_pet(self):
        """Monta a tela principal com cenário suave e mascote tridimensional."""
        canvas = self.canvas
        canvas.delete("all")
        width, height = 560, 270

        # Gradiente vertical sem serrilhamento ou blocos visíveis.
        for y in range(height):
            color = blend_color("#1463a4", COLORS["screen_dark"], y / height)
            canvas.create_line(0, y, width, y, fill=color)
        canvas.create_rectangle(5, 5, width - 5, height - 5,
                                outline=COLORS["cyan"], width=2)

        # Luz difusa atrás do personagem e partículas arredondadas.
        for inset, color in [(0, "#244f79"), (22, "#376f93"), (44, "#5795a4")]:
            canvas.create_oval(165 + inset, 5 + inset / 2,
                               395 - inset, 218 - inset / 3,
                               fill=color, outline="")
        for index, (x, y, size) in enumerate([
            (48, 45, 4), (92, 88, 6), (139, 34, 3), (429, 43, 5),
            (475, 91, 3), (512, 35, 5), (107, 148, 4), (457, 148, 6),
        ]):
            color = COLORS["yellow"] if index % 3 == 0 else "#d9f8ff"
            canvas.create_oval(x - size, y - size, x + size, y + size,
                               fill=color, outline="")
            canvas.create_oval(x - size / 3, y - size / 2,
                               x + size / 4, y + size / 4,
                               fill="#ffffff", outline="")

        canvas.create_text(24, 24, text=f"Dia {max(1, self.state_data['streak'])}",
                           anchor="w", font=(FONT_FAMILY, 10, "bold"), fill="#ffffff")
        canvas.create_text(width - 24, 24, text="♡", anchor="e",
                           font=(FONT_FAMILY, 22, "bold"), fill=COLORS["cyan"])

        mood = self.current_mood()
        photo = self.render_smooth_pet(205, 215, 62, mood, floating=False)
        if photo:
            self.home_pet_photo = photo
            canvas.create_image(280, 124, image=photo)
        else:
            self.draw_3d_pet(canvas, 280, 126, radius=65, mood=mood)

        # Caixa de mensagem arredondada com sombra, contraste alto e texto legível.
        canvas.create_polygon(
            rounded_rect_points(35, 211, width - 29, 258, 16),
            smooth=True, fill="#00112f", outline=""
        )
        canvas.create_polygon(
            rounded_rect_points(31, 207, width - 33, 254, 16),
            smooth=True, fill="#ffffff", outline="#7be9ff", width=2
        )
        canvas.create_text(width / 2, 230, text=self.speech_text,
                           font=(FONT_FAMILY, 10, "bold"), fill="#09214b",
                           width=450, justify="center")

    # =========================================================================
    # BLOCO 19 — PERFIL DO USUÁRIO E DO MASCOTE
    # =========================================================================
    def ask_profile_setup(self, first_time=False):
        dialog = tk.Toplevel(self)
        dialog.title("Configurar perfil" if first_time else "Editar perfil")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.configure(bg=COLORS["bg"])
        dialog.geometry("390x455")

        card = tk.Frame(dialog, bg=COLORS["card"], highlightbackground=COLORS["card_border"],
                        highlightthickness=2)
        card.pack(fill="both", expand=True, padx=15, pady=15)
        tk.Label(card, text="✨ Seu perfil", font=(FONT_FAMILY, 14, "bold"),
                 fg=COLORS["text"], bg=COLORS["card"]).pack(pady=(18, 12))

        entries = {}
        fields = [
            ("owner_name", "SEU NOME", self.state_data["owner_name"]),
            ("owner_nickname", "APELIDO", self.state_data["owner_nickname"]),
            ("owner_age", "IDADE", self.state_data["owner_age"]),
            ("name", "NOME DO PET", self.state_data["name"]),
        ]
        for key, label_text, initial in fields:
            tk.Label(card, text=label_text, font=(FONT_FAMILY, 8, "bold"),
                     fg=COLORS["text_muted"], bg=COLORS["card"]).pack(anchor="w", padx=28)
            entry = tk.Entry(card, font=(FONT_FAMILY, 10), bg=COLORS["track"],
                             fg=COLORS["text"], bd=0)
            entry.pack(fill="x", padx=28, pady=(2, 10), ipady=6)
            entry.insert(0, initial)
            entries[key] = entry

        def save_profile():
            self.state_data["owner_name"] = entries["owner_name"].get().strip() or "Amigo"
            self.state_data["owner_nickname"] = entries["owner_nickname"].get().strip() or self.state_data["owner_name"]
            self.state_data["owner_age"] = entries["owner_age"].get().strip()
            self.state_data["name"] = entries["name"].get().strip() or "Tama"
            self.speech_text = f"Bem-vindo, {self.state_data['owner_nickname']}!"
            self.save_and_refresh()
            dialog.destroy()

        tk.Button(card, text="Confirmar", command=save_profile, font=FONT_BTN,
                  bg=COLORS["primary"], fg="#ffffff", bd=0, padx=60, pady=9,
                  cursor="hand2").pack(pady=(5, 12))
        entries["owner_name"].focus_set()

    # =========================================================================
    # BLOCO 18 — REGRAS DE PONTOS, NÍVEIS, METAS E CONQUISTAS
    # =========================================================================
    def add_points(self, amount, reason):
        self.state_data["points"] += amount
        history = self.state_data["point_history"]
        history.append({"date": datetime.now().isoformat(), "amount": amount, "reason": reason})
        self.state_data["point_history"] = history[-100:]

    def add_xp(self, amount):
        self.state_data["xp"] += amount
        leveled_up = False
        while self.state_data["xp"] >= xp_needed_for_level(self.state_data["level"]):
            self.state_data["xp"] -= xp_needed_for_level(self.state_data["level"])
            self.state_data["level"] += 1
            leveled_up = True
        if leveled_up:
            self.speech_text = f"Parabéns! Você chegou ao nível {self.state_data['level']}!"
            try_send_notification("⭐ Novo nível!", self.speech_text)
            self.unlock_level_pets()

    def unlock_level_pets(self):
        level = self.state_data["level"]
        for required_level, pet_id in [(2, "gato"), (3, "cachorro"), (4, "coelho")]:
            if level >= required_level and pet_id not in self.state_data["unlocked_pets"]:
                self.state_data["unlocked_pets"].append(pet_id)

    def check_achievements(self):
        conditions = {
            "first_focus": self.state_data["total_productive_seconds"] > 0,
            "level_2": self.state_data["level"] >= 2,
            "one_hour": self.state_data["total_productive_seconds"] >= 3600,
            "goal_done": bool(self.state_data["goal_reward_dates"]),
            "streak_3": self.state_data["streak"] >= 3,
            "first_reward": bool(self.state_data["redeemed_rewards"]),
            "collector": len(self.state_data["unlocked_accessories"]) >= 4,
        }
        for achievement in ACHIEVEMENTS:
            achievement_id = achievement["id"]
            if conditions[achievement_id] and achievement_id not in self.state_data["achievements"]:
                self.state_data["achievements"].append(achievement_id)
                self.add_points(achievement["points"], f"Conquista: {achievement['name']}")
                self.speech_text = f"Conquista desbloqueada: {achievement['name']}!"
                try_send_notification("🏆 Nova conquista", self.speech_text)

    def update_streak(self):
        today = date.today()
        today_text = today.isoformat()
        last_text = self.state_data["last_productive_date"]
        if last_text == today_text:
            return
        if last_text:
            try:
                last_date = date.fromisoformat(last_text)
                self.state_data["streak"] = self.state_data["streak"] + 1 if last_date == today - timedelta(days=1) else 1
            except ValueError:
                self.state_data["streak"] = 1
        else:
            self.state_data["streak"] = 1
        self.state_data["last_productive_date"] = today_text

    def check_daily_goal(self):
        today_text = date.today().isoformat()
        productive = self.today_time().get("produtivo", 0)
        goal_seconds = self.state_data["daily_goal_minutes"] * 60
        if productive >= goal_seconds and today_text not in self.state_data["goal_reward_dates"]:
            self.state_data["goal_reward_dates"].append(today_text)
            self.state_data["goal_reward_dates"] = self.state_data["goal_reward_dates"][-365:]
            self.add_points(50, "Meta diária concluída")
            self.add_xp(50)
            self.speech_text = "Meta diária concluída! Você ganhou 50 pontos."
            try_send_notification("🎯 Meta concluída", self.speech_text)

    # =========================================================================
    # BLOCO 19 — TEMPO DE USO E LEMBRETES DE PAUSA
    # =========================================================================
    def today_time(self):
        today_text = date.today().isoformat()
        history = self.state_data["time_history"]
        if today_text not in history:
            history[today_text] = {"produtivo": 0, "distracao": 0, "neutro": 0}
        return history[today_text]

    def register_time(self, category):
        day = self.today_time()
        day[category] = day.get(category, 0) + TICK_SECONDS
        if category == "produtivo":
            self.state_data["total_productive_seconds"] += TICK_SECONDS
            self.continuous_focus_seconds += TICK_SECONDS
            if self.continuous_focus_seconds >= FOCUS_BREAK_MINUTES * 60 and not self.break_notified:
                try_send_notification("🧘 Hora de uma pausa", "Você completou 25 minutos de foco. Alongue-se e descanse os olhos.")
                self.speech_text = "Ótimo foco! Que tal uma pausa para descansar?"
                self.break_notified = True
        else:
            if self.continuous_focus_seconds >= 60:
                self.break_notified = False
            self.continuous_focus_seconds = 0

    def period_productive_seconds(self, days):
        total = 0
        for offset in range(days):
            key = (date.today() - timedelta(days=offset)).isoformat()
            total += self.state_data["time_history"].get(key, {}).get("produtivo", 0)
        return total

    def save_daily_goal(self):
        try:
            minutes = int(self.goal_entry.get())
            if not 5 <= minutes <= 480:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Meta inválida", "Digite um valor entre 5 e 480 minutos.")
            return
        self.state_data["daily_goal_minutes"] = minutes
        self.save_and_refresh()
        messagebox.showinfo("Meta salva", f"Sua meta diária agora é de {minutes} minutos.")

    # =========================================================================
    # BLOCO 20 — RESGATE E PERSONALIZAÇÃO
    # =========================================================================
    def redeem_reward(self, reward):
        if reward["status"] != "disponivel":
            messagebox.showinfo("Em breve", "Este prêmio dependerá de estoque ou de uma parceria externa.")
            return
        if reward["id"] in self.state_data["redeemed_rewards"]:
            messagebox.showinfo("Já resgatado", "Você já possui esta recompensa.")
            return
        if self.state_data["level"] < reward["level"]:
            messagebox.showwarning("Nível insuficiente", f"Alcance o nível {reward['level']} para liberar este prêmio.")
            return
        if self.state_data["points"] < reward["cost"]:
            messagebox.showwarning("Pontos insuficientes", f"Faltam {reward['cost'] - self.state_data['points']} pontos.")
            return
        if not messagebox.askyesno("Confirmar resgate", f"Trocar {reward['cost']} pontos por {reward['name']}?"):
            return

        self.state_data["points"] -= reward["cost"]
        self.state_data["redeemed_rewards"].append(reward["id"])
        if reward["type"] == "accessory":
            self.state_data["unlocked_accessories"].append(reward["value"])
        elif reward["type"] == "pet":
            self.state_data["unlocked_pets"].append(reward["value"])
        self.speech_text = f"Você resgatou: {reward['name']}!"
        self.check_achievements()
        self.save_and_refresh()
        messagebox.showinfo("Resgate concluído", self.speech_text)

    def select_pet(self, pet_id):
        if pet_id not in self.state_data["unlocked_pets"]:
            messagebox.showinfo("Mascote bloqueado", f"Este mascote é liberado por {PETS[pet_id]['unlock']}.")
            return
        self.state_data["appearance"] = pet_id
        self.speech_text = f"Agora sou um {PETS[pet_id]['name']}!"
        self.save_and_refresh()

    def select_accessory(self, accessory_id):
        if accessory_id not in self.state_data["unlocked_accessories"]:
            messagebox.showinfo("Acessório bloqueado", "Resgate este acessório na aba Recompensas.")
            return
        self.state_data["accessory"] = accessory_id
        self.speech_text = f"Novo visual: {ACCESSORIES[accessory_id]['name']}!"
        self.save_and_refresh()

    # =========================================================================
    # BLOCO 21 — DIAGNÓSTICO, TESTE E CICLO AUTOMÁTICO
    # =========================================================================
    def show_diagnostics(self):
        title = get_active_window_title()
        process_name = get_active_process_name()
        category, label = classify_activity(title, process_name)
        details = [
            f"Janela ativa: {title or 'não detectada'}",
            f"Processo: {process_name or 'não detectado'}",
            f"Classificação: {category}", f"Rótulo: {label}",
            f"Usuário: {self.state_data['owner_name']} ({self.state_data['owner_nickname']})",
        ]
        messagebox.showinfo("Diagnóstico", "\n".join(details))

    def test_notification(self):
        ok, error = try_send_notification(
            "🐣 Teste do Tamagotchi",
            "Se você está vendo esta mensagem, as notificações estão funcionando."
        )
        if ok:
            messagebox.showinfo("Notificação", "Notificação enviada com sucesso.")
        else:
            messagebox.showwarning("Notificação", f"{error}\n\n{platform_notification_tips()}")

    def start_polling(self):
        self.poll_active_window()
        self.after(POLL_INTERVAL_MS, self.start_polling)

    def poll_active_window(self):
        title = get_active_window_title()
        process_name = get_active_process_name()
        category, label = classify_activity(title, process_name)
        self.last_category = category
        self.register_time(category)

        if category == "produtivo":
            self.state_data["happiness"] = min(100, self.state_data["happiness"] + BOOST_PRODUCTIVE)
            self.add_xp(XP_PER_PRODUCTIVE_TICK)
            self.add_points(POINTS_PER_PRODUCTIVE_TICK, "Atividade produtiva")
            self.update_streak()
            self.label_app.config(text=f"Atividade produtiva: {label}")
            self.speech_text = "Muito bem! Continue focado."
        elif category == "distracao":
            self.state_data["happiness"] = max(0, self.state_data["happiness"] - PENALTY_DISTRACTION)
            self.label_app.config(text=f"Atenção: {label} está tirando o foco.")
            self.speech_text = "Sem culpa: termine o que precisa e volte ao foco."
        else:
            self.state_data["happiness"] = max(0, self.state_data["happiness"] - DECAY_PER_TICK)
            self.label_app.config(text="Sem atividade definida no momento.")

        if self.state_data["happiness"] <= CRITICAL_HAPPINESS and not self.notified_critical:
            try_send_notification("🐣 Seu mascote precisa de atenção",
                                  "Volte a uma atividade produtiva para recuperar a felicidade.")
            self.notified_critical = True
        elif self.state_data["happiness"] > CRITICAL_HAPPINESS:
            self.notified_critical = False

        self.check_daily_goal()
        self.check_achievements()
        self.save_and_refresh()

    # =========================================================================
    # BLOCO 22 — ATUALIZAÇÃO DE TODAS AS ABAS
    # =========================================================================
    def save_and_refresh(self):
        write_state(self.state_data)
        self.refresh_all()

    def refresh_all(self):
        self.unlock_level_pets()
        state = self.state_data
        state["name"] = state["name"] or "Tama"

        needed = xp_needed_for_level(state["level"])
        happiness = max(0, min(100, state["happiness"]))
        self.label_name.config(text=state["name"])
        self.badge_level.set_text(f"⭐ Nível {state['level']}")
        self.badge_points.set_text(f"◆ {state['points']} pontos")
        self.bar_happiness.set(happiness / 100, f"{int(happiness)}%")
        self.bar_xp.set(state["xp"] / needed, f"{int(state['xp'])}/{needed} XP")
        self.label_xp.config(text=f"Nível {state['level']} • faltam {max(0, needed - int(state['xp']))} XP")

        mood_messages = {
            "euforico": "Estou eufórico!", "feliz": "Estou feliz!",
            "neutro": "Estou bem.", "triste": "Estou um pouco triste.",
            "irritado": "Preciso retomar o foco.", "doente": "Preciso de atenção!",
        }
        self.label_status.config(text=mood_messages[self.current_mood()])
        self.draw_pet()
        self.draw_floating_pet()

        self.progress_cards["level"].config(text=str(state["level"]))
        self.progress_cards["points"].config(text=str(state["points"]))
        self.progress_cards["focus"].config(text=seconds_to_text(state["total_productive_seconds"]))
        self.progress_cards["streak"].config(text=f"{state['streak']} dias")
        self.progress_level_bar.set(state["xp"] / needed, f"{int(state['xp'])} de {needed} XP")

        today = self.today_time()
        goal_seconds = state["daily_goal_minutes"] * 60
        today_focus = today.get("produtivo", 0)
        self.goal_title.config(text=f"META DE HOJE — {state['daily_goal_minutes']} MINUTOS")
        self.progress_goal_bar.set(today_focus / max(1, goal_seconds),
                                   f"{seconds_to_text(today_focus)} de {state['daily_goal_minutes']} min")
        self.goal_hint.config(text="Meta concluída! Recompensa recebida." if today_focus >= goal_seconds
                              else "Complete a meta para ganhar 50 pontos e 50 XP.")

        self.time_labels["today"].config(text=seconds_to_text(today_focus))
        self.time_labels["week"].config(text=seconds_to_text(self.period_productive_seconds(7)))
        self.time_labels["month"].config(text=seconds_to_text(self.period_productive_seconds(30)))
        self.today_details.config(
            text=f"✅ Produtivo: {seconds_to_text(today.get('produtivo', 0))}\n"
                 f"⚠️ Distrações: {seconds_to_text(today.get('distracao', 0))}\n"
                 f"➖ Neutro: {seconds_to_text(today.get('neutro', 0))}"
        )
        # Respeita o texto enquanto o usuário estiver digitando a nova meta.
        if self.focus_get() != self.goal_entry:
            self.goal_entry.delete(0, tk.END)
            self.goal_entry.insert(0, str(state["daily_goal_minutes"]))

        self.refresh_rewards_tab()
        self.refresh_custom_tab()
        self.refresh_achievements_tab()


# =============================================================================
# BLOCO 23 — INICIALIZAÇÃO DO PROGRAMA
# =============================================================================
if __name__ == "__main__":
    app = Tamagotchi()
    app.mainloop()
