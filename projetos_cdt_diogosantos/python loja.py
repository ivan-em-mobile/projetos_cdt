import json
import os
import random
import sqlite3
from datetime import datetime, timedelta
from tkinter import messagebox, ttk
import customtkinter as ctk

# Tenta carregar a biblioteca Faker opcional
try:
    from faker import Faker

    fake = Faker("pt_BR")
except ImportError:
    fake = None

# =====================================================
# CONFIGURAÇÕES GLOBAIS E CONSTANTES
# =====================================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

NOME_LOJA = "⚽🇧🇷 NAÇÃO DOS MANTOS 🇧🇷⚽"
INSTAGRAM_LOJA = "📸 @nacaodosmantosoficial"
BANCO_DB = "loja_camisas.db"
ARQUIVO_CONFIG = "configuracao.json"
PRECO_PERSONALIZACAO = 20.00
ARQUIVO_USUARIOS = "usuarios.json"

TIMES_CATALOGO_BASE = {
    "Athletico-PR": {
        "preco": 340.90,
        "sigla": "CAP",
        "cor": "#C62828",
        "icone": "🛡️🌪️",
    },
    "Atletico-MG": {
        "preco": 159.90,
        "sigla": "CAM",
        "cor": "#212121",
        "icone": "🛡️🐓",
    },
    "Bahia": {"preco": 300.90, "sigla": "BAH", "cor": "#1565C0", "icone": "🛡️🌴"},
    "Botafogo": {
        "preco": 149.90,
        "sigla": "BOT",
        "cor": "#111111",
        "icone": "🛡️⭐",
    },
    "Chapecoense": {
        "preco": 119.90,
        "sigla": "CHA",
        "cor": "#2E7D32",
        "icone": "🛡️🟢",
    },
    "Corinthians": {
        "preco": 360.90,
        "sigla": "COR",
        "cor": "#424242",
        "icone": "🛡️🦅",
    },
    "Coritiba": {
        "preco": 420.90,
        "sigla": "CFC",
        "cor": "#388E3C",
        "icone": "🛡️🟢",
    },
    "Cruzeiro": {
        "preco": 432.90,
        "sigla": "CRU",
        "cor": "#1565C0",
        "icone": "🛡️🦊",
    },
    "Flamengo": {
        "preco": 350.90,
        "sigla": "FLA",
        "cor": "#B71C1C",
        "icone": "🛡️👺",
    },
    "Fluminense": {
        "preco": 159.90,
        "sigla": "FLU",
        "cor": "#00695C",
        "icone": "🛡️🟢",
    },
    "Gremio": {"preco": 300.90, "sigla": "GRE", "cor": "#0277BD", "icone": "🛡️🏟️"},
    "Internacional": {
        "preco": 500.90,
        "sigla": "INT",
        "cor": "#D32F2F",
        "icone": "🎈",
    },
    "Mirassol": {
        "preco": 119.90,
        "sigla": "MIR",
        "cor": "#F9A825",
        "icone": "🛡️🌻",
    },
    "Palmeiras": {
        "preco": 179.90,
        "sigla": "PAL",
        "cor": "#1B5E20",
        "icone": "🛡️🐷",
    },
    "Red Bull Bragantino": {
        "preco": 139.90,
        "sigla": "RBB",
        "cor": "#D32F2F",
        "icone": "🛡️🐂",
    },
    "Remo": {"preco": 119.90, "sigla": "REM", "cor": "#283593", "icone": "🛡️⚓"},
    "Santos": {
        "preco": 149.90,
        "sigla": "SAN",
        "cor": "#212121",
        "icone": "🛡️🐳",
    },
    "Sao Paulo": {
        "preco": 169.90,
        "sigla": "SPFC",
        "cor": "#C62828",
        "icone": "🛡️🧔🏼",
    },
    "Vasco": {
        "preco": 159.90,
        "sigla": "VAS",
        "cor": "#212121",
        "icone": "🛡️💢",
    },
    "Vitoria": {
        "preco": 129.90,
        "sigla": "VIT",
        "cor": "#C62828",
        "icone": "🛡️🦁",
    },
}


