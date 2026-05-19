# =========================================================
# AGENDA VOCAÇÃO - VERSÃO COMPLETA FINAL
# =========================================================

import json
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# =========================================================
# VARIÁVEL GLOBAL
# =========================================================

TIPO_USUARIO_LOGADO = "user"

# =========================================================
# BANCO DE DADOS
# =========================================================

def criar_banco():

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()

    # -----------------------------
    # TABELA DE COMPROMISSOS
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contatos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            dia TEXT NOT NULL,
            mes TEXT NOT NULL,
            hora TEXT NOT NULL

        )
    """)

    # -----------------------------
    # TABELA DE USUÁRIOS
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL

        )
    """)

    # -----------------------------
    # CRIA USUÁRIOS PADRÃO
    # -----------------------------

    cursor.execute("SELECT COUNT(*) FROM usuarios")

    if cursor.fetchone()[0] == 0:

        cursor.execute("""
            INSERT INTO usuarios
            (usuario, senha, tipo)

            VALUES (?, ?, ?)
        """, ("admin", "123", "admin"))

        cursor.execute("""
            INSERT INTO usuarios
            (usuario, senha, tipo)

            VALUES (?, ?, ?)
        """, ("user", "123", "user"))

    conexao.commit()
    conexao.close()

# =========================================================
# VALIDAÇÕES
# =========================================================

def validar_campos():

    nome = entry_nome.get().strip()
    dia = entry_dia.get().strip()
    mes = entry_mes.get().strip()
    hora = entry_hora.get().strip()

    # -----------------------------
    # CAMPOS VAZIOS
    # -----------------------------

    if not (nome and dia and mes and hora):

        messagebox.showwarning(
            "Campos Vazios",
            "Todos os campos devem ser preenchidos!"
        )

        return False

    # -----------------------------
    # NOME COM NÚMEROS
    # -----------------------------

    if any(char.isdigit() for char in nome):

        messagebox.showerror(
            "Nome Inválido",
            "O nome do compromisso não pode conter números!"
        )

        return False

    # -----------------------------
    # DIA
    # -----------------------------

    if not dia.isdigit():

        messagebox.showerror(
            "Erro",
            "O dia deve conter apenas números!"
        )

        return False

    if not (1 <= int(dia) <= 31):

        messagebox.showerror(
            "Erro",
            "Digite um dia válido entre 1 e 31."
        )

        return False

    # -----------------------------
    # MÊS
    # -----------------------------

    if not mes.isdigit():

        messagebox.showerror(
            "Erro",
            "O mês deve conter apenas números!"
        )

        return False

    if not (1 <= int(mes) <= 12):

        messagebox.showerror(
            "Erro",
            "Digite um mês válido entre 1 e 12."
        )

        return False

    return True

# =========================================================
# ADICIONAR
# =========================================================

def add_data():

    if not validar_campos():
        return

    nome = entry_nome.get().strip()
    dia = entry_dia.get().strip()
    mes = entry_mes.get().strip()
    hora = entry_hora.get().strip()

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO contatos
        (nome, dia, mes, hora)

        VALUES (?, ?, ?, ?)
    """, (nome, dia, mes, hora))

    conexao.commit()
    conexao.close()

    messagebox.showinfo(
        "Sucesso",
        "Compromisso agendado com sucesso!"
    )

    limpar_campos()
    listar_datas()

# =========================================================
# LISTAR
# =========================================================

def listar_datas():

    for linha in tabela.get_children():
        tabela.delete(linha)

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM contatos
    """)

    dados = cursor.fetchall()

    for linha in dados:

        data_formatada = f"{linha[2]}/{linha[3]}"

        tabela.insert(
            "",
            "end",
            values=(
                linha[0],
                linha[1],
                data_formatada,
                linha[4]
            )
        )

    conexao.close()

# =========================================================
# EDITAR
# =========================================================

