# =============================================================================
# 🍔 SISTEMA DE HAMBURGUERIA COM INTERFACE GRÁFICA (GUI - TKINTER)
# Linguagem: Python 3
# Bibliotecas Nativas: tkinter, sqlite3, json, urllib.request, os
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import json
import urllib.request
import os

# -----------------------------------------------------------------------------
# PALETA DE CORES PERSONALIZADA
# -----------------------------------------------------------------------------
COR_AZUL_PETROLEO = "#002a3a"  # Fundo principal da aplicação
COR_AZUL_PROFUNDO = "#004a6d"  # Fundo dos quadros (frames)
COR_AMARELO       = "#edcd01"  # Títulos e destaques
COR_VERDE         = "#00e04b"  # Botões de confirmação / sucesso
COR_LARANJA       = "#e03f2a"  # Botão de cadastro e acentos
COR_TURQUESA      = "#00e3e6"  # Botões dos itens do cardápio e ações secundárias
COR_ROSA         = "#fd3168"  # Botões de logout / alerta
COR_AZUL_CLARO    = "#d9fbff"  # Textos secundários e rótulos

# -----------------------------------------------------------------------------
# PASSO 1: Configuração do Banco de Dados e Pastas
# -----------------------------------------------------------------------------
NOME_PASTA = "projetos_cdt_seunome"
NOME_BANCO = "hamburgueria_cli.db"

def conectar_banco():
    """Garante a existência da pasta e conecta ao banco de dados SQLite."""
    os.makedirs(NOME_PASTA, exist_ok=True)
    caminho_banco = os.path.join(NOME_PASTA, NOME_BANCO)
    return sqlite3.connect(caminho_banco)

def inicializar_banco():
    """Cria as tabelas no banco de dados se não existirem."""
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            resumo_itens TEXT NOT NULL,
            endereco TEXT NOT NULL,
            forma_pagamento TEXT NOT NULL,
            valor_total REAL NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)
    conexao.commit()
    conexao.close()

# -----------------------------------------------------------------------------
# PASSO 2: Integração com API Externa (ViaCEP)
# -----------------------------------------------------------------------------
def buscar_endereco_por_cep(cep):
    """Consulta o CEP na API do ViaCEP e retorna os dados do endereço."""
    cep_limpo = "".join(filter(str.isdigit, cep))
    if len(cep_limpo) != 8:
        return None

    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    try:
        requisicao = urllib.request.urlopen(url)
        dados = json.loads(requisicao.read().decode('utf-8'))
        if "erro" in dados:
            return None
        return dados
    except Exception:
        return None

# -----------------------------------------------------------------------------
# PASSO 3: Dados do Cardápio
# -----------------------------------------------------------------------------
CARDAPIO = {
    1: {"nome": "Combo Smash Burguer", "preco": 28.00},
    2: {"nome": "Combo Bacon Salad", "preco": 32.00},
    3: {"nome": "Combo Monster Double", "preco": 38.00},
    4: {"nome": "Refrigerante Lata 350ml", "preco": 6.00},
    5: {"nome": "Suco Natural 500ml", "preco": 8.00},
    6: {"nome": "Milkshake Chocomaltado 400ml", "preco": 15.00}
}

