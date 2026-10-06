import tkinter as tk
from tkinter import messagebox
import sqlite3
import json

# ==========================================
# BANCO DE DADOS
# ==========================================

conexao = sqlite3.connect("central_tenis.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    usuario TEXT UNIQUE,
    senha TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    produto TEXT,
    preco REAL
)
""")

conexao.commit()

# ==========================================
# EXPORTAR JSON
# ==========================================

def exportar_json():

    dados = {}

    # Usuarios
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    lista_usuarios = []

    for u in usuarios:
        lista_usuarios.append({
            "id": u[0],
            "nome": u[1],
            "email": u[2],
            "usuario": u[3],
            "senha": u[4]
        })

    # Pedidos
    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()

    lista_pedidos = []

    for p in pedidos:
        lista_pedidos.append({
            "id": p[0],
            "usuario": p[1],
            "produto": p[2],
            "preco": p[3]
        })

    dados["usuarios"] = lista_usuarios
    dados["pedidos"] = lista_pedidos

    with open("backup_loja.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    messagebox.showinfo(
        "Exportação",
        "Banco de dados exportado para backup_loja.json"
    )

# ==========================================
# ESTOQUE
# ==========================================

estoque = [
    {"marca": "Nike", "modelo": "Air Max 90", "preco": 799.90},
    {"marca": "Nike", "modelo": "Jordan 1", "preco": 999.90},
    {"marca": "Adidas", "modelo": "Ultraboost", "preco": 699.90},
    {"marca": "Puma", "modelo": "RS-X", "preco": 450.00},
    {"marca": "Vans", "modelo": "Old Skool", "preco": 399.90},
    {"marca": "New Balance", "modelo": "9060", "preco": 950.00},
    {"marca": "Asics", "modelo": "Gel Kayano", "preco": 850.00},
    {"marca": "Converse", "modelo": "Chuck Taylor", "preco": 320.00},
    {"marca": "Jordan", "modelo": "Jordan 4 Retro", "preco": 1799.90},
    {"marca": "Yeezy", "modelo": "Boost 350", "preco": 2199.90},
    {"marca": "Balenciaga", "modelo": "Triple S", "preco": 4899.90},
    {"marca": "Gucci", "modelo": "Ace", "preco": 5200.00},
]

carrinho = []
usuario_logado = None

# ==========================================
# JANELA
# ==========================================

janela = tk.Tk()
janela.title("CENTRAL DOS TÊNIS")
janela.geometry("1200x700")
janela.configure(bg="#111827")

menu = tk.Frame(janela, bg="#7c3aed", width=250)
menu.pack(side="left", fill="y")

container = tk.Frame(janela, bg="#111827")
container.pack(side="right", expand=True, fill="both")

canvas = tk.Canvas(
    container,
    bg="#111827",
    highlightthickness=0
)

canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(
    container,
    orient="vertical",
    command=canvas.yview
)

scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

frame_conteudo = tk.Frame(
    canvas,
    bg="#111827"
)

canvas_window = canvas.create_window(
    (0, 0),
    window=frame_conteudo,
    anchor="n"
)

def centralizar_frame(event):
    largura_canvas = event.width
    canvas.itemconfig(canvas_window, width=largura_canvas)

canvas.bind("<Configure>", centralizar_frame)

def atualizar_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame_conteudo.bind("<Configure>", atualizar_scroll)

def rolar_mouse(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", rolar_mouse)

# ==========================================
# FUNÇÕES
# ==========================================

def limpar_tela():
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

# ==========================================
# CADASTRO
# ==========================================

def cadastrar_usuario():

    nome = entrada_nome.get()
    email = entrada_email.get()
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    if nome == "" or email == "" or usuario == "" or senha == "":
        messagebox.showwarning(
            "Aviso",
            "Preencha todos os campos!"
        )
        return

    try:

        cursor.execute("""
        INSERT INTO usuarios (nome, email, usuario, senha)
        VALUES (?, ?, ?, ?)
        """, (nome, email, usuario, senha))

        conexao.commit()

        messagebox.showinfo(
            "Sucesso",
            "Conta criada com sucesso!"
        )

        entrada_nome.delete(0, tk.END)
        entrada_email.delete(0, tk.END)
        entrada_usuario.delete(0, tk.END)
        entrada_senha.delete(0, tk.END)

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Erro",
            "Usuário já existe!"
        )

# ==========================================
# LOGIN
# ==========================================

def fazer_login():

    global usuario_logado

    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    cursor.execute("""
    SELECT * FROM usuarios
    WHERE usuario = ? AND senha = ?
    """, (usuario, senha))

    resultado = cursor.fetchone()

    if resultado:

        usuario_logado = usuario

        status_login.config(
            text=f"Logado: {resultado[1]}"
        )

        messagebox.showinfo(
            "Login",
            "Login realizado com sucesso!"
        )

    else:

        messagebox.showerror(
            "Erro",
            "Usuário ou senha incorretos!"
        )

# ==========================================
# CARRINHO
# ==========================================

def adicionar_carrinho(tenis):

    if usuario_logado is None:

        messagebox.showwarning(
            "Aviso",
            "Faça login primeiro!"
        )

        return

    carrinho.append(tenis)

    messagebox.showinfo(
        "Carrinho",
        f"{tenis['modelo']} adicionado!"
    )

# ==========================================
# FINALIZAR COMPRA
# ==========================================

def finalizar_compra():

    if len(carrinho) == 0:

        messagebox.showwarning(
            "Aviso",
            "Carrinho vazio!"
        )

        return

    total = sum(item['preco'] for item in carrinho)

    resposta = messagebox.askyesno(
        "Finalizar Compra",
        f"Total: R$ {total:.2f}\n\nDeseja finalizar?"
    )

    if resposta:

        for item in carrinho:

            cursor.execute("""
            INSERT INTO pedidos (usuario, produto, preco)
            VALUES (?, ?, ?)
            """, (
                usuario_logado,
                item['modelo'],
                item['preco']
            ))

        conexao.commit()

        carrinho.clear()

        messagebox.showinfo(
            "Compra",
            "Compra finalizada com sucesso!"
        )

        tela_carrinho()

# ==========================================
# TELA INÍCIO
# ==========================================

def tela_inicio():

    limpar_tela()

    banner = tk.Frame(
        frame_conteudo,
        bg="#1f2937",
        bd=5,
        relief="ridge"
    )

    banner.pack(
        pady=50,
        anchor="center"
    )

    titulo = tk.Label(
        banner,
        text="🔥 CENTRAL DOS TÊNIS 🔥",
        bg="#1f2937",
        fg="#22d3ee",
        font=("Arial Black", 34)
    )

    titulo.pack(pady=20)

    texto = tk.Label(
        banner,
        text="Os tênis mais exclusivos do Brasil 👟",
        bg="#1f2937",
        fg="white",
        font=("Arial", 18, "bold")
    )

    texto.pack(pady=10)

# ==========================================
# ESTOQUE
# ==========================================

def tela_estoque():

    limpar_tela()

    titulo = tk.Label(
        frame_conteudo,
        text="ESTOQUE DE TÊNIS",
        bg="#111827",
        fg="#22d3ee",
        font=("Arial Black", 24)
    )

    titulo.pack(pady=20)

    for tenis in estoque:

        card = tk.Frame(
            frame_conteudo,
            bg="#1f2937",
            bd=3,
            relief="ridge",
            width=500,
            height=180
        )

        card.pack(
            pady=10,
            anchor="center"
        )

        card.pack_propagate(False)

        nome = tk.Label(
            card,
            text=f"{tenis['marca']} - {tenis['modelo']}",
            bg="#1f2937",
            fg="white",
            font=("Arial", 16, "bold")
        )

        nome.pack(pady=10)

        preco = tk.Label(
            card,
            text=f"R$ {tenis['preco']:.2f}",
            bg="#1f2937",
            fg="#22d3ee",
            font=("Arial", 15)
        )

        preco.pack()

        botao = tk.Button(
            card,
            text="Adicionar ao Carrinho",
            command=lambda t=tenis: adicionar_carrinho(t),
            bg="#22d3ee",
            fg="#111827",
            font=("Arial", 11, "bold"),
            width=25
        )

        botao.pack(pady=15)

# ==========================================
# CARRINHO
# ==========================================

def tela_carrinho():

    limpar_tela()

    titulo = tk.Label(
        frame_conteudo,
        text="CARRINHO",
        bg="#111827",
        fg="#22d3ee",
        font=("Arial Black", 24)
    )

    titulo.pack(pady=20)

    if len(carrinho) == 0:

        vazio = tk.Label(
            frame_conteudo,
            text="Carrinho vazio!",
            bg="#111827",
            fg="white",
            font=("Arial", 15)
        )

        vazio.pack(pady=20)

    else:

        total = 0

        for tenis in carrinho:

            texto = tk.Label(
                frame_conteudo,
                text=f"{tenis['marca']} - {tenis['modelo']} | R$ {tenis['preco']:.2f}",
                bg="#111827",
                fg="white",
                font=("Arial", 13)
            )

            texto.pack(pady=5)

            total += tenis['preco']

        total_label = tk.Label(
            frame_conteudo,
            text=f"TOTAL: R$ {total:.2f}",
            bg="#111827",
            fg="#22d3ee",
            font=("Arial", 18, "bold")
        )

        total_label.pack(pady=20)

        botao_finalizar = tk.Button(
            frame_conteudo,
            text="💳 Finalizar Pedido",
            command=finalizar_compra,
            bg="#10b981",
            fg="white",
            font=("Arial", 14, "bold"),
            width=25,
            height=2
        )

        botao_finalizar.pack(pady=20)

# ==========================================
# LOGIN E CADASTRO
# ==========================================

frame_login = tk.Frame(
    menu,
    bg="#7c3aed"
)

frame_login.pack(pady=20)

label_nome = tk.Label(
    frame_login,
    text="Nome",
    bg="#7c3aed",
    fg="white",
    font=("Arial", 10, "bold")
)

label_nome.pack()

entrada_nome = tk.Entry(
    frame_login,
    width=24
)

entrada_nome.pack(pady=5)

label_email = tk.Label(
    frame_login,
    text="E-mail",
    bg="#7c3aed",
    fg="white",
    font=("Arial", 10, "bold")
)

label_email.pack()

entrada_email = tk.Entry(
    frame_login,
    width=24
)

entrada_email.pack(pady=5)

label_usuario = tk.Label(
    frame_login,
    text="Usuário",
    bg="#7c3aed",
    fg="white",
    font=("Arial", 10, "bold")
)

label_usuario.pack()

entrada_usuario = tk.Entry(
    frame_login,
    width=24
)

entrada_usuario.pack(pady=5)

label_senha = tk.Label(
    frame_login,
    text="Senha",
    bg="#7c3aed",
    fg="white",
    font=("Arial", 10, "bold")
)

label_senha.pack()

entrada_senha = tk.Entry(
    frame_login,
    show="*",
    width=24
)

entrada_senha.pack(pady=5)

botao_cadastro = tk.Button(
    frame_login,
    text="Criar Conta",
    command=cadastrar_usuario,
    bg="#22d3ee",
    fg="#111827",
    font=("Arial", 10, "bold"),
    width=20
)

botao_cadastro.pack(pady=5)

botao_login = tk.Button(
    frame_login,
    text="Entrar",
    command=fazer_login,
    bg="#22d3ee",
    fg="#111827",
    font=("Arial", 10, "bold"),
    width=20
)

botao_login.pack(pady=5)

status_login = tk.Label(
    menu,
    text="Nenhum usuário logado",
    bg="#7c3aed",
    fg="white",
    font=("Arial", 10, "bold")
)

status_login.pack(pady=15)

# ==========================================
# MENU
# ==========================================

botoes = [
    ("🏠 Início", tela_inicio),
    ("👟 Estoque", tela_estoque),
    ("🛒 Carrinho", tela_carrinho),
]

for texto, comando in botoes:

    botao = tk.Button(
        menu,
        text=texto,
        command=comando,
        bg="#22d3ee",
        fg="#111827",
        font=("Arial", 12, "bold"),
        width=22,
        height=2
    )

    botao.pack(pady=8)

# ==========================================
# BOTÃO EXPORTAR JSON
# ==========================================

botao_exportar = tk.Button(
    menu,
    text="📁 Exportar JSON",
    command=exportar_json,
    bg="#10b981",
    fg="white",
    font=("Arial", 11, "bold"),
    width=22,
    height=2
)

botao_exportar.pack(pady=20)

# ==========================================
# INICIAR
# ==========================================

tela_inicio()

janela.mainloop()

conexao.close()