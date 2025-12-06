import customtkinter as ctk
import tkinter as tk
import os
from PIL import Image, ImageTk

from pokedex_gui import PokedexPage
from batalha_simulada_gui import BatalhaSimuladaPage
from batalha_random_gui import BatalhaRandomPage

APP_TITLE = "Simulador Pokémon Fire Red"
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def load_image_asset(file_name, width, height, subfolder=""):
    path = os.path.join(ASSETS_PATH, subfolder, file_name)
    try:
        pil_image = Image.open(path).convert("RGBA")
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {path}")
        return None
    resized_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=resized_image, dark_image=resized_image, size=(width, height))


class PokemonApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1000x700")
        self.fullscreen = False

        self.bind("<Escape>", lambda e: self.set_window_state("normal"))
        self.bind("<F11>", lambda e: self.toggle_fullscreen())

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, PokedexPage, BatalhaSimuladaPage, BatalhaRandomPage):
            page = F(parent=self.container, controller=self)
            self.frames[F.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, name):
        self.frames[name].tkraise()

    def set_window_state(self, state):
        if state == "fullscreen":
            self.attributes("-fullscreen", True)
            self.fullscreen = True
        else:
            self.attributes("-fullscreen", False)
            self.fullscreen = False

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.set_window_state("normal")
        else:
            self.set_window_state("fullscreen")


class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.bg_canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        bg_path = os.path.join(ASSETS_PATH, "images", "background.png")
        try:
            self.bg_image_original = Image.open(bg_path).convert("RGBA")
            self.bg_canvas.bind("<Configure>", self._on_resize)
        except FileNotFoundError:
            self.bg_image_original = None
            self.bg_canvas.configure(bg=ctk.ThemeManager.theme['CTk']['fg_color']["red"])

        self.bg_image_tk = None

        ref_x = 20
        ref_y = -20
        spacing = 60

        def make_button(text, y_offset, callback):
            btn = ctk.CTkLabel(
                self,
                text=text,
                font=("Consolas", 22, "bold"),
                text_color="white",
                fg_color="transparent",
                bg_color='transparent'
            )
            btn.place(relx=0.0, rely=1.0, x=ref_x, y=ref_y - y_offset, anchor="sw")
            btn.bind("<Button-1>", lambda e: callback())
            btn.bind("<Enter>", lambda e: btn.configure(text_color="#cccccc"))
            btn.bind("<Leave>", lambda e: btn.configure(text_color="white"))
            return btn

        make_button("SAIR", 0, lambda: controller.destroy())
        make_button("TIMES ALEATÓRIOS", spacing, lambda: controller.show_frame("BatalhaRandomPage"))
        make_button("ESCOLHER TIME", spacing * 2, lambda: controller.show_frame("BatalhaSimuladaPage"))
        make_button("POKÉDEX", spacing * 3, lambda: controller.show_frame("PokedexPage"))

    def _on_resize(self, event):
        if not self.bg_image_original:
            return

        try:
            w = max(event.width, 1)
            h = max(event.height, 1)
            resized = self.bg_image_original.resize((w, h), Image.Resampling.LANCZOS)
            self.bg_image_tk = ImageTk.PhotoImage(resized)

            if not hasattr(self.bg_canvas, "img_id"):
                self.bg_canvas.img_id = self.bg_canvas.create_image(0, 0, anchor="nw", image=self.bg_image_tk)
            else:
                self.bg_canvas.itemconfig(self.bg_canvas.img_id, image=self.bg_image_tk)
        except:
            pass


if __name__ == "__main__":
    app = PokemonApp()
    app.mainloop()