# =====================================================
# CAMADA 1: GERENCIADOR DE BANCO DE DADOS (MODEL)
# =====================================================
class DatabaseManager:

    def __init__(self, db_name=BANCO_DB):
        self.db_name = db_name
        self.conexao = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conexao.cursor()
        self.inicializar_tabelas()

    def inicializar_tabelas(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque_pp INTEGER DEFAULT 20,
            estoque_p INTEGER DEFAULT 20,
            estoque_m INTEGER DEFAULT 20,
            estoque_g INTEGER DEFAULT 20,
            estoque_gg INTEGER DEFAULT 20,
            estoque_xg INTEGER DEFAULT 20
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            telefone TEXT NOT NULL,
            cpf TEXT NOT NULL,
            endereco TEXT NOT NULL,
            regiao TEXT NOT NULL,
            obs TEXT NOT NULL,
            detalhes TEXT NOT NULL,
            subtotal REAL NOT NULL,
            desconto REAL NOT NULL,
            taxa_entrega REAL NOT NULL,
            total REAL NOT NULL,
            data TEXT NOT NULL,
            previsao TEXT NOT NULL,
            rastreio TEXT NOT NULL,
            pagamento TEXT NOT NULL,
            banco TEXT NOT NULL,
            brinde TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            nota INTEGER NOT NULL,
            comentario TEXT NOT NULL,
            data TEXT NOT NULL
        )
        """)

        self.conexao.commit()
        self.popular_catalogo_inicial()

    def popular_catalogo_inicial(self):
        self.cursor.execute("SELECT COUNT(*) FROM produtos")
        if self.cursor.fetchone()[0] == 0:
            for time, dados in TIMES_CATALOGO_BASE.items():
                self.cursor.execute(
                    """
                    INSERT INTO produtos (nome, preco, estoque_pp, estoque_p, estoque_m, estoque_g, estoque_gg, estoque_xg)
                    VALUES (?, ?, 20, 20, 20, 20, 20, 20)
                """,
                    ("Camisa " + time, dados["preco"]),
                )
            self.conexao.commit()

    def listar_produtos(self):
        self.cursor.execute("SELECT id, nome, preco FROM produtos")
        return self.cursor.fetchall()

    def obter_produto_estoque(self, nome_produto, coluna_estoque):
        self.cursor.execute(
            f"SELECT {coluna_estoque}, preco FROM produtos WHERE nome = ?",
            (nome_produto,),
        )
        return self.cursor.fetchone()

    def atualizar_preco_produto(self, prod_id, novo_preco):
        with self.conexao:
            self.cursor.execute(
                "UPDATE produtos SET preco = ? WHERE id = ?",
                (novo_preco, prod_id),
            )

    def dar_baixa_estoque(self, nome_produto, coluna_estoque, qtd):
        self.cursor.execute(
            f"UPDATE produtos SET {coluna_estoque} = {coluna_estoque} - ? WHERE nome = ?",
            (qtd, nome_produto),
        )

    def salvar_pedido(self, dados_pedido):
        with self.conexao:
            self.cursor.execute(
                """
                INSERT INTO pedidos (cliente, telefone, cpf, endereco, regiao, obs, detalhes, subtotal, desconto, taxa_entrega, total, data, previsao, rastreio, pagamento, banco, brinde, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                dados_pedido,
            )

    def listar_pedidos_resumidos(self):
        self.cursor.execute(
            "SELECT id, cliente, telefone, total, pagamento, banco, data, status FROM pedidos ORDER BY id DESC"
        )
        return self.cursor.fetchall()

    def obter_detalhes_pedido(self, pedido_id):
        self.cursor.execute(
            """
            SELECT id, cliente, telefone, cpf, endereco, regiao, obs, detalhes, subtotal, desconto, taxa_entrega, total, data, previsao, rastreio, pagamento, banco, brinde, status 
            FROM pedidos WHERE id = ?
        """,
            (pedido_id,),
        )
        return self.cursor.fetchone()

    def listar_produtos_admin(self):
        self.cursor.execute(
            "SELECT id, nome, preco, estoque_pp, estoque_p, estoque_m, estoque_g, estoque_gg, estoque_xg FROM produtos"
        )
        return self.cursor.fetchall()

    def salvar_avaliacao(self, cliente, nota, comentario):
        with self.conexao:
            self.cursor.execute(
                """
                INSERT INTO avaliacoes (cliente, nota, comentario, data)
                VALUES (?, ?, ?, ?)
            """,
                (
                    cliente,
                    nota,
                    comentario,
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                ),
            )

    def listar_avaliacoes(self):
        self.cursor.execute(
            "SELECT cliente, nota, comentario, data FROM avaliacoes ORDER BY id DESC"
        )
        return self.cursor.fetchall()


# Instância do Gerenciador de Banco de Dados
db = DatabaseManager()


