'''
CONSULTAR LINHA 234, ACESSO AO ADMIN
FICANDO COM AS COPIAS DE SEGURANÇA, PARA NÃO PERDER NADA

'''
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from datetime import datetime
import sqlite3
import json
import os
import urllib.request
import io


# ============================================================
# CONFIGURAÇÕES E DIRETÓRIOS DO SISTEMA
# ============================================================

# Define o caminho absoluto da pasta do script para evitar erros de diretório
PASTA_DO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
NOME_BANCO_DADOS = os.path.join(PASTA_DO_SCRIPT, "chapa_quente.db")
PASTA_IMAGENS = os.path.join(PASTA_DO_SCRIPT, "imagens")

os.makedirs(PASTA_IMAGENS, exist_ok=True)

LARGURA = 900
ALTURA = 600

# Paleta de cores da interface gráfica
COR_FUNDO = "#101010"
COR_CARD = "#1b1b1b"
COR_CARD_2 = "#252525"
COR_VERMELHO = "#e63946"
COR_VERMELHO_ESCURO = "#b92330"
COR_BRANCO = "#ffffff"
COR_CINZA = "#aaaaaa"
COR_VERDE = "#2ecc71"

# Variáveis de estado global do programa
carrinho = []
imagens_checkout = {}
usuario_logado = None


# ============================================================
# CONEXÃO E ESTRUTURA DO BANCO DE DADOS SQLITE
# ============================================================

def obter_conexao():
    """Conecta ao banco de dados SQLite e ativa o suporte a Chaves Estrangeiras (Foreign Keys)."""
    conexao = sqlite3.connect(NOME_BANCO_DADOS)
    conexao.execute("PRAGMA foreign_keys = ON;")
    return conexao


def inicializar_banco():
    """Cria todas as tabelas necessárias no SQLite se ainda não existirem."""
    conexao = obter_conexao()
    cursor = conexao.cursor()

    # 1. Tabela de Utilizadores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('cliente','funcionario','administrador')),
            ativo INTEGER NOT NULL DEFAULT 1,
            data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 2. Tabela de Categorias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            ativo INTEGER NOT NULL DEFAULT 1
        );
    """)

    # 3. Tabela de Produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT DEFAULT '',
            preco REAL NOT NULL CHECK(preco >= 0),
            imagem TEXT DEFAULT '',
            estoque INTEGER NOT NULL DEFAULT 0 CHECK(estoque >= 0),
            estoque_minimo INTEGER NOT NULL DEFAULT 5 CHECK(estoque_minimo >= 0),
            ativo INTEGER NOT NULL DEFAULT 1,
            data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
        );
    """)

    # 4. Tabela de Pedidos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL UNIQUE,
            usuario_id INTEGER,
            cliente TEXT NOT NULL,
            endereco TEXT NOT NULL,
            tipo_residencia TEXT NOT NULL,
            numero_casa TEXT NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Recebido',
            pagamento TEXT NOT NULL,
            subtotal REAL NOT NULL DEFAULT 0,
            desconto REAL NOT NULL DEFAULT 0,
            total REAL NOT NULL DEFAULT 0,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
        );
    """)

    # 5. Tabela de Itens do Pedido
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            produto_id INTEGER,
            produto_nome TEXT NOT NULL,
            preco_unitario REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY(pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
            FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE SET NULL
        );
    """)

    # 6. Tabela de Movimentações de Estoque
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            usuario_id INTEGER,
            tipo TEXT NOT NULL CHECK(tipo IN ('entrada','saida','ajuste','perda')),
            quantidade INTEGER NOT NULL CHECK(quantidade > 0),
            estoque_anterior INTEGER NOT NULL,
            estoque_novo INTEGER NOT NULL,
            observacao TEXT DEFAULT '',
            data_movimentacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE CASCADE,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
        );
    """)

    conexao.commit()
    conexao.close()

    popular_cardapio_inicial()


def popular_cardapio_inicial():
    """Popula os produtos padrões na primeira execução do sistema."""
    cardapio_padrao = {
        "X-Burger": {"preco": 15.00, "descricao": "Pao, carne, queijo e molho especial", "imagem": "xburger.jpg", "emoji": "🍔", "cat": "Hamburgueres"},
        "X-Salada": {"preco": 18.00, "descricao": "Carne, queijo, alface e tomate", "imagem": "xsalada.jpg", "emoji": "🥬", "cat": "Hamburgueres"},
        "X-Bacon": {"preco": 22.00, "descricao": "Carne, queijo, bacon e molho", "imagem": "xbacon.jpg", "emoji": "🥓", "cat": "Hamburgueres"},
        "X-Tudo": {"preco": 28.00, "descricao": "Carne, queijo, bacon, salada e ovo", "imagem": "xtudo.jpg", "emoji": "🍔", "cat": "Hamburgueres"},
        "X-Frango": {"preco": 20.00, "descricao": "Frango grelhado, queijo e molho especial", "imagem": "xfrango.jpg", "emoji": "🍔", "cat": "Hamburgueres"},
        "X-Cheddar": {"preco": 23.00, "descricao": "Carne, cheddar cremoso e molho especial", "imagem": "xcheddar.jpg", "emoji": "🍔", "cat": "Hamburgueres"},
        "X-Duplo": {"preco": 30.00, "descricao": "Duas carnes, queijo, bacon e molho", "imagem": "xduplo.jpg", "emoji": "🍔", "cat": "Hamburgueres"},
        "X-Barbecue": {"preco": 26.00, "descricao": "Carne, queijo, bacon e molho barbecue", "imagem": "xbarbecue.jpg", "emoji": "🍔", "cat": "Hamburgueres"},
        "Batata Frita": {"preco": 12.00, "descricao": "Batata frita crocante", "imagem": "batata.jpg", "emoji": "🍟", "cat": "Acompanhamentos"},
        "Coca-Cola": {"preco": 7.00, "descricao": "Lata 350ml", "imagem": "coca.jpg", "emoji": "🥤", "cat": "Refrigerantes"},
        "Guarana": {"preco": 7.00, "descricao": "Lata 350ml", "imagem": "guarana.jpg", "emoji": "🥤", "cat": "Refrigerantes"},
        "Fanta Laranja": {"preco": 7.00, "descricao": "Lata 350ml", "imagem": "fanta.jpg", "emoji": "🥤", "cat": "Refrigerantes"},
        "Sprite": {"preco": 7.00, "descricao": "Lata 350ml", "imagem": "sprite.jpg", "emoji": "🥤", "cat": "Refrigerantes"},
        "Pepsi": {"preco": 7.00, "descricao": "Lata 350ml", "imagem": "pepsi.jpg", "emoji": "🥤", "cat": "Refrigerantes"},
        "Suco": {"preco": 8.00, "descricao": "Suco natural", "imagem": "suco.jpg", "emoji": "🧃", "cat": "Sucos"},
        "Suco de Laranja": {"preco": 9.00, "descricao": "Suco natural de laranja", "imagem": "suco_laranja.jpg", "emoji": "🧃", "cat": "Sucos"},
        "Suco de Maracuja": {"preco": 9.00, "descricao": "Suco natural de maracuja", "imagem": "suco_maracuja.jpg", "emoji": "🧃", "cat": "Sucos"},
        "Suco de Morango": {"preco": 10.00, "descricao": "Suco natural de morango", "imagem": "suco_morango.jpg", "emoji": "🧃", "cat": "Sucos"},
        "Suco de Limao": {"preco": 8.00, "descricao": "Suco natural de limao", "imagem": "suco_limao.jpg", "emoji": "🧃", "cat": "Sucos"},
        "Agua": {"preco": 4.00, "descricao": "Agua mineral 500ml", "imagem": "agua.jpg", "emoji": "💧", "cat": "Bebidas"}
    }

    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM produtos;")
    if cursor.fetchone()[0] == 0:
        categorias = ["Hamburgueres", "Acompanhamentos", "Refrigerantes", "Sucos", "Bebidas"]
        mapa_cat = {}
        for cat in categorias:
            cursor.execute("INSERT OR IGNORE INTO categorias (nome) VALUES (?);", (cat,))
            cursor.execute("SELECT id FROM categorias WHERE nome = ?;", (cat,))
            mapa_cat[cat] = cursor.fetchone()[0]

        for nome, item in cardapio_padrao.items():
            cat_id = mapa_cat.get(item["cat"])
            cursor.execute("""
                INSERT OR IGNORE INTO produtos (categoria_id, nome, descricao, preco, imagem, estoque)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (cat_id, nome, item["descricao"], item["preco"], item["imagem"], 50))

        conexao.commit()

    conexao.close()


