import os
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import requests
import threading
import unicodedata
import re
from datetime import datetime

try:
    from PIL import Image, ImageTk
    from io import BytesIO
    PIL_OK = True
except ImportError:
    PIL_OK = False


# ============================================================
# CONFIGURAÇÕES E DADOS DO RESTAURANTE
# ============================================================

# 1. Obtém o caminho absoluto da pasta onde ESTE arquivo .py está guardado
PASTA_DO_SCRIPT = os.path.dirname(os.path.abspath(__file__))

# 2. Define que o banco de dados será GRAVADO e ABERTO na mesma pasta do script
DB_NAME = os.path.join(PASTA_DO_SCRIPT, "restaurante.db")

INFO_RESTAURANTE = {
    "nome": "Gourmet Service",
    "endereco": "Av. Paulista, 1000 - Bela Vista, São Paulo - SP",
    "horario_abertura": 12,   # 12:00 PM (Meio-dia)
    "horario_fechamento": 20, # 8:00 PM (20:00)
    "taxa_entrega": "Grátis para compras acima de R$ 50,00 (Fixa R$ 7,00 para demais)",
    "tempo_entrega": "30 a 50 minutos"
}

CORES = {
    "dark": {
        "bg": "#121212",
        "card": "#1E1E1E",
        "text": "#FFFFFF",
        "sub": "#BDBDBD",
        "accent": "#693DE2",
        "accent2": "#8B39E7",
        "entry": "#292929",
        "success": "#35C759",
        "danger": "#E53935"
    },
    "light": {
        "bg": "#F4F4F9",
        "card": "#FFFFFF",
        "text": "#111111",
        "sub": "#666666",
        "accent": "#1D46B9",
        "accent2": "#0065D9",
        "entry": "#EEEEF5",
        "success": "#168A32",
        "danger": "#C62828"
    }
}

TEMA = "dark"

PRODUTOS = {
    "🍔 HAMBÚRGUERES": [
        {
            "nome": "Clássico Smash",
            "preco": 22.00,
            "descricao": "2x smash 80g e cheddar.",
            "imagem": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=500"
        },
        {
            "nome": "Chicken Crispy",
            "preco": 25.90,
            "descricao": "Frango crocante e coleslaw.",
            "imagem": "https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=500"
        },
        {
            "nome": "Poderoso Chefão",
            "preco": 34.90,
            "descricao": "Blend 180g, gorgonzola e bacon.",
            "imagem": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500"
        },
        {
            "nome": "Duplo Bacon",
            "preco": 38.50,
            "descricao": "2x blends 180g e triplo bacon.",
            "imagem": "https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=500"
        }
    ],
    "🍕 PIZZAS": [
        {
            "nome": "Marguerita",
            "preco": 42.00,
            "descricao": "Mussarela, tomate e manjericão.",
            "imagem": "https://images.unsplash.com/photo-1579751626657-72bc17010498?w=500"
        },
        {
            "nome": "Calabresa",
            "preco": 45.00,
            "descricao": "Molho, mussarela e calabresa.",
            "imagem": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=500"
        },
        {
            "nome": "Quatro Queijos",
            "preco": 50.00,
            "descricao": "Mussarela, provolone, gorgonzola e parmesão.",
            "imagem": "https://images.unsplash.com/photo-1571407970349-bc81e7e96d47?w=500"
        }
    ],
    "🥤 BEBIDAS": [
        {
            "nome": "Refrigerante",
            "preco": 6.50,
            "descricao": "Refrigerante gelado.",
            "imagem": "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=500"
        },
        {
            "nome": "Soda Artesanal",
            "preco": 12.00,
            "descricao": "Soda refrescante e artesanal.",
            "imagem": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500"
        },
        {
            "nome": "Milkshake",
            "preco": 18.00,
            "descricao": "Milkshake cremoso.",
            "imagem": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=500"
        }
    ]
}


# ============================================================
# BANCO DE DADOS
# ============================================================

def criar_banco():
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            usuario TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            usuario TEXT NOT NULL,
            data_hora TEXT NOT NULL,
            itens TEXT NOT NULL,
            total REAL NOT NULL,
            cep TEXT NOT NULL,
            endereco TEXT NOT NULL,
            numero TEXT NOT NULL,
            forma_pagamento TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def normalizar_texto(texto):
    texto = str(texto).lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto


def formatar_moeda(valor):
    return f"R$ {valor:.2f}".replace(".", ",")


def restaurante_aberto():
    hora_atual = datetime.now().hour
    return INFO_RESTAURANTE["horario_abertura"] <= hora_atual < INFO_RESTAURANTE["horario_fechamento"]


