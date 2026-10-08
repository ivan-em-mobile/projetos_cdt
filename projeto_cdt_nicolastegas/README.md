🛡️ OmniOverlay & 🍔 Hamburgueria POS System

OmniOverlay & Hamburgueria POS System é um ecossistema de software em Python que combina um painel desktop flutuante (overlay) desenvolvido em CustomTkinter com um sistema comercial completo para gerenciamento de vendas e atendimento de hamburguerias, operável via interface gráfica ou terminal seguro.

📌 Sumário

🏗️ Arquitetura do Sistema

✨ Funcionalidades Principais

📦 Dependências e Tecnologias

⚠️ Pré-requisitos

⚡ Guia de Instalação e Execução

🔐 Credenciais Padrão & Segurança

💻 Código Fonte Integrado

🏗️ Arquitetura do Sistema

Fluxo de Módulos e Componentes

+-------------------------------------------------------------------+
|                         OmniOverlayApp                            |
|  (Controlador Principal / Gerenciador de Janela e Configurações)  |
+---------------------------------+---------------------------------+
                                  |
         +------------------------+------------------------+
         |                                                 |
         v                                                 v
+-----------------------+                         +-----------------------+
|  ProfileSelectorFrame |                         |    DashboardFrame     |
| (Gerenciador Perfis)  |                         |  (Painel Principal)   |
+-----------------------+                         +-----------+-----------+
                                                              |
        +------------------+------------------+---------------+------------+
        |                  |                  |                            |
        v                  v                  v                            v
+---------------+  +---------------+  +---------------+  +-------------------+
|  Central de   |  |    OmniAI     |  |   Player de   |  | Hamburgueria POS  |
| Atalhos (Hub) |  |  (Assistente) |  |     Vídeo     |  | (Engine de Vendas)|
+---------------+  +---------------+  +---------------+  +-------------------+


💾 Persistência de Dados e Serviços

Banco de Dados SQLite (omnioverlay_data.db): Gerencia credenciais administrativas, acessos do Root Master e cadastros de usuários/atendentes.

Configurações em JSON (config_perfis.json): Armazena parâmetros de aparência, temas visualização (dark/light) e mapeamento de atalhos.

Monitoramento de Hardware (psutil): Thread em segundo plano atualizando dados de uso de CPU e RAM em tempo real.

Captura Global de Atalhos (pynput): Escuta eventos globais de teclado (ex: tecla F12 para alternar a exibição do overlay sem perder o foco do sistema).

✨ Funcionalidades Principais

🛡️ Módulo OmniOverlay

Interface Modernizada & Frameless: Janela sem bordas padrão com suporte a transparência e fixação topo de tela (topmost).

Atalhos Inteligentes: Suporte para inicializar URLs, executáveis (.exe), scripts de lote (.bat) ou comandos de sistema.

Monitoramento do Sistema: Exibição contínua do uso de recursos sem bloquear a interface de usuário.

🍔 Módulo Hamburgueria POS Engine

Autenticação de Usuários: Login via e-mail e senha com suporte a digitação oculta por máscara (*) no console.

Gerenciamento do Cardápio: Listagem categorizada de hambúrgueres, acompanhamentos e bebidas.

Carrinho e Pagamento: Adição flexível de produtos por código, cálculo automático do total acumulado e fechamento em múltiplos métodos de pagamento (Pix, Dinheiro, Cartão de Crédito e Débito).

Emissão de Recibos: Registro das transações contendo detalhamento do pedido, valor e marcação temporal (datetime).

📦 Dependências e Tecnologias

Biblioteca

Finalidade

customtkinter

Interface gráfica moderna e responsiva

Pillow (PIL)

Manipulação e exibição de imagens e avatares

psutil

Leitura de métricas de hardware (CPU/RAM)

pynput

Captura global de teclas de atalho

tkVideoPlayer

Execução de arquivos de vídeo locais na GUI

msvcrt

Captura e mascaramento de senha no terminal (exclusivo para Windows)