def obter_cardapio_do_banco():
    """Retorna os produtos ativos diretamente do banco SQLite."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, preco, descricao, imagem FROM produtos WHERE ativo = 1;")
    linhas = cursor.fetchall()
    conexao.close()

    cardapio = {}
    for p_id, nome, preco, descricao, imagem in linhas:
        cardapio[nome] = {
            "id": p_id,
            "preco": preco,
            "descricao": descricao,
            "imagem": imagem
        }
    return cardapio


# ============================================================
# FUNÇÃO UTILITÁRIA
# ============================================================

def formatar_real(valor):
    return f"R$ {valor:.2f}".replace(".", ",")


# ============================================================
# OPERAÇÕES DE USUÁRIOS NO SQLITE
# ============================================================

def cadastrar_usuario(nome, email, senha):
    email = email.lower().strip()
    if len(nome.strip()) < 2:
        return False, "Digite um nome válido."
    if len(email) < 5 or "@" not in email:
        return False, "Digite um e-mail válido."
    if len(senha) < 4:
        return False, "A senha deve possuir pelo menos 4 caracteres."

    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, tipo)
            VALUES (?, ?, ?, 'cliente');
        """, (nome.strip(), email, senha))
        conexao.commit()
        conexao.close()
        return True, "Usuário cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Este e-mail já está cadastrado."
    except Exception as e:
        return False, f"Erro ao cadastrar: {str(e)}"


def cadastrar_admin(nome, email, senha, codigo):
    email = email.lower().strip()
    if codigo != "CHAPA-ADMIN":
        return False, "Código de administrador incorreto."
    if len(nome.strip()) < 2:
        return False, "Digite um nome válido."
    if len(email) < 5 or "@" not in email:
        return False, "Digite um e-mail válido."
    if len(senha) < 4:
        return False, "A senha deve possuir pelo menos 4 caracteres."

    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, tipo)
            VALUES (?, ?, ?, 'administrador');
        """, (nome.strip(), email, senha))
        conexao.commit()
        conexao.close()
        return True, "Administrador criado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Este e-mail já está cadastrado."
    except Exception as e:
        return False, f"Erro ao cadastrar admin: {str(e)}"


def realizar_login_db(email, senha):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome, email, senha, tipo FROM usuarios 
        WHERE email = ? AND ativo = 1;
    """, (email.lower().strip(),))
    usuario = cursor.fetchone()
    conexao.close()

    if not usuario:
        return False, "E-mail não encontrado.", None
    if usuario[3] != senha:
        return False, "Senha incorreta.", None

    user_dict = {
        "id": usuario[0],
        "nome": usuario[1],
        "email": usuario[2],
        "tipo": usuario[4]
    }
    return True, "Sucesso", user_dict


# ============================================================
# MÓDULOS DE EXPORTAÇÃO PARA JSON
# ============================================================

