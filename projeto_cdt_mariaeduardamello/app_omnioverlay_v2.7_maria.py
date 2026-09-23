"""
===============================================================================
PROJETO: OmniOverlay - Dynamic Accent Colors, Full Theme, Profile & Root Master
===============================================================================
"""

import json
import os
import subprocess
import time
import urllib.parse
import webbrowser
import threading
import sqlite3
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageDraw
import cv2

import psutil
from pynput import keyboard

CONFIG_FILE = "app_config.json"
DB_FILE = "app_database.db"

COLOR_TEXT_PRIMARY = ("#0F172A", "#F8FAFC")      
COLOR_TEXT_SECONDARY = ("#475569", "#94A3B8")   
COLOR_BG_SURFACE = ("#F1F5F9", "#0F172A")       
COLOR_BG_CARD = ("#FFFFFF", "#1E293B")          
COLOR_INPUT_BG = ("#FFFFFF", "#1E293B")         
COLOR_BORDER = ("#CBD5E1", "#334155")           

COLOR_ACCENTS = {
    "azul": {"primary": "#2563EB", "hover": "#1D4ED8"},
    "vermelho": {"primary": "#DC2626", "hover": "#B91C1C"},
    "verde": {"primary": "#16A34A", "hover": "#15803D"},
    "roxo": {"primary": "#9333EA", "hover": "#7E22CE"},
}


