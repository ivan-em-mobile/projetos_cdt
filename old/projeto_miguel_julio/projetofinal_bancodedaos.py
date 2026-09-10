import sqlite3
import random
import tkinter as tk
from tkinter import ttk, messagebox

# ================= BANCO =================

conexao = sqlite3.connect('rpg_mesa.db')
cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS jogadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS personagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogador_id INTEGER,
    nome_personagem TEXT NOT NULL,
    raca TEXT NOT NULL,
    classe TEXT NOT NULL,
    nivel INTEGER,
    forca INTEGER,
    destreza INTEGER,
    inteligencia INTEGER,
    FOREIGN KEY (jogador_id) REFERENCES jogadores(id)
)
''')

conexao.commit()

# ================= FUNÇÕES =================

def criar_personagem():

    nome_jogador = entry_jogador.get()
    nome_personagem = entry_personagem.get()
    raca = combo_raca.get()
    classe = combo_classe.get()

    if not nome_jogador or not nome_personagem:
        messagebox.showwarning(
            "Erro",
            "Preencha todos os campos!"
        )
        return

    # criar jogador
    cursor.execute(
        'INSERT INTO jogadores (nome) VALUES (?)',
        (nome_jogador,)
    )

    jogador_id = cursor.lastrowid

    # atributos aleatórios
    forca = random.randint(1, 20)
    destreza = random.randint(1, 20)
    inteligencia = random.randint(1, 20)

    # criar personagem
    cursor.execute('''
        INSERT INTO personagens (
            jogador_id,
            nome_personagem,
            raca,
            classe,
            nivel,
            forca,
            destreza,
            inteligencia
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''',
    (
        jogador_id,
        nome_personagem,
        raca,
        classe,
        1,
        forca,
        destreza,
        inteligencia
    ))

    conexao.commit()

    messagebox.showinfo(
        "Sucesso",
        "Personagem criado!"
    )

    atualizar_lista()

    limpar_campos()

def atualizar_lista():

    tabela.delete(*tabela.get_children())

    cursor.execute('''
        SELECT
            personagens.id,
            jogadores.nome,
            personagens.nome_personagem,
            personagens.raca,
            personagens.classe,
            personagens.nivel,
            personagens.forca,
            personagens.destreza,
            personagens.inteligencia

        FROM personagens

        JOIN jogadores
        ON personagens.jogador_id = jogadores.id
    ''')

    personagens = cursor.fetchall()

    for p in personagens:

        tabela.insert(
            '',
            tk.END,
            values=p
        )

def excluir_personagem():

    item = tabela.selection()

    if not item:
        messagebox.showwarning(
            "Erro",
            "Selecione um personagem!"
        )
        return

    dados = tabela.item(item)

    personagem_id = dados['values'][0]

    cursor.execute(
        'DELETE FROM personagens WHERE id = ?',
        (personagem_id,)
    )

    conexao.commit()

    atualizar_lista()

    messagebox.showinfo(
        "Sucesso",
        "Personagem excluído!"
    )

def limpar_campos():

    entry_jogador.delete(0, tk.END)
    entry_personagem.delete(0, tk.END)

# ================= JANELA =================

janela = tk.Tk()

janela.title("RPG de Mesa")
janela.geometry("1000x600")
janela.configure(bg="#222222")

# ================= TÍTULO =================

titulo = tk.Label(
    janela,
    text="CRIADOR DE PERSONAGENS RPG",
    font=("Arial", 20, "bold"),
    bg="#222222",
    fg="white"
)

titulo.pack(pady=10)

# ================= FORMULÁRIO =================

frame_form = tk.Frame(
    janela,
    bg="#222222"
)

frame_form.pack(pady=10)

# jogador
tk.Label(
    frame_form,
    text="Jogador",
    bg="#222222",
    fg="white"
).grid(row=0, column=0)

entry_jogador = tk.Entry(frame_form)
entry_jogador.grid(row=1, column=0, padx=10)

# personagem
tk.Label(
    frame_form,
    text="Personagem",
    bg="#222222",
    fg="white"
).grid(row=0, column=1)

entry_personagem = tk.Entry(frame_form)
entry_personagem.grid(row=1, column=1, padx=10)

# raça
tk.Label(
    frame_form,
    text="Raça",
    bg="#222222",
    fg="white"
).grid(row=0, column=2)

combo_raca = ttk.Combobox(
    frame_form,
    values=[
        "Humano",
        "Elfo",
        "Anão",
        "Orc"
    ]
)

combo_raca.grid(row=1, column=2, padx=10)
combo_raca.current(0)

# classe
tk.Label(
    frame_form,
    text="Classe",
    bg="#222222",
    fg="white"
).grid(row=0, column=3)

combo_classe = ttk.Combobox(
    frame_form,
    values=[
        "Guerreiro",
        "Mago",
        "Ladino"
    ]
)

combo_classe.grid(row=1, column=3, padx=10)
combo_classe.current(0)

# ================= BOTÕES =================

frame_botoes = tk.Frame(
    janela,
    bg="#222222"
)

frame_botoes.pack(pady=10)

btn_criar = tk.Button(
    frame_botoes,
    text="Criar Personagem",
    command=criar_personagem,
    bg="green",
    fg="white",
    width=20
)

btn_criar.grid(row=0, column=0, padx=10)

btn_excluir = tk.Button(
    frame_botoes,
    text="Excluir Personagem",
    command=excluir_personagem,
    bg="red",
    fg="white",
    width=20
)

btn_excluir.grid(row=0, column=1, padx=10)

# ================= TABELA =================

colunas = (
    "ID",
    "Jogador",
    "Personagem",
    "Raça",
    "Classe",
    "Nível",
    "FOR",
    "DES",
    "INT"
)

tabela = ttk.Treeview(
    janela,
    columns=colunas,
    show="headings",
    height=15
)

for col in colunas:

    tabela.heading(col, text=col)

    tabela.column(
        col,
        width=100,
        anchor="center"
    )

tabela.pack(pady=20)

# ================= INICIAR =================

atualizar_lista()

janela.mainloop()

# ================= FECHAR =================

conexao.close()