def exportar_pedidos_json():
    """Lê todas as vendas registradas no SQLite e gera o arquivo 'pedidos.json'."""
    if not usuario_logado or usuario_logado.get("tipo") != "administrador":
        messagebox.showerror("Acesso negado", "Somente o administrador pode exportar dados.")
        return

    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT p.id, p.numero, p.cliente, p.endereco, p.tipo_residencia, p.numero_casa,
                   p.data, p.hora, p.status, p.pagamento, p.subtotal, p.desconto, p.total,
                   u.email
            FROM pedidos p
            LEFT JOIN usuarios u ON p.usuario_id = u.id
            ORDER BY p.id ASC;
        """)
        pedidos_db = cursor.fetchall()

        lista_pedidos_json = []

        for ped in pedidos_db:
            ped_id = ped[0]
            
            # Busca os itens associados ao pedido
            cursor.execute("""
                SELECT produto_nome, preco_unitario, quantidade
                FROM itens_pedido
                WHERE pedido_id = ?;
            """, (ped_id,))
            itens_db = cursor.fetchall()

            lista_itens = []
            for item in itens_db:
                lista_itens.append({
                    "produto": item[0],
                    "preco": item[1],
                    "quantidade": item[2]
                })

            lista_pedidos_json.append({
                "numero": ped[1],
                "cliente": ped[2],
                "endereco": ped[3],
                "tipo_residencia": ped[4],
                "numero_casa": ped[5],
                "data": ped[6],
                "hora": ped[7],
                "status": ped[8],
                "pagamento": ped[9],
                "usuario_email": ped[13] if ped[13] else "",
                "itens": lista_itens,
                "subtotal": ped[10],
                "desconto": ped[11],
                "total": ped[12]
            })

        conexao.close()

        caminho_arquivo = os.path.join(PASTA_DO_SCRIPT, "pedidos.json")
        with open(caminho_arquivo, "w", encoding="utf-8") as arq:
            json.dump(lista_pedidos_json, arq, ensure_ascii=False, indent=4)

        messagebox.showinfo("Exportação Concluída", f"Pedidos exportados com sucesso para:\n{caminho_arquivo}")

    except Exception as erro:
        messagebox.showerror("Erro ao Exportar", f"Ocorreu um erro ao exportar os pedidos:\n{str(erro)}")


def exportar_usuarios_json():
    """Lê todos os utilizadores cadastrados no SQLite e gera o arquivo 'usuarios.json'."""
    if not usuario_logado or usuario_logado.get("tipo") != "administrador":
        messagebox.showerror("Acesso negado", "Somente o administrador pode exportar dados.")
        return

    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        cursor.execute("SELECT nome, email, senha, tipo FROM usuarios WHERE ativo = 1;")
        usuarios_db = cursor.fetchall()
        conexao.close()

        dict_usuarios_json = {}

        for nome, email, senha, tipo in usuarios_db:
            dict_usuarios_json[email.lower()] = {
                "nome": nome,
                "senha": senha,
                "tipo": tipo
            }

        caminho_arquivo = os.path.join(PASTA_DO_SCRIPT, "usuarios.json")
        with open(caminho_arquivo, "w", encoding="utf-8") as arq:
            json.dump(dict_usuarios_json, arq, ensure_ascii=False, indent=4)

        messagebox.showinfo("Exportação Concluída", f"Utilizadores exportados com sucesso para:\n{caminho_arquivo}")

    except Exception as erro:
        messagebox.showerror("Erro ao Exportar", f"Ocorreu um erro ao exportar os utilizadores:\n{str(erro)}")


def exportar_dados_json():
    """Exporta o estoque atual de produtos para um arquivo JSON escolhido pelo usuário."""
    if not usuario_logado or usuario_logado.get("tipo") != "administrador":
        messagebox.showerror("Acesso negado", "Somente o administrador pode exportar os dados.")
        return

    try:
        nome_arquivo = filedialog.asksaveasfilename(
            title="Exportar estoque para JSON",
            defaultextension=".json",
            filetypes=[("Arquivo JSON", "*.json"), ("Todos os arquivos", "*.*")],
            initialfile="estoque_produtos.json",
            initialdir=PASTA_DO_SCRIPT
        )
        if not nome_arquivo:
            return

        cardapio = obter_cardapio_do_banco()
        dados = []
        for produto, info in cardapio.items():
            dados.append({
                "produto": produto,
                "preco": info["preco"],
                "descricao": info["descricao"],
                "imagem": info["imagem"]
            })

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        messagebox.showinfo("Exportação concluída", f"Os produtos foram exportados com sucesso!\n\nArquivo:\n{nome_arquivo}")
    except Exception as erro:
        messagebox.showerror("Erro ao exportar", f"Ocorreu um erro ao exportar o JSON:\n\n{erro}")


# ============================================================
# INTERFACE DE CADASTRO
# ============================================================

def abrir_cadastro():
    cadastro = tk.Toplevel(janela_login)
    cadastro.title("Criar conta")
    cadastro.geometry("420x560")
    cadastro.resizable(False, False)
    cadastro.configure(bg=COR_CARD)
    cadastro.transient(janela_login)
    cadastro.grab_set()

    tk.Label(cadastro, text="🍔 CRIAR CONTA", font=("Arial", 20, "bold"), bg=COR_CARD, fg=COR_BRANCO).pack(pady=(25, 5))
    tk.Label(cadastro, text="Escolha o tipo de conta que deseja criar", font=("Arial", 9), bg=COR_CARD, fg=COR_CINZA).pack(pady=(0, 18))

    tk.Label(cadastro, text="Tipo de conta", font=("Arial", 9, "bold"), bg=COR_CARD, fg=COR_CINZA).pack(anchor="w", padx=45)
    tipo_var = tk.StringVar(value="cliente")
    combo_tipo = ttk.Combobox(cadastro, textvariable=tipo_var, values=["cliente", "administrador"], state="readonly")
    combo_tipo.pack(fill="x", padx=45, pady=(5, 14), ipady=5)

    tk.Label(cadastro, text="Nome completo", font=("Arial", 9, "bold"), bg=COR_CARD, fg=COR_CINZA).pack(anchor="w", padx=45)
    entrada_nome = tk.Entry(cadastro, font=("Arial", 11), bg=COR_CARD_2, fg=COR_BRANCO, insertbackground=COR_BRANCO, relief="flat")
    entrada_nome.pack(fill="x", padx=45, pady=(5, 12), ipady=7)

    tk.Label(cadastro, text="E-mail", font=("Arial", 9, "bold"), bg=COR_CARD, fg=COR_CINZA).pack(anchor="w", padx=45)
    entrada_email = tk.Entry(cadastro, font=("Arial", 11), bg=COR_CARD_2, fg=COR_BRANCO, insertbackground=COR_BRANCO, relief="flat")
    entrada_email.pack(fill="x", padx=45, pady=(5, 12), ipady=7)

    tk.Label(cadastro, text="Senha", font=("Arial", 9, "bold"), bg=COR_CARD, fg=COR_CINZA).pack(anchor="w", padx=45)
    entrada_senha = tk.Entry(cadastro, font=("Arial", 11), show="*", bg=COR_CARD_2, fg=COR_BRANCO, insertbackground=COR_BRANCO, relief="flat")
    entrada_senha.pack(fill="x", padx=45, pady=(5, 12), ipady=7)

    label_codigo = tk.Label(cadastro, text="Código de administrador", font=("Arial", 9, "bold"), bg=COR_CARD, fg=COR_CINZA)
    entrada_codigo = tk.Entry(cadastro, font=("Arial", 11), show="*", bg=COR_CARD_2, fg=COR_BRANCO, insertbackground=COR_BRANCO, relief="flat")
    aviso_admin = tk.Label(cadastro, text="Use o código definido no programa para criar uma conta administrativa.", font=("Arial", 8), bg=COR_CARD, fg=COR_CINZA, wraplength=330, justify="center")

    def atualizar_tipo(event=None):
        if tipo_var.get() == "administrador":
            label_codigo.pack(anchor="w", padx=45)
            entrada_codigo.pack(fill="x", padx=45, pady=(5, 5), ipady=7)
            aviso_admin.pack(pady=(0, 8))
        else:
            label_codigo.pack_forget()
            entrada_codigo.pack_forget()
            aviso_admin.pack_forget()

    combo_tipo.bind("<<ComboboxSelected>>", atualizar_tipo)

    def realizar_cadastro():
        nome = entrada_nome.get().strip()
        email = entrada_email.get().strip()
        senha = entrada_senha.get()

        if tipo_var.get() == "administrador":
            codigo = entrada_codigo.get().strip()
            sucesso, mensagem = cadastrar_admin(nome, email, senha, codigo)
        else:
            sucesso, mensagem = cadastrar_usuario(nome, email, senha)

        if sucesso:
            messagebox.showinfo("Cadastro", mensagem, parent=cadastro)
            cadastro.destroy()
            entrada_login_email.delete(0, tk.END)
            entrada_login_email.insert(0, email)
            entrada_login_senha.focus()
        else:
            messagebox.showerror("Erro", mensagem, parent=cadastro)

    tk.Button(cadastro, text="CRIAR CONTA", command=realizar_cadastro, bg=COR_VERMELHO, fg=COR_BRANCO, activebackground=COR_VERMELHO_ESCURO, activeforeground=COR_BRANCO, relief="flat", cursor="hand2", font=("Arial", 10, "bold")).pack(fill="x", padx=45, pady=(5, 0), ipady=9)
    entrada_nome.focus()


# ============================================================
# LOGIN DO SISTEMA
# ============================================================

def realizar_login():
    global usuario_logado
    email = entrada_login_email.get().strip().lower()
    senha = entrada_login_senha.get()

    sucesso, mensagem, user_dict = realizar_login_db(email, senha)
    if not sucesso:
        messagebox.showerror("Login", mensagem, parent=janela_login)
        entrada_login_senha.delete(0, tk.END)
        return

    usuario_logado = user_dict
    janela_login.destroy()
    iniciar_sistema()


# ============================================================
# CADASTRAR FUNCIONÁRIO (ADMIN)
# ============================================================

def cadastrar_funcionario():
    if not usuario_logado or usuario_logado["tipo"] != "administrador":
        messagebox.showerror("Acesso negado", "Somente o administrador pode cadastrar funcionários.")
        return

    cadastro = tk.Toplevel(janela)
    cadastro.title("Cadastrar funcionário")
    cadastro.geometry("420x500")
    cadastro.resizable(False, False)
    cadastro.configure(bg=COR_CARD)
    cadastro.transient(janela)
    cadastro.grab_set()

    tk.Label(cadastro, text="👨‍🍳 NOVO FUNCIONÁRIO", font=("Arial", 18, "bold"), bg=COR_CARD, fg=COR_BRANCO).pack(pady=(25, 5))
    tk.Label(cadastro, text="Crie uma conta para funcionário ou administrador", font=("Arial", 9), bg=COR_CARD, fg=COR_CINZA).pack(pady=(0, 20))

    tk.Label(cadastro, text="Nome", bg=COR_CARD, fg=COR_CINZA, font=("Arial", 9, "bold")).pack(anchor="w", padx=45)
    nome = tk.Entry(cadastro, bg=COR_CARD_2, fg=COR_BRANCO, insertbackground=COR_BRANCO, relief="flat", font=("Arial", 11))
    nome.pack(fill="x", padx=45, pady=(5, 12), ipady=7)

    tk.Label(cadastro, text="E-mail", bg=COR_CARD, fg=COR_CINZA, font=("Arial", 9, "bold")).pack(anchor="w", padx=45)
    email = tk.Entry(cadastro, bg=COR_CARD_2, fg=COR_BRANCO, insertbackground=COR_BRANCO, relief="flat", font=("Arial", 11))
    email.pack(fill="x", padx=45, pady=(5, 12), ipady=7)

    tk.Label(cadastro, text="Senha", bg=COR_CARD, fg=COR_CINZA, font=("Arial", 9, "bold")).pack(anchor="w", padx=45)
    senha = tk.Entry(cadastro, show="*", bg=COR_CARD_2, fg=COR_BRANCO, insertbackground=COR_BRANCO, relief="flat", font=("Arial", 11))
    senha.pack(fill="x", padx=45, pady=(5, 12), ipady=7)

    tk.Label(cadastro, text="Tipo de conta", bg=COR_CARD, fg=COR_CINZA, font=("Arial", 9, "bold")).pack(anchor="w", padx=45)
    tipo_var = tk.StringVar(value="funcionario")
    combo = ttk.Combobox(cadastro, textvariable=tipo_var, values=["funcionario", "administrador"], state="readonly")
    combo.pack(fill="x", padx=45, pady=(5, 20), ipady=5)

    def salvar():
        nome_val = nome.get().strip()
        email_val = email.get().strip().lower()
        senha_val = senha.get()
        tipo_val = tipo_var.get()

        if not nome_val or not email_val or not senha_val:
            messagebox.showwarning("Atenção", "Preencha todos os campos.", parent=cadastro)
            return

        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?);",
                           (nome_val, email_val, senha_val, tipo_val))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!", parent=cadastro)
            cadastro.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este e-mail já está cadastrado.", parent=cadastro)

    tk.Button(cadastro, text="CADASTRAR CONTA", command=salvar, bg=COR_VERMELHO, fg=COR_BRANCO, activebackground=COR_VERMELHO_ESCURO, relief="flat", cursor="hand2", font=("Arial", 10, "bold")).pack(fill="x", padx=45, ipady=9)


# ============================================================
# PAINEL DO ADMINISTRADOR
# ============================================================

def abrir_painel_admin():
    if usuario_logado["tipo"] != "administrador":
        messagebox.showerror("Acesso negado", "Somente administradores podem acessar este painel.")
        return

    painel = tk.Toplevel(janela)
    painel.title("Painel administrativo")
    painel.geometry("700x520")
    painel.resizable(False, False)
    painel.configure(bg=COR_FUNDO)

    tk.Label(painel, text="👑 PAINEL ADMINISTRATIVO", font=("Arial", 20, "bold"), bg=COR_FUNDO, fg=COR_BRANCO).pack(pady=(20, 5))
    tk.Label(painel, text=f"Administrador: {usuario_logado['nome']}", font=("Arial", 10), bg=COR_FUNDO, fg=COR_CINZA).pack(pady=(0, 15))

    frame_botoes = tk.Frame(painel, bg=COR_FUNDO)
    frame_botoes.pack(fill="x", padx=30)

    tk.Button(frame_botoes, text="👨‍🍳 CADASTRAR FUNCIONÁRIO", command=cadastrar_funcionario, bg=COR_VERMELHO, fg=COR_BRANCO, relief="flat", cursor="hand2", font=("Arial", 10, "bold")).pack(fill="x", pady=4, ipady=7)
    tk.Button(frame_botoes, text="📦 EXPORTAR ESTOQUE (JSON)", command=exportar_dados_json, bg=COR_VERDE, fg=COR_BRANCO, relief="flat", cursor="hand2", font=("Arial", 10, "bold")).pack(fill="x", pady=4, ipady=7)
    tk.Button(frame_botoes, text="📄 EXPORTAR PEDIDOS (JSON)", command=exportar_pedidos_json, bg="#27ae60", fg=COR_BRANCO, relief="flat", cursor="hand2", font=("Arial", 10, "bold")).pack(fill="x", pady=4, ipady=7)
    tk.Button(frame_botoes, text="👥 EXPORTAR USUÁRIOS (JSON)", command=exportar_usuarios_json, bg="#2980b9", fg=COR_BRANCO, relief="flat", cursor="hand2", font=("Arial", 10, "bold")).pack(fill="x", pady=4, ipady=7)
    tk.Button(frame_botoes, text="📋 VISUALIZAR USUÁRIOS", command=lambda: visualizar_usuarios(painel), bg=COR_CARD_2, fg=COR_BRANCO, relief="flat", cursor="hand2", font=("Arial", 10, "bold")).pack(fill="x", pady=4, ipady=7)


# ============================================================
# VISUALIZAR USUÁRIOS NO PAINEL
# ============================================================

def visualizar_usuarios(pai):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, email, tipo FROM usuarios ORDER BY id DESC;")
    usuarios = cursor.fetchall()
    conexao.close()

    janela_usuarios = tk.Toplevel(pai)
    janela_usuarios.title("Usuários cadastrados")
    janela_usuarios.geometry("600x400")
    janela_usuarios.configure(bg=COR_CARD)

    tk.Label(janela_usuarios, text="USUÁRIOS CADASTRADOS", font=("Arial", 16, "bold"), bg=COR_CARD, fg=COR_BRANCO).pack(pady=15)

    tabela_usuarios = ttk.Treeview(janela_usuarios, columns=("Nome", "Email", "Tipo"), show="headings")
    tabela_usuarios.heading("Nome", text="Nome")
    tabela_usuarios.heading("Email", text="E-mail")
    tabela_usuarios.heading("Tipo", text="Tipo")

    tabela_usuarios.column("Nome", width=170)
    tabela_usuarios.column("Email", width=250)
    tabela_usuarios.column("Tipo", width=130)

    tabela_usuarios.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    for nome, email, tipo in usuarios:
        tabela_usuarios.insert("", tk.END, values=(nome, email, tipo.capitalize()))


# ============================================================
# LOGOUT E PROCESSAMENTO DE IMAGENS
# ============================================================

def fazer_logout():
    global usuario_logado
    resposta = messagebox.askyesno("Sair", "Deseja realmente sair da conta?")
    if resposta:
        usuario_logado = None
        janela.destroy()
        iniciar_login()


def criar_imagem_fallback(nome, emoji):
    caminho = os.path.join(PASTA_IMAGENS, nome)
    if os.path.exists(caminho):
        return

    imagem = Image.new("RGB", (400, 220), "#292929")
    desenho = ImageDraw.Draw(imagem)
    desenho.rounded_rectangle((5, 5, 395, 215), radius=25, fill="#202020")
    desenho.ellipse((100, 10, 300, 210), fill="#333333")

    try:
        fonte = ImageFont.truetype("seguiemj.ttf", 90)
    except Exception:
        fonte = ImageFont.load_default()

    desenho.text((200, 110), emoji, anchor="mm", font=fonte)
    imagem.save(caminho, "JPEG", quality=90)


def baixar_fotos():
    urls = {
        "xburger.jpg": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&q=80",
        "xsalada.jpg": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=600&q=80",
        "xbacon.jpg": "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=600&q=80",
        "xtudo.jpg": "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=600&q=80",
        "batata.jpg": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600&q=80",
        "refrigerante.jpg": "https://images.unsplash.com/photo-1629203849820-fdd70d49c38e?w=600&q=80",
        "suco.jpg": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&q=80",
        "agua.jpg": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=600&q=80",
        "xfrango.jpg": "https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=600&q=80",
        "xcheddar.jpg": "https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=600&q=80",
        "xduplo.jpg": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=600&q=80",
        "xbarbecue.jpg": "https://images.unsplash.com/photo-1550317138-10000687a72b?w=600&q=80",
        "coca.jpg": "https://images.unsplash.com/photo-1629203849820-fdd70d49c38e?w=600&q=80",
        "guarana.jpg": "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=600&q=80",
        "fanta.jpg": "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=600&q=80",
        "sprite.jpg": "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=600&q=80",
        "pepsi.jpg": "https://images.unsplash.com/photo-1629203849820-fdd70d49c38e?w=600&q=80",
        "suco_laranja.jpg": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&q=80",
        "suco_maracuja.jpg": "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=600&q=80",
        "suco_morango.jpg": "https://images.unsplash.com/photo-1546173159-315724a31696?w=600&q=80",
        "suco_limao.jpg": "https://images.unsplash.com/photo-1523677011781-c91d1bbe2f3f?w=600&q=80"
    }

    cardapio = obter_cardapio_do_banco()
    for produto, dados in cardapio.items():
        caminho = os.path.join(PASTA_IMAGENS, dados["imagem"])
        if os.path.exists(caminho):
            continue

        try:
            req_url = urls.get(dados["imagem"], "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&q=80")
            requisicao = urllib.request.Request(req_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(requisicao, timeout=5) as resposta:
                dados_imagem = resposta.read()
            imagem = Image.open(io.BytesIO(dados_imagem))
            imagem.convert("RGB").save(caminho, "JPEG", quality=90)
        except Exception:
            criar_imagem_fallback(dados["imagem"], "🍔")


def carregar_imagem(caminho, tamanho=(180, 90)):
    try:
        imagem = Image.open(caminho).convert("RGB")
        imagem.thumbnail(tamanho, Image.Resampling.LANCZOS)
        fundo = Image.new("RGB", tamanho, "#222222")
        x = (tamanho[0] - imagem.width) // 2
        y = (tamanho[1] - imagem.height) // 2
        fundo.paste(imagem, (x, y))
        return ImageTk.PhotoImage(fundo)
    except Exception:
        imagem = Image.new("RGB", tamanho, "#333333")
        desenho = ImageDraw.Draw(imagem)
        desenho.text((tamanho[0] // 2, tamanho[1] // 2), "🍔", anchor="mm")
        return ImageTk.PhotoImage(imagem)


# ============================================================
# LÓGICA DO CARRINHO DE COMPRAS
# ============================================================

def calcular_valores():
    subtotal = sum(item["preco"] * item["quantidade"] for item in carrinho)
    desconto = subtotal * 0.10 if subtotal >= 50 else 0
    total = subtotal - desconto
    return subtotal, desconto, total


def adicionar_produto(produto):
    cardapio = obter_cardapio_do_banco()
    for item in carrinho:
        if item["produto"] == produto:
            item["quantidade"] += 1
            atualizar_carrinho()
            return

    carrinho.append({
        "id": cardapio[produto]["id"],
        "produto": produto,
        "preco": cardapio[produto]["preco"],
        "quantidade": 1
    })
    atualizar_carrinho()


def remover_item():
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um item para remover.")
        return

    indice = tabela.index(selecionado[0])
    if 0 <= indice < len(carrinho):
        if carrinho[indice]["quantidade"] > 1:
            carrinho[indice]["quantidade"] -= 1
        else:
            carrinho.pop(indice)

    atualizar_carrinho()


def atualizar_carrinho():
    for item in tabela.get_children():
        tabela.delete(item)

    for item in carrinho:
        total_item = item["preco"] * item["quantidade"]
        tabela.insert("", tk.END, values=(item["produto"], item["quantidade"], formatar_real(total_item)))

    subtotal, desconto, total = calcular_valores()
    subtotal_label.config(text=f"Subtotal: {formatar_real(subtotal)}")
    desconto_label.config(text=f"Desconto: {formatar_real(desconto)}")
    total_label.config(text=f"TOTAL: {formatar_real(total)}")


# ============================================================
# CHECKOUT E GRAVAÇÃO DA VENDA NO SQLITE
# ============================================================

def abrir_checkout():
    if not carrinho:
        messagebox.showwarning("Carrinho vazio", "Adicione produtos antes de finalizar a compra.")
        return

    checkout = tk.Toplevel(janela)
    checkout.title("Finalizar compra")
    checkout.geometry("500x680")
    checkout.resizable(False, False)
    checkout.configure(bg=COR_CARD)
    checkout.transient(janela)
    checkout.grab_set()

    tk.Label(checkout, text="✓ FINALIZAR COMPRA", font=("Arial", 19, "bold"), bg=COR_CARD, fg=COR_BRANCO).pack(pady=(12, 2))
    tk.Label(checkout, text="Confira seus produtos", font=("Arial", 9), bg=COR_CARD, fg=COR_CINZA).pack(pady=(0, 7))

    frame_produtos = tk.Frame(checkout, bg="#111111", height=170)
    frame_produtos.pack(fill="x", padx=20, pady=(0, 8))
    frame_produtos.pack_propagate(False)

    canvas_checkout = tk.Canvas(frame_produtos, bg="#111111", highlightthickness=0)
    scrollbar_checkout = ttk.Scrollbar(frame_produtos, orient="vertical", command=canvas_checkout.yview)
    area_checkout = tk.Frame(canvas_checkout, bg="#111111")

    area_checkout.bind("<Configure>", lambda event: canvas_checkout.configure(scrollregion=canvas_checkout.bbox("all")))
    canvas_checkout.create_window((0, 0), window=area_checkout, anchor="nw")
    canvas_checkout.configure(yscrollcommand=scrollbar_checkout.set)
    canvas_checkout.pack(side="left", fill="both", expand=True)
    scrollbar_checkout.pack(side="right", fill="y")

    imagens_checkout.clear()
    cardapio = obter_cardapio_do_banco()

    for item in carrinho:
        produto = item["produto"]
        dados = cardapio[produto]
        caminho = os.path.join(PASTA_IMAGENS, dados["imagem"])
        imagem = carregar_imagem(caminho, (100, 65))
        imagens_checkout[produto] = imagem

        card_produto = tk.Frame(area_checkout, bg=COR_CARD_2)
        card_produto.pack(fill="x", padx=7, pady=4)

        tk.Label(card_produto, image=imagem, bg=COR_CARD_2).pack(side="left", padx=7, pady=5)
        informacoes = tk.Frame(card_produto, bg=COR_CARD_2)
        informacoes.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(informacoes, text=produto, font=("Arial", 10, "bold"), bg=COR_CARD_2, fg=COR_BRANCO).pack(anchor="w", pady=(6, 0))
        tk.Label(informacoes, text=f"Quantidade: {item['quantidade']}", font=("Arial", 8), bg=COR_CARD_2, fg=COR_CINZA).pack(anchor="w")
        valor_item = item["preco"] * item["quantidade"]
        tk.Label(informacoes, text=formatar_real(valor_item), font=("Arial", 10, "bold"), bg=COR_CARD_2, fg=COR_VERMELHO).pack(anchor="w")

    formulario = tk.Frame(checkout, bg=COR_CARD)
    formulario.pack(fill="x", padx=25)

    tk.Label(formulario, text="Nome do cliente *", font=("Arial", 9, "bold"), bg=COR_CARD, fg=COR_CINZA).pack(anchor="w")
    entrada_nome = tk.Entry(formulario, font=("Arial", 10), bg=COR_CARD_2, fg=COR_BRANCO, insertbackground=COR_BRANCO, relief="flat")
    entrada_nome.pack(fill="x", pady=(3, 6), ipady=5)
    if usuario_logado:
        entrada_nome.insert(0, usuario_logado["nome"])

    tk.Label(formulario, text="Endereço / Rua *", font=("Arial", 9, "bold"), bg=COR_CARD, fg=COR_CINZA).pack(anchor="w")
    entrada_endereco = tk.Entry(formulario, font=("Arial", 10), bg=COR_CARD_2, fg=COR_BRANCO, insertbackground=COR_BRANCO, relief="flat")
    entrada_endereco.pack(fill="x", pady=(3, 6), ipady=5)

    tk.Label(formulario, text="Tipo de residência", font=("Arial", 9, "bold"), bg=COR_CARD, fg=COR_CINZA).pack(anchor="w")
    tipo_var = tk.StringVar(value="Casa")
    combo_tipo = ttk.Combobox(formulario, textvariable=tipo_var, values=["Casa", "Apartamento", "Outro"], state="readonly")
    combo_tipo.pack(fill="x", pady=(3, 6), ipady=3)

    tk.Label(formulario, text="Número da casa *", font=("Arial", 9, "bold"), bg=COR_CARD, fg=COR_CINZA).pack(anchor="w")
    entrada_numero = tk.Entry(formulario, font=("Arial", 10), bg=COR_CARD_2, fg=COR_BRANCO, insertbackground=COR_BRANCO, relief="flat")
    entrada_numero.pack(fill="x", pady=(3, 6), ipady=5)

    tk.Label(formulario, text="Forma de pagamento *", font=("Arial", 9, "bold"), bg=COR_CARD, fg=COR_CINZA).pack(anchor="w")
    pagamento_var = tk.StringVar(value="PIX")
    combo_pagamento = ttk.Combobox(formulario, textvariable=pagamento_var, values=["PIX", "Dinheiro", "Cartão de Débito", "Cartão de Crédito"], state="readonly")
    combo_pagamento.pack(fill="x", pady=(3, 6), ipady=3)

    subtotal, desconto, total = calcular_valores()
    resumo = tk.Frame(checkout, bg="#111111")
    resumo.pack(fill="x", padx=25, pady=(2, 7))

    tk.Label(resumo, text=f"Subtotal: {formatar_real(subtotal)}", font=("Arial", 8), bg="#111111", fg=COR_CINZA).pack(anchor="w", padx=10, pady=(4, 0))
    tk.Label(resumo, text=f"Desconto: {formatar_real(desconto)}", font=("Arial", 8), bg="#111111", fg=COR_CINZA).pack(anchor="w", padx=10)
    tk.Label(resumo, text=f"TOTAL: {formatar_real(total)}", font=("Arial", 12, "bold"), bg="#111111", fg=COR_VERDE).pack(anchor="w", padx=10, pady=(0, 4))

    def confirmar_compra():
        nome = entrada_nome.get().strip()
        endereco = entrada_endereco.get().strip()
        numero_casa = entrada_numero.get().strip()
        tipo_residencia = tipo_var.get()
        pagamento = pagamento_var.get()

        if not nome or not endereco or not numero_casa:
            messagebox.showwarning("Dados incompletos", "Preencha todos os campos obrigatórios.", parent=checkout)
            return

        finalizar_pedido(nome, endereco, tipo_residencia, numero_casa, pagamento, checkout)

    tk.Button(checkout, text="✓ CONFIRMAR E FINALIZAR", command=confirmar_compra, bg=COR_VERMELHO, fg=COR_BRANCO, activebackground=COR_VERMELHO_ESCURO, activeforeground=COR_BRANCO, relief="flat", cursor="hand2", font=("Arial", 10, "bold")).pack(fill="x", padx=25, ipady=8)
    entrada_endereco.focus()


def finalizar_pedido(nome, endereco, tipo_residencia, numero_casa, pagamento, checkout):
    subtotal, desconto, total = calcular_valores()
    agora = datetime.now()
    numero_pedido = agora.strftime("%Y%m%d%H%M%S")
    data_str = agora.strftime("%d/%m/%Y")
    hora_str = agora.strftime("%H:%M:%S")

    conexao = obter_conexao()
    cursor = conexao.cursor()

    usuario_id = usuario_logado["id"] if usuario_logado else None

    # 1. Regista o pedido na tabela 'pedidos'
    cursor.execute("""
        INSERT INTO pedidos (numero, usuario_id, cliente, endereco, tipo_residencia, numero_casa, data, hora, status, pagamento, subtotal, desconto, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Recebido', ?, ?, ?, ?);
    """, (numero_pedido, usuario_id, nome, endereco, tipo_residencia, numero_casa, data_str, hora_str, pagamento, subtotal, desconto, total))

    pedido_id = cursor.lastrowid

    # 2. Regista os itens na tabela 'itens_pedido' e atualiza o estoque
    for item in carrinho:
        p_id = item["id"]
        p_nome = item["produto"]
        p_unitario = item["preco"]
        qtd = item["quantidade"]
        sub_item = p_unitario * qtd

        cursor.execute("""
            INSERT INTO itens_pedido (pedido_id, produto_id, produto_nome, preco_unitario, quantidade, subtotal)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (pedido_id, p_id, p_nome, p_unitario, qtd, sub_item))

        cursor.execute("SELECT estoque FROM produtos WHERE id = ?;", (p_id,))
        res_est = cursor.fetchone()
        if res_est:
            est_anterior = res_est[0]
            est_novo = max(0, est_anterior - qtd)

            cursor.execute("UPDATE produtos SET estoque = ? WHERE id = ?;", (est_novo, p_id))
            cursor.execute("""
                INSERT INTO movimentacoes_estoque (produto_id, usuario_id, tipo, quantidade, estoque_anterior, estoque_novo, observacao)
                VALUES (?, ?, 'saida', ?, ?, ?, ?);
            """, (p_id, usuario_id, qtd, est_anterior, est_novo, f"Saída referente ao pedido {numero_pedido}"))

    conexao.commit()
    conexao.close()

    pedido_dict = {
        "numero": numero_pedido,
        "cliente": nome,
        "endereco": endereco,
        "tipo_residencia": tipo_residencia,
        "numero_casa": numero_casa,
        "data": data_str,
        "hora": hora_str,
        "status": "Recebido",
        "pagamento": pagamento,
        "itens": [item.copy() for item in carrinho],
        "subtotal": subtotal,
        "desconto": desconto,
        "total": total
    }

    checkout.destroy()
    mostrar_recibo(pedido_dict)
    limpar_pedido()