def editar_data():

    if not entry_id.get():

        messagebox.showwarning(
            "Seleção",
            "Selecione um compromisso na tabela!"
        )

        return

    if not validar_campos():
        return

    id_editar = entry_id.get()

    novo_nome = entry_nome.get().strip()
    novo_dia = entry_dia.get().strip()
    novo_mes = entry_mes.get().strip()
    nova_hora = entry_hora.get().strip()

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE contatos

        SET
        nome = ?,
        dia = ?,
        mes = ?,
        hora = ?

        WHERE id = ?
    """, (

        novo_nome,
        novo_dia,
        novo_mes,
        nova_hora,
        id_editar

    ))

    conexao.commit()
    conexao.close()

    messagebox.showinfo(
        "Sucesso",
        "Compromisso editado com sucesso!"
    )

    limpar_campos()
    listar_datas()

# =========================================================
# DELETAR
# =========================================================

def deletar_data():

    if not entry_id.get():

        messagebox.showwarning(
            "Seleção",
            "Selecione um compromisso!"
        )

        return

    id_data = entry_id.get()
    nome = entry_nome.get()

    resposta = messagebox.askyesno(
        "Confirmação",
        f"Deseja apagar o compromisso:\n\n{nome} ?"
    )

    if resposta:

        conexao = sqlite3.connect("agenda.db")
        cursor = conexao.cursor()

        cursor.execute("""
            DELETE FROM contatos
            WHERE id = ?
        """, (id_data,))

        conexao.commit()

        # -----------------------------------
        # RESETAR ID PARA 1 SE NÃO HOUVER MAIS
        # -----------------------------------

        cursor.execute("""
            SELECT COUNT(*) FROM contatos
        """)

        quantidade = cursor.fetchone()[0]

        if quantidade == 0:

            cursor.execute("""
                DELETE FROM sqlite_sequence
                WHERE name='contatos'
            """)

            conexao.commit()

        conexao.close()

        messagebox.showinfo(
            "Sucesso",
            f"{nome} foi deletado!"
        )

        limpar_campos()
        listar_datas()

# =========================================================
# EXPORTAR JSON
# =========================================================

def exportar_para_json():

    if TIPO_USUARIO_LOGADO != "admin":

        messagebox.showerror(
            "Acesso Negado",
            "Apenas administradores podem exportar JSON."
        )

        return

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM contatos
    """)

    dados = cursor.fetchall()

    conexao.close()

    if not dados:

        messagebox.showwarning(
            "Aviso",
            "Não existem dados para exportar."
        )

        return

    lista_compromissos = []

    for linha in dados:

        lista_compromissos.append({

            "id": linha[0],
            "nome": linha[1],
            "dia": linha[2],
            "mes": linha[3],
            "hora": linha[4]

        })

    arquivo_destino = filedialog.asksaveasfilename(

        defaultextension=".json",

        filetypes=[
            ("Arquivos JSON", "*.json")
        ],

        title="Salvar Banco de Dados"

    )

    if arquivo_destino:

        with open(
            arquivo_destino,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                lista_compromissos,
                f,
                ensure_ascii=False,
                indent=4
            )

        messagebox.showinfo(
            "Sucesso",
            "Banco exportado com sucesso!"
        )

# =========================================================
# LIMPAR CAMPOS
# =========================================================

def limpar_campos():

    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.config(state="readonly")

    entry_nome.delete(0, tk.END)
    entry_dia.delete(0, tk.END)
    entry_mes.delete(0, tk.END)
    entry_hora.delete(0, tk.END)

# =========================================================
# SELECIONAR LINHA
# =========================================================

def selecionar_linha(event):

    item_selecionado = tabela.selection()

    if not item_selecionado:
        return

    valores = tabela.item(item_selecionado, "values")

    limpar_campos()

    dia_tab, mes_tab = valores[2].split("/")

    entry_id.config(state="normal")
    entry_id.insert(0, valores[0])
    entry_id.config(state="readonly")

    entry_nome.insert(0, valores[1])
    entry_dia.insert(0, dia_tab)
    entry_mes.insert(0, mes_tab)
    entry_hora.insert(0, valores[3])

