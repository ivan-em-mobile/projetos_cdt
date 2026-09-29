"""
"""


import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json
import random
from datetime import datetime

try:
    from faker import Faker
    fake = Faker("pt_BR")
except ImportError:
    fake = None


# =====================================================
# CONFIGURAÇÕES
# =====================================================

NOME_LOJA = "Nação dos Mantos"
BANCO = "loja_camisas.db"
ARQUIVO_JSON = "configuracao.json"
PRECO_PERSONALIZACAO = 20.00

times = [
    "Athletico-PR",
    "Atletico-MG",
    "Bahia",
    "Botafogo",
    "Chapecoense",
    "Corinthians",
    "Coritiba",
    "Cruzeiro",
    "Flamengo",
    "Fluminense",
    "Gremio",
    "Internacional",
    "Mirassol",
    "Palmeiras",
    "Red Bull Bragantino",
    "Remo",
    "Santos",
    "Sao Paulo",
    "Vasco",
    "Vitoria"
]

precos = {
    "Athletico-PR": 149.90,
    "Atletico-MG": 159.90,
    "Bahia": 139.90,
    "Botafogo": 149.90,
    "Chapecoense": 119.90,
    "Corinthians": 169.90,
    "Coritiba": 129.90,
    "Cruzeiro": 159.90,
    "Flamengo": 179.90,
    "Fluminense": 159.90,
    "Gremio": 159.90,
    "Internacional": 159.90,
    "Mirassol": 119.90,
    "Palmeiras": 179.90,
    "Red Bull Bragantino": 139.90,
    "Remo": 119.90,
    "Santos": 149.90,
    "Sao Paulo": 169.90,
    "Vasco": 159.90,
    "Vitoria": 129.90
}

siglas = {
    "Athletico-PR": "CAP",
    "Atletico-MG": "CAM",
    "Bahia": "BAH",
    "Botafogo": "BOT",
    "Chapecoense": "CHA",
    "Corinthians": "COR",
    "Coritiba": "CFC",
    "Cruzeiro": "CRU",
    "Flamengo": "FLA",
    "Fluminense": "FLU",
    "Gremio": "GRE",
    "Internacional": "INT",
    "Mirassol": "MIR",
    "Palmeiras": "PAL",
    "Red Bull Bragantino": "RBB",
    "Remo": "REM",
    "Santos": "SAN",
    "Sao Paulo": "SPFC",
    "Vasco": "VAS",
    "Vitoria": "VIT"
}

cores_escudos = {
    "Athletico-PR": "#c62828",
    "Atletico-MG": "#212121",
    "Bahia": "#1565c0",
    "Botafogo": "#111111",
    "Chapecoense": "#2e7d32",
    "Corinthians": "#424242",
    "Coritiba": "#388e3c",
    "Cruzeiro": "#1565c0",
    "Flamengo": "#b71c1c",
    "Fluminense": "#00695c",
    "Gremio": "#0277bd",
    "Internacional": "#d32f2f",
    "Mirassol": "#f9a825",
    "Palmeiras": "#1b5e20",
    "Red Bull Bragantino": "#d32f2f",
    "Remo": "#283593",
    "Santos": "#212121",
    "Sao Paulo": "#c62828",
    "Vasco": "#212121",
    "Vitoria": "#c62828"
}


# =====================================================
# BANCO DE DADOS
# =====================================================