def mostrar_recibo(pedido):
    janela_recibo = tk.Toplevel(janela)
    janela_recibo.title("Pedido finalizado")
    janela_recibo.geometry("450x570")
    janela_recibo.resizable(False, False)
    janela_recibo.configure(bg=COR_CARD)

    tk.Label(janela_recibo, text="🍔 PEDIDO CONFIRMADO", font=("Arial", 18, "bold"), bg=COR_CARD, fg=COR_VERMELHO).pack(pady=(15, 5))

    texto = tk.Text(janela_recibo, bg="#111111", fg=COR_BRANCO, font=("Consolas", 9), relief="flat", padx=12, pady=12)
    texto.pack(fill="both", expand=True, padx=18, pady=12)

    recibo = (
        "====================================\n"
        "       HAMBURGUERIA AUTOMATIZADA\n"
        "====================================\n\n"
        f"PEDIDO Nº: {pedido['numero']}\n"
        f"Cliente: {pedido['cliente']}\n"
        f"Data: {pedido['data']}  {pedido['hora']}\n\n"
        "ENDEREÇO DE ENTREGA\n"
        "------------------------------------\n"
        f"Endereço: {pedido['endereco']}\n"
        f"Tipo: {pedido['tipo_residencia']}\n"
        f"Número: {pedido['numero_casa']}\n\n"
        "ITENS DO PEDIDO\n"
        "------------------------------------\n"
    )

    for item in pedido["itens"]:
        valor_item = item["preco"] * item["quantidade"]
        recibo += f"{item['quantidade']}x {item['produto']}\n    {formatar_real(valor_item)}\n"

    recibo += (
        "\n------------------------------------\n"
        f"Subtotal: {formatar_real(pedido['subtotal'])}\n"
        f"Desconto: {formatar_real(pedido['desconto'])}\n"
        f"TOTAL: {formatar_real(pedido['total'])}\n\n"
        f"Pagamento: {pedido['pagamento']}\n"
        f"Status: {pedido['status']}\n\n"
        "Obrigado pela preferência!\n"
        "====================================\n"
    )

    texto.insert("1.0", recibo)
    texto.config(state="disabled")

    tk.Button(janela_recibo, text="FECHAR", command=janela_recibo.destroy, bg=COR_VERMELHO, fg=COR_BRANCO, activebackground=COR_VERMELHO_ESCURO, relief="flat", cursor="hand2", font=("Arial", 10, "bold")).pack(fill="x", padx=18, pady=(0, 18), ipady=8)