# =====================================================
# CAMADA 2: INTERFACE GRÁFICA PRINCIPAL
# =====================================================
class NacaoDosMantosApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(NOME_LOJA)
        self.geometry("550x450")

        self.carrinho = []
        self.time_selecionado = None
        self.desconto_aplicado = 0.0
        self.cupom_ativo = ""
        self.cards_times_lista = []
        self.botoes_times_dados = []

        self.win_admin = None
        self.win_historico = None

        self.withdraw()
        self.abrir_login()

        self.configurar_grid()
        self.construir_topo_e_tema()
        self.construir_painel_esquerdo()
        self.construir_painel_direito()

    def carregar_usuarios(self):
        if os.path.exists(ARQUIVO_USUARIOS):
            try:
                with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def salvar_usuarios(self, dados):
        with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    # --- TELA DE LOGIN: BRASIL, FUTEBOL E TROFÉUS ---
    def abrir_login(self):
        self.login = ctk.CTkToplevel(self)
        self.login.title("Login - Nacao dos Mantos")
        self.login.geometry("520x700")
        self.login.resizable(True, True)
        self.login.minsize(520, 700)
        self.login.configure(fg_color="#061A0B")
        self.login.grab_set()

        def fechar():
            self.destroy()

        self.login.protocol("WM_DELETE_WINDOW", fechar)

        frame = ctk.CTkFrame(
            self.login,
            corner_radius=30,
            border_width=3,
            border_color="#FFD700",
            fg_color="#101820",
        )
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(
            frame,
            text="BRASIL",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#FFD700",
        ).pack(pady=(25, 2))

        ctk.CTkLabel(
            frame,
            text="TROFEU   -   FUTEBOL   -   CAMISAS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00E676",
        ).pack(pady=6)

        ctk.CTkLabel(
            frame,
            text="NAÇÃO DOS MANTOS",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#FFFFFF",
        ).pack(pady=5)

        ctk.CTkLabel(
            frame,
            text="Futebol brasileiro e os grandes clubes do Brasil",
            font=ctk.CTkFont(size=13),
            text_color="#AAAAAA",
        ).pack(pady=8)

        self.login_user = ctk.CTkEntry(
            frame,
            placeholder_text="Usuario do torcedor",
            width=340,
            height=45,
            corner_radius=15,
        )
        self.login_user.pack(pady=8)

        self.login_pass = ctk.CTkEntry(
            frame,
            placeholder_text="Senha",
            show="*",
            width=340,
            height=45,
            corner_radius=15,
        )
        self.login_pass.pack(pady=8)

        self.login_msg = ctk.CTkLabel(frame, text="", text_color="#FF1744")
        self.login_msg.pack(pady=5)

        botoes = [
            ("ENTRAR NO CAMPO", "#00E676", "#00C853", self.verificar_login),
            ("CRIAR CONTA DE TORCEDOR", "#2979FF", "#1565C0", self.criar_conta),
            ("🎲 GERAR CLIENTE FAKER", "#651FFF", "#4527A0", self.gerar_conta_fake),
        ]

        for texto, cor, hover, cmd in botoes:
            altura = 48 if "FAKER" in texto else 42
            ctk.CTkButton(
                frame,
                text=texto,
                width=340,
                height=altura,
                fg_color=cor,
                hover_color=hover,
                text_color="#000000" if cor == "#00E676" else "#FFFFFF",
                font=ctk.CTkFont(size=13, weight="bold"),
                command=cmd,
            ).pack(pady=7)

        ctk.CTkLabel(
            frame,
            text="O maior acervo de camisas do Brasil\nNacao dos Mantos",
            text_color="#AAAAAA",
            font=ctk.CTkFont(size=11),
        ).pack(side="bottom", pady=18)

        self.login_pass.bind("<Return>", lambda e: self.verificar_login())
        self.login_user.bind("<Return>", lambda e: self.verificar_login())

    def verificar_login(self):
        usuarios = self.carregar_usuarios()
        u = self.login_user.get().strip()
        p = self.login_pass.get().strip()

        if (u == "admin" and p == "1234") or (
            u in usuarios and usuarios[u]["senha"] == p
        ):
            self.login.destroy()
            self.deiconify()
        else:
            self.login_msg.configure(
                text="Usuário ou senha incorretos!", text_color="red"
            )

    def criar_conta(self):
        u = self.login_user.get().strip()
        p = self.login_pass.get().strip()
        if not u or not p:
            messagebox.showwarning("Aviso", "Digite usuário e senha")
            return
        usuarios = self.carregar_usuarios()
        usuarios[u] = {"senha": p, "nome": u}
        self.salvar_usuarios(usuarios)
        messagebox.showinfo("Sucesso", "Conta criada com sucesso!")

    def gerar_conta_fake(self):
        if fake:
            nome = fake.name()
            usuario = (
                nome.lower().replace(" ", "") + str(random.randint(10, 99))
            )
            senha = str(random.randint(100000, 999999))
        else:
            usuario = "cliente" + str(random.randint(10, 99))
            senha = str(random.randint(100000, 999999))
        usuarios = self.carregar_usuarios()
        usuarios[usuario] = {
            "senha": senha,
            "nome": nome if fake else usuario,
        }
        self.salvar_usuarios(usuarios)
        self.login_user.delete(0, "end")
        self.login_user.insert(0, usuario)
        self.login_pass.delete(0, "end")
        self.login_pass.insert(0, senha)
        messagebox.showinfo(
            "Conta Faker criada", f"Usuário: {usuario}\nSenha: {senha}"
        )

    def configurar_grid(self):
        self.grid_columnconfigure(0, weight=6)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)

    def construir_topo_e_tema(self):
        frame_superior = ctk.CTkFrame(self, fg_color="transparent")
        frame_superior.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=(5, 0)
        )

        self.btn_tema = ctk.CTkButton(
            frame_superior,
            text="☀️ Modo Claro",
            width=130,
            height=26,
            fg_color="#FF9800",
            hover_color="#F57C00",
            text_color="#000000",
            font=ctk.CTkFont(weight="bold"),
            command=self.alternar_modo_tema,
        )
        self.btn_tema.pack(side="right", padx=(5, 0))

        self.btn_sair = ctk.CTkButton(
            frame_superior,
            text="🚪 Sair / Voltar ao Login",
            width=180,
            height=26,
            fg_color="#E91E63",
            hover_color="#AD1457",
            text_color="#FFFFFF",
            font=ctk.CTkFont(weight="bold"),
            command=self.sair_para_login,
        )
        self.btn_sair.pack(side="right", padx=(5, 0))

    def sair_para_login(self):
        self.withdraw()
        if hasattr(self, "login") and self.login.winfo_exists():
            self.login.lift()
            self.login.focus_force()
        else:
            self.abrir_login()

    def alternar_modo_tema(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.btn_tema.configure(text="🌙 Modo Escuro")
        else:
            ctk.set_appearance_mode("Dark")
            self.btn_tema.configure(text="☀️ Modo Claro")

    # --- PAINEL ESQUERDO (CATÁLOGO) ---
    def construir_painel_esquerdo(self):
        self.frame_esquerdo = ctk.CTkFrame(
            self, corner_radius=15, border_width=2, border_color="#FF9800"
        )
        self.frame_esquerdo.grid(
            row=0, column=0, padx=12, pady=(35, 12), sticky="nsew"
        )

        frame_topo_loja = ctk.CTkFrame(
            self.frame_esquerdo, fg_color="#1E1E2C", corner_radius=10
        )
        frame_topo_loja.pack(fill="x", padx=15, pady=(12, 5))

        ctk.CTkLabel(
            frame_topo_loja, text="🏆🇧🇷", font=ctk.CTkFont(size=36)
        ).pack(side="left", padx=10, pady=8)

        frame_titulos = ctk.CTkFrame(frame_topo_loja, fg_color="transparent")
        frame_titulos.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(
            frame_titulos,
            text=NOME_LOJA,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFD700",
        ).pack(anchor="w", pady=(2, 0))

        frame_insta = ctk.CTkFrame(frame_titulos, fg_color="transparent")
        frame_insta.pack(anchor="w", pady=1)

        ctk.CTkLabel(frame_insta, text="⭐", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=(0, 4)
        )
        ctk.CTkLabel(
            frame_insta,
            text=INSTAGRAM_LOJA,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#E1306C",
        ).pack(side="left")

        ctk.CTkLabel(
            frame_titulos,
            text="🏆 A Loja dos Campeões e Torcedores!",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#00E676",
        ).pack(anchor="w", pady=(0, 2))

        ctk.CTkLabel(
            frame_titulos,
            text="🚚 ENTREGA EM 3 A 4 DIAS",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color="#00E676",
        ).pack(anchor="w", pady=(0, 1))

        ctk.CTkLabel(
            frame_titulos,
            text="🎟️ A CADA 2 CAMISAS = 1 PARTICIPAÇÃO NO SORTEIO",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color="#FFD700",
        ).pack(anchor="w", pady=(0, 2))

        ctk.CTkLabel(
            self.frame_esquerdo,
            text="SEJA BEM-VINDO À NAÇÃO DOS MANTOS! ESCOLHA O SEU TIME:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FFD700",
            justify="center",
        ).pack(fill="x", padx=15, pady=(4, 8))

        frame_busca = ctk.CTkFrame(self.frame_esquerdo, fg_color="transparent")
        frame_busca.pack(fill="x", padx=15, pady=2)

        self.campo_busca = ctk.CTkEntry(
            frame_busca, placeholder_text="🔍 Pesquisar time...", height=30
        )
        self.campo_busca.pack(fill="x")
        self.campo_busca.bind("<KeyRelease>", lambda e: self.filtrar_times())

        self.scroll_times = ctk.CTkScrollableFrame(
            self.frame_esquerdo,
            label_text="🔥 MANTOS DISPONÍVEIS",
            label_text_color="#FFD700",
            height=160,
        )
        self.scroll_times.pack(fill="both", expand=True, padx=15, pady=5)

        self.construir_catalogo()

        self.label_selecionado = ctk.CTkLabel(
            self.frame_esquerdo,
            text="Time selecionado: Nenhum",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FF3D00",
        )
        self.label_selecionado.pack(anchor="w", padx=15, pady=2)

        frame_opcoes = ctk.CTkFrame(
            self.frame_esquerdo,
            corner_radius=10,
            fg_color="#1E1E2C",
            border_width=1,
            border_color="#FFD700",
        )
        frame_opcoes.pack(fill="x", padx=15, pady=5)

        box1 = ctk.CTkFrame(frame_opcoes, fg_color="transparent")
        box1.pack(fill="x", padx=10, pady=4)

        ctk.CTkLabel(box1, text="Tam:", font=ctk.CTkFont(weight="bold")).pack(
            side="left", padx=(0, 2)
        )
        self.combo_tamanho = ctk.CTkComboBox(
            box1,
            values=["PP", "P", "M", "G", "GG", "XG"],
            width=65,
            button_color="#FF9800",
        )
        self.combo_tamanho.set("M")
        self.combo_tamanho.pack(side="left", padx=2)

        ctk.CTkLabel(box1, text="Qtd:", font=ctk.CTkFont(weight="bold")).pack(
            side="left", padx=(6, 2)
        )
        self.campo_quantidade = ctk.CTkEntry(box1, width=40)
        self.campo_quantidade.insert(0, "1")
        self.campo_quantidade.pack(side="left", padx=2)

        self.var_brinde_item = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            box1,
            text="🎁 Brinde",
            variable=self.var_brinde_item,
            text_color="#FFD700",
            font=ctk.CTkFont(size=11, weight="bold"),
            checkbox_width=18,
            checkbox_height=18,
        ).pack(side="left", padx=(10, 0))

        self.var_personalizar = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            frame_opcoes,
            text="Personalizar (+R$ 20,00)",
            variable=self.var_personalizar,
            command=self.ativar_personalizacao,
            text_color="#FFD700",
            font=ctk.CTkFont(weight="bold"),
        ).pack(anchor="w", padx=10, pady=4)

        box2 = ctk.CTkFrame(frame_opcoes, fg_color="transparent")
        box2.pack(fill="x", padx=10, pady=(0, 6))

        self.campo_nome = ctk.CTkEntry(
            box2, placeholder_text="Nome na camisa", state="disabled", width=140
        )
        self.campo_nome.pack(side="left", padx=(0, 5))

        self.campo_numero = ctk.CTkEntry(
            box2, placeholder_text="N°", state="disabled", width=60
        )
        self.campo_numero.pack(side="left")

        ctk.CTkButton(
            self.frame_esquerdo,
            text="+ ADICIONAR AO CARRINHO",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#FF6D00",
            hover_color="#E65100",
            height=34,
            command=self.adicionar_carrinho,
        ).pack(fill="x", padx=15, pady=(2, 10))

    def construir_catalogo(self):
        for card, _ in self.cards_times_lista:
            card.destroy()
        self.cards_times_lista.clear()
        self.botoes_times_dados.clear()

        for prod in db.listar_produtos():
            prod_id, nome_prod, preco = prod
            nome_time = nome_prod.replace("Camisa ", "")
            info_time = TIMES_CATALOGO_BASE.get(
                nome_time, {"icone": "🛡️", "cor": "#FF9800"}
            )

            card = ctk.CTkFrame(
                self.scroll_times, corner_radius=10, fg_color="#1E1E2C"
            )
            card.pack(fill="x", padx=5, pady=4)

            ctk.CTkLabel(
                card, text=info_time["icone"], font=ctk.CTkFont(size=22)
            ).pack(side="left", padx=(10, 5), pady=4)
            ctk.CTkFrame(
                card, width=4, height=24, fg_color=info_time["cor"]
            ).pack(side="left", padx=(0, 8))

            info_txt = f"{nome_time} — R$ {preco:.2f}".replace(".", ",")
            ctk.CTkLabel(
                card,
                text=info_txt,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#FFFFFF",
            ).pack(side="left", padx=2)

            btn = ctk.CTkButton(
                card,
                text="Selecionar",
                width=95,
                height=28,
                fg_color="#D500F9",
                hover_color="#AA00FF",
                font=ctk.CTkFont(weight="bold"),
            )
            btn.configure(
                command=lambda t=nome_time, b=btn: self.selecionar_time(t, b)
            )
            btn.pack(side="right", padx=8, pady=4)

            self.botoes_times_dados.append((btn, nome_time))
            self.cards_times_lista.append((card, nome_time))

    def filtrar_times(self, *args):
        termo = self.campo_busca.get().lower()
        for card, nome_time in self.cards_times_lista:
            if termo in nome_time.lower():
                card.pack(fill="x", padx=5, pady=4)
            else:
                card.pack_forget()

    def selecionar_time(self, nome_time, btn_ref):
        self.time_selecionado = nome_time
        self.label_selecionado.configure(
            text=f"Time Selecionado: {nome_time}", text_color="#00E676"
        )

        for btn, _ in self.botoes_times_dados:
            btn.configure(
                fg_color="#D500F9", hover_color="#AA00FF", text="Selecionar"
            )
        btn_ref.configure(
            fg_color="#00E676",
            hover_color="#00C853",
            text="Selecionado ✓",
            text_color="#000000",
        )

    def ativar_personalizacao(self):
        if self.var_personalizar.get():
            self.campo_nome.configure(state="normal")
            self.campo_numero.configure(state="normal")
        else:
            self.campo_nome.delete(0, "end")
            self.campo_numero.delete(0, "end")
            self.campo_nome.configure(state="disabled")
            self.campo_numero.configure(state="disabled")

    # --- PAINEL DIREITO (CARRINHO E FORMULÁRIO) ---
    def construir_painel_direito(self):
        self.frame_direito = ctk.CTkFrame(
            self, corner_radius=15, border_width=2, border_color="#D500F9"
        )
        self.frame_direito.grid(
            row=0, column=1, padx=12, pady=(35, 12), sticky="nsew"
        )

        ctk.CTkLabel(
            self.frame_direito,
            text="🛒 CARRINHO DE COMPRAS",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#FFD700",
        ).pack(anchor="w", padx=15, pady=(8, 2))

        tree_frame = ctk.CTkFrame(self.frame_direito)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=2)

        self.lista_carrinho = ttk.Treeview(
            tree_frame,
            columns=(
                "produto",
                "tamanho",
                "personalizado",
                "quantidade",
                "brinde",
                "subtotal",
            ),
            show="headings",
            height=4,
        )

        cols = {
            "produto": "Produto",
            "tamanho": "Tam",
            "personalizado": "Pers.",
            "quantidade": "Qtd",
            "brinde": "Brinde",
            "subtotal": "Subtotal",
        }
        for c, t in cols.items():
            self.lista_carrinho.heading(c, text=t)

        self.lista_carrinho.column("produto", width=110)
        self.lista_carrinho.column("tamanho", width=35)
        self.lista_carrinho.column("personalizado", width=65)
        self.lista_carrinho.column("quantidade", width=35)
        self.lista_carrinho.column("brinde", width=60)
        self.lista_carrinho.column("subtotal", width=65)
        self.lista_carrinho.pack(fill="both", expand=True)

        ctk.CTkButton(
            self.frame_direito,
            text="✖ Remover Item",
            fg_color="#FF1744",
            hover_color="#D50000",
            font=ctk.CTkFont(weight="bold"),
            height=24,
            command=self.remover_item,
        ).pack(anchor="e", padx=15, pady=2)

        frame_cupom = ctk.CTkFrame(self.frame_direito, fg_color="transparent")
        frame_cupom.pack(fill="x", padx=15, pady=2)

        self.campo_cupom = ctk.CTkEntry(
            frame_cupom, placeholder_text="Cupom (ex: MANTO10)", width=150, height=26
        )
        self.campo_cupom.pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            frame_cupom,
            text="Aplicar Cupom",
            fg_color="#651FFF",
            hover_color="#4527A0",
            height=26,
            width=110,
            font=ctk.CTkFont(weight="bold"),
            command=self.aplicar_cupom,
        ).pack(side="left")

        self.label_subtotal = ctk.CTkLabel(
            self.frame_direito, text="Subtotal: R$ 0,00", font=ctk.CTkFont(size=12)
        )
        self.label_subtotal.pack(anchor="e", padx=15)

        self.label_desconto = ctk.CTkLabel(
            self.frame_direito,
            text="Desconto: -R$ 0,00",
            font=ctk.CTkFont(size=12),
            text_color="#00E676",
        )
        self.label_desconto.pack(anchor="e", padx=15)

        self.label_entrega = ctk.CTkLabel(
            self.frame_direito,
            text="Taxa de Entrega: R$ 0,00",
            font=ctk.CTkFont(size=12),
        )
        self.label_entrega.pack(anchor="e", padx=15)

        self.label_total = ctk.CTkLabel(
            self.frame_direito,
            text="TOTAL: R$ 0,00",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00E676",
        )
        self.label_total.pack(anchor="e", padx=15, pady=(0, 4))

        frame_cliente = ctk.CTkFrame(
            self.frame_direito, corner_radius=10, fg_color="#1E1E2C"
        )
        frame_cliente.pack(fill="x", padx=15, pady=2)

        self.campo_cliente = ctk.CTkEntry(
            frame_cliente, placeholder_text="Nome Completo", height=28
        )
        self.campo_cliente.pack(fill="x", padx=8, pady=(4, 2))

        box_contato = ctk.CTkFrame(frame_cliente, fg_color="transparent")
        box_contato.pack(fill="x", padx=8, pady=2)

        self.campo_tel = ctk.CTkEntry(
            box_contato, placeholder_text="WhatsApp / Telefone", height=28
        )
        self.campo_tel.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.campo_cpf = ctk.CTkEntry(
            box_contato,
            placeholder_text="CPF (Nota Fiscal)",
            height=28,
            width=130,
        )
        self.campo_cpf.pack(side="left")

        self.campo_endereco = ctk.CTkEntry(
            frame_cliente,
            placeholder_text="Endereço (Rua, Número, Bairro)",
            height=28,
        )
        self.campo_endereco.pack(fill="x", padx=8, pady=2)

        # =====================================================
        # BOTÃO CLIENTE FAKER
        # =====================================================
        ctk.CTkButton(
            frame_cliente,
            text="CLIENTE FAKER",
            fg_color="#651FFF",
            hover_color="#4527A0",
            font=ctk.CTkFont(weight="bold"),
            height=28,
            command=self.preencher_cliente_faker,
        ).pack(fill="x", padx=8, pady=2)

        box_frete = ctk.CTkFrame(frame_cliente, fg_color="transparent")
        box_frete.pack(fill="x", padx=8, pady=2)

        ctk.CTkLabel(
            box_frete,
            text="Região Frete:",
            font=ctk.CTkFont(size=11, weight="bold"),
        ).pack(side="left", padx=(0, 4))

        self.combo_regiao = ctk.CTkComboBox(
            box_frete,
            values=[
                "Capital (R$ 15,00)",
                "Região Metropolitana (R$ 30,00)",
                "Interior (R$ 35,00)",
            ],
            command=lambda v: self.atualizar_total(),
            height=26,
        )
        self.combo_regiao.set("Capital (R$ 15,00)")
        self.combo_regiao.pack(side="left", fill="x", expand=True)

        box_pag_banco = ctk.CTkFrame(frame_cliente, fg_color="transparent")
        box_pag_banco.pack(fill="x", padx=8, pady=2)

        ctk.CTkLabel(
            box_pag_banco, text="Pgto:", font=ctk.CTkFont(size=11, weight="bold")
        ).pack(side="left", padx=(0, 2))

        self.combo_pagamento = ctk.CTkComboBox(
            box_pag_banco,
            values=["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"],
            button_color="#651FFF",
            height=26,
            width=115,
        )
        self.combo_pagamento.set("Pix")
        self.combo_pagamento.pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            box_pag_banco,
            text="Banco:",
            font=ctk.CTkFont(size=11, weight="bold"),
        ).pack(side="left", padx=(0, 2))

        self.combo_banco_cliente = ctk.CTkComboBox(
            box_pag_banco,
            values=["Nubank", "Banco do Brasil", "Itaú", "Bradesco", "Inter", "Caixa"],
            button_color="#651FFF",
            height=26,
            width=115,
        )
        self.combo_banco_cliente.set("Nubank")
        self.combo_banco_cliente.pack(side="left", fill="x", expand=True)

        self.campo_obs = ctk.CTkEntry(
            frame_cliente, placeholder_text="Observações do Pedido", height=28
        )
        self.campo_obs.pack(fill="x", padx=8, pady=(2, 6))

        # Botões de Ação Final
        frame_acoes = ctk.CTkFrame(self.frame_direito, fg_color="transparent")
        frame_acoes.pack(fill="x", padx=15, pady=8)

        ctk.CTkButton(
            frame_acoes,
            text="✅ FINALIZAR PEDIDO",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#00E676",
            hover_color="#00C853",
            text_color="#000000",
            height=40,
            command=self.finalizar_pedido,
        ).pack(fill="x", pady=2)

        box_extras = ctk.CTkFrame(frame_acoes, fg_color="transparent")
        box_extras.pack(fill="x", pady=4)

        ctk.CTkButton(
            box_extras,
            text="📋 Histórico",
            fg_color="#2979FF",
            hover_color="#1565C0",
            font=ctk.CTkFont(weight="bold"),
            width=110,
            command=self.abrir_historico,
        ).pack(side="left", expand=True, padx=2)

        ctk.CTkButton(
            box_extras,
            text="⭐ Avaliar",
            fg_color="#FFD700",
            hover_color="#FFC107",
            text_color="#000000",
            font=ctk.CTkFont(weight="bold"),
            width=110,
            command=self.abrir_avaliacao,
        ).pack(side="left", expand=True, padx=2)

        ctk.CTkButton(
            box_extras,
            text="⚙️ Admin",
            fg_color="#651FFF",
            hover_color="#4527A0",
            font=ctk.CTkFont(weight="bold"),
            width=110,
            command=self.abrir_admin,
        ).pack(side="left", expand=True, padx=2)

    # =====================================================
    # CLIENTE FAKER
    # =====================================================
    def preencher_cliente_faker(self):
        if fake:
            nome = fake.name()
            telefone = fake.cellphone_number()
            cpf = fake.cpf()
            endereco = fake.street_address()
        else:
            nome = "Cliente Teste"
            telefone = "(11) 99999-9999"
            cpf = "000.000.000-00"
            endereco = "Rua Teste, 100"

        self.campo_cliente.delete(0, "end")
        self.campo_cliente.insert(0, nome)

        self.campo_tel.delete(0, "end")
        self.campo_tel.insert(0, telefone)

        self.campo_cpf.delete(0, "end")
        self.campo_cpf.insert(0, cpf)

        self.campo_endereco.delete(0, "end")
        self.campo_endereco.insert(0, endereco)

    # --- LÓGICA DE NEGÓCIO E AÇÕES ---
    def adicionar_carrinho(self):
        if not self.time_selecionado:
            messagebox.showwarning("Aviso", "Selecione um time do catálogo!")
            return

        try:
            qtd = int(self.campo_quantidade.get().strip())
            if qtd <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Aviso", "Quantidade inválida!")
            return

        nome_prod = f"Camisa {self.time_selecionado}"
        tam = self.combo_tamanho.get()
        coluna_est = f"estoque_{tam.lower()}"

        res = db.obter_produto_estoque(nome_prod, coluna_est)
        if not res or res[0] < qtd:
            messagebox.showerror("Erro", f"Estoque insuficiente para o tamanho {tam}!")
            return

        preco_base = res[1]
        pers_texto = "Não"
        adicional_pers = 0.0

        if self.var_personalizar.get():
            nome_p = self.campo_nome.get().strip()
            num_p = self.campo_numero.get().strip()

            if not nome_p or not num_p:
                messagebox.showwarning(
                    "Aviso",
                    "Preencha o nome e número da personalização!"
                )
                return

            pers_texto = f"{nome_p} #{num_p}"
            adicional_pers = PRECO_PERSONALIZACAO

        brinde = "Sim" if self.var_brinde_item.get() else "Não"
        subtotal_item = (preco_base + adicional_pers) * qtd

        item = {
            "produto": nome_prod,
            "tamanho": tam,
            "personalizado": pers_texto,
            "quantidade": qtd,
            "brinde": brinde,
            "subtotal": subtotal_item,
        }

        self.carrinho.append(item)
        self.atualizar_tabela_carrinho()
        self.atualizar_total()

    def atualizar_tabela_carrinho(self):
        for item in self.lista_carrinho.get_children():
            self.lista_carrinho.delete(item)

        for i in self.carrinho:
            self.lista_carrinho.insert(
                "",
                "end",
                values=(
                    i["produto"],
                    i["tamanho"],
                    i["personalizado"],
                    i["quantidade"],
                    i["brinde"],
                    f"R$ {i['subtotal']:.2f}".replace(".", ","),
                ),
            )

    def remover_item(self):
        sel = self.lista_carrinho.selection()

        if not sel:
            messagebox.showwarning(
                "Aviso",
                "Selecione um item do carrinho para remover!"
            )
            return

        idx = self.lista_carrinho.index(sel[0])
        del self.carrinho[idx]

        self.atualizar_tabela_carrinho()
        self.atualizar_total()

    def aplicar_cupom(self):
        cupom = self.campo_cupom.get().strip().upper()

        if cupom == "MANTO10":
            self.desconto_aplicado = 0.10
            self.cupom_ativo = "MANTO10"
            messagebox.showinfo(
                "Cupom Aplicado",
                "10% de desconto concedido!"
            )

        elif cupom == "MANTO20":
            self.desconto_aplicado = 0.20
            self.cupom_ativo = "MANTO20"
            messagebox.showinfo(
                "Cupom Aplicado",
                "20% de desconto concedido!"
            )

        else:
            self.desconto_aplicado = 0.0
            self.cupom_ativo = ""
            messagebox.showwarning(
                "Erro",
                "Cupom inválido ou expirado!"
            )

        self.atualizar_total()

    def calcular_taxa_entrega(self):
        regiao = self.combo_regiao.get()

        if "Capital" in regiao:
            return 15.00

        elif "Metropolitana" in regiao:
            return 30.00

        else:
            return 35.00

    def atualizar_total(self):
        subtotal = sum(i["subtotal"] for i in self.carrinho)
        val_desconto = subtotal * self.desconto_aplicado
        taxa = self.calcular_taxa_entrega() if self.carrinho else 0.0
        total = subtotal - val_desconto + taxa

        self.label_subtotal.configure(
            text=f"Subtotal: R$ {subtotal:.2f}".replace(".", ",")
        )

        self.label_desconto.configure(
            text=f"Desconto: -R$ {val_desconto:.2f}".replace(".", ",")
        )

        self.label_entrega.configure(
            text=f"Taxa de Entrega: R$ {taxa:.2f}".replace(".", ",")
        )

        self.label_total.configure(
            text=f"TOTAL: R$ {total:.2f}".replace(".", ",")
        )

    def finalizar_pedido(self):
        if not self.carrinho:
            messagebox.showwarning(
                "Aviso",
                "Seu carrinho está vazio!"
            )
            return

        cliente = self.campo_cliente.get().strip()
        tel = self.campo_tel.get().strip()
        cpf = self.campo_cpf.get().strip()
        endereco = self.campo_endereco.get().strip()

        if not cliente or not tel or not endereco:
            messagebox.showwarning(
                "Aviso",
                "Preencha Nome, WhatsApp e Endereço!"
            )
            return

        subtotal = sum(i["subtotal"] for i in self.carrinho)
        val_desconto = subtotal * self.desconto_aplicado
        taxa = self.calcular_taxa_entrega()
        total = subtotal - val_desconto + taxa

        dt_atual = datetime.now()
        data_str = dt_atual.strftime("%Y-%m-%d %H:%M")
        previsao_str = ""
        rastreio = f"NM{random.randint(100000, 999999)}BR"

        detalhes_lista = []

        for i in self.carrinho:
            detalhes_lista.append(
                f"{i['quantidade']}x {i['produto']} "
                f"({i['tamanho']}) "
                f"[Pers: {i['personalizado']}]"
            )

            coluna_est = f"estoque_{i['tamanho'].lower()}"

            db.dar_baixa_estoque(
                i['produto'],
                coluna_est,
                i['quantidade']
            )

        detalhes_str = " | ".join(detalhes_lista)

        brinde_geral = (
            "Sim"
            if any(i["brinde"] == "Sim" for i in self.carrinho)
            else "Não"
        )

        dados_pedido = (
            cliente,
            tel,
            cpf,
            endereco,
            self.combo_regiao.get(),
            self.campo_obs.get().strip(),
            detalhes_str,
            subtotal,
            val_desconto,
            taxa,
            total,
            data_str,
            previsao_str,
            rastreio,
            self.combo_pagamento.get(),
            self.combo_banco_cliente.get(),
            brinde_geral,
            "Processando",
        )

        db.salvar_pedido(dados_pedido)

        messagebox.showinfo(
            "Pedido Realizado! 🏆",
            f"Obrigado, {cliente}!\n\n"
            f"📦 Código de Rastreio: {rastreio}\n"
            f"💰 Total: R$ {total:.2f}\n\n"
        )

        self.carrinho.clear()
        self.atualizar_tabela_carrinho()
        self.atualizar_total()

        self.campo_cliente.delete(0, "end")
        self.campo_tel.delete(0, "end")
        self.campo_cpf.delete(0, "end")
        self.campo_endereco.delete(0, "end")
        self.campo_obs.delete(0, "end")

        self.construir_catalogo()

    # --- JANELAS SECUNDÁRIAS ---
    def abrir_historico(self):
        if self.win_historico and self.win_historico.winfo_exists():
            self.win_historico.focus()
            return

        self.win_historico = ctk.CTkToplevel(self)
        self.win_historico.title("📋 Histórico de Pedidos")
        self.win_historico.geometry("800x450")
        self.win_historico.grab_set()

        tree = ttk.Treeview(
            self.win_historico,
            columns=(
                "id",
                "cliente",
                "tel",
                "total",
                "pgto",
                "banco",
                "data",
                "status",
            ),
            show="headings",
        )

        cols = {
            "id": "ID",
            "cliente": "Cliente",
            "tel": "Telefone",
            "total": "Total",
            "pgto": "Pgto",
            "banco": "Banco",
            "data": "Data",
            "status": "Status",
        }

        for c, t in cols.items():
            tree.heading(c, text=t)
            tree.column(c, width=95)

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for p in db.listar_pedidos_resumidos():
            tree.insert("", "end", values=p)

    def abrir_avaliacao(self):
        win_av = ctk.CTkToplevel(self)
        win_av.title("⭐ Deixar Avaliação")
        win_av.geometry("400x320")
        win_av.grab_set()

        ctk.CTkLabel(
            win_av,
            text="Sua Avaliação é muito importante!",
            font=ctk.CTkFont(weight="bold"),
        ).pack(pady=10)

        c_nome = ctk.CTkEntry(
            win_av,
            placeholder_text="Seu Nome",
            width=250
        )
        c_nome.pack(pady=5)

        c_nota = ctk.CTkComboBox(
            win_av,
            values=[
                "5 - Excelente",
                "4 - Muito Bom",
                "3 - Bom",
                "2 - Regular",
                "1 - Ruim",
            ],
            width=250
        )
        c_nota.pack(pady=5)

        c_coment = ctk.CTkEntry(
            win_av,
            placeholder_text="Comentário",
            width=250,
            height=60
        )
        c_coment.pack(pady=5)

        def salvar():
            nome = c_nome.get().strip()
            nota = int(c_nota.get().split(" ")[0])
            coment = c_coment.get().strip()

            if nome and coment:
                db.salvar_avaliacao(nome, nota, coment)

                messagebox.showinfo(
                    "Obrigado!",
                    "Avaliação salva com sucesso!"
                )

                win_av.destroy()

            else:
                messagebox.showwarning(
                    "Aviso",
                    "Preencha todos os campos."
                )

        ctk.CTkButton(
            win_av,
            text="Enviar Avaliação",
            fg_color="#00E676",
            text_color="#000",
            command=salvar
        ).pack(pady=10)

    def abrir_admin(self):
        if self.win_admin and self.win_admin.winfo_exists():
            self.win_admin.focus()
            return

        self.win_admin = ctk.CTkToplevel(self)
        self.win_admin.title("⚙️ Painel do Administrador")
        self.win_admin.geometry("850x500")
        self.win_admin.grab_set()

        tree_admin = ttk.Treeview(
            self.win_admin,
            columns=(
                "id",
                "nome",
                "preco",
                "pp",
                "p",
                "m",
                "g",
                "gg",
                "xg",
            ),
            show="headings",
        )

        cols = {
            "id": "ID",
            "nome": "Produto",
            "preco": "Preço",
            "pp": "PP",
            "p": "P",
            "m": "M",
            "g": "G",
            "gg": "GG",
            "xg": "XG",
        }

        for c, t in cols.items():
            tree_admin.heading(c, text=t)
            tree_admin.column(c, width=80)

        tree_admin.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        def recarregar_admin():
            for item in tree_admin.get_children():
                tree_admin.delete(item)

            for prod in db.listar_produtos_admin():
                tree_admin.insert(
                    "",
                    "end",
                    values=prod
                )

        recarregar_admin()

        box_edit = ctk.CTkFrame(self.win_admin)
        box_edit.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            box_edit,
            text="Novo Preço (R$):"
        ).pack(
            side="left",
            padx=5
        )

        e_preco = ctk.CTkEntry(
            box_edit,
            width=100
        )
        e_preco.pack(
            side="left",
            padx=5
        )

        def atualizar_p():
            sel = tree_admin.selection()

            if not sel:
                messagebox.showwarning(
                    "Aviso",
                    "Selecione um produto."
                )
                return

            try:
                np = float(
                    e_preco.get().replace(",", ".")
                )

                p_id = tree_admin.item(
                    sel[0]
                )["values"][0]

                db.atualizar_preco_produto(
                    p_id,
                    np
                )

                recarregar_admin()
                self.construir_catalogo()

                messagebox.showinfo(
                    "Sucesso",
                    "Preço atualizado!"
                )

            except ValueError:
                messagebox.showerror(
                    "Erro",
                    "Valor inválido!"
                )

        ctk.CTkButton(
            box_edit,
            text="Atualizar Preço",
            command=atualizar_p
        ).pack(
            side="left",
            padx=5
        )


# =====================================================
# INICIALIZAÇÃO DA APLICAÇÃO
# =====================================================
if __name__ == "__main__":
    app = NacaoDosMantosApp()
    app.mainloop()