def todos_produtos():
    lista = []
    for categoria, produtos in PRODUTOS.items():
        for produto in produtos:
            item = produto.copy()
            item["categoria"] = categoria
            lista.append(item)
    return lista


def procurar_produto(texto):
    texto = normalizar_texto(texto)

    for produto in todos_produtos():
        nome = normalizar_texto(produto["nome"])
        if nome in texto:
            return produto

    palavras = texto.split()
    for produto in todos_produtos():
        nome = normalizar_texto(produto["nome"])
        if any(palavra in nome for palavra in palavras if len(palavra) >= 4):
            return produto

    return None


# ============================================================
# APLICAÇÃO
# ============================================================

class GourmetService:

    def __init__(self, root):
        self.root = root
        self.root.title("Gourmet Service")
        self.root.geometry("1050x720")
        self.root.minsize(900, 620)

        self.usuario_atual = None
        self.nome_atual = None

        self.carrinho = {}

        self.imagens = []
        self.janela_chat = None
        self.chat_texto = None
        self.chat_entry = None

        criar_banco()
        self.aplicar_estilo()
        self.mostrar_login()

    # ========================================================
    # TEMA
    # ========================================================

    def aplicar_estilo(self):
        cores = CORES[TEMA]
        self.root.configure(bg=cores["bg"])

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "TButton",
            background=cores["accent"],
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=8
        )

        style.map(
            "TButton",
            background=[("active", cores["accent2"])]
        )

        style.configure(
            "TEntry",
            fieldbackground=cores["entry"],
            foreground=cores["text"],
            insertcolor=cores["text"]
        )

    def alternar_tema(self):
        global TEMA
        TEMA = "light" if TEMA == "dark" else "dark"
        self.aplicar_estilo()

        if self.usuario_atual:
            self.mostrar_menu()
        else:
            self.mostrar_login()

    def sair_da_conta(self):
        self.usuario_atual = None
        self.nome_atual = None
        self.carrinho = {}
        if self.janela_chat:
            self.fechar_chat()
        self.mostrar_login()

    # ========================================================
    # LIMPAR TELA
    # ========================================================

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.imagens.clear()

    # ========================================================
    # LOGIN
    # ========================================================

    def mostrar_login(self):
        self.limpar_tela()
        cores = CORES[TEMA]

        frame = tk.Frame(self.root, bg=cores["bg"])
        frame.pack(expand=True)

        tk.Label(
            frame,
            text="🍔 GOURMET SERVICE",
            font=("Arial", 28, "bold"),
            bg=cores["bg"],
            fg=cores["accent2"]
        ).pack(pady=(20, 5))

        status_txt = "🟢 Aberto Agora" if restaurante_aberto() else "🔴 Fechado Agora"
        tk.Label(
            frame,
            text=f"Seu restaurante completo | Status: {status_txt}",
            font=("Arial", 11, "bold"),
            bg=cores["bg"],
            fg=cores["success"] if restaurante_aberto() else cores["danger"]
        ).pack(pady=(0, 20))

        card = tk.Frame(frame, bg=cores["card"], padx=35, pady=30)
        card.pack()

        tk.Label(
            card,
            text="Usuário",
            bg=cores["card"],
            fg=cores["text"],
            font=("Arial", 11, "bold")
        ).pack(anchor="w")

        self.login_usuario = tk.Entry(
            card,
            width=35,
            bg=cores["entry"],
            fg=cores["text"],
            insertbackground=cores["text"],
            relief="flat",
            font=("Arial", 11)
        )
        self.login_usuario.pack(pady=(5, 15), ipady=7)

        tk.Label(
            card,
            text="Senha",
            bg=cores["card"],
            fg=cores["text"],
            font=("Arial", 11, "bold")
        ).pack(anchor="w")

        self.login_senha = tk.Entry(
            card,
            width=35,
            show="*",
            bg=cores["entry"],
            fg=cores["text"],
            insertbackground=cores["text"],
            relief="flat",
            font=("Arial", 11)
        )
        self.login_senha.pack(pady=(5, 20), ipady=7)

        ttk.Button(card, text="ENTRAR", command=self.fazer_login).pack(fill="x", pady=5)
        ttk.Button(card, text="CRIAR NOVA CONTA", command=self.mostrar_cadastro).pack(fill="x", pady=5)

        tk.Button(
            card,
            text="☀️ / 🌙 Alterar tema",
            command=self.alternar_tema,
            bg=cores["card"],
            fg=cores["accent2"],
            relief="flat",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(pady=(15, 0))

        self.login_usuario.bind("<Return>", lambda event: self.fazer_login())
        self.login_senha.bind("<Return>", lambda event: self.fazer_login())

    def fazer_login(self):
        usuario = self.login_usuario.get().strip()
        senha = self.login_senha.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha usuário e senha.")
            return

        conexao = sqlite3.connect(DB_NAME)
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT nome FROM usuarios WHERE usuario = ? AND senha = ?",
            (usuario, senha)
        )

        resultado = cursor.fetchone()
        conexao.close()

        if resultado:
            self.usuario_atual = usuario
            self.nome_atual = resultado[0]
            self.carrinho = {}
            self.mostrar_menu()
        else:
            messagebox.showerror("Login", "Usuário ou senha incorretos.")

    # ========================================================
    # CADASTRO
    # ========================================================

    def mostrar_cadastro(self):
        self.limpar_tela()
        cores = CORES[TEMA]

        frame = tk.Frame(self.root, bg=cores["bg"])
        frame.pack(expand=True)

        tk.Label(
            frame,
            text="👤 CRIAR CONTA",
            font=("Arial", 26, "bold"),
            bg=cores["bg"],
            fg=cores["accent2"]
        ).pack(pady=(10, 25))

        card = tk.Frame(frame, bg=cores["card"], padx=35, pady=30)
        card.pack()

        campos = []
        for texto, mostrar in [
            ("Nome completo", ""),
            ("Usuário", ""),
            ("Senha", "*"),
            ("Confirmar senha", "*")
        ]:
            tk.Label(
                card,
                text=texto,
                bg=cores["card"],
                fg=cores["text"],
                font=("Arial", 11, "bold")
            ).pack(anchor="w")

            entrada = tk.Entry(
                card,
                width=35,
                show=mostrar,
                bg=cores["entry"],
                fg=cores["text"],
                insertbackground=cores["text"],
                relief="flat",
                font=("Arial", 11)
            )
            entrada.pack(pady=(5, 14), ipady=7)
            campos.append(entrada)

        self.cad_nome = campos[0]
        self.cad_usuario = campos[1]
        self.cad_senha = campos[2]
        self.cad_confirmar = campos[3]

        ttk.Button(card, text="CRIAR CONTA", command=self.criar_conta).pack(fill="x", pady=5)
        ttk.Button(card, text="VOLTAR PARA LOGIN", command=self.mostrar_login).pack(fill="x", pady=5)

    def criar_conta(self):
        nome = self.cad_nome.get().strip()
        usuario = self.cad_usuario.get().strip()
        senha = self.cad_senha.get()
        confirmar = self.cad_confirmar.get()

        if not nome or not usuario or not senha or not confirmar:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas não são iguais.")
            return

        try:
            conexao = sqlite3.connect(DB_NAME)
            cursor = conexao.cursor()

            cursor.execute(
                "INSERT INTO usuarios (usuario, nome, senha) VALUES (?, ?, ?)",
                (usuario, nome, senha)
            )

            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            self.mostrar_login()

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Esse usuário já existe.")

    # ========================================================
    # MENU
    # ========================================================

    def mostrar_menu(self):
        self.limpar_tela()
        cores = CORES[TEMA]

        header = tk.Frame(self.root, bg=cores["card"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🍔 Gourmet Service",
            font=("Arial", 20, "bold"),
            bg=cores["card"],
            fg=cores["accent2"]
        ).pack(side="left", padx=20)

        tk.Label(
            header,
            text=f"Olá, {self.nome_atual}!",
            font=("Arial", 11),
            bg=cores["card"],
            fg=cores["sub"]
        ).pack(side="left", padx=10)

        ttk.Button(header, text="🚪 Sair", command=self.sair_da_conta).pack(side="right", padx=8)
        ttk.Button(header, text="📜 Histórico", command=self.mostrar_historico).pack(side="right", padx=8)
        ttk.Button(header, text="🤖 Suporte IA", command=self.abrir_chat).pack(side="right", padx=8)
        ttk.Button(header, text="🛒 Carrinho", command=self.mostrar_carrinho).pack(side="right", padx=8)
        ttk.Button(header, text="☀️/🌙", command=self.alternar_tema).pack(side="right", padx=8)

        container = tk.Frame(self.root, bg=cores["bg"])
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg=cores["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

        conteudo = tk.Frame(canvas, bg=cores["bg"])
        conteudo.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=conteudo, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for categoria, produtos in PRODUTOS.items():
            tk.Label(
                conteudo,
                text=categoria,
                font=("Arial", 19, "bold"),
                bg=cores["bg"],
                fg=cores["text"]
            ).pack(anchor="w", padx=25, pady=(25, 12))

            grade = tk.Frame(conteudo, bg=cores["bg"])
            grade.pack(fill="x", padx=20)

            for coluna, produto in enumerate(produtos):
                self.criar_card_produto(grade, produto, coluna)

    def criar_card_produto(self, parent, produto, coluna):
        cores = CORES[TEMA]

        card = tk.Frame(parent, bg=cores["card"], width=280, height=340)
        card.grid(row=0, column=coluna, padx=8, pady=8, sticky="n")
        card.grid_propagate(False)

        imagem_label = tk.Label(
            card,
            text="🍔",
            bg=cores["card"],
            fg=cores["text"],
            font=("Arial", 50)
        )
        imagem_label.pack(pady=(12, 5))

        self.carregar_imagem(produto["imagem"], imagem_label)

        tk.Label(
            card,
            text=produto["nome"],
            font=("Arial", 14, "bold"),
            bg=cores["card"],
            fg=cores["text"]
        ).pack()

        tk.Label(
            card,
            text=produto["descricao"],
            font=("Arial", 9),
            bg=cores["card"],
            fg=cores["sub"],
            wraplength=240
        ).pack(pady=5)

        tk.Label(
            card,
            text=formatar_moeda(produto["preco"]),
            font=("Arial", 15, "bold"),
            bg=cores["card"],
            fg=cores["accent2"]
        ).pack(pady=5)

        ttk.Button(
            card,
            text="➕ Adicionar",
            command=lambda p=produto: self.adicionar_carrinho(p)
        ).pack(padx=25, pady=8, fill="x")

    def carregar_imagem(self, url, label):
        if not PIL_OK:
            return

        def baixar():
            try:
                resposta = requests.get(url, timeout=8)
                resposta.raise_for_status()

                imagem = Image.open(BytesIO(resposta.content))
                imagem.thumbnail((220, 130))

                foto = ImageTk.PhotoImage(imagem)

                def atualizar():
                    self.imagens.append(foto)
                    label.configure(image=foto, text="")

                self.root.after(0, atualizar)

            except Exception:
                pass

        threading.Thread(target=baixar, daemon=True).start()

    # ========================================================
    # HISTÓRICO DE COMPRAS
    # ========================================================

    def mostrar_historico(self):
        self.limpar_tela()
        cores = CORES[TEMA]

        header = tk.Frame(self.root, bg=cores["card"], height=65)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📜 MEUS PEDIDOS ANTERIORES",
            font=("Arial", 18, "bold"),
            bg=cores["card"],
            fg=cores["text"]
        ).pack(side="left", padx=20)

        ttk.Button(header, text="← Voltar ao cardápio", command=self.mostrar_menu).pack(side="right", padx=20)

        container = tk.Frame(self.root, bg=cores["bg"])
        container.pack(fill="both", expand=True, padx=30, pady=20)

        conexao = sqlite3.connect(DB_NAME)
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT data_hora, itens, total, endereco, numero, forma_pagamento FROM pedidos WHERE usuario = ? ORDER BY id DESC",
            (self.usuario_atual,)
        )
        pedidos = cursor.fetchall()
        conexao.close()

        if not pedidos:
            tk.Label(
                container,
                text="Você ainda não fez nenhum pedido.",
                font=("Arial", 16),
                bg=cores["bg"],
                fg=cores["sub"]
            ).pack(pady=80)
            return

        canvas = tk.Canvas(container, bg=cores["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        conteudo = tk.Frame(canvas, bg=cores["bg"])

        conteudo.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=conteudo, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for p in pedidos:
            card = tk.Frame(conteudo, bg=cores["card"], padx=15, pady=12)
            card.pack(fill="x", pady=8, expand=True)

            tk.Label(card, text=f"📅 Data: {p[0]}", font=("Arial", 11, "bold"), bg=cores["card"], fg=cores["accent2"]).pack(anchor="w")
            tk.Label(card, text=f"🛍️ Itens: {p[1]}", font=("Arial", 11), bg=cores["card"], fg=cores["text"]).pack(anchor="w", pady=2)
            tk.Label(card, text=f"💳 Pagamento: {p[5]} | 💰 Total: {formatar_moeda(p[2])}", font=("Arial", 11, "bold"), bg=cores["card"], fg=cores["text"]).pack(anchor="w")
            tk.Label(card, text=f"📍 Entregue em: {p[3]}, Nº {p[4]}", font=("Arial", 9), bg=cores["card"], fg=cores["sub"]).pack(anchor="w", pady=2)

    # ========================================================
    # CARRINHO
    # ========================================================

    def adicionar_carrinho(self, produto):
        nome = produto["nome"]

        if nome not in self.carrinho:
            self.carrinho[nome] = {
                "produto": produto,
                "quantidade": 0
            }

        self.carrinho[nome]["quantidade"] += 1
        messagebox.showinfo("Carrinho", f"{produto['nome']} foi adicionado ao carrinho!")

    def alterar_quantidade(self, nome, valor):
        if nome not in self.carrinho:
            return

        self.carrinho[nome]["quantidade"] += valor

        if self.carrinho[nome]["quantidade"] <= 0:
            del self.carrinho[nome]

        self.mostrar_carrinho()

    def remover_item(self, nome):
        if nome in self.carrinho:
            del self.carrinho[nome]

        self.mostrar_carrinho()

    def calcular_total(self):
        return sum(item["produto"]["preco"] * item["quantidade"] for item in self.carrinho.values())

    def mostrar_carrinho(self):
        self.limpar_tela()
        cores = CORES[TEMA]

        header = tk.Frame(self.root, bg=cores["card"], height=65)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🛒 MEU CARRINHO",
            font=("Arial", 20, "bold"),
            bg=cores["card"],
            fg=cores["text"]
        ).pack(side="left", padx=20)

        ttk.Button(header, text="← Voltar ao cardápio", command=self.mostrar_menu).pack(side="right", padx=20)

        container = tk.Frame(self.root, bg=cores["bg"])
        container.pack(fill="both", expand=True, padx=30, pady=20)

        if not self.carrinho:
            tk.Label(
                container,
                text="Seu carrinho está vazio.",
                font=("Arial", 18),
                bg=cores["bg"],
                fg=cores["sub"]
            ).pack(pady=80)

            ttk.Button(container, text="VER CARDÁPIO", command=self.mostrar_menu).pack()
            return

        for nome, item in self.carrinho.items():
            produto = item["produto"]
            quantidade = item["quantidade"]

            linha = tk.Frame(container, bg=cores["card"], padx=15, pady=12)
            linha.pack(fill="x", pady=5)

            tk.Label(
                linha,
                text=produto["nome"],
                font=("Arial", 13, "bold"),
                bg=cores["card"],
                fg=cores["text"],
                width=22,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                linha,
                text=formatar_moeda(produto["preco"]),
                bg=cores["card"],
                fg=cores["accent2"],
                font=("Arial", 11, "bold")
            ).pack(side="left", padx=15)

            ttk.Button(
                linha,
                text="−",
                command=lambda n=nome: self.alterar_quantidade(n, -1)
            ).pack(side="left", padx=2)

            tk.Label(
                linha,
                text=str(quantidade),
                width=4,
                bg=cores["card"],
                fg=cores["text"],
                font=("Arial", 11, "bold")
            ).pack(side="left")

            ttk.Button(
                linha,
                text="+",
                command=lambda n=nome: self.alterar_quantidade(n, 1)
            ).pack(side="left", padx=2)

            ttk.Button(
                linha,
                text="Remover",
                command=lambda n=nome: self.remover_item(n)
            ).pack(side="right")

        total = self.calcular_total()

        rodape = tk.Frame(container, bg=cores["bg"])
        rodape.pack(fill="x", pady=25)

        tk.Label(
            rodape,
            text=f"TOTAL: {formatar_moeda(total)}",
            font=("Arial", 20, "bold"),
            bg=cores["bg"],
            fg=cores["text"]
        ).pack(side="left")

        ttk.Button(rodape, text="FINALIZAR PEDIDO", command=self.finalizar_pedido).pack(side="right")

    # ========================================================
    # CHECKOUT
    # ========================================================

    def finalizar_pedido(self):
        if not self.carrinho:
            messagebox.showwarning("Carrinho", "Adicione algum produto antes de finalizar.")
            return

        cores = CORES[TEMA]

        janela = tk.Toplevel(self.root)
        janela.title("Finalizar pedido")
        janela.geometry("500x620")
        janela.configure(bg=cores["bg"])
        janela.transient(self.root)
        janela.grab_set()

        tk.Label(
            janela,
            text="📦 FINALIZAR PEDIDO",
            font=("Arial", 20, "bold"),
            bg=cores["bg"],
            fg=cores["accent2"]
        ).pack(pady=20)

        form = tk.Frame(janela, bg=cores["card"], padx=25, pady=20)
        form.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        tk.Label(
            form,
            text="CEP",
            bg=cores["card"],
            fg=cores["text"],
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        cep_entry = tk.Entry(
            form,
            bg=cores["entry"],
            fg=cores["text"],
            insertbackground=cores["text"],
            relief="flat"
        )
        cep_entry.pack(fill="x", pady=(5, 10), ipady=6)

        tk.Label(
            form,
            text="Endereço",
            bg=cores["card"],
            fg=cores["text"],
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        endereco_entry = tk.Entry(
            form,
            bg=cores["entry"],
            fg=cores["text"],
            insertbackground=cores["text"],
            relief="flat"
        )
        endereco_entry.pack(fill="x", pady=(5, 10), ipady=6)

        def buscar_cep():
            cep = re.sub(r"\D", "", cep_entry.get())

            if len(cep) != 8:
                messagebox.showwarning("CEP", "Digite um CEP válido com 8 números.", parent=janela)
                return

            try:
                resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=8)
                dados = resposta.json()

                if dados.get("erro"):
                    messagebox.showerror("CEP", "CEP não encontrado.", parent=janela)
                    return

                endereco = (
                    f"{dados.get('logradouro', '')}, "
                    f"{dados.get('bairro', '')}, "
                    f"{dados.get('localidade', '')} - "
                    f"{dados.get('uf', '')}"
                )

                endereco_entry.delete(0, tk.END)
                endereco_entry.insert(0, endereco)

            except Exception:
                messagebox.showerror("Erro", "Não foi possível consultar o CEP.", parent=janela)

        ttk.Button(form, text="🔎 Buscar endereço pelo CEP", command=buscar_cep).pack(fill="x", pady=(0, 12))

        tk.Label(
            form,
            text="Número / complemento",
            bg=cores["card"],
            fg=cores["text"],
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        numero_entry = tk.Entry(
            form,
            bg=cores["entry"],
            fg=cores["text"],
            insertbackground=cores["text"],
            relief="flat"
        )
        numero_entry.pack(fill="x", pady=(5, 15), ipady=6)

        tk.Label(
            form,
            text="Forma de pagamento",
            bg=cores["card"],
            fg=cores["text"],
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        pagamento = ttk.Combobox(
            form,
            values=["PIX", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"],
            state="readonly"
        )
        pagamento.current(0)
        pagamento.pack(fill="x", pady=(5, 20))

        tk.Label(
            form,
            text=f"Total: {formatar_moeda(self.calcular_total())}",
            bg=cores["card"],
            fg=cores["accent2"],
            font=("Arial", 16, "bold")
        ).pack(pady=5)

        def confirmar():
            cep = cep_entry.get().strip()
            endereco = endereco_entry.get().strip()
            numero = numero_entry.get().strip()
            forma = pagamento.get()

            if not cep or not endereco or not numero:
                messagebox.showwarning("Atenção", "Preencha CEP, endereço e número.", parent=janela)
                return

            resumo = [f"{item['quantidade']}x {item['produto']['nome']}" for item in self.carrinho.values()]
            itens = ", ".join(resumo)
            total = self.calcular_total()

            conexao = sqlite3.connect(DB_NAME)
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO pedidos
                (cliente, usuario, data_hora, itens, total, cep, endereco, numero, forma_pagamento)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.nome_atual,
                self.usuario_atual,
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                itens,
                total,
                cep,
                endereco,
                numero,
                forma
            ))

            conexao.commit()
            conexao.close()

            self.carrinho.clear()
            janela.destroy()

            messagebox.showinfo(
                "Pedido confirmado",
                "✅ Pedido realizado com sucesso!\n\nSeu pedido foi salvo no sistema."
            )

            self.mostrar_menu()

        ttk.Button(form, text="✅ CONFIRMAR PEDIDO", command=confirmar).pack(fill="x", pady=5)

    # ========================================================
    # CHATBOT IA INTELIGENTE
    # ========================================================

    def abrir_chat(self):
        if self.janela_chat is not None:
            try:
                if self.janela_chat.winfo_exists():
                    self.janela_chat.lift()
                    self.chat_entry.focus()
                    return
            except Exception:
                pass

        cores = CORES[TEMA]

        self.janela_chat = tk.Toplevel(self.root)
        self.janela_chat.title("🤖 Suporte IA - Gourmet Service")
        self.janela_chat.geometry("600x700")
        self.janela_chat.configure(bg=cores["bg"])
        self.janela_chat.protocol("WM_DELETE_WINDOW", self.fechar_chat)

        header = tk.Frame(self.janela_chat, bg=cores["accent"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🤖 Assistente IA Gourmet",
            font=("Arial", 18, "bold"),
            bg=cores["accent"],
            fg="white"
        ).pack(side="left", padx=20, pady=18)

        self.chat_texto = tk.Text(
            self.janela_chat,
            bg=cores["card"],
            fg=cores["text"],
            font=("Arial", 11),
            wrap="word",
            state="disabled",
            padx=15,
            pady=15,
            relief="flat"
        )
        self.chat_texto.pack(fill="both", expand=True, padx=12, pady=12)

        entrada_frame = tk.Frame(self.janela_chat, bg=cores["bg"])
        entrada_frame.pack(fill="x", padx=12, pady=(0, 12))

        self.chat_entry = tk.Entry(
            entrada_frame,
            bg=cores["entry"],
            fg=cores["text"],
            insertbackground=cores["text"],
            relief="flat",
            font=("Arial", 11)
        )
        self.chat_entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 8))

        ttk.Button(entrada_frame, text="ENVIAR", command=self.enviar_chat).pack(side="right")

        self.chat_entry.bind("<Return>", lambda event: self.enviar_chat())

        self.adicionar_chat(
            "IA",
            f"Olá, {self.nome_atual}! 👋\n"
            "Sou a IA do Gourmet Service. Como posso te ajudar hoje?\n"
            "Pergunte-me sobre horários, orçamento, itens mais baratos, localização, frete e muito mais!"
        )

        self.chat_entry.focus()

    def fechar_chat(self):
        if self.janela_chat:
            try:
                self.janela_chat.destroy()
            except Exception:
                pass

        self.janela_chat = None
        self.chat_texto = None
        self.chat_entry = None

    def adicionar_chat(self, autor, mensagem):
        if not self.chat_texto:
            return

        self.chat_texto.configure(state="normal")
        self.chat_texto.insert(tk.END, f"{autor}: {mensagem}\n\n")
        self.chat_texto.configure(state="disabled")
        self.chat_texto.see(tk.END)

    def enviar_chat(self):
        if not self.chat_entry:
            return

        mensagem = self.chat_entry.get().strip()
        if not mensagem:
            return

        self.chat_entry.delete(0, tk.END)
        self.adicionar_chat("Você", mensagem)
        self.adicionar_chat("IA", "Estou pensando...")

        self.root.after(400, lambda: self.processar_resposta_chat(mensagem))

    def processar_resposta_chat(self, mensagem):
        if not self.chat_texto:
            return

        self.chat_texto.configure(state="normal")
        conteudo = self.chat_texto.get("1.0", tk.END)
        indice = conteudo.rfind("IA: Estou pensando...")

        if indice >= 0:
            self.chat_texto.delete(f"1.0 + {indice} chars", tk.END)

        self.chat_texto.configure(state="disabled")
        resposta = self.gerar_resposta_ia(mensagem)
        self.adicionar_chat("IA", resposta)

    def gerar_resposta_ia(self, mensagem):
        texto = normalizar_texto(mensagem)

        if not texto:
            return "Digite algo para que eu possa te responder."

        # DATA E HORA / HORÁRIO / FUNCIONAMENTO
        if any(w in texto for w in ["hora", "horas", "horario", "aberto", "fechado", "funciona", "abrir", "fechar"]):
            agora = datetime.now()
            status = "🟢 ABERTO" if restaurante_aberto() else "🔴 FECHADO"
            return (
                f"🕒 Hora atual: {agora.strftime('%H:%M:%S (%d/%m/%Y)')}\n"
                f"📌 Status do restaurante: {status}\n"
                f"⏰ Horário de Funcionamento: Das {INFO_RESTAURANTE['horario_abertura']}h às {INFO_RESTAURANTE['horario_fechamento']}h (12:00 PM - 8:00 PM)."
            )

        # LOCALIZAÇÃO
        if any(w in texto for w in ["onde fica", "localizacao", "endereco", "onde ficam", "rua"]):
            return f"📍 Nosso endereço é:\n{INFO_RESTAURANTE['endereco']}"

        # ENTREGA E FRETE
        if any(w in texto for w in ["entrega", "frete", "demora", "tempo", "taxa"]):
            return (
                f"🚚 Informações de Entrega:\n"
                f"• Tempo estimado: {INFO_RESTAURANTE['tempo_entrega']}\n"
                f"• Taxa de entrega: {INFO_RESTAURANTE['taxa_entrega']}"
            )

        # LANCHE MAIS BARATO
        if "lanche mais barato" in texto or "hambuerguer mais barato" in texto or "hamburguer mais barato" in texto:
            lanches = sorted(PRODUTOS["🍔 HAMBÚRGUERES"], key=lambda x: x["preco"])
            m = lanches[0]
            return f"🍔 O hambúrguer/lanche mais barato é o **{m['nome']}** por {formatar_moeda(m['preco'])}."

        # PIZZA MAIS BARATA
        if "pizza mais barata" in texto:
            pizzas = sorted(PRODUTOS["🍕 PIZZAS"], key=lambda x: x["preco"])
            m = pizzas[0]
            return f"🍕 A pizza mais barata é a **{m['nome']}** por {formatar_moeda(m['preco'])}."

        # BEBIDA MAIS BARATA
        if "bebida mais barata" in texto:
            bebidas = sorted(PRODUTOS["🥤 BEBIDAS"], key=lambda x: x["preco"])
            m = bebidas[0]
            return f"🥤 A bebida mais barata é o **{m['nome']}** por {formatar_moeda(m['preco'])}."

        # ORDEM DE PREÇO / PRODUTOS ORDENADOS
        if any(w in texto for w in ["ordem de preco", "ordenar por preco", "lista de preco", "mais barato ao mais caro"]):
            prods = sorted(todos_produtos(), key=lambda x: x["preco"])
            res = ["📊 Produtos em ordem de preço:"]
            for p in prods:
                res.append(f"• {p['nome']} — {formatar_moeda(p['preco'])}")
            return "\n".join(res)

        # BUSCA POR ORÇAMENTO
        if any(w in texto for w in ["orcamento", "tenho", "posso gastar", "reais", "comprar com"]):
            numeros = re.findall(r"\d+", texto)
            if numeros:
                valor = float(numeros[0])
                cabem = [p for p in todos_produtos() if p["preco"] <= valor]
                if cabem:
                    res = [f"💵 Com R$ {valor:.2f}, você pode comprar:"]
                    for p in cabem:
                        res.append(f"• {p['nome']} — {formatar_moeda(p['preco'])}")
                    return "\n".join(res)
                else:
                    return f"💵 Com R$ {valor:.2f} infelizmente não temos opções (o item mais barato custa {formatar_moeda(min(p['preco'] for p in todos_produtos()))})."

        # PRODUTO MAIS EM CONTA GERAL
        if any(w in texto for w in ["mais em conta", "mais barato"]):
            m = min(todos_produtos(), key=lambda x: x["preco"])
            return f"💰 O produto mais em conta em todo o cardápio é **{m['nome']}** por apenas {formatar_moeda(m['preco'])}."

        # ANÁLISE DO CARRINHO
        if any(w in texto for w in ["carrinho", "compras", "meus itens"]):
            if not self.carrinho:
                return "🛒 Seu carrinho está vazio."
            res = ["🛒 Itens no seu carrinho:"]
            for item in self.carrinho.values():
                p = item["produto"]
                q = item["quantidade"]
                res.append(f"• {q}x {p['nome']} = {formatar_moeda(p['preco']*q)}")
            res.append(f"\n💰 **Total atual:** {formatar_moeda(self.calcular_total())}")
            return "\n".join(res)

        # HISTÓRICO / SAIR / AJUDA
        if "historico" in texto:
            return "📜 Você pode acessar o seu histórico de pedidos clicando no botão 'Histórico' no topo da página do cardápio."

        if "sair" in texto or "deslogar" in texto:
            return "🚪 Para sair da sua conta, basta clicar no botão 'Sair' localizado no cabeçalho superior."

        # SAUDAÇÃO E AJUDA GERAL
        saudacoes = ["oi", "ola", "olá", "bom dia", "boa tarde", "boa noite"]
        if any(texto.startswith(s) for s in saudacoes):
            return f"Olá, {self.nome_atual}! 👋 Como posso te ajudar com seu pedido hoje?"

        return (
            "🤖 Posso responder a diversas dúvidas! Experimente perguntar:\n"
            "• 'Qual o horário de funcionamento?'\n"
            "• 'Está aberto agora?'\n"
            "• 'Onde fica o restaurante?'\n"
            "• 'Qual a bebida / pizza / lanche mais barato?'\n"
            "• 'Mostre a lista de produtos em ordem de preço.'\n"
            "• 'O que posso comprar com 30 reais?'\n"
            "• 'Análise do meu carrinho.'"
        )


# ============================================================
# INICIALIZAÇÃO DA APLICAÇÃO
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = GourmetService(root)
    root.mainloop()