def limpar_pedido():
    carrinho.clear()
    atualizar_carrinho()


# ============================================================
# CONSULTA DE PEDIDOS NO SQLITE
# ============================================================

def visualizar_pedidos():
    if usuario_logado["tipo"] not in ["funcionario", "administrador"]:
        messagebox.showerror("Acesso negado", "Você não possui permissão para visualizar os pedidos.")
        return

    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT numero, cliente, data, pagamento, total, status FROM pedidos ORDER BY id DESC;")
    pedidos = cursor.fetchall()
    conexao.close()

    pedidos_janela = tk.Toplevel(janela)
    pedidos_janela.title("Pedidos da hamburgueria")
    pedidos_janela.geometry("800x500")
    pedidos_janela.configure(bg=COR_FUNDO)

    tk.Label(pedidos_janela, text="📋 PEDIDOS", font=("Arial", 20, "bold"), bg=COR_FUNDO, fg=COR_BRANCO).pack(pady=15)

    tabela_pedidos = ttk.Treeview(pedidos_janela, columns=("Numero", "Cliente", "Data", "Pagamento", "Total", "Status"), show="headings")
    for coluna in ("Numero", "Cliente", "Data", "Pagamento", "Total", "Status"):
        tabela_pedidos.heading(coluna, text=coluna)

    tabela_pedidos.column("Numero", width=120)
    tabela_pedidos.column("Cliente", width=160)
    tabela_pedidos.column("Data", width=130)
    tabela_pedidos.column("Pagamento", width=120)
    tabela_pedidos.column("Total", width=100)
    tabela_pedidos.column("Status", width=100)

    tabela_pedidos.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    for num, cli, dat, pag, tot, sta in pedidos:
        tabela_pedidos.insert("", tk.END, values=(num, cli, dat, pag, formatar_real(tot), sta))


