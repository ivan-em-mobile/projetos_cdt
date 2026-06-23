'''



'''


import hashlib
import json
import os
import sqlite3
import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import messagebox, ttk


DB_FILE = "agendamento.db"
USUARIOS_JSON = "usuarios.json"
SERVICOS_JSON = "servicos.json"
AGENDAMENTOS_JSON = "agendamentos.json"
COR_FUNDO = "#3399ff"
HORARIOS = [
    "08:00", "09:00", "10:00", "11:00", "12:00",
    "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"
]
DIAS_SEMANA = [
    "segunda-feira", "terca-feira", "quarta-feira", "quinta-feira",
    "sexta-feira", "sabado", "domingo"
]


usuario_logado = None


def conectar():
    conexao = sqlite3.connect(DB_FILE)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def iniciar_banco():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                username TEXT PRIMARY KEY,
                senha_hash TEXT NOT NULL,
                tipo TEXT NOT NULL CHECK (tipo IN ('cliente', 'prestador'))
            )
        """)
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS servicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                prestador TEXT NOT NULL,
                FOREIGN KEY (prestador) REFERENCES usuarios(username)
            )
        """)
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                servico_id INTEGER NOT NULL,
                data_hora TEXT NOT NULL,
                FOREIGN KEY (cliente) REFERENCES usuarios(username),
                FOREIGN KEY (servico_id) REFERENCES servicos(id) ON DELETE CASCADE,
                UNIQUE (servico_id, data_hora)
            )
        """)
    migrar_json_para_sqlite()


def banco_tem_dados():
    with conectar() as conexao:
        total = conexao.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    return total > 0


def carregar_json(arquivo):
    if not os.path.exists(arquivo):
        return {}

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        messagebox.showwarning("Aviso", f"Nao foi possivel importar {arquivo}.")
        return {}


def migrar_json_para_sqlite():
    if banco_tem_dados():
        return

    usuarios = carregar_json(USUARIOS_JSON)
    servicos = carregar_json(SERVICOS_JSON)
    agendamentos = carregar_json(AGENDAMENTOS_JSON)

    if not usuarios and not servicos and not agendamentos:
        return

    with conectar() as conexao:
        for username, dados in usuarios.items():
            senha = dados.get("senha", "")
            senha_hash = senha if len(senha) == 64 else gerar_hash(senha)
            conexao.execute(
                "INSERT OR IGNORE INTO usuarios (username, senha_hash, tipo) VALUES (?, ?, ?)",
                (username, senha_hash, dados.get("tipo", "cliente"))
            )

        for nome, dados in servicos.items():
            prestador = dados.get("prestador")
            if prestador:
                conexao.execute(
                    "INSERT OR IGNORE INTO servicos (nome, prestador) VALUES (?, ?)",
                    (nome, prestador)
                )

        for dados in agendamentos.values():
            servico = buscar_servico_por_nome(dados.get("servico", ""), conexao)
            if servico:
                conexao.execute(
                    """
                    INSERT OR IGNORE INTO agendamentos (cliente, servico_id, data_hora)
                    VALUES (?, ?, ?)
                    """,
                    (dados.get("cliente"), servico["id"], dados.get("data_hora"))
                )


def gerar_hash(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def limpar_tela():
    for widget in root.winfo_children():
        widget.destroy()


def criar_label(texto, tamanho=11, pady=0):
    tk.Label(root, text=texto, font=("Arial", tamanho), fg="white", bg=COR_FUNDO).pack(pady=pady)


def criar_entry(show=None):
    entry = tk.Entry(root, width=34, show=show)
    entry.pack(pady=3)
    return entry


def criar_botao(texto, comando, pady=4):
    tk.Button(root, text=texto, width=30, command=comando).pack(pady=pady)


def criar_combo(valores):
    combo = ttk.Combobox(root, values=valores, state="readonly", width=31)
    combo.pack(pady=3)
    if valores:
        combo.current(0)
    return combo


def obter_item_listbox(lista, mapa):
    selecao = lista.curselection()
    if not selecao:
        return None
    return mapa[selecao[0]]


def registrar_usuario(tipo, username, senha):
    username = username.strip()
    senha = senha.strip()

    if not username or not senha:
        messagebox.showerror("Erro", "Preencha usuario e senha!")
        return

    try:
        with conectar() as conexao:
            conexao.execute(
                "INSERT INTO usuarios (username, senha_hash, tipo) VALUES (?, ?, ?)",
                (username, gerar_hash(senha), tipo)
            )
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Usuario ja existe!")
        return

    messagebox.showinfo("Sucesso", f"Usuario {username} registrado como {tipo}!")


def login(username, senha):
    global usuario_logado

    username = username.strip()
    senha = senha.strip()

    if not username or not senha:
        messagebox.showerror("Erro", "Preencha usuario e senha!")
        return

    with conectar() as conexao:
        usuario = conexao.execute(
            "SELECT username, senha_hash, tipo FROM usuarios WHERE username = ?",
            (username,)
        ).fetchone()

    if usuario and usuario["senha_hash"] == gerar_hash(senha):
        usuario_logado = {"username": usuario["username"], "tipo": usuario["tipo"]}
        messagebox.showinfo("Login", f"Bem-vindo {usuario['username']} ({usuario['tipo']})")
        abrir_menu()
        return

    messagebox.showerror("Erro", "Usuario ou senha invalidos!")


def buscar_servico_por_nome(nome_servico, conexao=None):
    fechar_depois = conexao is None
    conexao = conexao or conectar()
    servico = conexao.execute(
        "SELECT id, nome, prestador FROM servicos WHERE nome = ?",
        (nome_servico,)
    ).fetchone()
    if fechar_depois:
        conexao.close()
    return servico


def listar_servicos():
    with conectar() as conexao:
        return conexao.execute(
            "SELECT id, nome, prestador FROM servicos ORDER BY nome"
        ).fetchall()


def listar_servicos_do_prestador(prestador):
    with conectar() as conexao:
        return conexao.execute(
            "SELECT id, nome, prestador FROM servicos WHERE prestador = ? ORDER BY nome",
            (prestador,)
        ).fetchall()


def listar_agendamentos_do_cliente(cliente):
    with conectar() as conexao:
        return conexao.execute(
            """
            SELECT a.id, a.data_hora, s.nome AS servico, s.prestador
            FROM agendamentos a
            JOIN servicos s ON s.id = a.servico_id
            WHERE a.cliente = ?
            ORDER BY a.data_hora
            """,
            (cliente,)
        ).fetchall()


def listar_agendamentos_do_prestador(prestador):
    with conectar() as conexao:
        return conexao.execute(
            """
            SELECT a.id, a.data_hora, a.cliente, s.nome AS servico
            FROM agendamentos a
            JOIN servicos s ON s.id = a.servico_id
            WHERE s.prestador = ?
            ORDER BY a.data_hora
            """,
            (prestador,)
        ).fetchall()


def adicionar_servico(nome_servico):
    nome_servico = nome_servico.strip()

    if not usuario_logado or usuario_logado["tipo"] != "prestador":
        messagebox.showerror("Erro", "Somente prestadores podem adicionar servicos!")
        return

    if not nome_servico:
        messagebox.showerror("Erro", "Digite o nome do servico!")
        return

    try:
        with conectar() as conexao:
            conexao.execute(
                "INSERT INTO servicos (nome, prestador) VALUES (?, ?)",
                (nome_servico, usuario_logado["username"])
            )
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Esse servico ja existe!")
        return

    messagebox.showinfo("Sucesso", f"Servico '{nome_servico}' adicionado!")
    abrir_menu()


def remover_servico(servico):
    if not usuario_logado or usuario_logado["tipo"] != "prestador":
        messagebox.showerror("Erro", "Somente prestadores podem remover servicos!")
        return

    if not servico:
        messagebox.showerror("Erro", "Selecione um servico para remover!")
        return

    if servico["prestador"] != usuario_logado["username"]:
        messagebox.showerror("Erro", "Voce so pode remover seus proprios servicos!")
        return

    with conectar() as conexao:
        conexao.execute("DELETE FROM servicos WHERE id = ?", (servico["id"],))

    messagebox.showinfo("Sucesso", f"Servico '{servico['nome']}' removido!")
    abrir_menu()


def montar_data_hora(dia_texto, horario):
    if not dia_texto or not horario:
        return ""
    data_iso = dia_texto.split(" - ")[0]
    return f"{data_iso} {horario}"


def agendar_servico(servico, dia_texto, horario):
    if not usuario_logado or usuario_logado["tipo"] != "cliente":
        messagebox.showerror("Erro", "Somente clientes podem agendar servicos!")
        return

    if not servico:
        messagebox.showerror("Erro", "Selecione um servico!")
        return

    data_hora = montar_data_hora(dia_texto, horario)
    if not data_hora:
        messagebox.showerror("Erro", "Selecione o dia e o horario!")
        return

    try:
        datetime.strptime(data_hora, "%Y-%m-%d %H:%M")
    except ValueError:
        messagebox.showerror("Erro", "Data ou horario invalido!")
        return

    try:
        with conectar() as conexao:
            conexao.execute(
                """
                INSERT INTO agendamentos (cliente, servico_id, data_hora)
                VALUES (?, ?, ?)
                """,
                (usuario_logado["username"], servico["id"], data_hora)
            )
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Esse horario ja esta ocupado!")
        return

    messagebox.showinfo("Sucesso", f"Servico '{servico['nome']}' agendado para {data_hora}")
    abrir_menu()


def cancelar_agendamento(agendamento):
    if not usuario_logado or usuario_logado["tipo"] != "cliente":
        messagebox.showerror("Erro", "Somente clientes podem cancelar agendamentos!")
        return

    if not agendamento:
        messagebox.showerror("Erro", "Selecione um agendamento!")
        return

    with conectar() as conexao:
        conexao.execute(
            "DELETE FROM agendamentos WHERE id = ? AND cliente = ?",
            (agendamento["id"], usuario_logado["username"])
        )

    messagebox.showinfo("Sucesso", "Agendamento cancelado!")
    abrir_menu()


def proximos_dias(quantidade=14):
    hoje = date.today()
    dias = []
    for i in range(quantidade):
        dia = hoje + timedelta(days=i)
        dias.append(f"{dia.isoformat()} - {DIAS_SEMANA[dia.weekday()]}")
    return dias


def exportar_arquivos_json():
    with conectar() as conexao:
        usuarios = {
            linha["username"]: {"senha_hash": linha["senha_hash"], "tipo": linha["tipo"]}
            for linha in conexao.execute("SELECT username, senha_hash, tipo FROM usuarios")
        }
        servicos = {
            linha["nome"]: {"id": linha["id"], "prestador": linha["prestador"]}
            for linha in conexao.execute("SELECT id, nome, prestador FROM servicos")
        }
        agendamentos = {
            str(linha["id"]): {
                "cliente": linha["cliente"],
                "servico": linha["servico"],
                "data_hora": linha["data_hora"]
            }
            for linha in conexao.execute(
                """
                SELECT a.id, a.cliente, s.nome AS servico, a.data_hora
                FROM agendamentos a
                JOIN servicos s ON s.id = a.servico_id
                """
            )
        }

    salvar_json(USUARIOS_JSON, usuarios)
    salvar_json(SERVICOS_JSON, servicos)
    salvar_json(AGENDAMENTOS_JSON, agendamentos)
    messagebox.showinfo("Exportacao", "Backup JSON criado com sucesso!")


def salvar_json(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def sair():
    global usuario_logado
    usuario_logado = None
    abrir_login()


def abrir_login():
    limpar_tela()

    criar_label("Login", tamanho=18, pady=10)
    criar_label("Usuario:")
    entry_user = criar_entry()
    criar_label("Senha:")
    entry_pass = criar_entry(show="*")

    criar_botao("Entrar", lambda: login(entry_user.get(), entry_pass.get()), pady=10)
    criar_botao("Registrar Cliente", lambda: registrar_usuario("cliente", entry_user.get(), entry_pass.get()))
    criar_botao("Registrar Prestador", lambda: registrar_usuario("prestador", entry_user.get(), entry_pass.get()))
    criar_botao("Exportar Backup JSON", exportar_arquivos_json, pady=10)


def abrir_menu():
    limpar_tela()

    criar_label(
        f"Menu - {usuario_logado['username']} ({usuario_logado['tipo']})",
        tamanho=14,
        pady=10
    )

    if usuario_logado["tipo"] == "prestador":
        abrir_menu_prestador()
    elif usuario_logado["tipo"] == "cliente":
        abrir_menu_cliente()

    criar_botao("Atualizar", abrir_menu, pady=8)
    criar_botao("Sair", sair, pady=8)


def abrir_menu_prestador():
    criar_label("Adicionar Servico:")
    entry_servico = criar_entry()
    criar_botao("Adicionar", lambda: adicionar_servico(entry_servico.get()))

    criar_label("Seus servicos:", pady=8)
    lista_servicos = tk.Listbox(root, width=42, height=5)
    lista_servicos.pack(pady=3)

    servicos = listar_servicos_do_prestador(usuario_logado["username"])
    for servico in servicos:
        lista_servicos.insert(tk.END, servico["nome"])

    criar_botao(
        "Remover Servico Selecionado",
        lambda: remover_servico(obter_item_listbox(lista_servicos, servicos))
    )

    criar_label("Agendamentos dos seus servicos:", pady=10)
    lista_agendamentos = tk.Listbox(root, width=60, height=8)
    lista_agendamentos.pack(pady=3)

    for agendamento in listar_agendamentos_do_prestador(usuario_logado["username"]):
        lista_agendamentos.insert(
            tk.END,
            f"{agendamento['data_hora']} - {agendamento['servico']} - Cliente: {agendamento['cliente']}"
        )


def abrir_menu_cliente():
    criar_label("Servicos disponiveis:", pady=5)
    lista_servicos = tk.Listbox(root, width=55, height=7)
    lista_servicos.pack(pady=3)

    servicos = listar_servicos()
    for servico in servicos:
        lista_servicos.insert(tk.END, f"{servico['nome']} - Prestador: {servico['prestador']}")

    criar_label("Escolha o dia:")
    combo_dia = criar_combo(proximos_dias())

    criar_label("Escolha o horario:")
    combo_horario = criar_combo(HORARIOS)

    criar_botao(
        "Agendar Servico Selecionado",
        lambda: agendar_servico(
            obter_item_listbox(lista_servicos, servicos),
            combo_dia.get(),
            combo_horario.get()
        )
    )

    criar_label("Seus agendamentos:", pady=10)
    lista_agendamentos = tk.Listbox(root, width=60, height=8)
    lista_agendamentos.pack(pady=3)

    agendamentos = listar_agendamentos_do_cliente(usuario_logado["username"])
    for agendamento in agendamentos:
        lista_agendamentos.insert(
            tk.END,
            f"{agendamento['data_hora']} - {agendamento['servico']} - Prestador: {agendamento['prestador']}"
        )

    criar_botao(
        "Cancelar Agendamento Selecionado",
        lambda: cancelar_agendamento(obter_item_listbox(lista_agendamentos, agendamentos))
    )


root = tk.Tk()
root.title("Sistema de Agendamento")
root.geometry("540x690")
root.configure(bg=COR_FUNDO)


def main():
    iniciar_banco()
    abrir_login()
    root.mainloop()


if __name__ == "__main__":
    main()