conexao = sqlite3.connect(BANCO)
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    detalhes TEXT NOT NULL,
    total REAL NOT NULL,
    data TEXT NOT NULL,
    rastreio TEXT NOT NULL,
    pagamento TEXT NOT NULL
)
""")

cursor.execute("SELECT COUNT(*) FROM produtos")
quantidade_produtos = cursor.fetchone()[0]

if quantidade_produtos == 0:
    for time in times:
        cursor.execute(
            """
            INSERT INTO produtos (nome, preco)
            VALUES (?, ?)
            """,
            (
                "Camisa " + time,
                precos[time]
            )
        )

conexao.commit()


# =====================================================
# ARQUIVO JSON
# =====================================================

configuracao = {
    "loja": NOME_LOJA,
    "categoria": "Camisas de times brasileiros",
    "times": times
}

with open(
    ARQUIVO_JSON,
    "w",
    encoding="utf-8"
) as arquivo:
    json.dump(
        configuracao,
        arquivo,
        ensure_ascii=False,
        indent=4
    )


# =====================================================
# VARIÁVEIS
# =====================================================

janela = tk.Tk()
janela.title(NOME_LOJA)
janela.state("zoomed")
janela.configure(bg="white")

carrinho = []
time_selecionado = None
botoes_times = []


# =====================================================
# FUNÇÃO PARA CRIAR ESCUDO
# =====================================================

def criar_escudo(parent, time):
    """
    Cria um escudo desenhado com a sigla do time.
    """

    canvas = tk.Canvas(
        parent,
        width=75,
        height=85,
        bg="white",
        highlightthickness=0
    )

    cor = cores_escudos.get(
        time,
        "#333333"
    )

    # Parte externa do escudo
    canvas.create_polygon(
        10, 5,
        65, 5,
        65, 55,
        38, 78,
        10, 55,
        fill=cor,
        outline="#000000",
        width=2
    )

    # Parte interna
    canvas.create_polygon(
        17, 12,
        58, 12,
        58, 51,
        38, 69,
        17, 51,
        fill="white",
        outline="#000000",
        width=1
    )

    # Sigla do time
    canvas.create_text(
        38,
        40,
        text=siglas.get(time, "TIME"),
        font=("Arial", 10, "bold"),
        fill=cor
    )

    return canvas


# =====================================================
# FUNÇÕES DO PROGRAMA
# =====================================================

def selecionar_time(time):
    global time_selecionado

    time_selecionado = time

    label_selecionado.config(
        text=f"Time selecionado: {time}"
    )

    for botao in botoes_times:
        botao.config(
            bg="#b71c1c",
            fg="white"
        )

    for botao, nome_time in botoes_times_dados:
        if nome_time == time:
            botao.config(
                bg="#2e7d32",
                fg="white"
            )


def atualizar_total():
    total = sum(
        item["subtotal"]
        for item in carrinho
    )

    label_total.config(
        text=f"Total: R$ {total:.2f}".replace(".", ",")
    )


def atualizar_carrinho():
    lista_carrinho.delete(
        *lista_carrinho.get_children()
    )

    for item in carrinho:
        personalizado = "Sim" if item["personalizado"] else "Não"

        lista_carrinho.insert(
            "",
            "end",
            values=(
                item["produto"],
                item["tamanho"],
                personalizado,
                item["quantidade"],
                f"R$ {item['subtotal']:.2f}".replace(".", ",")
            )
        )

    atualizar_total()


def ativar_personalizacao():
    if var_personalizar.get():
        campo_nome.config(state="normal")
        campo_numero.config(state="normal")
    else:
        campo_nome.delete(0, tk.END)
        campo_numero.delete(0, tk.END)

        campo_nome.config(state="disabled")
        campo_numero.config(state="disabled")


def adicionar_carrinho():
    if time_selecionado is None:
        messagebox.showwarning(
            "Aviso",
            "Selecione um time primeiro."
        )
        return

    tamanho = combo_tamanho.get()

    if tamanho == "":
        messagebox.showwarning(
            "Aviso",
            "Selecione o tamanho da camisa."
        )
        return

    try:
        quantidade = int(
            campo_quantidade.get()
        )

        if quantidade <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Erro",
            "Digite uma quantidade válida."
        )
        return

    personalizado = var_personalizar.get()
    nome = campo_nome.get().strip()
    numero = campo_numero.get().strip()

    if personalizado:
        if nome == "" or numero == "":
            messagebox.showwarning(
                "Aviso",
                "Preencha o nome e o número da camisa."
            )
            return

    preco = precos[time_selecionado]

    if personalizado:
        preco += PRECO_PERSONALIZACAO

    subtotal = preco * quantidade

    item = {
        "produto": "Camisa " + time_selecionado,
        "tamanho": tamanho,
        "personalizado": personalizado,
        "nome": nome,
        "numero": numero,
        "quantidade": quantidade,
        "subtotal": subtotal
    }

    carrinho.append(item)
    atualizar_carrinho()

    messagebox.showinfo(
        "Sucesso",
        "Camisa adicionada ao carrinho."
    )


def remover_item():
    selecionado = lista_carrinho.selection()

    if not selecionado:
        messagebox.showwarning(
            "Aviso",
            "Selecione um item para remover."
        )
        return

    indice = lista_carrinho.index(
        selecionado[0]
    )

    carrinho.pop(indice)
    atualizar_carrinho()


def gerar_cliente():
    if fake:
        nome = fake.name()
    else:
        nome = "Cliente Teste"

    campo_cliente.delete(0, tk.END)
    campo_cliente.insert(0, nome)


def finalizar_pedido():
    if not carrinho:
        messagebox.showwarning(
            "Aviso",
            "O carrinho está vazio."
        )
        return

    cliente = campo_cliente.get().strip()
    pagamento = combo_pagamento.get()

    if cliente == "":
        messagebox.showwarning(
            "Aviso",
            "Digite o nome do cliente."
        )
        return

    if pagamento == "":
        messagebox.showwarning(
            "Aviso",
            "Selecione uma forma de pagamento."
        )
        return

    total = sum(
        item["subtotal"]
        for item in carrinho
    )

    detalhes = []

    for item in carrinho:
        descricao = (
            f"{item['quantidade']}x "
            f"{item['produto']} "
            f"Tamanho: {item['tamanho']}"
        )

        if item["personalizado"]:
            descricao += (
                f" Nome: {item['nome']}"
                f" Número: {item['numero']}"
            )

        detalhes.append(descricao)

    detalhes_texto = " | ".join(detalhes)

    data = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    rastreio = (
        "NM" +
        str(random.randint(100000, 999999)) +
        "BR"
    )

    cursor.execute(
        """
        INSERT INTO pedidos (
            cliente,
            detalhes,
            total,
            data,
            rastreio,
            pagamento
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            cliente,
            detalhes_texto,
            total,
            data,
            rastreio,
            pagamento
        )
    )

    conexao.commit()

    carrinho.clear()
    atualizar_carrinho()

    campo_cliente.delete(0, tk.END)
    combo_pagamento.set("")

    messagebox.showinfo(
        "Pedido Finalizado",
        f"Pedido realizado com sucesso!\n\n"
        f"Cliente: {cliente}\n"
        f"Pagamento: {pagamento}\n"
        f"Código de rastreio: {rastreio}\n"
        f"Total: R$ {total:.2f}".replace(".", ",")
    )