# -----------------------------------------------------------------------------
# PASSO 4: Interface Gráfica Principal (Tkinter)
# -----------------------------------------------------------------------------
class AplicaçãoHamburgueria:
    def __init__(self, root):
        self.root = root
        self.root.title("🍔 Hamburgueria CDT - Sistema de Pedidos")
        self.root.geometry("680x580")
        self.root.resizable(False, False)
        
        self.usuario_logado = None
        self.carrinho = []

        # Fundo principal escuro
        self.root.configure(bg=COR_AZUL_PETROLEO)
        
        # Inicializa o banco de dados
        inicializar_banco()

        # Inicia na Tela de Login
        self.mostrar_tela_login()

    def limpar_tela(self):
        """Remove todos os elementos visuais da janela para trocar de tela."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # -------------------------------------------------------------------------
    # TELA 1: LOGIN E CADASTRO
    # -------------------------------------------------------------------------
    def mostrar_tela_login(self):
        self.limpar_tela()

        lbl_titulo = tk.Label(
            self.root, 
            text="🍔 Hamburgueria CDT", 
            font=("Helvetica", 22, "bold"), 
            fg=COR_AMARELO, 
            bg=COR_AZUL_PETROLEO
        )
        lbl_titulo.pack(pady=25)

        frame = tk.Frame(self.root, bg=COR_AZUL_PROFUNDO, padx=25, pady=25)
        frame.pack(pady=10)

        tk.Label(frame, text="E-mail:", font=("Arial", 11, "bold"), fg=COR_AZUL_CLARO, bg=COR_AZUL_PROFUNDO).grid(row=0, column=0, sticky="w", pady=8)
        self.ent_email = tk.Entry(frame, width=28, font=("Arial", 11))
        self.ent_email.grid(row=0, column=1, pady=8, padx=5)

        tk.Label(frame, text="Senha:", font=("Arial", 11, "bold"), fg=COR_AZUL_CLARO, bg=COR_AZUL_PROFUNDO).grid(row=1, column=0, sticky="w", pady=8)
        self.ent_senha = tk.Entry(frame, width=28, font=("Arial", 11), show="*")
        self.ent_senha.grid(row=1, column=1, pady=8, padx=5)

        btn_login = tk.Button(
            frame, 
            text="Entrar", 
            font=("Arial", 11, "bold"), 
            bg=COR_VERDE, 
            fg=COR_AZUL_PETROLEO, 
            width=12, 
            relief="flat",
            command=self.executar_login
        )
        btn_login.grid(row=2, column=1, sticky="e", pady=15)

        btn_cadastrar = tk.Button(
            self.root, 
            text="Criar Nova Conta", 
            font=("Arial", 10, "bold"), 
            bg=COR_LARANJA, 
            fg="white", 
            relief="flat",
            command=self.mostrar_tela_cadastro
        )
        btn_cadastrar.pack(pady=15)

    def mostrar_tela_cadastro(self):
        self.limpar_tela()

        lbl_titulo = tk.Label(
            self.root, 
            text="📝 Cadastro de Usuário", 
            font=("Helvetica", 20, "bold"), 
            fg=COR_AMARELO, 
            bg=COR_AZUL_PETROLEO
        )
        lbl_titulo.pack(pady=20)

        frame = tk.Frame(self.root, bg=COR_AZUL_PROFUNDO, padx=25, pady=25)
        frame.pack(pady=10)

        tk.Label(frame, text="Nome Completo:", font=("Arial", 11, "bold"), fg=COR_AZUL_CLARO, bg=COR_AZUL_PROFUNDO).grid(row=0, column=0, sticky="w", pady=6)
        self.ent_nome_cad = tk.Entry(frame, width=28, font=("Arial", 11))
        self.ent_nome_cad.grid(row=0, column=1, pady=6, padx=5)

        tk.Label(frame, text="E-mail:", font=("Arial", 11, "bold"), fg=COR_AZUL_CLARO, bg=COR_AZUL_PROFUNDO).grid(row=1, column=0, sticky="w", pady=6)
        self.ent_email_cad = tk.Entry(frame, width=28, font=("Arial", 11))
        self.ent_email_cad.grid(row=1, column=1, pady=6, padx=5)

        tk.Label(frame, text="Senha:", font=("Arial", 11, "bold"), fg=COR_AZUL_CLARO, bg=COR_AZUL_PROFUNDO).grid(row=2, column=0, sticky="w", pady=6)
        self.ent_senha_cad = tk.Entry(frame, width=28, font=("Arial", 11), show="*")
        self.ent_senha_cad.grid(row=2, column=1, pady=6, padx=5)

        btn_salvar = tk.Button(
            frame, 
            text="Salvar Cadastro", 
            font=("Arial", 10, "bold"), 
            bg=COR_VERDE, 
            fg=COR_AZUL_PETROLEO, 
            relief="flat",
            command=self.executar_cadastro
        )
        btn_salvar.grid(row=3, column=1, sticky="e", pady=15)

        btn_voltar = tk.Button(
            self.root, 
            text="Voltar ao Login", 
            font=("Arial", 10), 
            bg=COR_AZUL_PROFUNDO, 
            fg=COR_AZUL_CLARO, 
            relief="flat",
            command=self.mostrar_tela_login
        )
        btn_voltar.pack(pady=10)

    def executar_login(self):
        email = self.ent_email.get().strip().lower()
        senha = self.ent_senha.get().strip()

        if not email or not senha:
            messagebox.showwarning("Aviso", "Preencha e-mail e senha!")
            return

        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        usuario = cursor.fetchone()
        conexao.close()

        if usuario:
            self.usuario_logado = {"id": usuario[0], "nome": usuario[1]}
            messagebox.showinfo("Sucesso", f"Bem-vindo(a), {usuario[1]}!")
            self.mostrar_tela_pedidos()
        else:
            messagebox.showerror("Erro", "E-mail ou senha incorretos!")

    def executar_cadastro(self):
        nome = self.ent_nome_cad.get().strip()
        email = self.ent_email_cad.get().strip().lower()
        senha = self.ent_senha_cad.get().strip()

        if not nome or not email or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Cadastro realizado! Faça seu login.")
            self.mostrar_tela_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este e-mail já está cadastrado!")

    # -------------------------------------------------------------------------
    # TELA 2: CARDÁPIO E CARRINHO DE COMPRAS
    # -------------------------------------------------------------------------
    def mostrar_tela_pedidos(self):
        self.limpar_tela()

        # Cabeçalho Superior
        frame_topo = tk.Frame(self.root, bg=COR_AZUL_PETROLEO)
        frame_topo.pack(fill="x", padx=15, pady=10)
        
        lbl_welcome = tk.Label(
            frame_topo, 
            text=f"Cliente: {self.usuario_logado['nome']}", 
            font=("Arial", 12, "bold"), 
            fg=COR_AMARELO, 
            bg=COR_AZUL_PETROLEO
        )
        lbl_welcome.pack(side="left")

        # Botão para ver Histórico de Pedidos (Turquesa)
        btn_historico = tk.Button(
            frame_topo, 
            text="📋 Meus Pedidos", 
            font=("Arial", 9, "bold"), 
            bg=COR_TURQUESA, 
            fg=COR_AZUL_PETROLEO, 
            relief="flat",
            command=self.abrir_janela_historico
        )
        btn_historico.pack(side="left", padx=15)

        # Botão Sair da Conta (Rosa)
        btn_logout = tk.Button(
            frame_topo, 
            text="Sair da Conta", 
            font=("Arial", 9, "bold"), 
            bg=COR_ROSA, 
            fg="white", 
            relief="flat",
            command=self.mostrar_tela_login
        )
        btn_logout.pack(side="right")

        # Container Principal
        frame_conteudo = tk.Frame(self.root, bg=COR_AZUL_PETROLEO)
        frame_conteudo.pack(fill="both", expand=True, padx=15, pady=5)

        # Coluna Esquerda: Cardápio
        frame_cardapio = tk.LabelFrame(
            frame_conteudo, 
            text="🍔 Cardápio", 
            font=("Arial", 11, "bold"), 
            fg=COR_AMARELO, 
            bg=COR_AZUL_PROFUNDO, 
            padx=10, 
            pady=10
        )
        frame_cardapio.pack(side="left", fill="both", expand=True, padx=5)

        for cod, item in CARDAPIO.items():
            btn_item = tk.Button(
                frame_cardapio, 
                text=f"{item['nome']}\nR$ {item['preco']:.2f}", 
                font=("Arial", 9, "bold"), 
                bg=COR_TURQUESA, 
                fg=COR_AZUL_PETROLEO, 
                relief="flat",
                command=lambda i=item: self.adicionar_ao_carrinho(i)
            )
            btn_item.pack(fill="x", pady=4)

        # Coluna Direita: Carrinho
        frame_carrinho = tk.LabelFrame(
            frame_conteudo, 
            text="🛒 Carrinho", 
            font=("Arial", 11, "bold"), 
            fg=COR_AMARELO, 
            bg=COR_AZUL_PROFUNDO, 
            padx=10, 
            pady=10
        )
        frame_carrinho.pack(side="right", fill="both", expand=True, padx=5)

        self.lst_carrinho = tk.Listbox(
            frame_carrinho, 
            font=("Arial", 10), 
            height=10, 
            bg=COR_AZUL_PETROLEO, 
            fg=COR_AZUL_CLARO, 
            selectbackground=COR_TURQUESA,
            selectforeground=COR_AZUL_PETROLEO,
            relief="flat"
        )
        self.lst_carrinho.pack(fill="both", expand=True, pady=5)

        self.lbl_total = tk.Label(
            frame_carrinho, 
            text="Total: R$ 0.00", 
            font=("Arial", 13, "bold"), 
            fg=COR_AMARELO, 
            bg=COR_AZUL_PROFUNDO
        )
        self.lbl_total.pack(pady=5)

        btn_checkout = tk.Button(
            frame_carrinho, 
            text="Finalizar Pedido", 
            font=("Arial", 11, "bold"), 
            bg=COR_VERDE, 
            fg=COR_AZUL_PETROLEO, 
            relief="flat",
            command=self.finalizar_pedido
        )
        btn_checkout.pack(fill="x", pady=5)

        self.atualizar_carrinho()

    def adicionar_ao_carrinho(self, item):
        self.carrinho.append(item)
        self.atualizar_carrinho()

    def atualizar_carrinho(self):
        self.lst_carrinho.delete(0, tk.END)
        total = 0.0
        for item in self.carrinho:
            self.lst_carrinho.insert(tk.END, f"{item['nome']} - R$ {item['preco']:.2f}")
            total += item['preco']
        self.lbl_total.config(text=f"Total: R$ {total:.2f}")

    def finalizar_pedido(self):
        if not self.carrinho:
            messagebox.showwarning("Carrinho Vazio", "Adicione pelo menos um item ao carrinho!")
            return

        total = sum(item['preco'] for item in self.carrinho)

        cep = simpledialog.askstring("CEP de Entrega", "Digite o seu CEP (somente números):")
        if not cep:
            return

        dados_cep = buscar_endereco_por_cep(cep)
        if not dados_cep:
            messagebox.showerror("Erro", "CEP não encontrado!")
            return

        logradouro = dados_cep.get("logradouro", "")
        bairro = dados_cep.get("bairro", "")
        localidade = dados_cep.get("localidade", "")
        uf = dados_cep.get("uf", "")

        numero = simpledialog.askstring("Número", f"Endereço: {logradouro}, {bairro}\nDigite o número da residência:")
        if not numero:
            return

        endereco_final = f"{logradouro}, Nº {numero} - {bairro}, {localidade}/{uf} (CEP: {cep})"
        resumo_itens = ", ".join([item['nome'] for item in self.carrinho])
        
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO pedidos (usuario_id, resumo_itens, endereco, forma_pagamento, valor_total)
            VALUES (?, ?, ?, ?, ?)
        """, (self.usuario_logado["id"], resumo_itens, endereco_final, "PIX / Cartão", total))
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso!", f"Pedido Realizado com Sucesso!\n\nItens: {resumo_itens}\nTotal: R$ {total:.2f}\nEntrega: {endereco_final}")
        self.carrinho.clear()
        self.atualizar_carrinho()

    # -------------------------------------------------------------------------
    # TELA 3: NOVA TELA DE HISTÓRICO DE PEDIDOS (SQLITE)
    # -------------------------------------------------------------------------
    def abrir_janela_historico(self):
        """Abre uma janela modal exibindo todos os pedidos do usuário gravados no SQLite."""
        # Busca no banco de dados SQLite
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT id, resumo_itens, valor_total, endereco 
            FROM pedidos 
            WHERE usuario_id = ?
            ORDER BY id DESC
        """, (self.usuario_logado["id"],))
        pedidos = cursor.fetchall()
        conexao.close()

        if not pedidos:
            messagebox.showinfo("Histórico Vazio", "Você ainda não possui nenhum pedido registrado!")
            return

        # Cria a janela do Histórico (Janela Sobreposta)
        janela_hist = tk.Toplevel(self.root)
        janela_hist.title("📋 Histórico de Pedidos")
        janela_hist.geometry("650x380")
        janela_hist.configure(bg=COR_AZUL_PETROLEO)

        lbl_titulo = tk.Label(
            janela_hist, 
            text=f"Histórico de Pedidos de {self.usuario_logado['nome']}", 
            font=("Arial", 14, "bold"), 
            fg=COR_AMARELO, 
            bg=COR_AZUL_PETROLEO
        )
        lbl_titulo.pack(pady=10)

        # Configuração da Tabela (Treeview)
        colunas = ("id", "itens", "total", "endereco")
        tabela = ttk.Treeview(janela_hist, columns=colunas, show="headings", height=10)

        tabela.heading("id", text="Nº Pedido")
        tabela.heading("itens", text="Itens do Pedido")
        tabela.heading("total", text="Valor Total")
        tabela.heading("endereco", text="Endereço de Entrega")

        tabela.column("id", width=80, anchor="center")
        tabela.column("itens", width=220)
        tabela.column("total", width=90, anchor="center")
        tabela.column("endereco", width=220)

        # Inserção das linhas na tabela
        for ped in pedidos:
            tabela.insert("", tk.END, values=(ped[0], ped[1], f"R$ {ped[2]:.2f}", ped[3]))

        tabela.pack(fill="both", expand=True, padx=15, pady=10)

        btn_fechar = tk.Button(
            janela_hist, 
            text="Fechar", 
            font=("Arial", 10, "bold"), 
            bg=COR_ROSA, 
            fg="white", 
            relief="flat",
            command=janela_hist.destroy
        )
        btn_fechar.pack(pady=10)

# -----------------------------------------------------------------------------
# PASSO 5: Execução do Programa
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicaçãoHamburgueria(root)
    root.mainloop()