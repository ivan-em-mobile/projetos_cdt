import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import random
import sqlite3
import csv
import os
import sys

# =========================
# PYINSTALLER / CAMINHO
# =========================

def caminho_arquivo(nome):
    if getattr(sys, 'frozen', False):
        pasta = os.path.dirname(sys.executable)
    else:
        pasta = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(pasta, nome)

db_path = caminho_arquivo("pontoplay.db")

# =========================
# BANCO DE DADOS
# =========================

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    telefone TEXT,
    email TEXT,
    senha TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS estatisticas (
    id INTEGER PRIMARY KEY,
    acessos INTEGER,
    partidas INTEGER,
    jackpots INTEGER,
    arrecadado INTEGER
)
""")

cursor.execute("""
INSERT OR IGNORE INTO estatisticas
(id, acessos, partidas, jackpots, arrecadado)
VALUES (1,0,0,0,0)
""")

conn.commit()

# =========================
# CONFIGURAÇÕES
# =========================

SIMBOLOS = ['💰', '💲', '🔝', '🎲', '💣', '🔞', '💸']

credits = 100

ADM_EMAIL = "admin@pontoplay.com"
ADM_SENHA = "123456"

usuario_atual = ""

# =========================
# CORES
# =========================

PRETO = "#0d0d0d"
AZUL = "#025487"
BRANCO = "white"
CINZA = "#1a1a1a"
VERDE = "#00ff99"

# =========================
# EXPORTAR CSV
# =========================

def exportar_usuarios():

    cursor.execute("""
    SELECT nome, telefone, email
    FROM usuarios
    """)

    usuarios = cursor.fetchall()

    if not usuarios:
        messagebox.showwarning(
            "Aviso",
            "Nenhum usuário cadastrado!"
        )
        return

    caminho = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Arquivo CSV", "*.csv")],
        title="Salvar usuários"
    )

    if not caminho:
        return

    with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:

        writer = csv.writer(arquivo)

        writer.writerow([
            "Nome",
            "Telefone",
            "Email"
        ])

        for usuario in usuarios:
            writer.writerow(usuario)

    messagebox.showinfo(
        "Sucesso",
        "Usuários exportados com sucesso!"
    )

# =========================
# FUNÇÕES
# =========================

def atualizar_creditos():
    label_creditos.config(text=f"💰 CRÉDITOS: {credits}")

# =========================
# PAINEL ADMIN
# =========================

def abrir_painel_admin():

    painel = tk.Toplevel(janela)
    painel.title("PAINEL ADM")
    painel.geometry("500x600")
    painel.config(bg=PRETO)

    cursor.execute("SELECT * FROM estatisticas WHERE id=1")
    stats = cursor.fetchone()

    acessos = stats[1]
    partidas = stats[2]
    jackpots = stats[3]
    arrecadado = stats[4]

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]

    titulo = tk.Label(
        painel,
        text="👑 PAINEL ADMINISTRADOR",
        font=("Arial Black", 24, "bold"),
        bg=PRETO,
        fg=BRANCO
    )

    titulo.pack(pady=30)

    infos = [
        f"👥 Usuários cadastrados: {total_usuarios}",
        f"📈 Acessos ao sistema: {acessos}",
        f"🎲 Partidas jogadas: {partidas}",
        f"🏆 Jackpots: {jackpots}",
        f"💸 Créditos arrecadados: {arrecadado}"
    ]

    for info in infos:
        tk.Label(
            painel,
            text=info,
            font=("Arial", 16, "bold"),
            bg=PRETO,
            fg=BRANCO
        ).pack(pady=12)

    btn_exportar = tk.Button(
        painel,
        text="📁 EXPORTAR USUÁRIOS",
        command=exportar_usuarios,
        bg=AZUL,
        fg="black",
        font=("Arial Black", 14, "bold"),
        relief="flat",
        cursor="hand2",
        width=25,
        height=2
    )

    btn_exportar.pack(pady=30)

# =========================
# PLACEHOLDERS
# =========================

def limpar_placeholder(event, entry, texto):
    if entry.get() == texto:
        entry.delete(0, tk.END)
        entry.config(fg=BRANCO)

def restaurar_placeholder(event, entry, texto):
    if entry.get() == "":
        entry.insert(0, texto)
        entry.config(fg="gray")

def limpar_placeholder_senha(event):
    if entry_senha.get() == "Senha":
        entry_senha.delete(0, tk.END)
        entry_senha.config(fg=BRANCO, show="*")

def restaurar_placeholder_senha(event):
    if entry_senha.get() == "":
        entry_senha.config(show="")
        entry_senha.insert(0, "Senha")
        entry_senha.config(fg="gray")

# =========================
# CADASTRO
# =========================

def cadastrar():

    global usuario_atual

    nome = entry_nome.get()
    telefone = entry_telefone.get()
    email = entry_email.get()
    senha = entry_senha.get()

    if not nome or nome == "Nome" or \
       not telefone or telefone == "Telefone" or \
       not email or email == "E-mail" or \
       not senha or senha == "Senha":

        messagebox.showwarning(
            "Erro",
            "Preencha todos os campos!"
        )
        return

    if email == ADM_EMAIL and senha == ADM_SENHA:
        abrir_painel_admin()
        return

    cursor.execute("""
    INSERT INTO usuarios
    (nome, telefone, email, senha)
    VALUES (?, ?, ?, ?)
    """, (nome, telefone, email, senha))

    conn.commit()

    usuario_atual = nome

    cursor.execute("""
    UPDATE estatisticas
    SET acessos = acessos + 1
    WHERE id=1
    """)

    conn.commit()

    usuario_label.config(text=f"👤 {usuario_atual}")

    messagebox.showinfo(
        "Sucesso",
        f"Bem-vindo {nome}!"
    )

    tela_cadastro.pack_forget()
    tela_jogo.pack(fill="both", expand=True)

# =========================
# HOVER
# =========================

def hover_entrar(e):
    btn_girar['bg'] = VERDE

def hover_sair(e):
    btn_girar['bg'] = AZUL

# =========================
# GIRAR SLOT
# =========================

def girar():

    global credits

    if credits < 10:
        messagebox.showwarning(
            "Erro",
            "❌ Sem créditos!"
        )
        return

    credits -= 10

    for i in range(25):

        label1.config(text=random.choice(SIMBOLOS))
        label2.config(text=random.choice(SIMBOLOS))
        label3.config(text=random.choice(SIMBOLOS))

        janela.update()
        janela.after(60)

    resultado = [random.choice(SIMBOLOS) for _ in range(3)]

    label1.config(text=resultado[0])
    label2.config(text=resultado[1])
    label3.config(text=resultado[2])

    cursor.execute("""
    UPDATE estatisticas
    SET partidas = partidas + 1,
        arrecadado = arrecadado + 10
    WHERE id=1
    """)

    if resultado[0] == resultado[1] == resultado[2]:

        credits += 100

        cursor.execute("""
        UPDATE estatisticas
        SET jackpots = jackpots + 1
        WHERE id=1
        """)

        status.config(
            text="🎉 JACKPOT +100",
            fg=VERDE
        )

    elif (
        resultado[0] == resultado[1]
        or resultado[0] == resultado[2]
        or resultado[1] == resultado[2]
    ):

        credits += 30

        status.config(
            text="🔥 DOIS IGUAIS +30",
            fg=AZUL
        )

    else:

        status.config(
            text="❌ VOCÊ PERDEU",
            fg="red"
        )

    conn.commit()

    atualizar_creditos()

# =========================
# JANELA
# =========================

janela = tk.Tk()

janela.title("🎰 PONTOPLAY FORTUNE")
janela.geometry("1200x800")
janela.config(bg=PRETO)

# =========================
# LOGIN
# =========================

tela_cadastro = tk.Frame(janela, bg=PRETO)
tela_cadastro.pack(fill="both", expand=True)

titulo = tk.Label(
    tela_cadastro,
    text="🎰 PONTOPLAY FORTUNE 🎰",
    font=("Arial Black", 38, "bold"),
    bg=PRETO,
    fg=BRANCO
)

titulo.pack(pady=40)

def criar_entry(texto):

    entry = tk.Entry(
        tela_cadastro,
        width=35,
        font=("Arial", 18),
        bg=CINZA,
        fg="gray",
        insertbackground=BRANCO,
        relief="flat",
        justify="center"
    )

    entry.pack(pady=12, ipady=10)

    entry.insert(0, texto)

    entry.bind(
        "<FocusIn>",
        lambda e: limpar_placeholder(e, entry, texto)
    )

    entry.bind(
        "<FocusOut>",
        lambda e: restaurar_placeholder(e, entry, texto)
    )

    return entry

entry_nome = criar_entry("Nome")
entry_telefone = criar_entry("Telefone")
entry_email = criar_entry("E-mail")

entry_senha = tk.Entry(
    tela_cadastro,
    width=35,
    font=("Arial", 18),
    bg=CINZA,
    fg="gray",
    insertbackground=BRANCO,
    relief="flat",
    justify="center",
    show=""
)

entry_senha.pack(pady=12, ipady=10)

entry_senha.insert(0, "Senha")

entry_senha.bind("<FocusIn>", limpar_placeholder_senha)
entry_senha.bind("<FocusOut>", restaurar_placeholder_senha)

btn_cadastro = tk.Button(
    tela_cadastro,
    text="🎲 ENTRAR",
    command=cadastrar,
    bg=AZUL,
    fg="black",
    font=("Arial Black", 18, "bold"),
    width=20,
    height=2,
    relief="flat",
    cursor="hand2"
)

btn_cadastro.pack(pady=30)

# =========================
# JOGO
# =========================

tela_jogo = tk.Frame(janela, bg=PRETO)

menu_topo = tk.Frame(
    tela_jogo,
    bg=CINZA,
    height=70
)

menu_topo.pack(fill="x")

usuario_label = tk.Label(
    menu_topo,
    text="👤 Jogador",
    font=("Arial", 16, "bold"),
    bg=CINZA,
    fg=BRANCO
)

usuario_label.pack(side="left", padx=20)

titulo_jogo = tk.Label(
    tela_jogo,
    text="🎰 SLOT MACHINE 🎰",
    font=("Arial Black", 32, "bold"),
    bg=PRETO,
    fg=BRANCO
)

titulo_jogo.pack(pady=30)

frame_slots = tk.Frame(
    tela_jogo,
    bg=PRETO
)

frame_slots.pack(pady=40)

def criar_slot(coluna):

    label = tk.Label(
        frame_slots,
        text="❔",
        font=("Arial", 100, "bold"),
        bg=CINZA,
        fg=BRANCO,
        width=2,
        height=1,
        relief="solid",
        bd=4
    )

    label.grid(row=0, column=coluna, padx=15)

    return label

label1 = criar_slot(0)
label2 = criar_slot(1)
label3 = criar_slot(2)

btn_girar = tk.Button(
    tela_jogo,
    text="🎲 GIRAR",
    command=girar,
    font=("Arial Black", 22, "bold"),
    bg=AZUL,
    fg="black",
    width=20,
    height=2,
    relief="flat",
    cursor="hand2"
)

btn_girar.pack(pady=30)

btn_girar.bind("<Enter>", hover_entrar)
btn_girar.bind("<Leave>", hover_sair)

status = tk.Label(
    tela_jogo,
    text="🔥 Boa sorte!",
    font=("Arial", 20, "bold"),
    bg=PRETO,
    fg=BRANCO
)

status.pack(pady=15)

label_creditos = tk.Label(
    tela_jogo,
    text=f"💰 CRÉDITOS: {credits}",
    font=("Arial Black", 28, "bold"),
    bg=PRETO,
    fg=BRANCO
)

label_creditos.pack(pady=20)

# =========================
# FECHAR APP
# =========================

def fechar_programa():
    conn.close()
    janela.destroy()

janela.protocol("WM_DELETE_WINDOW", fechar_programa)

# =========================
# INICIAR
# =========================

janela.mainloop()