def mostrar_historico():
    tela = tk.Toplevel(janela)
    tela.title("Histórico de Pedidos")
    tela.geometry("1100x450")
    tela.configure(bg="white")

    tabela_pedidos = ttk.Treeview(
        tela,
        columns=(
            "id",
            "cliente",
            "detalhes",
            "total",
            "data",
            "rastreio",
            "pagamento"
        ),
        show="headings"
    )

    colunas = {
        "id": "ID",
        "cliente": "Cliente",
        "detalhes": "Itens",
        "total": "Total",
        "data": "Data",
        "rastreio": "Rastreio",
        "pagamento": "Pagamento"
    }

    for coluna, titulo in colunas.items():
        tabela_pedidos.heading(
            coluna,
            text=titulo
        )

    tabela_pedidos.column(
        "id",
        width=40
    )

    tabela_pedidos.column(
        "cliente",
        width=130
    )

    tabela_pedidos.column(
        "detalhes",
        width=380
    )

    tabela_pedidos.column(
        "total",
        width=90
    )

    tabela_pedidos.column(
        "data",
        width=120
    )

    tabela_pedidos.column(
        "rastreio",
        width=130
    )

    tabela_pedidos.column(
        "pagamento",
        width=120
    )

    tabela_pedidos.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    cursor.execute("""
        SELECT
            id,
            cliente,
            detalhes,
            total,
            data,
            rastreio,
            pagamento
        FROM pedidos
        ORDER BY id DESC
    """)

    pedidos = cursor.fetchall()

    for pedido in pedidos:
        tabela_pedidos.insert(
            "",
            "end",
            values=(
                pedido[0],
                pedido[1],
                pedido[2],
                f"R$ {pedido[3]:.2f}".replace(".", ","),
                pedido[4],
                pedido[5],
                pedido[6]
            )
        )


def fechar_programa():
    conexao.close()
    janela.destroy()


# =====================================================
# INTERFACE
# =====================================================

lado_esquerdo = tk.Frame(
    janela,
    bg="white",
    padx=15,
    pady=15
)

lado_esquerdo.pack(
    side="left",
    fill="both",
    expand=True
)

