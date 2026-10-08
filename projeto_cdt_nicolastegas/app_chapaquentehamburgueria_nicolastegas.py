import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from datetime import datetime
import json
import os
import urllib.request
import io


# ============================================================
# CHAPA QUENTE HAMBURGUERIA
# ============================================================

LARGURA = 900
ALTURA = 600

COR_FUNDO = "#101010"
COR_CARD = "#1b1b1b"
COR_CARD_2 = "#252525"
COR_VERMELHO = "#e63946"
COR_VERMELHO_ESCURO = "#b92330"
COR_BRANCO = "#ffffff"
COR_CINZA = "#aaaaaa"
COR_VERDE = "#2ecc71"

ARQUIVO_PEDIDOS = "pedidos.json"
ARQUIVO_USUARIOS = "usuarios.json"
PASTA_IMAGENS = "imagens"

os.makedirs(PASTA_IMAGENS, exist_ok=True)


# ============================================================
# CARDAPIO
# ============================================================

CARDAPIO = {

    "X-Burger": {
        "preco": 15.00,
        "descricao": "Pao, carne, queijo e molho especial",
        "imagem": "xburger.jpg",
        "emoji": "🍔"
    },

    "X-Salada": {
        "preco": 18.00,
        "descricao": "Carne, queijo, alface e tomate",
        "imagem": "xsalada.jpg",
        "emoji": "🥬"
    },

    "X-Bacon": {
        "preco": 22.00,
        "descricao": "Carne, queijo, bacon e molho",
        "imagem": "xbacon.jpg",
        "emoji": "🥓"
    },

    "X-Tudo": {
        "preco": 28.00,
        "descricao": "Carne, queijo, bacon, salada e ovo",
        "imagem": "xtudo.jpg",
        "emoji": "🍔"
    },

    "X-Frango": {
        "preco": 20.00,
        "descricao": "Frango grelhado, queijo e molho especial",
        "imagem": "xfrango.jpg",
        "emoji": "🍔"
    },

    "X-Cheddar": {
        "preco": 23.00,
        "descricao": "Carne, cheddar cremoso e molho especial",
        "imagem": "xcheddar.jpg",
        "emoji": "🍔"
    },

    "X-Duplo": {
        "preco": 30.00,
        "descricao": "Duas carnes, queijo, bacon e molho",
        "imagem": "xduplo.jpg",
        "emoji": "🍔"
    },

    "X-Barbecue": {
        "preco": 26.00,
        "descricao": "Carne, queijo, bacon e molho barbecue",
        "imagem": "xbarbecue.jpg",
        "emoji": "🍔"
    },

    "Batata Frita": {
        "preco": 12.00,
        "descricao": "Batata frita crocante",
        "imagem": "batata.jpg",
        "emoji": "🍟"
    },

    "Coca-Cola": {
        "preco": 7.00,
        "descricao": "Lata 350ml",
        "imagem": "coca.jpg",
        "emoji": "🥤"
    },

    "Guarana": {
        "preco": 7.00,
        "descricao": "Lata 350ml",
        "imagem": "guarana.jpg",
        "emoji": "🥤"
    },

    "Fanta Laranja": {
        "preco": 7.00,
        "descricao": "Lata 350ml",
        "imagem": "fanta.jpg",
        "emoji": "🥤"
    },

    "Sprite": {
        "preco": 7.00,
        "descricao": "Lata 350ml",
        "imagem": "sprite.jpg",
        "emoji": "🥤"
    },

    "Pepsi": {
        "preco": 7.00,
        "descricao": "Lata 350ml",
        "imagem": "pepsi.jpg",
        "emoji": "🥤"
    },

    "Suco": {
        "preco": 8.00,
        "descricao": "Suco natural",
        "imagem": "suco.jpg",
        "emoji": "🧃"
    },

    "Suco de Laranja": {
        "preco": 9.00,
        "descricao": "Suco natural de laranja",
        "imagem": "suco_laranja.jpg",
        "emoji": "🧃"
    },

    "Suco de Maracuja": {
        "preco": 9.00,
        "descricao": "Suco natural de maracuja",
        "imagem": "suco_maracuja.jpg",
        "emoji": "🧃"
    },

    "Suco de Morango": {
        "preco": 10.00,
        "descricao": "Suco natural de morango",
        "imagem": "suco_morango.jpg",
        "emoji": "🧃"
    },

    "Suco de Limao": {
        "preco": 8.00,
        "descricao": "Suco natural de limao",
        "imagem": "suco_limao.jpg",
        "emoji": "🧃"
    },

    "Agua": {
        "preco": 4.00,
        "descricao": "Agua mineral 500ml",
        "imagem": "agua.jpg",
        "emoji": "💧"
    }
}


# ============================================================
# VARIAVEIS
# ============================================================

carrinho = []
imagens_checkout = {}

usuario_logado = None


# ============================================================
# FORMATAR DINHEIRO
# ============================================================

def formatar_real(valor):
    return f"R$ {valor:.2f}".replace(".", ",")


# ============================================================
# SISTEMA DE USUARIOS
# ============================================================

def carregar_usuarios():

    if not os.path.exists(ARQUIVO_USUARIOS):

        # Não existe administrador padrão.
        # O primeiro administrador deverá ser criado pelo próprio usuário
        # através da opção "CRIAR CONTA DE ADMINISTRADOR".
        return {}

    try:

        with open(
            ARQUIVO_USUARIOS,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)

    except Exception:

        return {}