# ============================================================
# JANELA PRINCIPAL
# ============================================================

def iniciar_sistema():
    global janela, tabela, subtotal_label, desconto_label, total_label, relogio

    janela = tk.Tk()
    janela.title("Chapa Quente Hamburgueria")
    janela.geometry(f"{LARGURA}x{ALTURA}")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    topo = tk.Frame(janela, bg="#0b0b0b", height=65)
    topo.pack(fill="x")
    topo.pack_propagate(False)

    tk.Label(topo, text="🍔 Chapa Quente", font=("Arial", 20, "bold"), bg="#0b0b0b", fg=COR_BRANCO).pack(side="left", padx=20)
    tk.Label(topo, text="Hamburgueria", font=("Arial", 10, "bold"), bg="#0b0b0b", fg=COR_VERMELHO).pack(side="left")

    info_usuario = tk.Frame(topo, bg="#0b0b0b")
    info_usuario.pack(side="right", padx=10)

    tk.Label(info_usuario, text=f"{usuario_logado['nome']} | {usuario_logado['tipo'].capitalize()}", font=("Arial", 8, "bold"), bg="#0b0b0b", fg=COR_CINZA).pack(side="left", padx=8)
    tk.Button(info_usuario, text="SAIR", command=fazer_logout, bg="#333333", fg=COR_BRANCO, activebackground="#444444", relief="flat", cursor="hand2", font=("Arial", 8, "bold")).pack(side="left")

    if usuario_logado["tipo"] in ["funcionario", "administrador"]:
        tk.Button(info_usuario, text="📋 PEDIDOS", command=visualizar_pedidos, bg=COR_VERMELHO, fg=COR_BRANCO, relief="flat", cursor="hand2", font=("Arial", 8, "bold")).pack(side="left", padx=5)

    if usuario_logado["tipo"] == "administrador":
        tk.Button(info_usuario, text="👑 ADMIN", command=abrir_painel_admin, bg="#6c2bd9", fg=COR_BRANCO, relief="flat", cursor="hand2", font=("Arial", 8, "bold")).pack(side="left", padx=5)

    relogio = tk.Label(topo, text="", font=("Arial", 8), bg="#0b0b0b", fg=COR_CINZA)
    relogio.pack(side="right", padx=10)

    def atualizar_relogio():
        relogio.config(text=datetime.now().strftime("%d/%m/%Y  •  %H:%M:%S"))
        janela.after(1000, atualizar_relogio)

    principal = tk.Frame(janela, bg=COR_FUNDO)
    principal.pack(fill="both", expand=True, padx=10, pady=10)

    esquerda = tk.Frame(principal, bg=COR_FUNDO, width=570)
    esquerda.pack(side="left", fill="both", expand=True)

    tk.Label(esquerda, text="🍔 Cardápio", font=("Arial", 17, "bold"), bg=COR_FUNDO, fg=COR_BRANCO).pack(anchor="w", pady=(0, 5))

    canvas = tk.Canvas(esquerda, bg=COR_FUNDO, highlightthickness=0)
    scrollbar_produtos = ttk.Scrollbar(esquerda, orient="vertical", command=canvas.yview)
    area_produtos = tk.Frame(canvas, bg=COR_FUNDO)

    area_produtos.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=area_produtos, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_produtos.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_produtos.pack(side="right", fill="y")

    cardapio = obter_cardapio_do_banco()

    for indice, (produto, dados) in enumerate(cardapio.items()):
        linha = indice // 2
        coluna = indice % 2

        card = tk.Frame(area_produtos, bg=COR_CARD, width=260, height=105)
        card.grid(row=linha, column=coluna, padx=5, pady=5)
        card.grid_propagate(False)

        tk.Label(card, text=produto, font=("Arial", 11, "bold"), bg=COR_CARD, fg=COR_BRANCO).pack(anchor="w", padx=12, pady=(10, 2))
        tk.Label(card, text=dados["descricao"], font=("Arial", 8), bg=COR_CARD, fg=COR_CINZA).pack(anchor="w", padx=12)

        rodape = tk.Frame(card, bg=COR_CARD)
        rodape.pack(fill="x", padx=12, pady=7)

        tk.Label(rodape, text=formatar_real(dados["preco"]), font=("Arial", 11, "bold"), bg=COR_CARD, fg=COR_VERMELHO).pack(side="left")
        tk.Button(rodape, text="+ ADICIONAR", command=lambda p=produto: adicionar_produto(p), bg=COR_VERMELHO, fg=COR_BRANCO, activebackground=COR_VERMELHO_ESCURO, relief="flat", cursor="hand2", font=("Arial", 8, "bold")).pack(side="right")

    direita = tk.Frame(principal, bg=COR_CARD, width=295)
    direita.pack(side="right", fill="y", padx=(10, 0))
    direita.pack_propagate(False)

    tk.Label(direita, text="🛒 Seu Pedido", font=("Arial", 17, "bold"), bg=COR_CARD, fg=COR_BRANCO).pack(anchor="w", padx=15, pady=(15, 8))

    colunas = ("Produto", "Qtd", "Total")
    tabela = ttk.Treeview(direita, columns=colunas, show="headings", height=8)
    tabela.heading("Produto", text="Produto")
    tabela.heading("Qtd", text="Qtd")
    tabela.heading("Total", text="Total")

    tabela.column("Produto", width=125)
    tabela.column("Qtd", width=35, anchor="center")
    tabela.column("Total", width=70, anchor="e")
    tabela.pack(fill="x", padx=15)

    tk.Button(direita, text="🗑 Remover item", command=remover_item, bg="#333333", fg=COR_BRANCO, activebackground="#444444", relief="flat", cursor="hand2", font=("Arial", 8, "bold")).pack(fill="x", padx=15, pady=6, ipady=5)
    tk.Frame(direita, bg="#333333", height=1).pack(fill="x", padx=15, pady=3)

    subtotal_label = tk.Label(direita, text="Subtotal: R$ 0,00", font=("Arial", 9), bg=COR_CARD, fg=COR_CINZA)
    subtotal_label.pack(anchor="w", padx=15, pady=2)

    desconto_label = tk.Label(direita, text="Desconto: R$ 0,00", font=("Arial", 9), bg=COR_CARD, fg=COR_CINZA)
    desconto_label.pack(anchor="w", padx=15, pady=2)

    total_label = tk.Label(direita, text="TOTAL: R$ 0,00", font=("Arial", 14, "bold"), bg=COR_CARD, fg=COR_VERMELHO)
    total_label.pack(anchor="w", padx=15, pady=(4, 8))

    tk.Label(direita, text="Na próxima tela você verá as imagens\ndos produtos e informará os dados.", font=("Arial", 8), justify="left", bg=COR_CARD, fg=COR_CINZA).pack(anchor="w", padx=15, pady=(0, 8))
    tk.Button(direita, text="✓ FINALIZAR COMPRA", command=abrir_checkout, bg=COR_VERMELHO, fg=COR_BRANCO, activebackground=COR_VERMELHO_ESCURO, relief="flat", cursor="hand2", font=("Arial", 10, "bold")).pack(fill="x", padx=15, ipady=9)
    tk.Button(direita, text="＋ NOVO PEDIDO", command=limpar_pedido, bg="#333333", fg=COR_BRANCO, activebackground="#444444", relief="flat", cursor="hand2", font=("Arial", 9, "bold")).pack(fill="x", padx=15, pady=7, ipady=6)

    atualizar_carrinho()
    atualizar_relogio()
    janela.mainloop()