lado_direito = tk.Frame(
    janela,
    bg="#c62828",
    padx=15,
    pady=15
)

lado_direito.pack(
    side="right",
    fill="both",
    expand=True
)

titulo = tk.Label(
    lado_esquerdo,
    text=NOME_LOJA,
    font=("Arial", 24, "bold"),
    bg="white",
    fg="#b71c1c"
)

titulo.pack(
    anchor="w"
)

subtitulo = tk.Label(
    lado_esquerdo,
    text="Loja de camisas dos times brasileiros",
    font=("Arial", 11),
    bg="white",
    fg="#555555"
)

subtitulo.pack(
    anchor="w",
    pady=(0, 10)
)


# =====================================================
# LISTA DE TIMES COM ESCUDOS
# =====================================================

frame_times = tk.LabelFrame(
    lado_esquerdo,
    text="Escolha seu time",
    bg="white",
    padx=8,
    pady=8
)

frame_times.pack(
    fill="both",
    expand=True
)

canvas_times = tk.Canvas(
    frame_times,
    bg="white",
    highlightthickness=0
)

barra_times = ttk.Scrollbar(
    frame_times,
    orient="vertical",
    command=canvas_times.yview
)

lista_times = tk.Frame(
    canvas_times,
    bg="white"
)

lista_times.bind(
    "<Configure>",
    lambda evento: canvas_times.configure(
        scrollregion=canvas_times.bbox("all")
    )
)

canvas_times.create_window(
    (0, 0),
    window=lista_times,
    anchor="nw"
)

canvas_times.configure(
    yscrollcommand=barra_times.set
)

canvas_times.pack(
    side="left",
    fill="both",
    expand=True
)

barra_times.pack(
    side="right",
    fill="y"
)

botoes_times_dados = []

for numero, time in enumerate(times, start=1):

    linha = tk.Frame(
        lista_times,
        bg="white",
        relief="solid",
        borderwidth=1
    )

    linha.pack(
        fill="x",
        padx=5,
        pady=4
    )

    escudo = criar_escudo(
        linha,
        time
    )

    escudo.pack(
        side="left",
        padx=5
    )

    informacoes = tk.Label(
        linha,
        text=(
            f"{numero} - {time}\n"
            f"Preço: R$ {precos[time]:.2f}".replace(".", ",")
        ),
        font=("Arial", 11, "bold"),
        bg="white",
        anchor="w"
    )

    informacoes.pack(
        side="left",
        fill="x",
        expand=True
    )

    botao = tk.Button(
        linha,
        text="Selecionar",
        bg="#b71c1c",
        fg="white",
        command=lambda nome=time: selecionar_time(nome)
    )

    botao.pack(
        side="right",
        padx=8
    )

    botoes_times.append(botao)
    botoes_times_dados.append(
        (botao, time)
    )


label_selecionado = tk.Label(
    lado_esquerdo,
    text="Time selecionado: nenhum",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#2e7d32"
)

label_selecionado.pack(
    anchor="w",
    pady=8
)


# =====================================================
# OPÇÕES
# =====================================================

frame_opcoes = tk.LabelFrame(
    lado_esquerdo,
    text="Opções da camisa",
    bg="white",
    padx=8,
    pady=8
)

frame_opcoes.pack(
    fill="x",
    pady=5
)

tk.Label(
    frame_opcoes,
    text="Tamanho:",
    bg="white"
).pack(
    side="left"
)

combo_tamanho = ttk.Combobox(
    frame_opcoes,
    values=[
        "PP",
        "P",
        "M",
        "G",
        "GG",
        "XG"
    ],
    state="readonly",
    width=6
)

combo_tamanho.set("M")

combo_tamanho.pack(
    side="left",
    padx=8
)

tk.Label(
    frame_opcoes,
    text="Quantidade:",
    bg="white"
).pack(
    side="left"
)

campo_quantidade = tk.Entry(
    frame_opcoes,
    width=6
)

campo_quantidade.insert(
    0,
    "1"
)

campo_quantidade.pack(
    side="left",
    padx=8
)

var_personalizar = tk.BooleanVar(
    value=False
)

tk.Checkbutton(
    frame_opcoes,
    text="Personalizar + R$ 20,00",
    variable=var_personalizar,
    command=ativar_personalizacao,
    bg="white"
).pack(
    anchor="w",
    pady=8
)

