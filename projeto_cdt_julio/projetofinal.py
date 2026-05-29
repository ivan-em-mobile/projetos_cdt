# RPG SYSTEM COMPLETO ATUALIZADO


import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ==========================================
# BANCO DE DADOS
# ==========================================

conexao = sqlite3.connect("rpg_system.db")
cursor = conexao.cursor()

# PERSONAGENS
cursor.execute("""
CREATE TABLE IF NOT EXISTS personagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    classe TEXT
)
""")

# NPCS
cursor.execute("""
CREATE TABLE IF NOT EXISTS npcs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    funcao TEXT
)
""")

# CAMPANHAS
cursor.execute("""
CREATE TABLE IF NOT EXISTS campanhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    historia TEXT
)
""")

# SESSÕES
cursor.execute("""
CREATE TABLE IF NOT EXISTS sessoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campanha_id INTEGER,
    descricao TEXT
)
""")

conexao.commit()

# ==========================================
# JANELA
# ==========================================

janela = tk.Tk()
janela.title("RPG SYSTEM")
janela.geometry("1400x800")
janela.config(bg="#0f172a")

# ==========================================
# CORES
# ==========================================

FUNDO = "#0f172a"
MENU = "#111827"
ROXO = "#6d28d9"
ROXO_CLARO = "#c084fc"
VERMELHO = "#dc2626"
TEXTO = "white"

# ==========================================
# FRAME PRINCIPAL
# ==========================================

frame_principal = tk.Frame(janela, bg=FUNDO)
frame_principal.pack(fill="both", expand=True)

# MENU
menu_lateral = tk.Frame(frame_principal, bg=MENU, width=250)
menu_lateral.pack(side="left", fill="y")

# ÁREA
area = tk.Frame(frame_principal, bg=FUNDO)
area.pack(side="right", fill="both", expand=True)

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def limpar_area():
    for widget in area.winfo_children():
        widget.destroy()


def titulo(texto):
    tk.Label(
        area,
        text=texto,
        font=("Arial", 24, "bold"),
        bg=FUNDO,
        fg=ROXO_CLARO
    ).pack(pady=20)

# ==========================================
# PERSONAGENS
# ==========================================

def tela_personagens():

    limpar_area()
    titulo("PERSONAGENS")

    tabela = ttk.Treeview(
        area,
        columns=("ID", "Nome", "Classe"),
        show="headings",
        height=20
    )

    tabela.heading("ID", text="ID")
    tabela.heading("Nome", text="Nome")
    tabela.heading("Classe", text="Classe")

    tabela.column("ID", width=50)
    tabela.column("Nome", width=250)
    tabela.column("Classe", width=200)

    tabela.pack(pady=20, fill="x")

    cursor.execute("SELECT * FROM personagens")

    for personagem in cursor.fetchall():
        tabela.insert("", tk.END, values=personagem)


def criar_personagem():

    limpar_area()
    titulo("CRIAR PERSONAGEM")

    frame = tk.Frame(area, bg=FUNDO)
    frame.pack(pady=20)

    tk.Label(frame, text="Nome", bg=FUNDO, fg=TEXTO).grid(row=0, column=0, pady=10)

    entry_nome = tk.Entry(frame, width=30)
    entry_nome.grid(row=0, column=1)

    tk.Label(frame, text="Classe", bg=FUNDO, fg=TEXTO).grid(row=1, column=0, pady=10)

    combo = ttk.Combobox(
        frame,
        values=["Mago", "Guerreiro", "Ladino", "Arqueiro", "Clérigo"],
        width=27
    )

    combo.grid(row=1, column=1)
    combo.current(0)

    def salvar():

        nome = entry_nome.get()
        classe = combo.get()

        if nome == "":
            messagebox.showwarning("Erro", "Digite um nome!")
            return

        cursor.execute(
            "INSERT INTO personagens(nome, classe) VALUES (?, ?)",
            (nome, classe)
        )

        conexao.commit()

        messagebox.showinfo("Sucesso", "Personagem criado!")

        tela_personagens()

    tk.Button(
        area,
        text="CRIAR PERSONAGEM",
        command=salvar,
        bg=ROXO,
        fg="white",
        font=("Arial", 12, "bold"),
        width=25,
        height=2,
        bd=0
    ).pack(pady=20)