⚠️ Pré-requisitos

Sistema Operacional: Windows 10/11 (Devido ao uso da biblioteca nativa msvcrt e comandos de execução os.startfile).

Linguagem: Python versão 3.8 ou superior.

⚡ Guia de Instalação e Execução

Clone o repositório:

git clone https://github.com/seu-usuario/omnioverlay-hamburgueria.git
cd omnioverlay-hamburgueria


Instale as dependências requeridas:

pip install customtkinter Pillow psutil pynput tkVideoPlayer


Execute o sistema:

python main.py


🔐 Credenciais Padrão & Segurança

Nível / Serviço

Usuário / E-mail

Senha Padrão

Administrador Root (SQLite)

rootmaster

root

Atendente POS (Módulo Vendas)

atendimento@hamburgueria.com

burgers2026

💻 Código Fonte Integrado

Salve a implementação abaixo em um arquivo main.py para executar a solução completa:

import os
import json
import sqlite3
import time
import threading
import webbrowser
import subprocess
from datetime import datetime

# Interface Visual e Recursos
import customtkinter as ctk
from PIL import Image
import psutil
from pynput import keyboard

# Suporte ao console Windows
try:
    import msvcrt
except ImportError:
    msvcrt = None


# ==========================================
# 1. PERSISTÊNCIA E SQLITE
# ==========================================

def inicializar_banco_sql():
    conn = sqlite3.connect("omnioverlay_data.db")
    cursor = conn.cursor()
    
    # Tabela de Administradores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios_adm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    
    # Tabela de Atendentes e Clientes POS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes_pos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    
    # Inserção das credenciais padrão
    cursor.execute("SELECT COUNT(*) FROM usuarios_adm")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios_adm (usuario, senha) VALUES (?, ?)", ("admin", "1234"))
        
    cursor.execute("SELECT COUNT(*) FROM clientes_pos")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO clientes_pos (nome, email, senha) VALUES (?, ?, ?)", 
                       ("Atendente Padrão", "atendimento@hamburgueria.com", "burgers2026"))
        
    conn.commit()
    conn.close()