# ============================================================
# TELA DE LOGIN
# ============================================================

def iniciar_login():
    global janela_login, entrada_login_email, entrada_login_senha

    janela_login = tk.Tk()
    janela_login.title("Login - Chapa Quente")
    janela_login.geometry("430x500")
    janela_login.resizable(False, False)
    janela_login.configure(bg=COR_FUNDO)

    tk.Label(janela_login, text="🍔", font=("Arial", 45), bg=COR_FUNDO, fg=COR_VERMELHO).pack(pady=(35, 0))
    tk.Label(janela_login, text="CHAPA QUENTE", font=("Arial", 24, "bold"), bg=COR_FUNDO, fg=COR_BRANCO).pack()
    tk.Label(janela_login, text="HAMBURGUERIA", font=("Arial", 10, "bold"), bg=COR_FUNDO, fg=COR_VERMELHO).pack(pady=(0, 25))

    tk.Label(janela_login, text="E-mail", font=("Arial", 9, "bold"), bg=COR_FUNDO, fg=COR_CINZA).pack(anchor="w", padx=55)
    entrada_login_email = tk.Entry(janela_login, font=("Arial", 11), bg=COR_CARD_2, fg=COR_BRANCO, insertbackground=COR_BRANCO, relief="flat")
    entrada_login_email.pack(fill="x", padx=55, pady=(5, 15), ipady=8)

    tk.Label(janela_login, text="Senha", font=("Arial", 9, "bold"), bg=COR_FUNDO, fg=COR_CINZA).pack(anchor="w", padx=55)
    entrada_login_senha = tk.Entry(janela_login, font=("Arial", 11), show="*", bg=COR_CARD_2, fg=COR_BRANCO, insertbackground=COR_BRANCO, relief="flat")
    entrada_login_senha.pack(fill="x", padx=55, pady=(5, 20), ipady=8)

    tk.Button(janela_login, text="ENTRAR", command=realizar_login, bg=COR_VERMELHO, fg=COR_BRANCO, activebackground=COR_VERMELHO_ESCURO, activeforeground=COR_BRANCO, relief="flat", cursor="hand2", font=("Arial", 10, "bold")).pack(fill="x", padx=55, ipady=9)
    tk.Button(janela_login, text="CRIAR NOVA CONTA", command=abrir_cadastro, bg=COR_CARD_2, fg=COR_BRANCO, activebackground="#333333", relief="flat", cursor="hand2", font=("Arial", 9, "bold")).pack(fill="x", padx=55, pady=10, ipady=8)

    tk.Label(janela_login, text="Você pode criar uma conta de cliente ou administrador.\nA conta de administrador exige o código administrativo.", font=("Arial", 8), bg=COR_FUNDO, fg=COR_CINZA, justify="center").pack(pady=5)

    janela_login.bind("<Return>", lambda event: realizar_login())
    entrada_login_email.focus()
    janela_login.mainloop()


# ============================================================
# INÍCIO DA EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    inicializar_banco()
    baixar_fotos()
    iniciar_login()