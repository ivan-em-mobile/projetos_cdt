# RPG SYSTEM COMPLETO COM EXPORTAÇÃO JSON

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import json

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

FUNDO = "#1699c5"
MENU = "#4083E7"
ROXO = "#0ba2c7"
ROXO_CLARO = "#1139eb"
VERMELHO = "#dc2626"
AZUL = "#07C0EA"
TEXTO = "white"

# ==========================================
# FRAME PRINCIPAL
# ==========================================

frame_principal = tk.Frame(janela, bg=FUNDO)
frame_principal.pack(fill="both", expand=True)

menu_lateral = tk.Frame(frame_principal, bg=MENU, width=250)
menu_lateral.pack(side="left", fill="y")

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
# EXPORTAR JSON
# ==========================================

def exportar_json():

    dados = {}

    # PERSONAGENS
    cursor.execute("SELECT * FROM personagens")

    personagens = []

    for p in cursor.fetchall():
        personagens.append({
            "id": p[0],
            "nome": p[1],
            "classe": p[2]
        })

    dados["personagens"] = personagens

    # NPCS
    cursor.execute("SELECT * FROM npcs")

    npcs = []

    for n in cursor.fetchall():
        npcs.append({
            "id": n[0],
            "nome": n[1],
            "funcao": n[2]
        })

    dados["npcs"] = npcs

    # CAMPANHAS
    cursor.execute("SELECT * FROM campanhas")

    campanhas = []

    for c in cursor.fetchall():
        campanhas.append({
            "id": c[0],
            "nome": c[1],
            "historia": c[2]
        })

    dados["campanhas"] = campanhas

    # SESSÕES
    cursor.execute("SELECT * FROM sessoes")

    sessoes = []

    for s in cursor.fetchall():
        sessoes.append({
            "id": s[0],
            "campanha_id": s[1],
            "descricao": s[2]
        })

    dados["sessoes"] = sessoes

    arquivo = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Arquivo JSON", "*.json")],
        title="Salvar JSON"
    )

    if arquivo == "":
        return

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(
            dados,
            f,
            indent=4,
            ensure_ascii=False
        )

    messagebox.showinfo(
        "Sucesso",
        "Arquivo JSON exportado!"
    )

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
# CAMPANHAS
# ==========================================

def tela_campanhas():

    limpar_area()
    titulo("CAMPANHAS")

    tabela = ttk.Treeview(
        area,
        columns=("ID", "Nome"),
        show="headings",
        height=20
    )

    tabela.heading("ID", text="ID")
    tabela.heading("Nome", text="Nome")

    tabela.column("ID", width=50)
    tabela.column("Nome", width=400)

    tabela.pack(pady=20, fill="x")

    cursor.execute("SELECT id, nome FROM campanhas")

    for campanha in cursor.fetchall():
        tabela.insert("", tk.END, values=campanha)

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
        height=15
    )

    entry_historia.grid(row=1, column=1, pady=10)

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
        fg=TEXTO
    ).pack(pady=10)

    entry_id = tk.Entry(frame, width=20)
    entry_id.pack(pady=10)

    def excluir():

        campanha_id = entry_id.get()

        if campanha_id == "":
            messagebox.showwarning("Erro", "Digite um ID!")
            return

        cursor.execute(
            "DELETE FROM sessoes WHERE campanha_id = ?",
            (campanha_id,)
        )

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

    tk.Label(frame, text="Descrição", bg=FUNDO, fg=TEXTO).grid(row=1, column=0, pady=10)

    entry_desc = tk.Text(
        frame,
        width=70,
        height=15
    )

    entry_desc.grid(row=1, column=1, pady=10)

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
# EXPORTAR JSON
# ==========================================

tk.Button(
    menu_lateral,
    text="Exportar JSON",
    command=exportar_json,
    bg=AZUL,
    fg="white",
    width=25,
    height=2,
    bd=0,
    font=("Arial", 11, "bold")
).pack(pady=20)

# ==========================================
# INICIAR
# ==========================================

tela_personagens()

janela.mainloop()

conexao.close()