def salvar_usuarios(usuarios):

    with open(
        ARQUIVO_USUARIOS,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            usuarios,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def cadastrar_usuario(nome, email, senha):
    usuarios = carregar_usuarios()
    email = email.lower().strip()

    if email in usuarios:
        return False, "Este e-mail já está cadastrado."

    if len(nome.strip()) < 2:
        return False, "Digite um nome válido."

    if len(email) < 5 or "@" not in email:
        return False, "Digite um e-mail válido."

    if len(senha) < 4:
        return False, "A senha deve possuir pelo menos 4 caracteres."

    usuarios[email] = {
        "nome": nome.strip(),
        "senha": senha,
        "tipo": "usuario"
    }

    salvar_usuarios(usuarios)

    return True, "Usuário cadastrado com sucesso!"


def cadastrar_admin(nome, email, senha, codigo):
    usuarios = carregar_usuarios()
    email = email.lower().strip()

    if email in usuarios:
        return False, "Este e-mail já está cadastrado."

    # Código definido pelo dono do sistema para permitir a criação
    # da primeira conta administrativa.
    if codigo != "CHAPA-ADMIN":
        return False, "Código de administrador incorreto."

    if len(nome.strip()) < 2:
        return False, "Digite um nome válido."

    if len(email) < 5 or "@" not in email:
        return False, "Digite um e-mail válido."

    if len(senha) < 4:
        return False, "A senha deve possuir pelo menos 4 caracteres."

    usuarios[email] = {
        "nome": nome.strip(),
        "senha": senha,
        "tipo": "administrador"
    }

    salvar_usuarios(usuarios)

    return True, "Administrador criado com sucesso!"



# ============================================================
# TELA DE CADASTRO
# ============================================================

def abrir_cadastro():
    cadastro = tk.Toplevel(janela_login)
    cadastro.title("Criar conta")
    cadastro.geometry("420x560")
    cadastro.resizable(False, False)
    cadastro.configure(bg=COR_CARD)

    cadastro.transient(janela_login)
    cadastro.grab_set()

    tk.Label(
        cadastro,
        text="🍔 CRIAR CONTA",
        font=("Arial", 20, "bold"),
        bg=COR_CARD,
        fg=COR_BRANCO
    ).pack(pady=(25, 5))

    tk.Label(
        cadastro,
        text="Escolha o tipo de conta que deseja criar",
        font=("Arial", 9),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(pady=(0, 18))

    # Tipo de conta
    tk.Label(
        cadastro,
        text="Tipo de conta",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w", padx=45)

    tipo_var = tk.StringVar(value="cliente")

    combo_tipo = ttk.Combobox(
        cadastro,
        textvariable=tipo_var,
        values=["cliente", "administrador"],
        state="readonly"
    )
    combo_tipo.pack(
        fill="x",
        padx=45,
        pady=(5, 14),
        ipady=5
    )

    # Nome
    tk.Label(
        cadastro,
        text="Nome completo",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w", padx=45)

    entrada_nome = tk.Entry(
        cadastro,
        font=("Arial", 11),
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat"
    )
    entrada_nome.pack(
        fill="x",
        padx=45,
        pady=(5, 12),
        ipady=7
    )

    # E-mail
    tk.Label(
        cadastro,
        text="E-mail",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w", padx=45)

    entrada_email = tk.Entry(
        cadastro,
        font=("Arial", 11),
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat"
    )
    entrada_email.pack(
        fill="x",
        padx=45,
        pady=(5, 12),
        ipady=7
    )

    # Senha
    tk.Label(
        cadastro,
        text="Senha",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w", padx=45)

    entrada_senha = tk.Entry(
        cadastro,
        font=("Arial", 11),
        show="*",
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat"
    )
    entrada_senha.pack(
        fill="x",
        padx=45,
        pady=(5, 12),
        ipady=7
    )

    # Código administrativo, inicialmente oculto.
    label_codigo = tk.Label(
        cadastro,
        text="Código de administrador",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    )

    entrada_codigo = tk.Entry(
        cadastro,
        font=("Arial", 11),
        show="*",
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat"
    )

    aviso_admin = tk.Label(
        cadastro,
        text="Use o código definido no programa para criar uma conta administrativa.",
        font=("Arial", 8),
        bg=COR_CARD,
        fg=COR_CINZA,
        wraplength=330,
        justify="center"
    )

    def atualizar_tipo(event=None):
        if tipo_var.get() == "administrador":
            label_codigo.pack(anchor="w", padx=45)
            entrada_codigo.pack(
                fill="x",
                padx=45,
                pady=(5, 5),
                ipady=7
            )
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
            sucesso, mensagem = cadastrar_admin(
                nome,
                email,
                senha,
                codigo
            )
        else:
            sucesso, mensagem = cadastrar_usuario(
                nome,
                email,
                senha
            )

        if sucesso:
            messagebox.showinfo(
                "Cadastro",
                mensagem,
                parent=cadastro
            )

            cadastro.destroy()
            entrada_login_email.delete(0, tk.END)
            entrada_login_email.insert(0, email)
            entrada_login_senha.focus()

        else:
            messagebox.showerror(
                "Erro",
                mensagem,
                parent=cadastro
            )

    tk.Button(
        cadastro,
        text="CRIAR CONTA",
        command=realizar_cadastro,
        bg=COR_VERMELHO,
        fg=COR_BRANCO,
        activebackground=COR_VERMELHO_ESCURO,
        activeforeground=COR_BRANCO,
        relief="flat",
        cursor="hand2",
        font=("Arial", 10, "bold")
    ).pack(
        fill="x",
        padx=45,
        pady=(5, 0),
        ipady=9
    )

    entrada_nome.focus()



# ============================================================
# LOGIN
# ============================================================

def realizar_login():

    global usuario_logado

    email = entrada_login_email.get().strip().lower()
    senha = entrada_login_senha.get()

    usuarios = carregar_usuarios()

    if email not in usuarios:

        messagebox.showerror(
            "Login",
            "E-mail não encontrado.",
            parent=janela_login
        )

        return

    usuario = usuarios[email]

    if usuario["senha"] != senha:

        messagebox.showerror(
            "Login",
            "Senha incorreta.",
            parent=janela_login
        )

        entrada_login_senha.delete(0, tk.END)

        return

    usuario_logado = {
        "email": email,
        "nome": usuario["nome"],
        "tipo": usuario["tipo"]
    }

    janela_login.destroy()

    iniciar_sistema()


# ============================================================
# ADMINISTRADOR - CADASTRAR FUNCIONARIO
# ============================================================

def cadastrar_funcionario():

    if not usuario_logado:
        return

    if usuario_logado["tipo"] != "administrador":

        messagebox.showerror(
            "Acesso negado",
            "Somente o administrador pode cadastrar funcionários."
        )

        return

    cadastro = tk.Toplevel(janela)

    cadastro.title("Cadastrar funcionário")
    cadastro.geometry("420x500")
    cadastro.resizable(False, False)
    cadastro.configure(bg=COR_CARD)

    cadastro.transient(janela)
    cadastro.grab_set()

    tk.Label(
        cadastro,
        text="👨‍🍳 NOVO FUNCIONÁRIO",
        font=("Arial", 18, "bold"),
        bg=COR_CARD,
        fg=COR_BRANCO
    ).pack(pady=(25, 5))

    tk.Label(
        cadastro,
        text="Crie uma conta para funcionário ou administrador",
        font=("Arial", 9),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(pady=(0, 20))

    # Nome

    tk.Label(
        cadastro,
        text="Nome",
        bg=COR_CARD,
        fg=COR_CINZA,
        font=("Arial", 9, "bold")
    ).pack(anchor="w", padx=45)

    nome = tk.Entry(
        cadastro,
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat",
        font=("Arial", 11)
    )

    nome.pack(
        fill="x",
        padx=45,
        pady=(5, 12),
        ipady=7
    )

    # Email

    tk.Label(
        cadastro,
        text="E-mail",
        bg=COR_CARD,
        fg=COR_CINZA,
        font=("Arial", 9, "bold")
    ).pack(anchor="w", padx=45)

    email = tk.Entry(
        cadastro,
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat",
        font=("Arial", 11)
    )

    email.pack(
        fill="x",
        padx=45,
        pady=(5, 12),
        ipady=7
    )

    # Senha

    tk.Label(
        cadastro,
        text="Senha",
        bg=COR_CARD,
        fg=COR_CINZA,
        font=("Arial", 9, "bold")
    ).pack(anchor="w", padx=45)

    senha = tk.Entry(
        cadastro,
        show="*",
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat",
        font=("Arial", 11)
    )

    senha.pack(
        fill="x",
        padx=45,
        pady=(5, 12),
        ipady=7
    )

    # Tipo

    tk.Label(
        cadastro,
        text="Tipo de conta",
        bg=COR_CARD,
        fg=COR_CINZA,
        font=("Arial", 9, "bold")
    ).pack(anchor="w", padx=45)

    tipo_var = tk.StringVar(value="funcionario")

    combo = ttk.Combobox(
        cadastro,
        textvariable=tipo_var,
        values=[
            "funcionario",
            "administrador"
        ],
        state="readonly"
    )

    combo.pack(
        fill="x",
        padx=45,
        pady=(5, 20),
        ipady=5
    )

    def salvar():

        nome_valor = nome.get().strip()
        email_valor = email.get().strip().lower()
        senha_valor = senha.get()
        tipo_valor = tipo_var.get()

        usuarios = carregar_usuarios()

        if not nome_valor or not email_valor or not senha_valor:

            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos.",
                parent=cadastro
            )

            return

        if email_valor in usuarios:

            messagebox.showerror(
                "Erro",
                "Este e-mail já está cadastrado.",
                parent=cadastro
            )

            return

        usuarios[email_valor] = {
            "nome": nome_valor,
            "senha": senha_valor,
            "tipo": tipo_valor
        }

        salvar_usuarios(usuarios)

        messagebox.showinfo(
            "Sucesso",
            "Conta criada com sucesso!",
            parent=cadastro
        )

        cadastro.destroy()

    tk.Button(
        cadastro,
        text="CADASTRAR CONTA",
        command=salvar,
        bg=COR_VERMELHO,
        fg=COR_BRANCO,
        activebackground=COR_VERMELHO_ESCURO,
        relief="flat",
        cursor="hand2",
        font=("Arial", 10, "bold")
    ).pack(
        fill="x",
        padx=45,
        ipady=9
    )


# ============================================================
# EXPORTAR ESTOQUE PARA JSON
# ============================================================
def exportar_dados_json():

    if not usuario_logado or usuario_logado.get("tipo") != "administrador":
        messagebox.showerror(
            "Acesso negado",
            "Somente o administrador pode exportar os dados."
        )
        return

    try:
        nome_arquivo = filedialog.asksaveasfilename(
            title="Exportar estoque para JSON",
            defaultextension=".json",
            filetypes=[
                ("Arquivo JSON", "*.json"),
                ("Todos os arquivos", "*.*")
            ],
            initialfile="estoque_produtos.json"
        )

        if not nome_arquivo:
            return

        dados = []

        for produto, info in CARDAPIO.items():
            dados.append({
                "produto": produto,
                "preco": info["preco"],
                "descricao": info["descricao"],
                "imagem": info["imagem"]
            })

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        messagebox.showinfo(
            "Exportação concluída",
            "Os produtos foram exportados com sucesso!\n\n"
            f"Arquivo:\n{nome_arquivo}"
        )

    except Exception as erro:
        messagebox.showerror(
            "Erro ao exportar",
            f"Ocorreu um erro ao exportar o JSON:\n\n{erro}"
        )


# ============================================================
# PAINEL DO ADMINISTRADOR
# ============================================================

def abrir_painel_admin():

    if usuario_logado["tipo"] != "administrador":

        messagebox.showerror(
            "Acesso negado",
            "Somente administradores podem acessar este painel."
        )

        return

    painel = tk.Toplevel(janela)

    painel.title("Painel administrativo")
    painel.geometry("700x500")
    painel.resizable(False, False)
    painel.configure(bg=COR_FUNDO)

    tk.Label(
        painel,
        text="👑 PAINEL ADMINISTRATIVO",
        font=("Arial", 20, "bold"),
        bg=COR_FUNDO,
        fg=COR_BRANCO
    ).pack(pady=(20, 5))

    tk.Label(
        painel,
        text=f"Administrador: {usuario_logado['nome']}",
        font=("Arial", 10),
        bg=COR_FUNDO,
        fg=COR_CINZA
    ).pack(pady=(0, 15))

    frame_botoes = tk.Frame(
        painel,
        bg=COR_FUNDO
    )

    frame_botoes.pack(
        fill="x",
        padx=30
    )

    tk.Button(
        frame_botoes,
        text="👨‍🍳 CADASTRAR FUNCIONÁRIO",
        command=cadastrar_funcionario,
        bg=COR_VERMELHO,
        fg=COR_BRANCO,
        relief="flat",
        cursor="hand2",
        font=("Arial", 10, "bold")
    ).pack(
        fill="x",
        pady=5,
        ipady=8
    )

    tk.Button(
        frame_botoes,
        text="📄 EXPORTAR JSON",
        command=exportar_dados_json,
        bg=COR_VERDE,
        fg=COR_BRANCO,
        relief="flat",
        cursor="hand2",
        font=("Arial", 10, "bold")
    ).pack(
        fill="x",
        pady=5,
        ipady=8
    )

    tk.Button(
        frame_botoes,
        text="📋 VISUALIZAR USUÁRIOS",
        command=lambda: visualizar_usuarios(painel),
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        relief="flat",
        cursor="hand2",
        font=("Arial", 10, "bold")
    ).pack(
        fill="x",
        pady=5,
        ipady=8
    )


# ============================================================
# VISUALIZAR USUARIOS
# ============================================================

def visualizar_usuarios(pai):

    usuarios = carregar_usuarios()

    janela_usuarios = tk.Toplevel(pai)

    janela_usuarios.title("Usuários cadastrados")
    janela_usuarios.geometry("600x400")
    janela_usuarios.configure(bg=COR_CARD)

    tk.Label(
        janela_usuarios,
        text="USUÁRIOS CADASTRADOS",
        font=("Arial", 16, "bold"),
        bg=COR_CARD,
        fg=COR_BRANCO
    ).pack(pady=15)

    tabela_usuarios = ttk.Treeview(
        janela_usuarios,
        columns=("Nome", "Email", "Tipo"),
        show="headings"
    )

    tabela_usuarios.heading(
        "Nome",
        text="Nome"
    )

    tabela_usuarios.heading(
        "Email",
        text="E-mail"
    )

    tabela_usuarios.heading(
        "Tipo",
        text="Tipo"
    )

    tabela_usuarios.column(
        "Nome",
        width=170
    )

    tabela_usuarios.column(
        "Email",
        width=250
    )

    tabela_usuarios.column(
        "Tipo",
        width=130
    )

    tabela_usuarios.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    for email, dados in usuarios.items():

        tabela_usuarios.insert(
            "",
            tk.END,
            values=(
                dados["nome"],
                email,
                dados["tipo"].capitalize()
            )
        )


# ============================================================
# LOGOUT
# ============================================================

def fazer_logout():

    global usuario_logado

    resposta = messagebox.askyesno(
        "Sair",
        "Deseja realmente sair da conta?"
    )

    if resposta:

        usuario_logado = None

        janela.destroy()

        iniciar_login()


# ============================================================
# CRIAR IMAGEM FALLBACK
# ============================================================

def criar_imagem_fallback(nome, emoji):

    caminho = os.path.join(
        PASTA_IMAGENS,
        nome
    )

    if os.path.exists(caminho):
        return

    imagem = Image.new(
        "RGB",
        (400, 220),
        "#292929"
    )

    desenho = ImageDraw.Draw(imagem)

    desenho.rounded_rectangle(
        (5, 5, 395, 215),
        radius=25,
        fill="#202020"
    )

    desenho.ellipse(
        (100, 10, 300, 210),
        fill="#333333"
    )

    try:

        fonte = ImageFont.truetype(
            "seguiemj.ttf",
            90
        )

    except Exception:

        fonte = ImageFont.load_default()

    desenho.text(
        (200, 110),
        emoji,
        anchor="mm",
        font=fonte
    )

    imagem.save(
        caminho,
        "JPEG",
        quality=90
    )


# ============================================================
# DOWNLOAD DAS IMAGENS
# ============================================================

def baixar_fotos():

    urls = {

        "xburger.jpg":
            "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&q=80",

        "xsalada.jpg":
            "https://images.unsplash.com/photo-1550547660-d9450f859349?w=600&q=80",

        "xbacon.jpg":
            "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=600&q=80",

        "xtudo.jpg":
            "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=600&q=80",

        "batata.jpg":
            "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600&q=80",

        "refrigerante.jpg":
            "https://images.unsplash.com/photo-1629203849820-fdd70d49c38e?w=600&q=80",

        "suco.jpg":
            "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&q=80",

        "agua.jpg":
            "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=600&q=80",

        "xfrango.jpg":
            "https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=600&q=80",

        "xcheddar.jpg":
            "https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=600&q=80",

        "xduplo.jpg":
            "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=600&q=80",

        "xbarbecue.jpg":
            "https://images.unsplash.com/photo-1550317138-10000687a72b?w=600&q=80",

        "coca.jpg":
            "https://images.unsplash.com/photo-1629203849820-fdd70d49c38e?w=600&q=80",

        "guarana.jpg":
            "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=600&q=80",

        "fanta.jpg":
            "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=600&q=80",

        "sprite.jpg":
            "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=600&q=80",

        "pepsi.jpg":
            "https://images.unsplash.com/photo-1629203849820-fdd70d49c38e?w=600&q=80",

        "suco_laranja.jpg":
            "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&q=80",

        "suco_maracuja.jpg":
            "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=600&q=80",

        "suco_morango.jpg":
            "https://images.unsplash.com/photo-1546173159-315724a31696?w=600&q=80",

        "suco_limao.jpg":
            "https://images.unsplash.com/photo-1523677011781-c91d1bbe2f3f?w=600&q=80"
    }

    for produto, dados in CARDAPIO.items():

        caminho = os.path.join(
            PASTA_IMAGENS,
            dados["imagem"]
        )

        if os.path.exists(caminho):
            continue

        try:

            requisicao = urllib.request.Request(
                urls[dados["imagem"]],
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            with urllib.request.urlopen(
                requisicao,
                timeout=5
            ) as resposta:

                dados_imagem = resposta.read()

            imagem = Image.open(
                io.BytesIO(dados_imagem)
            )

            imagem.convert("RGB").save(
                caminho,
                "JPEG",
                quality=90
            )

        except Exception:

            criar_imagem_fallback(
                dados["imagem"],
                dados["emoji"]
            )


# ============================================================
# CARREGAR IMAGEM
# ============================================================

def carregar_imagem(caminho, tamanho=(180, 90)):

    try:

        imagem = Image.open(
            caminho
        ).convert("RGB")

        imagem.thumbnail(
            tamanho,
            Image.Resampling.LANCZOS
        )

        fundo = Image.new(
            "RGB",
            tamanho,
            "#222222"
        )

        x = (
            tamanho[0] -
            imagem.width
        ) // 2

        y = (
            tamanho[1] -
            imagem.height
        ) // 2

        fundo.paste(
            imagem,
            (x, y)
        )

        return ImageTk.PhotoImage(
            fundo
        )

    except Exception:

        imagem = Image.new(
            "RGB",
            tamanho,
            "#333333"
        )

        desenho = ImageDraw.Draw(
            imagem
        )

        desenho.text(
            (
                tamanho[0] // 2,
                tamanho[1] // 2
            ),
            "🍔",
            anchor="mm"
        )

        return ImageTk.PhotoImage(
            imagem
        )


# ============================================================
# CALCULAR VALORES
# ============================================================

def calcular_valores():

    subtotal = sum(
        item["preco"] * item["quantidade"]
        for item in carrinho
    )

    if subtotal >= 50:

        desconto = subtotal * 0.10

    else:

        desconto = 0

    total = subtotal - desconto

    return subtotal, desconto, total


# ============================================================
# ADICIONAR PRODUTO
# ============================================================

def adicionar_produto(produto):

    for item in carrinho:

        if item["produto"] == produto:

            item["quantidade"] += 1

            atualizar_carrinho()

            return

    carrinho.append(
        {
            "produto": produto,
            "preco": CARDAPIO[produto]["preco"],
            "quantidade": 1
        }
    )

    atualizar_carrinho()


# ============================================================
# REMOVER ITEM
# ============================================================

def remover_item():

    selecionado = tabela.selection()

    if not selecionado:

        messagebox.showwarning(
            "Atenção",
            "Selecione um item para remover."
        )

        return

    indice = tabela.index(
        selecionado[0]
    )

    if 0 <= indice < len(carrinho):

        if carrinho[indice]["quantidade"] > 1:

            carrinho[indice]["quantidade"] -= 1

        else:

            carrinho.pop(indice)

    atualizar_carrinho()


# ============================================================
# ATUALIZAR CARRINHO
# ============================================================

def atualizar_carrinho():

    for item in tabela.get_children():

        tabela.delete(item)

    for item in carrinho:

        total_item = (
            item["preco"] *
            item["quantidade"]
        )

        tabela.insert(
            "",
            tk.END,
            values=(
                item["produto"],
                item["quantidade"],
                formatar_real(total_item)
            )
        )

    subtotal, desconto, total = calcular_valores()

    subtotal_label.config(
        text=f"Subtotal: {formatar_real(subtotal)}"
    )

    desconto_label.config(
        text=f"Desconto: {formatar_real(desconto)}"
    )

    total_label.config(
        text=f"TOTAL: {formatar_real(total)}"
    )


# ============================================================
# CHECKOUT
# ============================================================

def abrir_checkout():

    if not carrinho:

        messagebox.showwarning(
            "Carrinho vazio",
            "Adicione produtos antes de finalizar a compra."
        )

        return

    checkout = tk.Toplevel(janela)

    checkout.title(
        "Finalizar compra"
    )

    checkout.geometry(
        "500x680"
    )

    checkout.resizable(
        False,
        False
    )

    checkout.configure(
        bg=COR_CARD
    )

    checkout.transient(janela)
    checkout.grab_set()

    tk.Label(
        checkout,
        text="✓ FINALIZAR COMPRA",
        font=("Arial", 19, "bold"),
        bg=COR_CARD,
        fg=COR_BRANCO
    ).pack(
        pady=(12, 2)
    )

    tk.Label(
        checkout,
        text="Confira seus produtos",
        font=("Arial", 9),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(
        pady=(0, 7)
    )

    frame_produtos = tk.Frame(
        checkout,
        bg="#111111",
        height=170
    )

    frame_produtos.pack(
        fill="x",
        padx=20,
        pady=(0, 8)
    )

    frame_produtos.pack_propagate(False)

    canvas_checkout = tk.Canvas(
        frame_produtos,
        bg="#111111",
        highlightthickness=0
    )

    scrollbar_checkout = ttk.Scrollbar(
        frame_produtos,
        orient="vertical",
        command=canvas_checkout.yview
    )

    area_checkout = tk.Frame(
        canvas_checkout,
        bg="#111111"
    )

    area_checkout.bind(
        "<Configure>",
        lambda event:
        canvas_checkout.configure(
            scrollregion=canvas_checkout.bbox("all")
        )
    )

    canvas_checkout.create_window(
        (0, 0),
        window=area_checkout,
        anchor="nw"
    )

    canvas_checkout.configure(
        yscrollcommand=scrollbar_checkout.set
    )

    canvas_checkout.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar_checkout.pack(
        side="right",
        fill="y"
    )

    imagens_checkout.clear()

    for item in carrinho:

        produto = item["produto"]

        dados = CARDAPIO[produto]

        caminho = os.path.join(
            PASTA_IMAGENS,
            dados["imagem"]
        )

        imagem = carregar_imagem(
            caminho,
            (100, 65)
        )

        imagens_checkout[produto] = imagem

        card_produto = tk.Frame(
            area_checkout,
            bg=COR_CARD_2
        )

        card_produto.pack(
            fill="x",
            padx=7,
            pady=4
        )

        tk.Label(
            card_produto,
            image=imagem,
            bg=COR_CARD_2
        ).pack(
            side="left",
            padx=7,
            pady=5
        )

        informacoes = tk.Frame(
            card_produto,
            bg=COR_CARD_2
        )

        informacoes.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            informacoes,
            text=produto,
            font=("Arial", 10, "bold"),
            bg=COR_CARD_2,
            fg=COR_BRANCO
        ).pack(
            anchor="w",
            pady=(6, 0)
        )

        tk.Label(
            informacoes,
            text=f"Quantidade: {item['quantidade']}",
            font=("Arial", 8),
            bg=COR_CARD_2,
            fg=COR_CINZA
        ).pack(
            anchor="w"
        )

        valor_item = (
            item["preco"] *
            item["quantidade"]
        )

        tk.Label(
            informacoes,
            text=formatar_real(valor_item),
            font=("Arial", 10, "bold"),
            bg=COR_CARD_2,
            fg=COR_VERMELHO
        ).pack(
            anchor="w"
        )

    # ========================================================
    # FORMULARIO
    # ========================================================

    formulario = tk.Frame(
        checkout,
        bg=COR_CARD
    )

    formulario.pack(
        fill="x",
        padx=25
    )

    tk.Label(
        formulario,
        text="Nome do cliente *",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w")

    entrada_nome = tk.Entry(
        formulario,
        font=("Arial", 10),
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat"
    )

    entrada_nome.pack(
        fill="x",
        pady=(3, 6),
        ipady=5
    )

    # Preenche o nome do usuário logado

    if usuario_logado:

        entrada_nome.insert(
            0,
            usuario_logado["nome"]
        )

    tk.Label(
        formulario,
        text="Endereço / Rua *",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w")

    entrada_endereco = tk.Entry(
        formulario,
        font=("Arial", 10),
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat"
    )

    entrada_endereco.pack(
        fill="x",
        pady=(3, 6),
        ipady=5
    )

    tk.Label(
        formulario,
        text="Tipo de residência",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w")

    tipo_var = tk.StringVar(
        value="Casa"
    )

    combo_tipo = ttk.Combobox(
        formulario,
        textvariable=tipo_var,
        values=[
            "Casa",
            "Apartamento",
            "Outro"
        ],
        state="readonly"
    )

    combo_tipo.pack(
        fill="x",
        pady=(3, 6),
        ipady=3
    )

    tk.Label(
        formulario,
        text="Número da casa *",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w")

    entrada_numero = tk.Entry(
        formulario,
        font=("Arial", 10),
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat"
    )

    entrada_numero.pack(
        fill="x",
        pady=(3, 6),
        ipady=5
    )

    tk.Label(
        formulario,
        text="Forma de pagamento *",
        font=("Arial", 9, "bold"),
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(anchor="w")

    pagamento_var = tk.StringVar(
        value="PIX"
    )

    combo_pagamento = ttk.Combobox(
        formulario,
        textvariable=pagamento_var,
        values=[
            "PIX",
            "Dinheiro",
            "Cartão de Débito",
            "Cartão de Crédito"
        ],
        state="readonly"
    )

    combo_pagamento.pack(
        fill="x",
        pady=(3, 6),
        ipady=3
    )

    subtotal, desconto, total = calcular_valores()

    resumo = tk.Frame(
        checkout,
        bg="#111111"
    )

    resumo.pack(
        fill="x",
        padx=25,
        pady=(2, 7)
    )

    tk.Label(
        resumo,
        text=f"Subtotal: {formatar_real(subtotal)}",
        font=("Arial", 8),
        bg="#111111",
        fg=COR_CINZA
    ).pack(
        anchor="w",
        padx=10,
        pady=(4, 0)
    )

    tk.Label(
        resumo,
        text=f"Desconto: {formatar_real(desconto)}",
        font=("Arial", 8),
        bg="#111111",
        fg=COR_CINZA
    ).pack(
        anchor="w",
        padx=10
    )

    tk.Label(
        resumo,
        text=f"TOTAL: {formatar_real(total)}",
        font=("Arial", 12, "bold"),
        bg="#111111",
        fg=COR_VERDE
    ).pack(
        anchor="w",
        padx=10,
        pady=(0, 4)
    )

    # ========================================================
    # CONFIRMAR COMPRA
    # ========================================================

    def confirmar_compra():

        nome = entrada_nome.get().strip()
        endereco = entrada_endereco.get().strip()
        numero_casa = entrada_numero.get().strip()
        tipo_residencia = tipo_var.get()
        pagamento = pagamento_var.get()

        if not nome:

            messagebox.showwarning(
                "Dados incompletos",
                "Digite o nome do cliente.",
                parent=checkout
            )

            return

        if not endereco:

            messagebox.showwarning(
                "Dados incompletos",
                "Digite o endereço / rua.",
                parent=checkout
            )

            return

        if not numero_casa:

            messagebox.showwarning(
                "Dados incompletos",
                "Digite o número da casa.",
                parent=checkout
            )

            return

        finalizar_pedido(
            nome,
            endereco,
            tipo_residencia,
            numero_casa,
            pagamento,
            checkout
        )

    tk.Button(
        checkout,
        text="✓ CONFIRMAR E FINALIZAR",
        command=confirmar_compra,
        bg=COR_VERMELHO,
        fg=COR_BRANCO,
        activebackground=COR_VERMELHO_ESCURO,
        activeforeground=COR_BRANCO,
        relief="flat",
        cursor="hand2",
        font=("Arial", 10, "bold")
    ).pack(
        fill="x",
        padx=25,
        ipady=8
    )

    entrada_endereco.focus()


# ============================================================
# FINALIZAR PEDIDO
# ============================================================

def finalizar_pedido(
    nome,
    endereco,
    tipo_residencia,
    numero_casa,
    pagamento,
    checkout
):

    subtotal, desconto, total = calcular_valores()

    agora = datetime.now()

    numero = agora.strftime(
        "%Y%m%d%H%M%S"
    )

    pedido = {

        "numero": numero,

        "cliente": nome,

        "endereco": endereco,

        "tipo_residencia": tipo_residencia,

        "numero_casa": numero_casa,

        "data": agora.strftime(
            "%d/%m/%Y"
        ),

        "hora": agora.strftime(
            "%H:%M:%S"
        ),

        "status": "Recebido",

        "pagamento": pagamento,

        "usuario_email": (
            usuario_logado["email"]
            if usuario_logado
            else ""
        ),

        "itens": [
            item.copy()
            for item in carrinho
        ],

        "subtotal": subtotal,

        "desconto": desconto,

        "total": total
    }

    salvar_pedido(pedido)

    checkout.destroy()

    mostrar_recibo(pedido)

    limpar_pedido()


# ============================================================
# SALVAR PEDIDO
# ============================================================

def salvar_pedido(pedido):

    pedidos = []

    if os.path.exists(
        ARQUIVO_PEDIDOS
    ):

        try:

            with open(
                ARQUIVO_PEDIDOS,
                "r",
                encoding="utf-8"
            ) as arquivo:

                pedidos = json.load(
                    arquivo
                )

        except Exception:

            pedidos = []

    pedidos.append(
        pedido
    )

    with open(
        ARQUIVO_PEDIDOS,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            pedidos,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


# ============================================================
# RECIBO
# ============================================================

def mostrar_recibo(pedido):

    janela_recibo = tk.Toplevel(
        janela
    )

    janela_recibo.title(
        "Pedido finalizado"
    )

    janela_recibo.geometry(
        "450x570"
    )

    janela_recibo.resizable(
        False,
        False
    )

    janela_recibo.configure(
        bg=COR_CARD
    )

    tk.Label(
        janela_recibo,
        text="🍔 PEDIDO CONFIRMADO",
        font=("Arial", 18, "bold"),
        bg=COR_CARD,
        fg=COR_VERMELHO
    ).pack(
        pady=(15, 5)
    )

    texto = tk.Text(
        janela_recibo,
        bg="#111111",
        fg=COR_BRANCO,
        font=("Consolas", 9),
        relief="flat",
        padx=12,
        pady=12
    )

    texto.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=12
    )

    recibo = (

        "====================================\n"
        "       HAMBURGUERIA AUTOMATIZADA\n"
        "====================================\n\n"

        f"PEDIDO Nº: {pedido['numero']}\n"

        f"Cliente: {pedido['cliente']}\n"

        f"Data: {pedido['data']}  "
        f"{pedido['hora']}\n\n"

        "ENDEREÇO DE ENTREGA\n"

        "------------------------------------\n"

        f"Endereço: {pedido['endereco']}\n"

        f"Tipo: {pedido['tipo_residencia']}\n"

        f"Número: {pedido['numero_casa']}\n\n"

        "ITENS DO PEDIDO\n"

        "------------------------------------\n"
    )

    for item in pedido["itens"]:

        valor_item = (
            item["preco"] *
            item["quantidade"]
        )

        recibo += (

            f"{item['quantidade']}x "
            f"{item['produto']}\n"

            f"    "
            f"{formatar_real(valor_item)}\n"
        )

    recibo += (

        "\n------------------------------------\n"

        f"Subtotal: "
        f"{formatar_real(pedido['subtotal'])}\n"

        f"Desconto: "
        f"{formatar_real(pedido['desconto'])}\n"

        f"TOTAL: "
        f"{formatar_real(pedido['total'])}\n\n"

        f"Pagamento: "
        f"{pedido['pagamento']}\n"

        f"Status: "
        f"{pedido['status']}\n\n"

        "Obrigado pela preferência!\n"

        "====================================\n"
    )

    texto.insert(
        "1.0",
        recibo
    )

    texto.config(
        state="disabled"
    )

    tk.Button(
        janela_recibo,
        text="FECHAR",
        command=janela_recibo.destroy,
        bg=COR_VERMELHO,
        fg=COR_BRANCO,
        activebackground=COR_VERMELHO_ESCURO,
        relief="flat",
        cursor="hand2",
        font=("Arial", 10, "bold")
    ).pack(
        fill="x",
        padx=18,
        pady=(0, 18),
        ipady=8
    )


# ============================================================
# NOVO PEDIDO
# ============================================================

def limpar_pedido():

    carrinho.clear()

    atualizar_carrinho()


# ============================================================
# VISUALIZAR PEDIDOS - FUNCIONARIO / ADMIN
# ============================================================

def visualizar_pedidos():

    if usuario_logado["tipo"] not in [
        "funcionario",
        "administrador"
    ]:

        messagebox.showerror(
            "Acesso negado",
            "Você não possui permissão para visualizar os pedidos."
        )

        return

    pedidos_janela = tk.Toplevel(janela)

    pedidos_janela.title(
        "Pedidos da hamburgueria"
    )

    pedidos_janela.geometry(
        "800x500"
    )

    pedidos_janela.configure(
        bg=COR_FUNDO
    )

    tk.Label(
        pedidos_janela,
        text="📋 PEDIDOS",
        font=("Arial", 20, "bold"),
        bg=COR_FUNDO,
        fg=COR_BRANCO
    ).pack(pady=15)

    tabela_pedidos = ttk.Treeview(
        pedidos_janela,
        columns=(
            "Numero",
            "Cliente",
            "Data",
            "Pagamento",
            "Total",
            "Status"
        ),
        show="headings"
    )

    for coluna in (
        "Numero",
        "Cliente",
        "Data",
        "Pagamento",
        "Total",
        "Status"
    ):

        tabela_pedidos.heading(
            coluna,
            text=coluna
        )

    tabela_pedidos.column(
        "Numero",
        width=120
    )

    tabela_pedidos.column(
        "Cliente",
        width=160
    )

    tabela_pedidos.column(
        "Data",
        width=130
    )

    tabela_pedidos.column(
        "Pagamento",
        width=120
    )

    tabela_pedidos.column(
        "Total",
        width=100
    )

    tabela_pedidos.column(
        "Status",
        width=100
    )

    tabela_pedidos.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    pedidos = []

    if os.path.exists(
        ARQUIVO_PEDIDOS
    ):

        try:

            with open(
                ARQUIVO_PEDIDOS,
                "r",
                encoding="utf-8"
            ) as arquivo:

                pedidos = json.load(
                    arquivo
                )

        except Exception:

            pedidos = []

    for pedido in pedidos:

        tabela_pedidos.insert(
            "",
            tk.END,
            values=(
                pedido["numero"],
                pedido["cliente"],
                pedido["data"],
                pedido["pagamento"],
                formatar_real(
                    pedido["total"]
                ),
                pedido["status"]
            )
        )


# ============================================================
# JANELA PRINCIPAL
# ============================================================

def iniciar_sistema():

    global janela
    global tabela
    global subtotal_label
    global desconto_label
    global total_label
    global relogio

    janela = tk.Tk()

    janela.title(
        "Chapa Quente Hamburgueria"
    )

    janela.geometry(
        f"{LARGURA}x{ALTURA}"
    )

    janela.resizable(
        False,
        False
    )

    janela.configure(
        bg=COR_FUNDO
    )

    # ========================================================
    # CABECALHO
    # ========================================================

    topo = tk.Frame(
        janela,
        bg="#0b0b0b",
        height=65
    )

    topo.pack(
        fill="x"
    )

    topo.pack_propagate(
        False
    )

    tk.Label(
        topo,
        text="🍔 Chapa Quente",
        font=("Arial", 20, "bold"),
        bg="#0b0b0b",
        fg=COR_BRANCO
    ).pack(
        side="left",
        padx=20
    )

    tk.Label(
        topo,
        text="Hamburgueria",
        font=("Arial", 10, "bold"),
        bg="#0b0b0b",
        fg=COR_VERMELHO
    ).pack(
        side="left"
    )

    # ========================================================
    # USUARIO LOGADO
    # ========================================================

    info_usuario = tk.Frame(
        topo,
        bg="#0b0b0b"
    )

    info_usuario.pack(
        side="right",
        padx=10
    )

    tk.Label(
        info_usuario,
        text=(
            f"{usuario_logado['nome']} | "
            f"{usuario_logado['tipo'].capitalize()}"
        ),
        font=("Arial", 8, "bold"),
        bg="#0b0b0b",
        fg=COR_CINZA
    ).pack(
        side="left",
        padx=8
    )

    tk.Button(
        info_usuario,
        text="SAIR",
        command=fazer_logout,
        bg="#333333",
        fg=COR_BRANCO,
        activebackground="#444444",
        relief="flat",
        cursor="hand2",
        font=("Arial", 8, "bold")
    ).pack(
        side="left"
    )

    # ========================================================
    # BOTOES DE FUNCIONARIO / ADMIN
    # ========================================================

    if usuario_logado["tipo"] in [
        "funcionario",
        "administrador"
    ]:

        tk.Button(
            info_usuario,
            text="📋 PEDIDOS",
            command=visualizar_pedidos,
            bg=COR_VERMELHO,
            fg=COR_BRANCO,
            relief="flat",
            cursor="hand2",
            font=("Arial", 8, "bold")
        ).pack(
            side="left",
            padx=5
        )

    if usuario_logado["tipo"] == "administrador":

        tk.Button(
            info_usuario,
            text="👑 ADMIN",
            command=abrir_painel_admin,
            bg="#6c2bd9",
            fg=COR_BRANCO,
            relief="flat",
            cursor="hand2",
            font=("Arial", 8, "bold")
        ).pack(
            side="left",
            padx=5
        )

    relogio = tk.Label(
        topo,
        text="",
        font=("Arial", 8),
        bg="#0b0b0b",
        fg=COR_CINZA
    )

    relogio.pack(
        side="right",
        padx=10
    )

    # ========================================================
    # RELOGIO
    # ========================================================

    def atualizar_relogio():

        relogio.config(
            text=datetime.now().strftime(
                "%d/%m/%Y  •  %H:%M:%S"
            )
        )

        janela.after(
            1000,
            atualizar_relogio
        )

    # ========================================================
    # CORPO
    # ========================================================

    principal = tk.Frame(
        janela,
        bg=COR_FUNDO
    )

    principal.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # ========================================================
    # LADO ESQUERDO
    # ========================================================

    esquerda = tk.Frame(
        principal,
        bg=COR_FUNDO,
        width=570
    )

    esquerda.pack(
        side="left",
        fill="both",
        expand=True
    )

    tk.Label(
        esquerda,
        text="🍔 Cardápio",
        font=("Arial", 17, "bold"),
        bg=COR_FUNDO,
        fg=COR_BRANCO
    ).pack(
        anchor="w",
        pady=(0, 5)
    )

    canvas = tk.Canvas(
        esquerda,
        bg=COR_FUNDO,
        highlightthickness=0
    )

    scrollbar_produtos = ttk.Scrollbar(
        esquerda,
        orient="vertical",
        command=canvas.yview
    )

    area_produtos = tk.Frame(
        canvas,
        bg=COR_FUNDO
    )

    area_produtos.bind(
        "<Configure>",
        lambda event:
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=area_produtos,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar_produtos.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar_produtos.pack(
        side="right",
        fill="y"
    )

    # ========================================================
    # CARDS
    # ========================================================

    for indice, (produto, dados) in enumerate(
        CARDAPIO.items()
    ):

        linha = indice // 2
        coluna = indice % 2

        card = tk.Frame(
            area_produtos,
            bg=COR_CARD,
            width=260,
            height=105
        )

        card.grid(
            row=linha,
            column=coluna,
            padx=5,
            pady=5
        )

        card.grid_propagate(False)

        tk.Label(
            card,
            text=produto,
            font=("Arial", 11, "bold"),
            bg=COR_CARD,
            fg=COR_BRANCO
        ).pack(
            anchor="w",
            padx=12,
            pady=(10, 2)
        )

        tk.Label(
            card,
            text=dados["descricao"],
            font=("Arial", 8),
            bg=COR_CARD,
            fg=COR_CINZA
        ).pack(
            anchor="w",
            padx=12
        )

        rodape = tk.Frame(
            card,
            bg=COR_CARD
        )

        rodape.pack(
            fill="x",
            padx=12,
            pady=7
        )

        tk.Label(
            rodape,
            text=formatar_real(
                dados["preco"]
            ),
            font=("Arial", 11, "bold"),
            bg=COR_CARD,
            fg=COR_VERMELHO
        ).pack(
            side="left"
        )

        tk.Button(
            rodape,
            text="+ ADICIONAR",
            command=lambda p=produto:
            adicionar_produto(p),
            bg=COR_VERMELHO,
            fg=COR_BRANCO,
            activebackground=COR_VERMELHO_ESCURO,
            relief="flat",
            cursor="hand2",
            font=("Arial", 8, "bold")
        ).pack(
            side="right"
        )

    # ========================================================
    # LADO DIREITO
    # ========================================================

    direita = tk.Frame(
        principal,
        bg=COR_CARD,
        width=295
    )

    direita.pack(
        side="right",
        fill="y",
        padx=(10, 0)
    )

    direita.pack_propagate(
        False
    )

    tk.Label(
        direita,
        text="🛒 Seu Pedido",
        font=("Arial", 17, "bold"),
        bg=COR_CARD,
        fg=COR_BRANCO
    ).pack(
        anchor="w",
        padx=15,
        pady=(15, 8)
    )

    colunas = (
        "Produto",
        "Qtd",
        "Total"
    )

    tabela = ttk.Treeview(
        direita,
        columns=colunas,
        show="headings",
        height=8
    )

    tabela.heading(
        "Produto",
        text="Produto"
    )

    tabela.heading(
        "Qtd",
        text="Qtd"
    )

    tabela.heading(
        "Total",
        text="Total"
    )

    tabela.column(
        "Produto",
        width=125
    )

    tabela.column(
        "Qtd",
        width=35,
        anchor="center"
    )

    tabela.column(
        "Total",
        width=70,
        anchor="e"
    )

    tabela.pack(
        fill="x",
        padx=15
    )

    tk.Button(
        direita,
        text="🗑 Remover item",
        command=remover_item,
        bg="#333333",
        fg=COR_BRANCO,
        activebackground="#444444",
        relief="flat",
        cursor="hand2",
        font=("Arial", 8, "bold")
    ).pack(
        fill="x",
        padx=15,
        pady=6,
        ipady=5
    )

    tk.Frame(
        direita,
        bg="#333333",
        height=1
    ).pack(
        fill="x",
        padx=15,
        pady=3
    )

    subtotal_label = tk.Label(
        direita,
        text="Subtotal: R$ 0,00",
        font=("Arial", 9),
        bg=COR_CARD,
        fg=COR_CINZA
    )

    subtotal_label.pack(
        anchor="w",
        padx=15,
        pady=2
    )

    desconto_label = tk.Label(
        direita,
        text="Desconto: R$ 0,00",
        font=("Arial", 9),
        bg=COR_CARD,
        fg=COR_CINZA
    )

    desconto_label.pack(
        anchor="w",
        padx=15,
        pady=2
    )

    total_label = tk.Label(
        direita,
        text="TOTAL: R$ 0,00",
        font=("Arial", 14, "bold"),
        bg=COR_CARD,
        fg=COR_VERMELHO
    )

    total_label.pack(
        anchor="w",
        padx=15,
        pady=(4, 8)
    )

    tk.Label(
        direita,
        text="Na próxima tela você verá as imagens\n"
             "dos produtos e informará os dados.",
        font=("Arial", 8),
        justify="left",
        bg=COR_CARD,
        fg=COR_CINZA
    ).pack(
        anchor="w",
        padx=15,
        pady=(0, 8)
    )

    tk.Button(
        direita,
        text="✓ FINALIZAR COMPRA",
        command=abrir_checkout,
        bg=COR_VERMELHO,
        fg=COR_BRANCO,
        activebackground=COR_VERMELHO_ESCURO,
        relief="flat",
        cursor="hand2",
        font=("Arial", 10, "bold")
    ).pack(
        fill="x",
        padx=15,
        ipady=9
    )

    tk.Button(
        direita,
        text="＋ NOVO PEDIDO",
        command=limpar_pedido,
        bg="#333333",
        fg=COR_BRANCO,
        activebackground="#444444",
        relief="flat",
        cursor="hand2",
        font=("Arial", 9, "bold")
    ).pack(
        fill="x",
        padx=15,
        pady=7,
        ipady=6
    )

    atualizar_carrinho()
    atualizar_relogio()

    janela.mainloop()


# ============================================================
# TELA DE LOGIN
# ============================================================

def iniciar_login():

    global janela_login
    global entrada_login_email
    global entrada_login_senha

    janela_login = tk.Tk()

    janela_login.title(
        "Login - Chapa Quente"
    )

    janela_login.geometry(
        "430x500"
    )

    janela_login.resizable(
        False,
        False
    )

    janela_login.configure(
        bg=COR_FUNDO
    )

    # ========================================================
    # TITULO
    # ========================================================

    tk.Label(
        janela_login,
        text="🍔",
        font=("Arial", 45),
        bg=COR_FUNDO,
        fg=COR_VERMELHO
    ).pack(
        pady=(35, 0)
    )

    tk.Label(
        janela_login,
        text="CHAPA QUENTE",
        font=("Arial", 24, "bold"),
        bg=COR_FUNDO,
        fg=COR_BRANCO
    ).pack()

    tk.Label(
        janela_login,
        text="HAMBURGUERIA",
        font=("Arial", 10, "bold"),
        bg=COR_FUNDO,
        fg=COR_VERMELHO
    ).pack(
        pady=(0, 25)
    )

    # ========================================================
    # EMAIL
    # ========================================================

    tk.Label(
        janela_login,
        text="E-mail",
        font=("Arial", 9, "bold"),
        bg=COR_FUNDO,
        fg=COR_CINZA
    ).pack(
        anchor="w",
        padx=55
    )

    entrada_login_email = tk.Entry(
        janela_login,
        font=("Arial", 11),
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat"
    )

    entrada_login_email.pack(
        fill="x",
        padx=55,
        pady=(5, 15),
        ipady=8
    )

    # ========================================================
    # SENHA
    # ========================================================

    tk.Label(
        janela_login,
        text="Senha",
        font=("Arial", 9, "bold"),
        bg=COR_FUNDO,
        fg=COR_CINZA
    ).pack(
        anchor="w",
        padx=55
    )

    entrada_login_senha = tk.Entry(
        janela_login,
        font=("Arial", 11),
        show="*",
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        insertbackground=COR_BRANCO,
        relief="flat"
    )

    entrada_login_senha.pack(
        fill="x",
        padx=55,
        pady=(5, 20),
        ipady=8
    )

    # ========================================================
    # ENTRAR
    # ========================================================

    tk.Button(
        janela_login,
        text="ENTRAR",
        command=realizar_login,
        bg=COR_VERMELHO,
        fg=COR_BRANCO,
        activebackground=COR_VERMELHO_ESCURO,
        activeforeground=COR_BRANCO,
        relief="flat",
        cursor="hand2",
        font=("Arial", 10, "bold")
    ).pack(
        fill="x",
        padx=55,
        ipady=9
    )

    # ========================================================
    # CADASTRO
    # ========================================================

    tk.Button(
        janela_login,
        text="CRIAR NOVA CONTA",
        command=abrir_cadastro,
        bg=COR_CARD_2,
        fg=COR_BRANCO,
        activebackground="#333333",
        relief="flat",
        cursor="hand2",
        font=("Arial", 9, "bold")
    ).pack(
        fill="x",
        padx=55,
        pady=10,
        ipady=8
    )

    tk.Label(
        janela_login,
        text="Você pode criar uma conta de cliente ou administrador.\n"
             "A conta de administrador exige o código administrativo.",
        font=("Arial", 8),
        bg=COR_FUNDO,
        fg=COR_CINZA,
        justify="center"
    ).pack(
        pady=5
    )

    janela_login.bind(
        "<Return>",
        lambda event: realizar_login()
    )

    entrada_login_email.focus()

    janela_login.mainloop()


# ============================================================
# INICIAR PROGRAMA
# ============================================================

iniciar_login()