# ==========================================
# ALTERAR PERSONAGEM
# ==========================================

def alterar_personagem():

    limpar_area()
    titulo("ALTERAR PERSONAGEM")

    frame = tk.Frame(area, bg=FUNDO)
    frame.pack(pady=20)

    tk.Label(frame, text="ID", bg=FUNDO, fg=TEXTO).grid(row=0, column=0, pady=10)

    entry_id = tk.Entry(frame)
    entry_id.grid(row=0, column=1)

    tk.Label(frame, text="Novo Nome", bg=FUNDO, fg=TEXTO).grid(row=1, column=0, pady=10)

    entry_nome = tk.Entry(frame)
    entry_nome.grid(row=1, column=1)

    tk.Label(frame, text="Nova Classe", bg=FUNDO, fg=TEXTO).grid(row=2, column=0, pady=10)

    combo = ttk.Combobox(
        frame,
        values=["Mago", "Guerreiro", "Ladino", "Arqueiro", "Clérigo"]
    )

    combo.grid(row=2, column=1)
    combo.current(0)

    def alterar():

        cursor.execute(
            "UPDATE personagens SET nome = ?, classe = ? WHERE id = ?",
            (
                entry_nome.get(),
                combo.get(),
                entry_id.get()
            )
        )

        conexao.commit()

        messagebox.showinfo("Sucesso", "Personagem alterado!")

        tela_personagens()

    tk.Button(
        area,
        text="ALTERAR",
        command=alterar,
        bg=ROXO,
        fg="white",
        width=20,
        height=2,
        bd=0
    ).pack(pady=20)

# ==========================================
# EXCLUIR PERSONAGEM
# ==========================================

def excluir_personagem():

    limpar_area()
    titulo("EXCLUIR PERSONAGEM")

    frame = tk.Frame(area, bg=FUNDO)
    frame.pack(pady=20)

    tk.Label(frame, text="ID", bg=FUNDO, fg=TEXTO).pack(pady=10)

    entry = tk.Entry(frame)
    entry.pack(pady=10)

    def excluir():

        personagem_id = entry.get()

        if personagem_id == "":
            messagebox.showwarning("Erro", "Digite um ID!")
            return

        cursor.execute(
            "DELETE FROM personagens WHERE id = ?",
            (personagem_id,)
        )

        conexao.commit()

        messagebox.showinfo("Sucesso", "Personagem excluído!")

        tela_personagens()

    tk.Button(
        frame,
        text="EXCLUIR",
        command=excluir,
        bg=VERMELHO,
        fg="white",
        width=20,
        height=2,
        bd=0
    ).pack(pady=20)

# ==========================================
# NPCS
# ==========================================

def tela_npcs():

    limpar_area()
    titulo("NPCS")

    tabela = ttk.Treeview(
        area,
        columns=("ID", "Nome", "Função"),
        show="headings",
        height=20
    )

    tabela.heading("ID", text="ID")
    tabela.heading("Nome", text="Nome")
    tabela.heading("Função", text="Função")

    tabela.column("ID", width=50)
    tabela.column("Nome", width=250)
    tabela.column("Função", width=300)

    tabela.pack(pady=20, fill="x")

    cursor.execute("SELECT * FROM npcs")

    for npc in cursor.fetchall():
        tabela.insert("", tk.END, values=npc)


def criar_npc():

    limpar_area()
    titulo("CRIAR NPC")

    frame = tk.Frame(area, bg=FUNDO)
    frame.pack(pady=20)

    tk.Label(frame, text="Nome", bg=FUNDO, fg=TEXTO).grid(row=0, column=0, pady=10)

    entry_nome = tk.Entry(frame, width=30)
    entry_nome.grid(row=0, column=1)

    tk.Label(frame, text="Função", bg=FUNDO, fg=TEXTO).grid(row=1, column=0, pady=10)

    entry_funcao = tk.Entry(frame, width=30)
    entry_funcao.grid(row=1, column=1)

    def salvar():

        cursor.execute(
            "INSERT INTO npcs(nome, funcao) VALUES (?, ?)",
            (entry_nome.get(), entry_funcao.get())
        )

        conexao.commit()

        messagebox.showinfo("Sucesso", "NPC criado!")

        tela_npcs()

    tk.Button(
        area,
        text="CRIAR NPC",
        command=salvar,
        bg=ROXO,
        fg="white",
        width=20,
        height=2,
        bd=0
    ).pack(pady=20)