linha_personalizacao = tk.Frame(
    frame_opcoes,
    bg="white"
)

linha_personalizacao.pack(
    fill="x"
)

tk.Label(
    linha_personalizacao,
    text="Nome:",
    bg="white"
).pack(
    side="left"
)

campo_nome = tk.Entry(
    linha_personalizacao,
    width=15,
    state="disabled"
)

campo_nome.pack(
    side="left",
    padx=5
)

tk.Label(
    linha_personalizacao,
    text="Número:",
    bg="white"
).pack(
    side="left"
)

campo_numero = tk.Entry(
    linha_personalizacao,
    width=6,
    state="disabled"
)

campo_numero.pack(
    side="left",
    padx=5
)

tk.Button(
    lado_esquerdo,
    text="Adicionar ao Carrinho",
    command=adicionar_carrinho,
    bg="#b71c1c",
    fg="white",
    font=("Arial", 11, "bold")
).pack(
    fill="x",
    pady=5
)


# =====================================================
# CARRINHO
# =====================================================

tk.Label(
    lado_direito,
    text="CARRINHO",
    font=("Arial", 20, "bold"),
    bg="#c62828",
    fg="white"
).pack(
    anchor="w"
)

frame_carrinho = tk.LabelFrame(
    lado_direito,
    text="Produtos selecionados",
    bg="#c62828",
    fg="white",
    padx=8,
    pady=8
)

frame_carrinho.pack(
    fill="both",
    expand=True,
    pady=8
)

lista_carrinho = ttk.Treeview(
    frame_carrinho,
    columns=(
        "produto",
        "tamanho",
        "personalizado",
        "quantidade",
        "subtotal"
    ),
    show="headings"
)

colunas_carrinho = {
    "produto": "Produto",
    "tamanho": "Tam.",
    "personalizado": "Pers.",
    "quantidade": "Qtd.",
    "subtotal": "Subtotal"
}

for coluna, titulo in colunas_carrinho.items():
    lista_carrinho.heading(
        coluna,
        text=titulo
    )

lista_carrinho.pack(
    fill="both",
    expand=True
)

tk.Button(
    frame_carrinho,
    text="Remover Item",
    command=remover_item,
    bg="#8e0000",
    fg="white"
).pack(
    pady=5
)

label_total = tk.Label(
    lado_direito,
    text="Total: R$ 0,00",
    font=("Arial", 17, "bold"),
    bg="#c62828",
    fg="white"
)

label_total.pack(
    anchor="e",
    pady=8
)


# =====================================================
# CLIENTE E PAGAMENTO
# =====================================================

frame_cliente = tk.LabelFrame(
    lado_direito,
    text="Dados do cliente",
    bg="#c62828",
    fg="white",
    padx=8,
    pady=8
)

frame_cliente.pack(
    fill="x"
)

tk.Label(
    frame_cliente,
    text="Nome do cliente:",
    bg="#c62828",
    fg="white"
).pack(
    anchor="w"
)

campo_cliente = tk.Entry(
    frame_cliente
)

campo_cliente.pack(
    fill="x",
    pady=5
)

tk.Button(
    frame_cliente,
    text="Gerar Cliente Faker",
    command=gerar_cliente,
    bg="#6a1b9a",
    fg="white"
).pack(
    fill="x"
)

tk.Label(
    frame_cliente,
    text="Forma de pagamento:",
    bg="#c62828",
    fg="white"
).pack(
    anchor="w",
    pady=(8, 2)
)

combo_pagamento = ttk.Combobox(
    frame_cliente,
    values=[
        "Pix",
        "Cartão de Crédito",
        "Cartão de Débito",
        "Dinheiro"
    ],
    state="readonly"
)

combo_pagamento.pack(
    fill="x"
)

tk.Button(
    lado_direito,
    text="FINALIZAR PEDIDO",
    command=finalizar_pedido,
    bg="#2e7d32",
    fg="white",
    font=("Arial", 12, "bold")
).pack(
    fill="x",
    pady=8
)

tk.Button(
    lado_direito,
    text="Histórico de Pedidos",
    command=mostrar_historico,
    bg="#333333",
    fg="white"
).pack(
    fill="x"
)


# =====================================================
# INICIAR PROGRAMA
# =====================================================

janela.protocol(
    "WM_DELETE_WINDOW",
    fechar_programa
)

janela.mainloop()