def inicializar_banco_sql():
    try:
        conexao = sqlite3.connect(DB_FILE)
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_db (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE,
                senha TEXT,
                nivel TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs_sistema (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                acao TEXT,
                data_hora TEXT
            )
        """)
        
        cursor.execute("SELECT * FROM usuarios_db WHERE nome = ?", ("Root Master",))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO usuarios_db (nome, senha, nivel) VALUES (?, ?, ?)", 
                           ("Root Master", "12345678", "Administrador"))
            conexao.commit()
            
        conexao.close()
    except Exception as e:
        print(f"[ERRO SQL] {e}")


def criar_avatar_circular(caminho_imagem, tamanho=(40, 40)):
    try:
        img = Image.open(caminho_imagem).convert("RGBA")
        img = ImageOps.fit(img, tamanho, Image.Resampling.LANCZOS)
        
        mascara = Image.new("L", tamanho, 0)
        draw = ImageDraw.Draw(mascara)
        draw.ellipse((0, 0, tamanho[0], tamanho[1]), fill=255)
        
        resultado = Image.new("RGBA", tamanho, (0, 0, 0, 0))
        resultado.paste(img, (0, 0), mascara)
        return resultado
    except Exception as e:
        print(f"[ERRO AVATAR] {e}")
        return None


class GlobalHotkeyManager:
    def __init__(self, app_controller):
        self.controller = app_controller
        self.listener = None
        self.teclas_pressionadas = set()

    def iniciar(self):
        try:
            self.alt_keys = {keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt}
            self.z_key = keyboard.KeyCode.from_char('z')
            self.z_key_caps = keyboard.KeyCode.from_char('Z')

            self.listener = keyboard.Listener(
                on_press=self.ao_pressionar,
                on_release=self.ao_soltar
            )
            self.listener.daemon = True
            self.listener.start()
        except Exception as e:
            print(f"[ERRO] {e}")

    def ao_pressionar(self, key):
        try:
            self.teclas_pressionadas.add(key)
            tem_alt = any(k in self.teclas_pressionadas for k in self.alt_keys)
            tem_z = (self.z_key in self.teclas_pressionadas) or (self.z_key_caps in self.teclas_pressionadas)

            if tem_alt and tem_z:
                self.teclas_pressionadas.clear()
                self.controller.after(0, self.controller.alternar_visibilidade_overlay)
        except Exception:
            pass

    def ao_soltar(self, key):
        try:
            if key in self.teclas_pressionadas:
                self.teclas_pressionadas.remove(key)
            for k in self.alt_keys:
                if k in self.teclas_pressionadas:
                    self.teclas_pressionadas.remove(k)
        except Exception:
            pass


class AccountManager:
    @staticmethod
    def carregar_dados():
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    if "perfis" in dados and len(dados["perfis"]) > 0:
                        for p in dados["perfis"]:
                            p.setdefault("atalhos_custom", [])
                            p.setdefault("foto_perfil", "")
                            p.setdefault("cor_fundo", "#0F172A")
                            p.setdefault("modo_layout", "grid")
                        return dados
            except Exception as e:
                print(f"[ERRO] {e}")

        dados_padrao = {
            "perfis": [
                {
                    "id": "p1",
                    "nome": "Jogador Principal",
                    "cor_acento": "azul",
                    "foto_perfil": "",
                    "cor_fundo": "#0F172A",
                    "modo_layout": "grid",
                    "atalhos_custom": []
                },
                {
                    "id": "p_root",
                    "nome": "Root Master",
                    "cor_acento": "roxo",
                    "foto_perfil": "",
                    "cor_fundo": "#0F172A",
                    "modo_layout": "grid",
                    "atalhos_custom": []
                }
            ],
            "ultimo_perfil": "p1",
            "modo_tema": "dark"
        }
        AccountManager.salvar_dados(dados_padrao)
        return dados_padrao

    @staticmethod
    def salvar_dados(dados):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[ERRO] {e}")


class JanelaSenhaModal(ctk.CTkToplevel):
    def __init__(self, parent, callback_sucesso):
        super().__init__(parent)
        self.callback_sucesso = callback_sucesso
        
        self.title("Autenticação Root Master")
        self.geometry("380x200")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_SURFACE)
        self.attributes("-topmost", True)
        
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        x = (largura_tela - 380) // 2
        y = (altura_tela - 200) // 2
        self.geometry(f"380x200+{x}+{y}")

        ctk.CTkLabel(
            self,
            text="🛡️ Acesso Restrito - Root Master",
            font=("Segoe UI", 13, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        ).pack(pady=(16, 8))

        ctk.CTkLabel(
            self,
            text="Digite a senha cadastrada no banco SQL:",
            font=("Segoe UI", 11),
            text_color=COLOR_TEXT_SECONDARY
        ).pack(pady=(0, 8))

        self.entry_senha = ctk.CTkEntry(
            self,
            placeholder_text="Senha...",
            show="*",
            height=36,
            width=300,
            fg_color=COLOR_INPUT_BG,
            text_color=COLOR_TEXT_PRIMARY,
            border_color=COLOR_BORDER
        )
        self.entry_senha.pack(pady=4)
        self.entry_senha.focus()
        self.entry_senha.bind("<Return>", lambda e: self.verificar())

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=12)

        ctk.CTkButton(
            btn_frame,
            text="Confirmar",
            width=130,
            height=32,
            fg_color="#16A34A",
            hover_color="#15803D",
            text_color="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            command=self.verificar
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            width=130,
            height=32,
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            command=self.destroy
        ).pack(side="left", padx=6)

    def verificar(self):
        senha = self.entry_senha.get().strip()
        if not senha:
            return

        try:
            conexao = sqlite3.connect(DB_FILE)
            cursor = conexao.cursor()
            cursor.execute("SELECT senha FROM usuarios_db WHERE nome = ?", ("Root Master",))
            resultado = cursor.fetchone()
            conexao.close()

            if resultado and resultado[0] == senha:
                self.destroy()
                self.callback_sucesso()
            else:
                self.entry_senha.delete(0, "end")
        except Exception as e:
            print(f"[ERRO SQL] {e}")


class PainelAdmWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Painel Administrativo - Root Master")
        self.geometry("500x400")
        self.configure(fg_color=COLOR_BG_SURFACE)
        self.attributes("-topmost", True)

        ctk.CTkLabel(
            self,
            text="🛠️ Painel de Controle Administrativo",
            font=("Segoe UI", 16, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        ).pack(pady=20)

        ctk.CTkLabel(
            self,
            text="Bem-vindo ao painel de gerenciamento exclusivo do ADM.",
            font=("Segoe UI", 12),
            text_color=COLOR_TEXT_SECONDARY
        ).pack(pady=5)

        ctk.CTkButton(
            self,
            text="📥 Exportar Dados SQL para JSON",
            width=300,
            height=40,
            fg_color="#9333EA",
            hover_color="#7E22CE",
            text_color="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
            command=self.executar_exportacao_json
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Fechar Painel",
            width=150,
            height=35,
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="#FFFFFF",
            command=self.destroy
        ).pack(pady=10)

    def executar_exportacao_json(self):
        try:
            conexao = sqlite3.connect(DB_FILE)
            conexao.row_factory = sqlite3.Row
            cursor = conexao.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tabelas = cursor.fetchall()

            dados_completos = {}
            for tabela in tabelas:
                nome_tabela = tabela["name"]
                cursor.execute(f"SELECT * FROM {nome_tabela}")
                linhas = cursor.fetchall()
                dados_completos[nome_tabela] = [dict(linha) for linha in linhas]

            conexao.close()

            with open("backup_banco_sql.json", "w", encoding="utf-8") as f:
                json.dump(dados_completos, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[ERRO] {e}")


class ProfileSelectorFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent", corner_radius=12)
        self.controller = controller
        self.criar_interface()

    def criar_interface(self):
        header = ctk.CTkFrame(self, fg_color="transparent", height=50, corner_radius=0)
        header.pack(fill="x")

        lbl_titulo = ctk.CTkLabel(
            header,
            text="🎮 Escolha sua Conta",
            font=("Segoe UI", 14, "bold"),
            text_color=COLOR_TEXT_PRIMARY,
        )
        lbl_titulo.pack(side="left", padx=16, pady=12)

        btn_fechar = ctk.CTkButton(
            header,
            text="✕",
            width=30,
            height=30,
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="#FFFFFF",
            command=self.controller.destroy,
        )
        btn_fechar.pack(side="right", padx=12)

        self.scroll_perfis = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_perfis.pack(fill="both", expand=True, padx=20, pady=15)

        frame_criar = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_color=COLOR_BORDER, border_width=1)
        frame_criar.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkLabel(
            frame_criar,
            text="Criar Nova Conta",
            font=("Segoe UI", 11, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        ).pack(anchor="w", padx=12, pady=(8, 2))

        self.entry_novo_nome = ctk.CTkEntry(
            frame_criar,
            placeholder_text="Nome da conta...",
            height=36,
            fg_color=COLOR_INPUT_BG,
            text_color=COLOR_TEXT_PRIMARY,
            border_color=COLOR_BORDER
        )
        self.entry_novo_nome.pack(fill="x", padx=12, pady=4)
        self.entry_novo_nome.bind("<Return>", lambda e: self.acao_criar_perfil())

        btn_novo = ctk.CTkButton(
            frame_criar,
            text="+ Criar e Entrar",
            height=36,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            command=self.acao_criar_perfil,
        )
        btn_novo.pack(fill="x", padx=12, pady=(4, 12))

    def atualizar_lista(self):
        for widget in self.scroll_perfis.winfo_children():
            widget.destroy()

        perfis = self.controller.dados_config.get("perfis", [])

        for perfil in perfis:
            card = ctk.CTkFrame(self.scroll_perfis, fg_color=COLOR_BG_CARD, corner_radius=12, border_color=COLOR_BORDER, border_width=1)
            card.pack(fill="x", pady=6, ipady=4)

            foto_path = perfil.get("foto_perfil", "")
            img_avatar = None
            if foto_path and os.path.exists(foto_path):
                try:
                    pil_img = criar_avatar_circular(foto_path, tamanho=(36, 36))
                    if pil_img:
                        img_avatar = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(36, 36))
                except Exception:
                    img_avatar = None

            is_root = perfil["nome"] == "Root Master"

            lbl_avatar = ctk.CTkLabel(
                card,
                text="" if img_avatar else ("🛡️" if is_root else "👤"),
                image=img_avatar,
                width=42,
                height=42,
                corner_radius=21,
                fg_color=COLOR_BG_SURFACE,
                text_color=COLOR_TEXT_PRIMARY,
                font=("Segoe UI", 16),
            )
            lbl_avatar.pack(side="left", padx=12)

            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True)

            lbl_nome = ctk.CTkLabel(
                info_frame,
                text=perfil["nome"],
                font=("Segoe UI", 12, "bold"),
                text_color=COLOR_TEXT_PRIMARY,
                anchor="w",
            )
            lbl_nome.pack(fill="x", pady=(12, 0))

            btn_entrar = ctk.CTkButton(
                card,
                text="Entrar",
                width=80,
                height=32,
                corner_radius=6,
                fg_color="#16A34A",
                hover_color="#15803D",
                text_color="#FFFFFF",
                font=("Segoe UI", 11, "bold"),
                command=lambda p=perfil: self.tentar_entrar_perfil(p),
            )
            btn_entrar.pack(side="right", padx=12)

            if not is_root:
                btn_excluir = ctk.CTkButton(
                    card,
                    text="🗑️",
                    width=36,
                    height=32,
                    corner_radius=6,
                    fg_color="#EF4444",
                    hover_color="#DC2626",
                    text_color="#FFFFFF",
                    font=("Segoe UI", 12),
                    command=lambda p=perfil: self.acao_excluir_perfil(p),
                )
                btn_excluir.pack(side="right", padx=(0, 4))

    def tentar_entrar_perfil(self, perfil):
        if perfil["nome"] == "Root Master":
            JanelaSenhaModal(self.controller, lambda: self.controller.entrar_no_perfil(perfil))
        else:
            self.controller.entrar_no_perfil(perfil)

    def acao_criar_perfil(self):
        nome = self.entry_novo_nome.get().strip()
        if not nome:
            return

        if nome.lower() == "root master":
            return

        novo_id = f"p_{int(time.time())}"
        novo_perfil = {
            "id": novo_id,
            "nome": nome,
            "cor_acento": "azul",
            "foto_perfil": "",
            "cor_fundo": "#0F172A",
            "modo_layout": "grid",
            "atalhos_custom": []
        }

        self.controller.dados_config["perfis"].append(novo_perfil)
        AccountManager.salvar_dados(self.controller.dados_config)

        self.entry_novo_nome.delete(0, "end")
        self.controller.entrar_no_perfil(novo_perfil)

    def acao_excluir_perfil(self, perfil):
        if perfil["nome"] == "Root Master":
            return

        perfis = self.controller.dados_config.get("perfis", [])
        if len(perfis) <= 1:
            return

        self.controller.dados_config["perfis"] = [p for p in perfis if p["id"] != perfil["id"]]
        AccountManager.salvar_dados(self.controller.dados_config)
        self.atualizar_lista()


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent", corner_radius=12)
        self.controller = controller

        self._offset_x = 0
        self._offset_y = 0
        self.modo_cinema_ativo = False
        
        self.dynamic_accent_buttons = []
        self.dynamic_accent_borders = []
        
        self.icone_foto_temp = ""

        self.video_path = None
        self.video_rodando = False
        self.video_pausado = False
        self.video_thread = None

        self.criar_interface()
        self.atualizar_monitor_sistema()

    def criar_interface(self):
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=12,
            border_color=COLOR_BORDER,
            border_width=1,
            height=60,
        )
        self.header_frame.pack(fill="x", padx=16, pady=(16, 8))

        self.header_frame.bind("<Button-1>", self.iniciar_arraste)
        self.header_frame.bind("<B1-Motion>", self.arrastar_janela)

        self.btn_avatar = ctk.CTkButton(
            self.header_frame,
            text="👤",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            font=("Segoe UI", 15),
            command=self.trocar_foto_perfil,
        )
        self.btn_avatar.pack(side="left", padx=(12, 8))
        self.dynamic_accent_buttons.append(self.btn_avatar)

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame,
            text="OmniOverlay",
            font=("Segoe UI", 13, "bold"),
            text_color=COLOR_TEXT_PRIMARY,
        )
        self.lbl_titulo.pack(side="left", padx=2)

        self.frame_hardware = ctk.CTkFrame(
            self.header_frame,
            fg_color=COLOR_BG_CARD,
            corner_radius=8,
            border_color=COLOR_BORDER,
            border_width=1,
            height=36
        )
        self.frame_hardware.pack(side="left", padx=16, pady=10)

        self.lbl_cpu = ctk.CTkLabel(
            self.frame_hardware,
            text="⚡ CPU: 0%",
            font=("Segoe UI", 10, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        self.lbl_cpu.pack(side="left", padx=8)

        self.lbl_ram = ctk.CTkLabel(
            self.frame_hardware,
            text="💾 RAM: 0%",
            font=("Segoe UI", 10, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        self.lbl_ram.pack(side="left", padx=(0, 8))

        btn_fechar = ctk.CTkButton(
            self.header_frame,
            text="✕",
            width=32,
            height=32,
            corner_radius=8,
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="#FFFFFF",
            command=self.controller.destroy,
        )
        btn_fechar.pack(side="right", padx=(4, 12))

        self.btn_tema = ctk.CTkButton(
            self.header_frame,
            text="☀️" if self.controller.modo_tema_atual == "dark" else "🌙",
            width=32,
            height=32,
            corner_radius=8,
            fg_color=COLOR_BG_CARD,
            hover_color=COLOR_BORDER,
            text_color=COLOR_TEXT_PRIMARY,
            font=("Segoe UI", 12),
            command=self.controller.alternar_tema_global,
        )
        self.btn_tema.pack(side="right", padx=4)

        self.btn_modo_cinema = ctk.CTkButton(
            self.header_frame,
            text="🎬 Cinema",
            width=85,
            height=32,
            corner_radius=8,
            fg_color="#9333EA",
            hover_color="#7E22CE",
            text_color="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            command=self.toggle_modo_cinema,
        )
        self.btn_modo_cinema.pack(side="right", padx=4)

        btn_trocar_conta = ctk.CTkButton(
            self.header_frame,
            text="🔄 Contas",
            width=85,
            height=32,
            corner_radius=8,
            fg_color=COLOR_BG_CARD,
            hover_color=COLOR_BORDER,
            text_color=COLOR_TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
            command=self.controller.abrir_seletor_perfis,
        )
        btn_trocar_conta.pack(side="right", padx=4)

        self.frame_busca = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=12,
            border_color=COLOR_BORDER,
            border_width=1,
        )
        self.frame_busca.pack(fill="x", padx=16, pady=4)

        self.entry_universal = ctk.CTkEntry(
            self.frame_busca,
            placeholder_text="Cole um Link Web ou o caminho de um Programa (.exe) para abrir...",
            height=38,
            corner_radius=8,
            fg_color=COLOR_INPUT_BG,
            text_color=COLOR_TEXT_PRIMARY,
            border_color=COLOR_BORDER,
            font=("Segoe UI", 11),
        )
        self.entry_universal.pack(side="left", fill="x", expand=True, padx=8, pady=8)
        self.entry_universal.bind("<Return>", lambda e: self.executar_busca_universal())

        btn_procurar_arquivo = ctk.CTkButton(
            self.frame_busca,
            text="📁 Buscar App",
            width=100,
            height=38,
            fg_color=COLOR_BG_CARD,
            hover_color=COLOR_BORDER,
            text_color=COLOR_TEXT_PRIMARY,
            command=self.selecionar_executavel_direto,
        )
        btn_procurar_arquivo.pack(side="right", padx=(0, 4), pady=8)

        btn_executar = ctk.CTkButton(
            self.frame_busca,
            text="Abrir 🚀",
            width=90,
            height=38,
            corner_radius=8,
            text_color="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            command=self.executar_busca_universal,
        )
        btn_executar.pack(side="right", padx=8, pady=8)
        self.dynamic_accent_buttons.append(btn_executar)

        self.tabview = ctk.CTkTabview(
            self,
            corner_radius=12,
            fg_color="transparent",
            border_color=COLOR_BORDER,
            border_width=1,
            text_color=COLOR_TEXT_PRIMARY,
            segmented_button_fg_color=COLOR_BG_CARD,
            segmented_button_selected_color="#2563EB",
            segmented_button_selected_hover_color="#1D4ED8",
            segmented_button_unselected_color=COLOR_BG_CARD,
            segmented_button_unselected_hover_color=COLOR_BORDER
        )
        self.tabview.pack(fill="both", expand=True, padx=16, pady=(8, 16))
        self.dynamic_accent_buttons.append(self.tabview)

        self.tab_hub = self.tabview.add("🚀 Central de Atalhos")
        self.tab_ia = self.tabview.add("🤖 Assistente IA")
        self.tab_video = self.tabview.add("🎬 Player de Vídeo")
        self.tab_config = self.tabview.add("⚙️ Configurações")

        self.montar_aba_hub()
        self.montar_aba_ia()
        self.montar_aba_player_video()
        self.montar_aba_config()

    def carregar_perfil(self, perfil):
        self.lbl_titulo.configure(text=f"OmniOverlay - {perfil['nome']}")
        self.aplicar_cor_acento(perfil.get("cor_acento", "azul"))
        self.atualizar_foto_avatar(perfil.get("foto_perfil", ""))
        
        if self.controller.modo_tema_atual == "light":
            self.controller.atualizar_cor_fundo_raiz("#F1F5F9")
        else:
            self.controller.atualizar_cor_fundo_raiz(perfil.get("cor_fundo", "#0F172A"))
            
        self.atualizar_atalhos_customizados()

    def atualizar_monitor_sistema(self):
        try:
            cpu_usage = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory()

            self.lbl_cpu.configure(text=f"⚡ CPU: {cpu_usage:.0f}%")
            self.lbl_ram.configure(text=f"💾 RAM: {ram.percent:.0f}%")

            if hasattr(self, 'bar_cpu_detalhada'):
                self.bar_cpu_detalhada.set(cpu_usage / 100.0)
                self.lbl_cpu_valor_detalhado.configure(text=f"{cpu_usage:.1f}%")

                self.bar_ram_detalhada.set(ram.percent / 100.0)
                ram_usada_gb = ram.used / (1024**3)
                ram_total_gb = ram.total / (1024**3)
                self.lbl_ram_valor_detalhado.configure(
                    text=f"{ram.percent:.1f}% ({ram_usada_gb:.1f} GB / {ram_total_gb:.1f} GB)"
                )

                cor_cpu = "#16A34A" if cpu_usage < 60 else ("#EAB308" if cpu_usage < 85 else "#EF4444")
                self.bar_cpu_detalhada.configure(progress_color=cor_cpu)

                cor_ram = "#16A34A" if ram.percent < 70 else ("#EAB308" if ram.percent < 88 else "#EF4444")
                self.bar_ram_detalhada.configure(progress_color=cor_ram)
        except Exception:
            pass

        self.after(1500, self.atualizar_monitor_sistema)

    def atualizar_foto_avatar(self, foto_path):
        if foto_path and os.path.exists(foto_path):
            try:
                pil_img = criar_avatar_circular(foto_path, tamanho=(32, 32))
                if pil_img:
                    img_avatar = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(32, 32))
                    self.btn_avatar.configure(image=img_avatar, text="")
                    return
            except Exception:
                pass
        self.btn_avatar.configure(image="", text="👤" if self.controller.perfil_ativo["nome"] != "Root Master" else "🛡️")

    def trocar_foto_perfil(self):
        caminho = filedialog.askopenfilename(
            title="Escolha sua Foto de Perfil",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.ico *.bmp")]
        )
        if caminho and self.controller.perfil_ativo:
            self.controller.perfil_ativo["foto_perfil"] = caminho
            AccountManager.salvar_dados(self.controller.dados_config)
            self.atualizar_foto_avatar(caminho)

    def aplicar_cor_acento(self, nome_cor):
        cor = COLOR_ACCENTS.get(nome_cor, COLOR_ACCENTS["azul"])
        
        for item in self.dynamic_accent_buttons:
            try:
                if isinstance(item, ctk.CTkButton):
                    item.configure(fg_color=cor["primary"], hover_color=cor["hover"])
                elif isinstance(item, ctk.CTkTabview):
                    item.configure(segmented_button_selected_color=cor["primary"], segmented_button_selected_hover_color=cor["hover"])
            except Exception:
                pass

        for frame_borda in self.dynamic_accent_borders:
            try:
                frame_borda.configure(border_color=cor["primary"])
            except Exception:
                pass

        if self.controller.perfil_ativo:
            self.controller.perfil_ativo["cor_acento"] = nome_cor
            AccountManager.salvar_dados(self.controller.dados_config)

    def iniciar_arraste(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def arrastar_janela(self, event):
        if not self.modo_cinema_ativo:
            x = self.controller.winfo_x() + (event.x - self._offset_x)
            y = self.controller.winfo_y() + (event.y - self._offset_y)
            self.controller.geometry(f"+{x}+{y}")

    def toggle_modo_cinema(self):
        self.modo_cinema_ativo = not self.modo_cinema_ativo

        if self.modo_cinema_ativo:
            self.controller.attributes("-alpha", 1.0)
            self.frame_busca.pack_forget()
            self.btn_modo_cinema.configure(text="❌ Sair Cinema", fg_color="#DC2626", hover_color="#B91C1C")
            
            ws = self.controller.winfo_screenwidth()
            hs = self.controller.winfo_screenheight()
            self.controller.geometry(f"{ws}x{hs}+0+0")
        else:
            self.controller.attributes("-alpha", 0.98)
            self.frame_busca.pack(fill="x", padx=16, pady=4, after=self.header_frame)
            self.btn_modo_cinema.configure(text="🎬 Cinema", fg_color="#9333EA", hover_color="#7E22CE")
            self.controller.centralizar_janela(920, 800)

    def executar_busca_universal(self):
        alvo = self.entry_universal.get().strip()
        if alvo:
            self.abrir_inteligente(alvo)
            self.entry_universal.delete(0, "end")

    def selecionar_executavel_direto(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o Executável",
            filetypes=[("Executáveis e Atalhos", "*.exe *.lnk *.bat *.cmd"), ("Todos os Arquivos", "*.*")]
        )
        if caminho:
            self.entry_universal.insert(0, caminho)

    def abrir_inteligente(self, alvo):
        try:
            if alvo.startswith("http://") or alvo.startswith("https://"):
                webbrowser.open(alvo)
            elif "://" in alvo:
                webbrowser.open(alvo)
            elif os.path.exists(alvo):
                os.startfile(alvo)
            else:
                subprocess.Popen(alvo, shell=True)
        except Exception as e:
            print(f"[ERRO] {e}")

    def montar_aba_hub(self):
        frame_adicionar = ctk.CTkFrame(self.tab_hub, fg_color=COLOR_BG_CARD, corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        frame_adicionar.pack(fill="x", pady=(8, 8), padx=8, ipady=4)
        self.dynamic_accent_borders.append(frame_adicionar)

        ctk.CTkLabel(
            frame_adicionar,
            text="➕ Adicionar Novo Atalho ao Seu Perfil",
            font=("Segoe UI", 11, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        ).pack(anchor="w", padx=12, pady=(6, 2))

        form_top = ctk.CTkFrame(frame_adicionar, fg_color="transparent")
        form_top.pack(fill="x", padx=8, pady=2)

        self.entry_nome_atalho = ctk.CTkEntry(
            form_top,
            placeholder_text="Nome do Atalho...",
            height=32,
            fg_color=COLOR_INPUT_BG,
            text_color=COLOR_TEXT_PRIMARY,
            border_color=COLOR_BORDER
        )
        self.entry_nome_atalho.pack(side="left", fill="x", expand=True, padx=4)

        self.entry_url_atalho = ctk.CTkEntry(
            form_top,
            placeholder_text="Link Web ou Caminho (.exe)...",
            height=32,
            fg_color=COLOR_INPUT_BG,
            text_color=COLOR_TEXT_PRIMARY,
            border_color=COLOR_BORDER
        )
        self.entry_url_atalho.pack(side="left", fill="x", expand=True, padx=4)

        btn_browse_app = ctk.CTkButton(
            form_top,
            text="💻 Buscar App",
            width=100,
            height=32,
            fg_color=COLOR_BG_SURFACE,
            hover_color=COLOR_BORDER,
            text_color=COLOR_TEXT_PRIMARY,
            command=self.procurar_app_para_atalho,
        )
        btn_browse_app.pack(side="left", padx=4)

        form_bot = ctk.CTkFrame(frame_adicionar, fg_color="transparent")
        form_bot.pack(fill="x", padx=8, pady=(4, 6))

        ctk.CTkLabel(form_bot, text="Ícone:", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(side="left", padx=4)

        self.combo_icone = ctk.CTkComboBox(
            form_bot,
            values=["🎮", "💻", "🚀", "🌐", "🎵", "⚡", "📂", "🛠️"],
            width=70,
            height=30,
            fg_color=COLOR_INPUT_BG,
            text_color=COLOR_TEXT_PRIMARY,
            dropdown_fg_color=COLOR_BG_CARD,
            dropdown_text_color=COLOR_TEXT_PRIMARY
        )
        self.combo_icone.pack(side="left", padx=4)
        self.combo_icone.set("🎮")

        self.btn_foto_atalho = ctk.CTkButton(
            form_bot,
            text="🖼️ Foto Custom",
            width=110,
            height=30,
            fg_color=COLOR_BG_SURFACE,
            hover_color=COLOR_BORDER,
            text_color=COLOR_TEXT_PRIMARY,
            command=self.escolher_foto_icone_atalho,
        )
        self.btn_foto_atalho.pack(side="left", padx=4)

        btn_add_atalho = ctk.CTkButton(
            form_bot,
            text="+ Salvar Atalho",
            width=120,
            height=30,
            fg_color="#16A34A",
            hover_color="#15803D",
            text_color="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            command=self.adicionar_atalho_customizado,
        )
        btn_add_atalho.pack(side="right", padx=4)

        self.tabview_hub = ctk.CTkTabview(
            self.tab_hub,
            corner_radius=10,
            fg_color="transparent",
            text_color=COLOR_TEXT_PRIMARY,
            segmented_button_fg_color=COLOR_BG_CARD,
            segmented_button_selected_color="#2563EB",
            segmented_button_selected_hover_color="#1D4ED8",
            segmented_button_unselected_color=COLOR_BG_CARD,
            segmented_button_unselected_hover_color=COLOR_BORDER
        )
        self.tabview_hub.pack(fill="both", expand=True, padx=4, pady=0)
        self.dynamic_accent_buttons.append(self.tabview_hub)

        self.cat_custom = self.tabview_hub.add("⭐ Meus Atalhos")
        self.cat_media = self.tabview_hub.add("🎵 Mídia & Streaming")
        self.cat_games = self.tabview_hub.add("🎮 Jogos & Plataformas")
        self.cat_tools = self.tabview_hub.add("⚙️ Sistema & Ferramentas")

        self.scroll_custom = ctk.CTkScrollableFrame(self.cat_custom, fg_color="transparent")
        self.scroll_custom.pack(fill="both", expand=True)

        self.container_custom_items = ctk.CTkFrame(self.scroll_custom, fg_color="transparent")
        self.container_custom_items.pack(fill="x", pady=4)

        self.montar_categoria_estatica(self.cat_media, [
            ("🟢 Spotify", "https://open.spotify.com"),
            ("▶️ YouTube", "https://www.youtube.com"),
            ("🔴 Netflix", "https://www.netflix.com"),
            ("💜 Twitch", "https://www.twitch.tv"),
            ("📦 Prime Video", "https://www.primevideo.com"),
            ("💬 WhatsApp Web", "https://web.whatsapp.com"),
            ("🎵 Soundcloud", "https://soundcloud.com"),
            ("📺 Disney+", "https://www.disneyplus.com"),
        ])

        self.montar_categoria_estatica(self.cat_games, [
            ("🚀 Steam", "steam://open/main"),
            ("🛡️ Epic Games", "epicgames://"),
            ("💬 Discord", "https://discord.com/app"),
            ("💻 Discord App", "discord://"),
            ("🎮 Roblox", "https://www.roblox.com"),
            ("🔴 Roblox App", "roblox://"),
            ("🌐 Poki Jogos", "https://poki.com"),
        ])

        self.montar_categoria_estatica(self.cat_tools, [
            ("📁 Gerenciador de Arquivos", "explorer.exe"),
            ("⚙️ Configurações do Windows", "ms-settings:"),
            ("📝 Bloco de Notas", "notepad.exe"),
            ("🌐 Google Chrome", "https://www.google.com"),
            ("💻 Prompt de Comando", "cmd.exe"),
            ("⚡ Gerenciador de Tarefas", "taskmgr.exe"),
        ])

    def montar_categoria_estatica(self, container, lista_atalhos):
        scroll = ctk.CTkScrollableFrame(container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=4, pady=4)

        for nome, alvo in lista_atalhos:
            btn = ctk.CTkButton(
                scroll,
                text=nome,
                height=38,
                corner_radius=8,
                fg_color=COLOR_BG_CARD,
                hover_color=COLOR_BORDER,
                text_color=COLOR_TEXT_PRIMARY,
                border_color=COLOR_BORDER,
                border_width=1,
                font=("Segoe UI", 11, "bold"),
                anchor="w",
                command=lambda a=alvo: self.abrir_inteligente(a)
            )
            btn.pack(fill="x", pady=3, padx=4)

    def procurar_app_para_atalho(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o Executável",
            filetypes=[("Executáveis e Atalhos", "*.exe *.lnk *.bat *.cmd"), ("Todos os Arquivos", "*.*")]
        )
        if caminho:
            self.entry_url_atalho.delete(0, "end")
            self.entry_url_atalho.insert(0, caminho)
            if not self.entry_nome_atalho.get():
                nome_sugerido = os.path.splitext(os.path.basename(caminho))[0].capitalize()
                self.entry_nome_atalho.insert(0, nome_sugerido)

    def escolher_foto_icone_atalho(self):
        caminho = filedialog.askopenfilename(
            title="Escolha uma imagem para o ícone",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.ico *.bmp")]
        )
        if caminho:
            self.icone_foto_temp = caminho
            self.btn_foto_atalho.configure(text="✅ Foto OK")

    def adicionar_atalho_customizado(self):
        nome = self.entry_nome_atalho.get().strip()
        alvo = self.entry_url_atalho.get().strip()
        icone = self.combo_icone.get()

        if not nome or not alvo:
            return

        perfil = self.controller.perfil_ativo
        if perfil:
            novo_item = {
                "nome": nome,
                "alvo": alvo,
                "icone": icone,
                "foto_icone": self.icone_foto_temp
            }
            perfil["atalhos_custom"].append(novo_item)
            AccountManager.salvar_dados(self.controller.dados_config)

            self.entry_nome_atalho.delete(0, "end")
            self.entry_url_atalho.delete(0, "end")
            self.icone_foto_temp = ""
            self.btn_foto_atalho.configure(text="🖼️ Foto Custom")
            self.atualizar_atalhos_customizados()

    def remover_atalho_customizado(self, index):
        perfil = self.controller.perfil_ativo
        if perfil and 0 <= index < len(perfil["atalhos_custom"]):
            perfil["atalhos_custom"].pop(index)
            AccountManager.salvar_dados(self.controller.dados_config)
            self.atualizar_atalhos_customizados()

    def atualizar_atalhos_customizados(self):
        for widget in self.container_custom_items.winfo_children():
            widget.destroy()

        perfil = self.controller.perfil_ativo
        if not perfil:
            return

        lista = perfil.get("atalhos_custom", [])
        modo_layout = perfil.get("modo_layout", "grid")

        if not lista:
            lbl_vazio = ctk.CTkLabel(
                self.container_custom_items,
                text="Nenhum atalho personalizado criado ainda.",
                text_color=COLOR_TEXT_SECONDARY,
                font=("Segoe UI", 11)
            )
            lbl_vazio.pack(anchor="w", padx=8, pady=12)
            return

        if modo_layout == "grid":
            grid_frame = ctk.CTkFrame(self.container_custom_items, fg_color="transparent")
            grid_frame.pack(fill="x", expand=True)

            cols = 2
            for idx, item in enumerate(lista):
                r = idx // cols
                c = idx % cols

                card_frame = ctk.CTkFrame(
                    grid_frame,
                    fg_color=COLOR_BG_CARD,
                    border_color=COLOR_BORDER,
                    border_width=1,
                    corner_radius=8
                )
                card_frame.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                grid_frame.grid_columnconfigure(c, weight=1)

                foto_icon = item.get("foto_icone", "")
                img_obj = None
                if foto_icon and os.path.exists(foto_icon):
                    try:
                        pil_img = Image.open(foto_icon)
                        img_obj = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(20, 20))
                    except Exception:
                        img_obj = None

                prefixo_icone = item.get("icone", "🎮")
                texto_exibicao = f"{prefixo_icone} {item['nome']}" if not img_obj else f" {item['nome']}"

                btn_exec = ctk.CTkButton(
                    card_frame,
                    text=texto_exibicao,
                    image=img_obj,
                    compound="left",
                    height=38,
                    fg_color="transparent",
                    hover_color=COLOR_BORDER,
                    text_color=COLOR_TEXT_PRIMARY,
                    font=("Segoe UI", 11, "bold"),
                    anchor="w",
                    command=lambda a=item['alvo']: self.abrir_inteligente(a),
                )
                btn_exec.pack(side="left", fill="both", expand=True, padx=(8, 0))

                btn_del = ctk.CTkButton(
                    card_frame,
                    text="🗑️",
                    width=28,
                    height=26,
                    fg_color="#EF4444",
                    hover_color="#DC2626",
                    text_color="#FFFFFF",
                    command=lambda i=idx: self.remover_atalho_customizado(i),
                )
                btn_del.pack(side="right", padx=6, pady=6)

    def montar_aba_ia(self):
        ia_container = ctk.CTkFrame(self.tab_ia, fg_color="transparent")
        ia_container.pack(fill="both", expand=True, padx=8, pady=8)

        ctk.CTkLabel(
            ia_container,
            text="🤖 OmniAI - Assistente Inteligente",
            font=("Segoe UI", 13, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 8))

        self.chat_historico = ctk.CTkTextbox(
            ia_container,
            fg_color=COLOR_BG_CARD,
            text_color=COLOR_TEXT_PRIMARY,
            corner_radius=10,
            border_color=COLOR_BORDER,
            border_width=1,
            font=("Segoe UI", 11)
        )
        self.chat_historico.pack(fill="both", expand=True, pady=(0, 8))
        self.chat_historico.insert("end", "OmniAI: Olá! Pronto para a jogatina de hoje? Me pergunte sobre dicas de games, atalhos ou desempenho do PC!\n\n")
        self.chat_historico.configure(state="disabled")

        chat_input_frame = ctk.CTkFrame(ia_container, fg_color="transparent")
        chat_input_frame.pack(fill="x", pady=0)

        self.entry_chat = ctk.CTkEntry(
            chat_input_frame,
            placeholder_text="Digite sua pergunta sobre jogos...",
            height=38,
            fg_color=COLOR_INPUT_BG,
            text_color=COLOR_TEXT_PRIMARY,
            border_color=COLOR_BORDER
        )
        self.entry_chat.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.entry_chat.bind("<Return>", lambda e: self.enviar_mensagem_ia())

        btn_enviar_ia = ctk.CTkButton(
            chat_input_frame,
            text="Enviar 💬",
            width=90,
            height=38,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            command=self.enviar_mensagem_ia
        )
        btn_enviar_ia.pack(side="right")
        self.dynamic_accent_buttons.append(btn_enviar_ia)

    def enviar_mensagem_ia(self):
        texto = self.entry_chat.get().strip()
        if not texto:
            return

        self.chat_historico.configure(state="normal")
        self.chat_historico.insert("end", f"Você: {texto}\n")
        
        txt_lower = texto.lower()
        
        # --- REPERTÓRIO INTELIGENTE LOCAL SOBRE JOGOS E GERAL ---
        if any(p in txt_lower for p in ["jogo", "jogar", "game", "games", "jogatina"]):
            resposta = "OmniAI: 🎮 Os games são ótimos para relaxar! Você pode organizar seus jogos favoritos (como Steam, Epic Games, Roblox ou atalhos próprios) na aba 'Central de Atalhos' > 'Jogos & Plataformas'."
        elif any(p in txt_lower for p in ["fps", "trava", "lag", "lento", "otimizar", "desempenho", "rodar"]):
            resposta = "OmniAI: ⚡ Para melhorar o desempenho nos jogos, verifique o uso do seu processador e memória RAM no monitor do topo do painel, feche abas desnecessárias do navegador e ajuste os gráficos para focar em taxa de quadros (FPS)."
        elif any(p in txt_lower for p in ["minecraft", "bloco", "sobrevivencia"]):
            resposta = "OmniAI: 🧱 Minecraft é clássico! A dica de ouro é sempre fazer uma base iluminada antes da primeira noite e nunca cavar direto para baixo."
        elif any(p in txt_lower for p in ["roblox", "blox", "robux"]):
            resposta = "OmniAI: 🔴 Roblox tem milhares de experiências incríveis! Você pode abrir o launcher oficial rapidamente pela aba de Jogos do nosso overlay."
        elif any(p in txt_lower for p in ["steam", "valves"]):
            resposta = "OmniAI: 🚀 A Steam é a maior plataforma de PC gaming. Dica: fique de olho nas promoções sazonais de verão e inverno para garantir ótimos jogos por um preço menor!"
        elif any(p in txt_lower for p in ["epic", "epic games", "jogo gratis"]):
            resposta = "OmniAI: 🎁 A Epic Games Store dá jogos de graça todas as quintas-feiras! Vale sempre a pena dar uma olhada no site deles para resgatar os títulos."
        elif any(p in txt_lower for p in ["melhor", "indicação", "indicar", "recomenda", "jogos bons"]):
            resposta = "OmniAI: 🏆 Depende do seu estilo! Se gosta de ação, jogos de tiro e aventura em mundo aberto são ótimos. Se prefere relaxar, jogos de simuladores, indies ou de construção fazem muito sucesso."
        elif any(p in txt_lower for p in ["multiplayer", "online", "amigos", "co-op"]):
            resposta = "OmniAI: 👥 Jogar com amigos é outra experiência! Jogos competitivos testam a mira e a estratégia, enquanto os cooperativos focam no trabalho em equipe (e em boas risadas)."
        elif any(p in txt_lower for p in ["olá", "oi", "bom dia", "boa tarde", "boa noite", "eae"]):
            resposta = "OmniAI: Olá! Pronto para a jogatina de hoje? Me pergunte sobre dicas de games, atalhos ou desempenho do PC!"
        elif any(p in txt_lower for p in ["ajuda", "socorro", "o que fazer", "comandos"]):
            resposta = "OmniAI: 🛠️ Você pode me perguntar sobre: Jogos, FPS/Desempenho, Steam, Roblox, Minecraft, Epic Games ou como usar o OmniOverlay!"
        else:
            resposta = f"OmniAI: Entendi o que você disse sobre '{texto}'. Como sou a IA local do OmniOverlay, adoro falar sobre games, atalhos e organização de PC. Quer uma dica sobre algum jogo específico?"

        self.chat_historico.insert("end", f"{resposta}\n\n")
        self.chat_historico.configure(state="disabled")
        self.chat_historico.see("end")
        self.entry_chat.delete(0, "end")

    def montar_aba_player_video(self):
        video_container = ctk.CTkFrame(self.tab_video, fg_color="transparent")
        video_container.pack(fill="both", expand=True, padx=8, pady=8)

        ctk.CTkLabel(
            video_container,
            text="🎬 Player de Vídeo em Overlay",
            font=("Segoe UI", 13, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))

        controles_video = ctk.CTkFrame(video_container, fg_color=COLOR_BG_CARD, corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        controles_video.pack(side="bottom", fill="x", pady=(4, 0))
        self.dynamic_accent_borders.append(controles_video)

        btn_escolher_video = ctk.CTkButton(
            controles_video,
            text="📁 Abrir Vídeo",
            width=110,
            height=32,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            command=self.carregar_arquivo_video
        )
        btn_escolher_video.pack(side="left", padx=8, pady=8)
        self.dynamic_accent_buttons.append(btn_escolher_video)

        self.btn_play_video = ctk.CTkButton(
            controles_video,
            text="▶️ Play / Pause",
            width=110,
            height=32,
            fg_color=COLOR_BG_SURFACE,
            hover_color=COLOR_BORDER,
            text_color=COLOR_TEXT_PRIMARY,
            command=self.toggle_play_video
        )
        self.btn_play_video.pack(side="left", padx=4, pady=8)

        self.lbl_video_display = ctk.CTkLabel(video_container, text="Nenhum vídeo carregado", fg_color="#0F172A", corner_radius=8)
        self.lbl_video_display.pack(side="top", fill="both", expand=True, pady=(0, 4))

    def carregar_arquivo_video(self):
        caminho = filedialog.askopenfilename(
            title="Selecione um Vídeo",
            filetypes=[("Arquivos de Vídeo", "*.mp4 *.avi *.mkv *.mov"), ("Todos os Arquivos", "*.*")]
        )
        if caminho:
            self.video_rodando = False
            time.sleep(0.1) 
            self.video_path = caminho
            self.video_rodando = True
            self.video_pausado = False
            self.btn_play_video.configure(text="⏸️ Pausar")
            
            self.video_thread = threading.Thread(target=self._executar_loop_video, daemon=True)
            self.video_thread.start()

    def _executar_loop_video(self):
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0 or fps > 60:
            fps = 30
        delay = 1.0 / fps

        while self.video_rodando and cap.isOpened():
            if self.video_pausado:
                time.sleep(0.1)
                continue

            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            try:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(frame_rgb)
                
                max_w = max(self.lbl_video_display.winfo_width(), 300)
                max_h = max(self.lbl_video_display.winfo_height(), 200)
                
                orig_w, orig_h = pil_img.size
                ratio = min(max_w / orig_w, max_h / orig_h)
                new_w = int(orig_w * ratio)
                new_h = int(orig_h * ratio)
                
                pil_img = pil_img.resize((new_w, new_h), Image.Resampling.BILINEAR)
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(new_w, new_h))
                
                self.after(0, lambda img=ctk_img: self.lbl_video_display.configure(image=img, text=""))
            except Exception:
                pass

            time.sleep(delay)

        cap.release()

    def toggle_play_video(self):
        if not self.video_path:
            return
        
        self.video_pausado = not self.video_pausado
        if self.video_pausado:
            self.btn_play_video.configure(text="▶️ Retomar")
        else:
            self.btn_play_video.configure(text="⏸️ Pausar")

    def montar_aba_config(self):
        config_container = ctk.CTkScrollableFrame(self.tab_config, fg_color="transparent")
        config_container.pack(fill="both", expand=True, padx=4, pady=4)

        ctk.CTkLabel(
            config_container,
            text="🛡️ Painel Administrativo (Root Master)",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        ).pack(anchor="w", padx=8, pady=(4, 8))

        frame_root = ctk.CTkFrame(config_container, fg_color=COLOR_BG_CARD, corner_radius=10, border_color="#9333EA", border_width=1)
        frame_root.pack(fill="x", padx=4, pady=4, ipady=6)
        self.dynamic_accent_borders.append(frame_root)

        ctk.CTkLabel(
            frame_root,
            text="Acesse o Painel ADM protegido por senha:",
            font=("Segoe UI", 11),
            text_color=COLOR_TEXT_PRIMARY
        ).pack(anchor="w", padx=12, pady=(8, 4))

        btn_abrir_adm = ctk.CTkButton(
            frame_root,
            text="🔐 Abrir Painel ADM",
            width=220,
            height=34,
            fg_color="#9333EA",
            hover_color="#7E22CE",
            text_color="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            command=self.acao_abrir_painel_adm
        )
        btn_abrir_adm.pack(anchor="w", padx=12, pady=(0, 10))

        ctk.CTkLabel(
            config_container,
            text="⚙️ Aparência & Temas de Cores",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        ).pack(anchor="w", padx=8, pady=(16, 8))

        frame_cores = ctk.CTkFrame(config_container, fg_color=COLOR_BG_CARD, corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        frame_cores.pack(fill="x", padx=4, pady=4, ipady=4)
        self.dynamic_accent_borders.append(frame_cores)

        ctk.CTkLabel(
            frame_cores,
            text="Cor de Destaque do Sistema:",
            font=("Segoe UI", 11),
            text_color=COLOR_TEXT_PRIMARY
        ).pack(anchor="w", padx=12, pady=(8, 4))

        botoes_cores_frame = ctk.CTkFrame(frame_cores, fg_color="transparent")
        botoes_cores_frame.pack(anchor="w", padx=12, pady=(0, 10))

        cores_disponiveis = [("Azul", "azul", "#2563EB"), ("Vermelho", "vermelho", "#DC2626"), ("Verde", "verde", "#16A34A"), ("Roxo", "roxo", "#9333EA")]
        for nome, chave, cor_hex in cores_disponiveis:
            btn_cor = ctk.CTkButton(
                botoes_cores_frame,
                text=nome,
                width=90,
                height=32,
                fg_color=cor_hex,
                hover_color=cor_hex,
                text_color="#FFFFFF",
                font=("Segoe UI", 11, "bold"),
                command=lambda c=chave: self.aplicar_cor_acento(c)
            )
            btn_cor.pack(side="left", padx=4)

        ctk.CTkLabel(
            config_container,
            text="🎨 Cor Sólida de Fundo do Perfil",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        ).pack(anchor="w", padx=8, pady=(16, 8))

        frame_fundo_cor = ctk.CTkFrame(config_container, fg_color=COLOR_BG_CARD, corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        frame_fundo_cor.pack(fill="x", padx=4, pady=4, ipady=4)
        self.dynamic_accent_borders.append(frame_fundo_cor)

        ctk.CTkLabel(
            frame_fundo_cor,
            text="Selecione um estilo de cor para o plano de fundo:",
            font=("Segoe UI", 11),
            text_color=COLOR_TEXT_PRIMARY
        ).pack(anchor="w", padx=12, pady=(8, 4))

        botoes_fundo_frame = ctk.CTkFrame(frame_fundo_cor, fg_color="transparent")
        botoes_fundo_frame.pack(anchor="w", padx=12, pady=(0, 10))

        cores_fundo_opcoes = [
            ("Dark Midnight", "#0F172A"),
            ("Dark Slate", "#1E293B"),
            ("Azul Profundo", "#1E3A8A"),
            ("Roxo Noturno", "#3B0764"),
            ("Verde Militar", "#064E3B")
        ]
        for nome_c, hex_c in cores_fundo_opcoes:
            btn_f_cor = ctk.CTkButton(
                botoes_fundo_frame,
                text=nome_c,
                width=110,
                height=30,
                fg_color=hex_c,
                hover_color=hex_c,
                text_color="#FFFFFF",
                font=("Segoe UI", 10, "bold"),
                command=lambda hc=hex_c: self.alterar_cor_fundo_perfil(hc)
            )
            btn_f_cor.pack(side="left", padx=3)

        ctk.CTkLabel(
            config_container,
            text="📊 Monitoramento Detalhado de Hardware",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        ).pack(anchor="w", padx=8, pady=(16, 8))

        frame_hw_detalhado = ctk.CTkFrame(config_container, fg_color=COLOR_BG_CARD, corner_radius=10, border_color=COLOR_BORDER, border_width=1)
        frame_hw_detalhado.pack(fill="x", padx=4, pady=4, ipady=8)
        self.dynamic_accent_borders.append(frame_hw_detalhado)

        ctk.CTkLabel(frame_hw_detalhado, text="Uso da CPU:", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=12, pady=(6, 0))
        self.bar_cpu_detalhada = ctk.CTkProgressBar(frame_hw_detalhado, height=12)
        self.bar_cpu_detalhada.pack(fill="x", padx=12, pady=2)
        self.bar_cpu_detalhada.set(0)

        self.lbl_cpu_valor_detalhado = ctk.CTkLabel(frame_hw_detalhado, text="0.0%", font=("Segoe UI", 10), text_color=COLOR_TEXT_PRIMARY)
        self.lbl_cpu_valor_detalhado.pack(anchor="e", padx=12)

        ctk.CTkLabel(frame_hw_detalhado, text="Uso da Memória RAM:", font=("Segoe UI", 10, "bold"), text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=12, pady=(6, 0))
        self.bar_ram_detalhada = ctk.CTkProgressBar(frame_hw_detalhado, height=12)
        self.bar_ram_detalhada.pack(fill="x", padx=12, pady=2)
        self.bar_ram_detalhada.set(0)

        self.lbl_ram_valor_detalhado = ctk.CTkLabel(frame_hw_detalhado, text="0.0%", font=("Segoe UI", 10), text_color=COLOR_TEXT_PRIMARY)
        self.lbl_ram_valor_detalhado.pack(anchor="e", padx=12)

    def acao_abrir_painel_adm(self):
        JanelaSenhaModal(self.controller, lambda: PainelAdmWindow(self.controller))

    def alterar_cor_fundo_perfil(self, hex_cor):
        if self.controller.modo_tema_atual == "light":
            print("[AVISO] Você está no Modo Claro. Mude para o Modo Escuro para customizar cores sólidas escuras de fundo.")
            return

        if self.controller.perfil_ativo:
            self.controller.perfil_ativo["cor_fundo"] = hex_cor
            AccountManager.salvar_dados(self.controller.dados_config)
            self.controller.atualizar_cor_fundo_raiz(hex_cor)


class OmniOverlayApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        inicializar_banco_sql()

        self.dados_config = AccountManager.carregar_dados()
        self.modo_tema_atual = self.dados_config.get("modo_tema", "dark")
        ctk.set_appearance_mode(self.modo_tema_atual)

        self.title("OmniOverlay")
        self.geometry("920x800")
        self.overrideredirect(False)
        self.attributes("-alpha", 0.98)

        self.perfil_ativo = None
        
        cor_inicial_container = "#F1F5F9" if self.modo_tema_atual == "light" else "#0F172A"
        self.container = ctk.CTkFrame(self, fg_color=cor_inicial_container)
        self.container.pack(fill="both", expand=True)

        self.profile_frame = None
        self.dashboard_frame = None

        self.hotkey_manager = GlobalHotkeyManager(self)
        self.hotkey_manager.iniciar()

        self.centralizar_janela(920, 800)
        self.verificar_perfil_inicial()

    def atualizar_cor_fundo_raiz(self, hex_cor):
        try:
            self.container.configure(fg_color=hex_cor)
        except Exception as e:
            print(f"[ERRO] {e}")

    def centralizar_janela(self, largura, altura):
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def alternar_visibilidade_overlay(self):
        if self.state() == "withdrawn":
            self.deiconify()
            self.focus_force()
        else:
            self.withdraw()

    def verificar_perfil_inicial(self):
        ultimo_id = self.dados_config.get("ultimo_perfil", "p1")
        perfis = self.dados_config.get("perfis", [])
        
        perfil_encontrado = next((p for p in perfis if p["id"] == ultimo_id), None)
        if not perfil_encontrado and len(perfis) > 0:
            perfil_encontrado = perfis[0]

        if perfil_encontrado:
            self.entrar_no_perfil(perfil_encontrado)
        else:
            self.abrir_seletor_perfis()

    def entrar_no_perfil(self, perfil):
        self.perfil_ativo = perfil
        self.dados_config["ultimo_perfil"] = perfil["id"]
        AccountManager.salvar_dados(self.dados_config)

        if self.profile_frame:
            self.profile_frame.destroy()
            self.profile_frame = None

        if self.dashboard_frame:
            self.dashboard_frame.destroy()

        self.dashboard_frame = DashboardFrame(self.container, self)
        self.dashboard_frame.pack(fill="both", expand=True)
        self.dashboard_frame.carregar_perfil(perfil)
        
        if self.modo_tema_atual == "light":
            self.atualizar_cor_fundo_raiz("#F1F5F9")
        else:
            self.atualizar_cor_fundo_raiz(perfil.get("cor_fundo", "#0F172A"))

    def abrir_seletor_perfis(self):
        if self.dashboard_frame:
            self.dashboard_frame.destroy()
            self.dashboard_frame = None

        if self.profile_frame:
            self.profile_frame.destroy()

        self.profile_frame = ProfileSelectorFrame(self.container, self)
        self.profile_frame.pack(fill="both", expand=True)

        if self.modo_tema_atual == "light":
            self.atualizar_cor_fundo_raiz("#F1F5F9")
        else:
            cor_atual = self.perfil_ativo.get("cor_fundo", "#0F172A") if self.perfil_ativo else "#0F172A"
            self.atualizar_cor_fundo_raiz(cor_atual)

        self.profile_frame.atualizar_lista()

    def alternar_tema_global(self):
        if self.modo_tema_atual == "dark":
            self.modo_tema_atual = "light"
        else:
            self.modo_tema_atual = "dark"

        ctk.set_appearance_mode(self.modo_tema_atual)
        self.dados_config["modo_tema"] = self.modo_tema_atual
        AccountManager.salvar_dados(self.dados_config)

        if self.modo_tema_atual == "light":
            self.atualizar_cor_fundo_raiz("#F1F5F9")
        else:
            if self.perfil_ativo:
                self.atualizar_cor_fundo_raiz(self.perfil_ativo.get("cor_fundo", "#0F172A"))

        if self.dashboard_frame:
            self.dashboard_frame.destroy()
            self.dashboard_frame = DashboardFrame(self.container, self)
            if self.perfil_ativo:
                self.dashboard_frame.pack(fill="both", expand=True)
                self.dashboard_frame.carregar_perfil(self.perfil_ativo)
        elif self.profile_frame:
            self.profile_frame.destroy()
            self.profile_frame = ProfileSelectorFrame(self.container, self)
            self.profile_frame.pack(fill="both", expand=True)
            self.profile_frame.atualizar_lista()


if __name__ == "__main__":
    app = OmniOverlayApp()
    app.mainloop()
    
    
def atualizar_fundo_tela(self, caminho_img):
    if caminho_img and os.path.exists(caminho_img):
        try:
                pil_img = Image.open(caminho_img)
                pil_img = pil_img.resize((920, 800), Image.Resampling.LANCZOS)
                
                # Salvamos a referência para evitar que o Garbage Collector apague a imagem
                self.imagem_fundo_atual = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(920, 800))
                
                self.lbl_fundo_bg.configure(image=self.imagem_fundo_atual, text="")
                self.lbl_fundo_bg.place(x=0, y=0, relwidth=1, relheight=1)
                self.lbl_fundo_bg.lower() # Mantém estritamente no fundo
                return
        except Exception as e:
                print(f"[ERRO] Falha ao carregar fundo de tela: {e}")
        
        self.imagem_fundo_atual = None
        self.lbl_fundo_bg.configure(image="", text="")
        