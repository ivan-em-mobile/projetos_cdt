import json
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


TIPO_USUARIO_LOGADO = "user"

#Banco de dados
def criar_banco():
    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()

    # Tabela de compromissos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            dia TEXT NOT NULL,
            mes TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    """)

    # Tabela de usuários (para o login)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    """)

    # Cria usuários padrão caso a tabela esteja vazia
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO usuarios (usuario, senha, tipo) VALUES (?, ?, ?)",
            ("admin", "123", "admin"),
        )
        cursor.execute(
            "INSERT INTO usuarios (usuario, senha, tipo) VALUES (?, ?, ?)",
            ("user", "123", "user"),
        )

    conexao.commit()
    conexao.close()


def add_data():
    nome = entry_nome.get().strip()
    dia = entry_dia.get().strip()
    mes = entry_mes.get().strip()
    hora = entry_hora.get().strip()

    if not (nome and dia and mes and hora):
        messagebox.showwarning("⚠️ Erro", "Todos os campos devem ser preenchidos!")
        return

    try:
        if not (1 <= int(dia) <= 31):
            messagebox.showerror(
                "❌ Erro", "Dia inválido! Digite um número entre 1 e 31."
            )
            return
    except ValueError:
        messagebox.showerror("⚠️ Erro", "O dia deve ser um número inteiro!")
        return

    try:
        if not (1 <= int(mes) <= 12):
            messagebox.showerror(
                "❌ Erro", "Mês inválido! Digite um número entre 1 e 12."
            )
            return
    except ValueError:
        messagebox.showerror("⚠️ Erro", "O mês deve ser um número inteiro!")
        return

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO contatos (nome, dia, mes, hora) 
        VALUES (?, ?, ?, ?)
    """,
        (nome, dia, mes, hora),
    )
    conexao.commit()
    conexao.close()

    messagebox.showinfo("✅ Sucesso", "Compromisso agendado com sucesso!")
    limpar_campos()
    listar_datas()


def listar_datas():
    for linha in tabela.get_children():
        tabela.delete(linha)

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM contatos")
    dados = cursor.fetchall()

    for linha in dados:
        data_formatada = f"{linha[2]}/{linha[3]}"
        tabela.insert(
            "",
            "end",
            values=(linha[0], linha[1], data_formatada, linha[4]),
        )

    conexao.close()


def editar_data():
    if not entry_id.get():
        messagebox.showwarning(
            "⚠️ Seleção", "Selecione um compromisso na tabela para editar!"
        )
        return

    id_editar = entry_id.get()
    novo_nome = entry_nome.get().strip()
    novo_dia = entry_dia.get().strip()
    novo_mes = entry_mes.get().strip()
    nova_hora = entry_hora.get().strip()

    if not (novo_nome and novo_dia and novo_mes and nova_hora):
        messagebox.showwarning(
            "⚠️ Erro", "Todos os campos devem ser preenchidos para editar!"
        )
        return

    try:
        if not (1 <= int(novo_dia) <= 31):
            messagebox.showerror(
                "❌ Erro", "Dia inválido! Digite um número entre 1 e 31."
            )
            return
    except ValueError:
        messagebox.showerror("⚠️ Erro", "O dia deve ser um número inteiro!")
        return

    try:
        if not (1 <= int(novo_mes) <= 12):
            messagebox.showerror(
                "❌ Erro", "Mês inválido! Digite um número entre 1 e 12."
            )
            return
    except ValueError:
        messagebox.showerror("⚠️ Erro", "O mês deve ser um número inteiro!")
        return

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()
    cursor.execute(
        """
        UPDATE contatos 
        SET nome = ?, dia = ?, mes = ?, hora = ? 
        WHERE id = ?
    """,
        (novo_nome, novo_dia, novo_mes, nova_hora, id_editar),
    )
    conexao.commit()
    conexao.close()

    messagebox.showinfo("✅ Sucesso", "Compromisso editado com sucesso!")
    limpar_campos()
    listar_datas()


def deletar_data():
    if not entry_id.get():
        messagebox.showwarning(
            "⚠️ Seleção", "Selecione um compromisso na tabela para deletar!"
        )
        return

    id_data = entry_id.get()

    resposta = messagebox.askyesno(
        "Confirmação",
        f"Tem certeza que deseja apagar o compromisso ID {id_data}?",
    )

    if resposta:
        conexao = sqlite3.connect("agenda.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM contatos WHERE id = ?", (id_data,))
        conexao.commit()
        conexao.close()

        messagebox.showinfo("✅ Sucesso", "Compromisso deletado com sucesso!")
        limpar_campos()
        listar_datas()


#  FUNÇÃO: EXPORTAR PARA JSON (EXCLUSIVA ADMIN)
def exportar_para_json():
    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM contatos")
    dados = cursor.fetchall()
    conexao.close()

    if not dados:
        messagebox.showinfo("Aviso", "Não há dados para exportar.")
        return

    # Converte os dados do banco para uma lista de dicionários
    lista_compromissos = []
    for linha in dados:
        lista_compromissos.append(
            {
                "id": linha[0],
                "nome": linha[1],
                "dia": linha[2],
                "mes": linha[3],
                "hora": linha[4],
            }
        )

    # Abre a caixinha do Windows para escolher onde salvar o arquivo
    arquivo_destino = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Arquivos JSON", "*.json")],
        title="Salvar Banco de Dados como JSON",
    )

    if arquivo_destino:
        with open(arquivo_destino, "w", encoding="utf-8") as f:
            json.dump(lista_compromissos, f, ensure_ascii=False, indent=4)
        messagebox.showinfo(
            "✅ Sucesso", "Banco de dados exportado em JSON com sucesso!"
        )


# 2. FUNÇÕES AUXILIARES DA INTERFACE
def limpar_campos():
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.config(state="readonly")
    entry_nome.delete(0, tk.END)
    entry_dia.delete(0, tk.END)
    entry_mes.delete(0, tk.END)
    entry_hora.delete(0, tk.END)


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


# 3. CONTROLE DE LOGIN E PERMISSÕES
def realizar_login():
    global TIPO_USUARIO_LOGADO
    usuario = entry_usuario.get().strip()
    senha = entry_senha.get().strip()

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT tipo FROM usuarios WHERE usuario = ? AND senha = ?",
        (usuario, senha),
    )
    resultado = cursor.fetchone()
    conexao.close()

    if resultado:
        TIPO_USUARIO_LOGADO = resultado[0]  # Pega se é 'admin' ou 'user'
        messagebox.showinfo(
            "Sucesso", f"Login efetuado como: {TIPO_USUARIO_LOGADO.upper()}"
        )
        janela_login.destroy()
        abrir_agenda()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")


def abrir_agenda():
    global entry_id, entry_nome, entry_dia, entry_mes, entry_hora, tabela

    janela_principal = tk.Tk()
    janela_principal.title(
        f"Minha Agenda de Compromissos - ({TIPO_USUARIO_LOGADO.upper()})"
    )
    janela_principal.geometry("580x540")
    janela_principal.resizable(False, False)
    janela_principal.configure(bg="#FFFFFF")

    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("TLabelframe", background="#FFFFFF", bordercolor="#0056b3")
    estilo.configure("TLabelframe.Label", background="#FFFFFF", foreground="#0056b3")
    estilo.configure(
        "Treeview", background="#FFFFFF", foreground="#333333", rowheight=25
    )
    estilo.configure(
        "Treeview.Heading",
        background="#0056b3",
        foreground="#FFFFFF",
        font=("Arial", 10, "bold"),
    )
    estilo.map("Treeview", background=[("selected", "#007BFF")])

    # --- Formulário de Entrada ---
    frame_campos = ttk.LabelFrame(
        janela_principal, text=" Dados do Compromisso ", padding=10
    )
    frame_campos.pack(fill="x", padx=15, pady=15)

    tk.Label(frame_campos, text="ID:", bg="#FFFFFF", fg="#0056b3").grid(
        row=0, column=0, sticky="w"
    )
    entry_id = tk.Entry(
        frame_campos,
        width=5,
        state="readonly",
        readonlybackground="#F0F4F8",
        fg="#0056b3",
    )
    entry_id.grid(row=0, column=1, sticky="w", pady=5)

    tk.Label(frame_campos, text="Nome:", bg="#FFFFFF", fg="#0056b3").grid(
        row=1, column=0, sticky="w"
    )
    entry_nome = tk.Entry(frame_campos, width=40, bd=1, relief="solid")
    entry_nome.grid(row=1, column=1, columnspan=5, sticky="w", pady=5)

    tk.Label(frame_campos, text="Dia (1-31):", bg="#FFFFFF", fg="#0056b3").grid(
        row=2, column=0, sticky="w"
    )
    entry_dia = tk.Entry(frame_campos, width=5, bd=1, relief="solid")
    entry_dia.grid(row=2, column=1, sticky="w", pady=5)

    tk.Label(frame_campos, text="Mês (1-12):", bg="#FFFFFF", fg="#0056b3").grid(
        row=2, column=2, sticky="w"
    )
    entry_mes = tk.Entry(frame_campos, width=5, bd=1, relief="solid")
    entry_mes.grid(row=2, column=3, sticky="w", pady=5)

    tk.Label(frame_campos, text="Hora:", bg="#FFFFFF", fg="#0056b3").grid(
        row=2, column=4, sticky="w"
    )
    entry_hora = tk.Entry(frame_campos, width=8, bd=1, relief="solid")
    entry_hora.grid(row=2, column=5, sticky="w", pady=5)

    # --- Botões Estilizados ---
    frame_botoes = tk.Frame(janela_principal, bg="#FFFFFF")
    frame_botoes.pack(pady=5)

    estilo_botao = {
        "font": ("Arial", 10, "bold"),
        "bg": "#0056b3",
        "fg": "#FFFFFF",
        "activebackground": "#004085",
        "activeforeground": "#FFFFFF",
        "bd": 0,
        "padx": 10,
        "pady": 5,
        "cursor": "hand2",
    }

    # Botão Adicionar (Disponível para todos)
    btn_adicionar = tk.Button(
        frame_botoes, text="Adicionar", command=add_data, **estilo_botao
    )
    btn_adicionar.pack(side="left", padx=5)

    # AGORA DISPONÍVEL PARA TODOS: Editar e Deletar mudaram para fora do IF!
    btn_editar = tk.Button(
        frame_botoes, text="Salvar Edição", command=editar_data, **estilo_botao
    )
    btn_editar.pack(side="left", padx=5)

    btn_deletar = tk.Button(
        frame_botoes, text="Deletar", command=deletar_data, **estilo_botao
    )
    btn_deletar.pack(side="left", padx=5)

    # Apenas o botão de Exportar JSON continua restrito ao ADMIN
    if TIPO_USUARIO_LOGADO == "admin":
        btn_json = tk.Button(
            frame_botoes,
            text="Exportar JSON 📥",
            command=exportar_para_json,
            font=("Arial", 10, "bold"),
            bg="#28a745",
            fg="#FFFFFF",
            activebackground="#218838",
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
        )
        btn_json.pack(side="left", padx=5)

    btn_limpar = tk.Button(
        frame_botoes,
        text="Limpar",
        command=limpar_campos,
        font=("Arial", 10),
        bg="#FFFFFF",
        fg="#0056b3",
        activebackground="#F0F4F8",
        bd=1,
        relief="solid",
        padx=10,
        pady=4,
        cursor="hand2",
    )
    btn_limpar.pack(side="left", padx=5)

    # --- Tabela ---
    frame_tabela = tk.Frame(janela_principal, bg="#FFFFFF")
    frame_tabela.pack(fill="both", expand=True, padx=15, pady=15)

    colunas = ("id", "nome", "data", "hora")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=10)

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome do Compromisso")
    tabela.heading("data", text="Data (D/M)")
    tabela.heading("hora", text="Horário")

    tabela.column("id", width=40, anchor="center")
    tabela.column("nome", width=250, anchor="w")
    tabela.column("data", width=100, anchor="center")
    tabela.column("hora", width=100, anchor="center")

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)

    tabela.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tabela.bind("<<TreeviewSelect>>", selecionar_linha)

    listar_datas()
    janela_principal.mainloop()


# --- CONSTRUÇÃO DA TELA DE LOGIN ---
criar_banco()

janela_login = tk.Tk()
janela_login.title("Login - AGENDA VOCAÇÃO")
janela_login.geometry("350x280")
janela_login.resizable(False, False)
janela_login.configure(bg="#FFFFFF")

lbl_titulo = tk.Label(
    janela_login,
    text="AGENDA VOCAÇÃO",
    font=("Arial", 14, "bold"),
    bg="#FFFFFF",
    fg="#0056b3",
)
lbl_titulo.pack(pady=20)

frame_login = tk.Frame(janela_login, bg="#FFFFFF")
frame_login.pack(pady=10)

tk.Label(
    frame_login, text="Usuário:", font=("Arial", 10, "bold"), bg="#FFFFFF", fg="#0056b3"
).grid(row=0, column=0, sticky="w", pady=5)
entry_usuario = tk.Entry(
    frame_login, width=25, bd=1, relief="solid", font=("Arial", 10)
)
entry_usuario.grid(row=0, column=1, pady=5, padx=5)

tk.Label(
    frame_login, text="Senha:", font=("Arial", 10, "bold"), bg="#FFFFFF", fg="#0056b3"
).grid(row=1, column=0, sticky="w", pady=5)
entry_senha = tk.Entry(
    frame_login, width=25, bd=1, relief="solid", font=("Arial", 10), show="*"
)
entry_senha.grid(row=1, column=1, pady=5, padx=5)

btn_entrar = tk.Button(
    janela_login,
    text="ENTRAR",
    command=realizar_login,
    font=("Arial", 11, "bold"),
    bg="#0056b3",
    fg="#FFFFFF",
    activebackground="#004085",
    activeforeground="#FFFFFF",
    bd=0,
    width=15,
    pady=5,
    cursor="hand2",
)
btn_entrar.pack(pady=20)

janela_login.mainloop()