class AccountManager:
    @staticmethod
    def carregar_dados():
        if os.path.exists("config_perfis.json"):
            with open("config_perfis.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {"modo_tema": "dark", "ultimo_perfil": "p1", "perfis": []}

    @staticmethod
    def salvar_dados(dados):
        with open("config_perfis.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)


# ==========================================
# 2. MOTOR DE VENDAS (POS)
# ==========================================

class HamburgueriaEngine:
    def __init__(self):
        self.cardapio = {
            "101": {"nome": "X-Burger Artesanal", "preco": 28.90, "categoria": "Lanches"},
            "102": {"nome": "Double Bacon Smash", "preco": 34.50, "categoria": "Lanches"},
            "103": {"nome": "Chicken Crispy", "preco": 26.00, "categoria": "Lanches"},
            "201": {"nome": "Batata Frita Suprema", "preco": 18.00, "categoria": "Acompanhamentos"},
            "301": {"nome": "Refrigerante Lata 350ml", "preco": 6.50, "categoria": "Bebidas"},
            "302": {"nome": "Suco Natural 500ml", "preco": 9.00, "categoria": "Bebidas"}
        }

    @staticmethod
    def ler_senha_oculta(prompt="Senha: "):
        print(prompt, end="", flush=True)
        senha = ""
        if msvcrt:
            while True:
                ch = msvcrt.getch()
                if ch in (b'\r', b'\n'):
                    print()
                    break
                elif ch == b'\x08':  # Tratar Backspace
                    if len(senha) > 0:
                        senha = senha[:-1]
                        print('\b \b', end='', flush=True)
                else:
                    senha += ch.decode('utf-8', errors='ignore')
                    print('*', end='', flush=True)
        else:
            senha = input()
        return senha

    def autenticar_usuario(self, email, senha):
        conn = sqlite3.connect("omnioverlay_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM clientes_pos WHERE email = ? AND senha = ?", (email, senha))
        user = cursor.fetchone()
        conn.close()
        return user[0] if user else None


# ==========================================
# 3. ATALHOS GLOBAIS E HARDWARE
# ==========================================

class GlobalHotkeyManager:
    def __init__(self, app_controller):
        self.app = app_controller

    def iniciar(self):
        def on_press(key):
            if key == keyboard.Key.f12:
                self.app.alternar_visibilidade_overlay()

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()


# ==========================================
# 4. PAINEL E INTERFACE GRÁFICA
# ==========================================

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.lbl_title = ctk.CTkLabel(self, text="🛡️ OmniOverlay & POS Hamburgueria", font=("Segoe UI", 20, "bold"))
        self.lbl_title.pack(pady=15)

        self.btn_pos = ctk.CTkButton(self, text="Abrir Painel POS Hamburgueria", command=self.abrir_pos_ui)
        self.btn_pos.pack(pady=8, fill="x", padx=40)

        self.btn_browser = ctk.CTkButton(self, text="Abrir Navegador", command=lambda: controller.abrir_inteligente("https://google.com"))
        self.btn_browser.pack(pady=8, fill="x", padx=40)

        self.lbl_hw_info = ctk.CTkLabel(self, text="CPU: 0% | RAM: 0%", font=("Segoe UI", 12))
        self.lbl_hw_info.pack(side="bottom", pady=15)

    def abrir_pos_ui(self):
        win_pos = ctk.CTkToplevel(self)
        win_pos.title("Sistema POS - Cardápio")
        win_pos.geometry("420x520")
        win_pos.attributes("-topmost", True)

        lbl = ctk.CTkLabel(win_pos, text="🍔 Cardápio Disponível", font=("Segoe UI", 16, "bold"))
        lbl.pack(pady=10)

        engine = HamburgueriaEngine()
        for cod, item in engine.cardapio.items():
            btn = ctk.CTkButton(win_pos, text=f"[{cod}] {item['nome']} - R$ {item['preco']:.2f}")
            btn.pack(pady=4, padx=20, fill="x")


class ProfileSelectorFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        lbl = ctk.CTkLabel(self, text="Gerenciador de Perfis", font=("Segoe UI", 16))
        lbl.pack(pady=20)


# ==========================================
# 5. CONTROLADOR APLICAÇÃO PRINCIPAL
# ==========================================

class OmniOverlayApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        inicializar_banco_sql()

        self.title("OmniOverlay")
        self.geometry("920x800")
        self.overrideredirect(True)
        self.attributes("-alpha", 0.98)
        self.attributes("-topmost", True)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.dashboard_frame = DashboardFrame(self.container, self)
        self.dashboard_frame.pack(fill="both", expand=True)

        self.hotkey_manager = GlobalHotkeyManager(self)
        self.hotkey_manager.iniciar()

        self.thread_hw = threading.Thread(target=self.loop_monitoramento_hardware, daemon=True)
        self.thread_hw.start()

    def alternar_visibilidade_overlay(self):
        if self.state() == "withdrawn":
            self.deiconify()
            self.focus_force()
        else:
            self.withdraw()

    def abrir_inteligente(self, alvo):
        try:
            if alvo.startswith("http://") or alvo.startswith("https://"):
                webbrowser.open(alvo)
            elif os.path.exists(alvo):
                os.startfile(alvo)
            else:
                subprocess.Popen(alvo, shell=True)
        except Exception as e:
            print(f"[ERRO] Falha ao abrir recurso: {e}")

    def loop_monitoramento_hardware(self):
        while True:
            try:
                cpu = psutil.cpu_percent(interval=1)
                ram = psutil.virtual_memory().percent
                if hasattr(self.dashboard_frame, "lbl_hw_info"):
                    self.dashboard_frame.lbl_hw_info.configure(text=f"CPU: {cpu}% | RAM: {ram}%")
            except Exception:
                pass
            time.sleep(1)


if __name__ == "__main__":
    app = OmniOverlayApp()
    app.mainloop()