# ==========================================
# CAMPANHAS
# ==========================================

def tela_campanhas():

    limpar_area()
    titulo("CAMPANHAS")

    frame_principal = tk.Frame(area, bg=FUNDO)
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

    # LISTA DE CAMPANHAS

    frame_lista = tk.Frame(frame_principal, bg=MENU)
    frame_lista.pack(side="left", fill="y", padx=10)

    tk.Label(
        frame_lista,
        text="Campanhas",
        bg=MENU,
        fg=ROXO_CLARO,
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    lista_campanhas = tk.Listbox(
        frame_lista,
        width=30,
        height=25,
        bg="#1e293b",
        fg="white",
        font=("Arial", 11),
        selectbackground=ROXO,
        bd=0
    )

    lista_campanhas.pack(padx=10, pady=10)

    # DETALHES

    frame_detalhes = tk.Frame(frame_principal, bg=FUNDO)
    frame_detalhes.pack(side="right", fill="both", expand=True)

    titulo_nome = tk.Label(
        frame_detalhes,
        text="Selecione uma campanha",
        bg=FUNDO,
        fg=ROXO_CLARO,
        font=("Arial", 20, "bold")
    )

    titulo_nome.pack(pady=10)

    texto_historia = tk.Text(
        frame_detalhes,
        wrap="word",
        font=("Arial", 11),
        bg="#1e293b",
        fg="white",
        height=15
    )

    texto_historia.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(texto_historia)
    scrollbar.pack(side="right", fill="y")

    texto_historia.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=texto_historia.yview)

    # SESSÕES

    tk.Label(
        frame_detalhes,
        text="Sessões da Campanha",
        bg=FUNDO,
        fg=ROXO_CLARO,
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    lista_sessoes = tk.Listbox(
        frame_detalhes,
        height=8,
        bg="#111827",
        fg="white",
        font=("Arial", 10),
        selectbackground=ROXO,
        bd=0
    )

    lista_sessoes.pack(fill="x", padx=10, pady=10)

    # CARREGAR CAMPANHAS

    cursor.execute("SELECT * FROM campanhas")
    campanhas = cursor.fetchall()

    dados_campanhas = {}

    for campanha in campanhas:

        campanha_id = campanha[0]
        nome = campanha[1]
        historia = campanha[2]

        dados_campanhas[nome] = {
            "id": campanha_id,
            "historia": historia
        }

        lista_campanhas.insert(tk.END, nome)

    # MOSTRAR CAMPANHA

    def mostrar_campanha(event):

        selecao = lista_campanhas.curselection()

        if not selecao:
            return

        nome_campanha = lista_campanhas.get(selecao)

        campanha = dados_campanhas[nome_campanha]

        titulo_nome.config(text=nome_campanha)

        texto_historia.delete("1.0", tk.END)
        texto_historia.insert(tk.END, campanha["historia"])

        lista_sessoes.delete(0, tk.END)

        cursor.execute(
            "SELECT descricao FROM sessoes WHERE campanha_id = ?",
            (campanha["id"],)
        )

        sessoes = cursor.fetchall()

        if len(sessoes) == 0:
            lista_sessoes.insert(tk.END, "Nenhuma sessão encontrada")

        else:
            for numero, sessao in enumerate(sessoes, start=1):

                texto = sessao[0].split("\n")[0][:60]

                lista_sessoes.insert(
                    tk.END,
                    f"Sessão {numero} - {texto}"
                )

    lista_campanhas.bind("<<ListboxSelect>>", mostrar_campanha)


def criar_campanha():

    limpar_area()
    titulo("CRIAR CAMPANHA")

    frame = tk.Frame(area, bg=FUNDO)
    frame.pack(pady=20)

    tk.Label(frame, text="Nome", bg=FUNDO, fg=TEXTO).grid(row=0, column=0, pady=10)

    entry_nome = tk.Entry(frame, width=40)
    entry_nome.grid(row=0, column=1)

    tk.Label(frame, text="História", bg=FUNDO, fg=TEXTO).grid(row=1, column=0, pady=10)

    entry_historia = tk.Text(
        frame,
        width=70,
        height=15,
        font=("Arial", 11),
        wrap="word"
    )

    entry_historia.grid(row=1, column=1, pady=10)

    scrollbar = tk.Scrollbar(frame, command=entry_historia.yview)
    scrollbar.grid(row=1, column=2, sticky="ns")

    entry_historia.config(yscrollcommand=scrollbar.set)

    def salvar():

        historia = entry_historia.get("1.0", tk.END)

        cursor.execute(
            "INSERT INTO campanhas(nome, historia) VALUES (?, ?)",
            (entry_nome.get(), historia)
        )

        conexao.commit()

        messagebox.showinfo("Sucesso", "Campanha criada!")

        tela_campanhas()

    tk.Button(
        area,
        text="CRIAR CAMPANHA",
        command=salvar,
        bg=ROXO,
        fg="white",
        width=25,
        height=2,
        bd=0
    ).pack(pady=20)

# ==========================================
# EXCLUIR CAMPANHA
# ==========================================

def excluir_campanha():

    limpar_area()
    titulo("EXCLUIR CAMPANHA")

    frame = tk.Frame(area, bg=FUNDO)
    frame.pack(pady=30)

    tk.Label(
        frame,
        text="ID da Campanha",
        bg=FUNDO,
        fg=TEXTO,
        font=("Arial", 12)
    ).pack(pady=10)

    entry_id = tk.Entry(frame, width=20)
    entry_id.pack(pady=10)

    def excluir():

        campanha_id = entry_id.get()

        if campanha_id == "":
            messagebox.showwarning("Erro", "Digite um ID!")
            return

        # EXCLUIR SESSÕES DA CAMPANHA
        cursor.execute(
            "DELETE FROM sessoes WHERE campanha_id = ?",
            (campanha_id,)
        )

        # EXCLUIR CAMPANHA
        cursor.execute(
            "DELETE FROM campanhas WHERE id = ?",
            (campanha_id,)
        )

        conexao.commit()

        messagebox.showinfo("Sucesso", "Campanha excluída!")

        tela_campanhas()

    tk.Button(
        frame,
        text="EXCLUIR CAMPANHA",
        command=excluir,
        bg=VERMELHO,
        fg="white",
        width=25,
        height=2,
        bd=0
    ).pack(pady=20)

# ==========================================
# EXCLUIR NPC
# ==========================================

def excluir_npc():

    limpar_area()
    titulo("EXCLUIR NPC")

    frame = tk.Frame(area, bg=FUNDO)
    frame.pack(pady=30)

    tk.Label(
        frame,
        text="ID do NPC",
        bg=FUNDO,
        fg=TEXTO,
        font=("Arial", 12)
    ).pack(pady=10)

    entry_id = tk.Entry(frame, width=20)
    entry_id.pack(pady=10)

    def excluir():

        npc_id = entry_id.get()

        if npc_id == "":
            messagebox.showwarning("Erro", "Digite um ID!")
            return

        cursor.execute(
            "DELETE FROM npcs WHERE id = ?",
            (npc_id,)
        )

        conexao.commit()

        messagebox.showinfo("Sucesso", "NPC excluído!")

        tela_npcs()

    tk.Button(
        frame,
        text="EXCLUIR NPC",
        command=excluir,
        bg=VERMELHO,
        fg="white",
        width=25,
        height=2,
        bd=0
    ).pack(pady=20)

# ==========================================
# SESSÕES
# ==========================================

def criar_sessao():

    limpar_area()
    titulo("CRIAR SESSÃO")

    frame = tk.Frame(area, bg=FUNDO)
    frame.pack(pady=20)

    tk.Label(frame, text="ID da Campanha", bg=FUNDO, fg=TEXTO).grid(row=0, column=0, pady=10)

    entry_id = tk.Entry(frame, width=20)
    entry_id.grid(row=0, column=1)

    tk.Label(frame, text="Descrição da Sessão", bg=FUNDO, fg=TEXTO).grid(row=1, column=0, pady=10)

    entry_desc = tk.Text(
        frame,
        width=70,
        height=18,
        font=("Arial", 11),
        wrap="word"
    )

    entry_desc.grid(row=1, column=1, pady=10)

    scrollbar = tk.Scrollbar(frame, command=entry_desc.yview)
    scrollbar.grid(row=1, column=2, sticky="ns")

    entry_desc.config(yscrollcommand=scrollbar.set)

    def salvar():

        descricao = entry_desc.get("1.0", tk.END)

        cursor.execute(
            "INSERT INTO sessoes(campanha_id, descricao) VALUES (?, ?)",
            (entry_id.get(), descricao)
        )

        conexao.commit()

        messagebox.showinfo("Sucesso", "Sessão criada!")

    tk.Button(
        area,
        text="CRIAR SESSÃO",
        command=salvar,
        bg=ROXO,
        fg="white",
        width=25,
        height=2,
        bd=0
    ).pack(pady=20)

# ==========================================
# ESTILO BOTÕES
# ==========================================

estilo = {
    "font": ("Arial", 11, "bold"),
    "width": 25,
    "height": 2,
    "bg": ROXO,
    "fg": "white",
    "bd": 0,
    "cursor": "hand2"
}

# ==========================================
# MENU JOGADOR
# ==========================================

tk.Label(
    menu_lateral,
    text="JOGADOR",
    bg=MENU,
    fg=ROXO_CLARO,
    font=("Arial", 14, "bold")
).pack(pady=15)

tk.Button(
    menu_lateral,
    text="Criar Personagem",
    command=criar_personagem,
    **estilo
).pack(pady=5)

tk.Button(
    menu_lateral,
    text="Ver Personagens",
    command=tela_personagens,
    **estilo
).pack(pady=5)

tk.Button(
    menu_lateral,
    text="Alterar Personagem",
    command=alterar_personagem,
    **estilo
).pack(pady=5)

tk.Button(
    menu_lateral,
    text="Excluir Personagem",
    command=excluir_personagem,
    bg=VERMELHO,
    fg="white",
    width=25,
    height=2,
    bd=0
).pack(pady=5)

# ==========================================
# MENU MESTRE
# ==========================================

tk.Label(
    menu_lateral,
    text="MESTRE",
    bg=MENU,
    fg=ROXO_CLARO,
    font=("Arial", 14, "bold")
).pack(pady=20)

tk.Button(
    menu_lateral,
    text="Criar NPC",
    command=criar_npc,
    **estilo
).pack(pady=5)

tk.Button(
    menu_lateral,
    text="Ver NPCS",
    command=tela_npcs,
    **estilo
).pack(pady=5)

tk.Button(
    menu_lateral,
    text="Excluir NPC",
    command=excluir_npc,
    bg=VERMELHO,
    fg="white",
    width=25,
    height=2,
    bd=0
).pack(pady=5)

tk.Button(
    menu_lateral,
    text="Criar Campanha",
    command=criar_campanha,
    **estilo
).pack(pady=5)

tk.Button(
    menu_lateral,
    text="Ver Campanhas",
    command=tela_campanhas,
    **estilo
).pack(pady=5)

tk.Button(
    menu_lateral,
    text="Excluir Campanha",
    command=excluir_campanha,
    bg=VERMELHO,
    fg="white",
    width=25,
    height=2,
    bd=0
).pack(pady=5)

tk.Button(
    menu_lateral,
    text="Criar Sessão",
    command=criar_sessao,
    **estilo
).pack(pady=5)

# ==========================================
# INICIAR
# ==========================================

tela_personagens()

janela.mainloop()

conexao.close()