# =========================================================
# LOGIN
# =========================================================

def realizar_login():

    global TIPO_USUARIO_LOGADO

    usuario = entry_usuario.get().strip()
    senha = entry_senha.get().strip()

    if not usuario or not senha:

        messagebox.showwarning(
            "Campos Vazios",
            "Digite usuário e senha."
        )

        return

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT tipo FROM usuarios
        WHERE usuario = ? AND senha = ?
    """, (usuario, senha))

    resultado = cursor.fetchone()

    conexao.close()

    if resultado:

        TIPO_USUARIO_LOGADO = resultado[0]

        messagebox.showinfo(
            "Login",
            f"Login efetuado como {TIPO_USUARIO_LOGADO.upper()}"
        )

        janela_login.destroy()

        abrir_agenda()

    else:

        messagebox.showerror(
            "Erro",
            "Usuário ou senha incorretos!"
        )

# =========================================================
# TELA PRINCIPAL
# =========================================================

def abrir_agenda():

    global entry_id
    global entry_nome
    global entry_dia
    global entry_mes
    global entry_hora
    global tabela

    janela_principal = tk.Tk()

    janela_principal.title(
        f"AGENDA VOCAÇÃO - {TIPO_USUARIO_LOGADO.upper()}"
    )

    janela_principal.geometry("650x560")
    janela_principal.resizable(False, False)
    janela_principal.configure(bg="#FFFFFF")

    # =====================================================
    # ESTILO
    # =====================================================

    estilo = ttk.Style()

    estilo.theme_use("clam")

    estilo.configure(
        "Treeview",
        rowheight=25,
        font=("Arial", 10)
    )

    estilo.configure(
        "Treeview.Heading",
        background="#0056b3",
        foreground="white",
        font=("Arial", 10, "bold")
    )

    # =====================================================
    # TÍTULO
    # =====================================================

    titulo = tk.Label(
        janela_principal,
        text="AGENDA VOCAÇÃO",
        font=("Arial", 22, "bold"),
        bg="white",
        fg="#0056b3"
    )

    titulo.pack(pady=15)

    # =====================================================
    # CAMPOS
    # =====================================================

    frame_campos = ttk.LabelFrame(
        janela_principal,
        text=" Dados do Compromisso ",
        padding=10
    )

    frame_campos.pack(
        fill="x",
        padx=15,
        pady=10
    )

    tk.Label(
        frame_campos,
        text="ID:",
        bg="white",
        fg="#0056b3"
    ).grid(row=0, column=0, sticky="w")

    entry_id = tk.Entry(
        frame_campos,
        width=5,
        state="readonly"
    )

    entry_id.grid(row=0, column=1)

    tk.Label(
        frame_campos,
        text="Nome:",
        bg="white",
        fg="#0056b3"
    ).grid(row=1, column=0, sticky="w")

    entry_nome = tk.Entry(
        frame_campos,
        width=40
    )

    entry_nome.grid(
        row=1,
        column=1,
        columnspan=5,
        pady=5
    )

    tk.Label(
        frame_campos,
        text="Dia:",
        bg="white",
        fg="#0056b3"
    ).grid(row=2, column=0)

    entry_dia = tk.Entry(
        frame_campos,
        width=5
    )

    entry_dia.grid(row=2, column=1)

    tk.Label(
        frame_campos,
        text="Mês:",
        bg="white",
        fg="#0056b3"
    ).grid(row=2, column=2)

    entry_mes = tk.Entry(
        frame_campos,
        width=5
    )

    entry_mes.grid(row=2, column=3)

    tk.Label(
        frame_campos,
        text="Hora:",
        bg="white",
        fg="#0056b3"
    ).grid(row=2, column=4)

    entry_hora = tk.Entry(
        frame_campos,
        width=10
    )

    entry_hora.grid(row=2, column=5)

    # =====================================================
    # BOTÕES
    # =====================================================

    frame_botoes = tk.Frame(
        janela_principal,
        bg="white"
    )

    frame_botoes.pack(pady=10)

    estilo_botao = {

        "font": ("Arial", 10, "bold"),
        "bg": "#0056b3",
        "fg": "white",
        "activebackground": "#004085",
        "activeforeground": "white",
        "bd": 0,
        "padx": 12,
        "pady": 6,
        "cursor": "hand2"

    }

    tk.Button(
        frame_botoes,
        text="Adicionar",
        command=add_data,
        **estilo_botao
    ).pack(side="left", padx=5)

    tk.Button(
        frame_botoes,
        text="Editar",
        command=editar_data,
        **estilo_botao
    ).pack(side="left", padx=5)

    tk.Button(
        frame_botoes,
        text="Deletar",
        command=deletar_data,
        **estilo_botao
    ).pack(side="left", padx=5)

    tk.Button(
        frame_botoes,
        text="Limpar",
        command=limpar_campos,
        **estilo_botao
    ).pack(side="left", padx=5)

    # -----------------------------------------------------
    # EXPORTAR JSON APENAS ADMIN
    # -----------------------------------------------------

    if TIPO_USUARIO_LOGADO == "admin":

        tk.Button(
            frame_botoes,
            text="Exportar JSON",
            command=exportar_para_json,
            bg="#28a745",
            fg="white",
            activebackground="#1e7e34",
            activeforeground="white",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            font=("Arial", 10, "bold")
        ).pack(side="left", padx=5)

    # =====================================================
    # TABELA
    # =====================================================

    frame_tabela = tk.Frame(
        janela_principal,
        bg="white"
    )

    frame_tabela.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    colunas = (
        "id",
        "nome",
        "data",
        "hora"
    )

    tabela = ttk.Treeview(
        frame_tabela,
        columns=colunas,
        show="headings",
        height=12
    )

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Compromisso")
    tabela.heading("data", text="Data")
    tabela.heading("hora", text="Hora")

    tabela.column("id", width=50, anchor="center")
    tabela.column("nome", width=320)
    tabela.column("data", width=100, anchor="center")
    tabela.column("hora", width=100, anchor="center")

    scrollbar = ttk.Scrollbar(
        frame_tabela,
        orient="vertical",
        command=tabela.yview
    )

    tabela.configure(
        yscrollcommand=scrollbar.set
    )

    tabela.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    tabela.bind(
        "<<TreeviewSelect>>",
        selecionar_linha
    )

    listar_datas()

    janela_principal.mainloop()

# =========================================================
# INICIAR
# =========================================================

criar_banco()

# =========================================================
# TELA LOGIN
# =========================================================

janela_login = tk.Tk()

janela_login.title("Login - AGENDA VOCAÇÃO")

janela_login.geometry("370x300")

janela_login.resizable(False, False)

janela_login.configure(bg="white")

titulo_login = tk.Label(
    janela_login,
    text="AGENDA VOCAÇÃO",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="#a6c844"
)

titulo_login.pack(pady=20)

frame_login = tk.Frame(
    janela_login,
    bg="white"
)

frame_login.pack(pady=10)

tk.Label(
    frame_login,
    text="Usuário:",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#0056b3"
).grid(row=0, column=0, pady=5, sticky="w")

entry_usuario = tk.Entry(
    frame_login,
    width=25,
    font=("Arial", 10)
)

entry_usuario.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)

tk.Label(
    frame_login,
    text="Senha:",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#0056b3"
).grid(row=1, column=0, pady=5, sticky="w")

entry_senha = tk.Entry(
    frame_login,
    width=25,
    show="*",
    font=("Arial", 10)
)

entry_senha.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)

btn_entrar = tk.Button(

    janela_login,

    text="ENTRAR",

    command=realizar_login,

    font=("Arial", 11, "bold"),

    bg="#0056b3",
    fg="white",

    activebackground="#004085",
    activeforeground="white",

    bd=0,

    width=18,
    pady=6,

    cursor="hand2"
)

btn_entrar.pack(pady=25)

janela_login.mainloop()