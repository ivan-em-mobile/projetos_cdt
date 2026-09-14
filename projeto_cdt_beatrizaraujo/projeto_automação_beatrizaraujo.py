# ============================================================
# CAIXA DE ENTRADA → AÇÃO
# APP DE AUTOMAÇÃO E TRIAGEM DE SOLICITAÇÕES
#
# Tecnologias:
# Tkinter | SQLite | JSON | Faker
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import json
import re
from datetime import datetime, date, timedelta
from faker import Faker


# ============================================================
# CONFIGURAÇÕES
# ============================================================

BANCO = "tarefas.db"
ARQUIVO_JSON = "tarefas.json"

fake = Faker("pt_BR")


# ============================================================
# CORES DO APP
# ============================================================

BG = "#F4F6FA"
SIDEBAR = "#151A24"
SIDEBAR_HOVER = "#202735"
WHITE = "#FFFFFF"
TEXT = "#202634"
TEXT_LIGHT = "#7B8494"
PRIMARY = "#5B5FEF"
PRIMARY_HOVER = "#484CD8"
BORDER = "#E3E6ED"

GREEN = "#20A36A"
GREEN_BG = "#E8F7F0"

RED = "#E05252"
RED_BG = "#FCECEC"

ORANGE = "#E99A35"
ORANGE_BG = "#FFF4E3"

BLUE = "#4C82E8"
BLUE_BG = "#EAF1FF"


# ============================================================
# BANCO DE DADOS
# ============================================================

def conectar_banco():
    return sqlite3.connect(BANCO)


def criar_banco():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto_original TEXT NOT NULL,
            titulo TEXT NOT NULL,
            responsavel TEXT NOT NULL,
            prazo TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            categoria TEXT NOT NULL,
            status TEXT NOT NULL,
            criada_em TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


# ============================================================
# RESPONSÁVEL
# ============================================================

def identificar_responsavel(texto):

    texto = " ".join(texto.strip().split())

    padroes = [

        r"\brespons[aá]vel\s*(?:é|e|:|-)?\s*(?:o|a)?\s*([A-Za-zÀ-ÿ]+)",

        r"\bpreciso\s+que\s+(?:o|a)?\s*([A-Za-zÀ-ÿ]+)"
        r"\s+(?:faça|faca|façam|fazer)\b",

        r"\bquero\s+que\s+(?:o|a)?\s*([A-Za-zÀ-ÿ]+)"
        r"\s+(?:faça|faca|fazer)\b",

        r"\b(?:o|a)\s+([A-Za-zÀ-ÿ]+)"
        r"\s+(?:precisa|deve|vai|irá|ira|fica|ficará|ficara)\b",

        r"\b([A-Za-zÀ-ÿ]+)"
        r"\s+(?:precisa|deve|vai|irá|ira|fica|ficará|ficara)\b",

        r"\btarefa\s+para\s+(?:o|a)?\s*([A-Za-zÀ-ÿ]+)",

        r"\bé\s+para\s+(?:o|a)?\s*([A-Za-zÀ-ÿ]+)",

        r"\b(?:pelo|pela)\s+([A-Za-zÀ-ÿ]+)"
    ]

    palavras_proibidas = {
        "precisa", "deve", "vai", "ira", "irá",
        "fica", "ficará", "ficara",
        "fazer", "faça", "faca", "façam",
        "entregar", "enviar", "realizar",
        "preparar", "criar", "organizar",
        "finalizar", "relatório", "relatorio",
        "documento", "documentos", "projeto",
        "trabalho", "tarefa", "planilha",
        "arquivo", "reunião", "reuniao",
        "cliente", "vendas", "venda",
        "pagamento", "sistema", "código",
        "codigo", "hoje", "amanhã",
        "amanha", "sexta", "segunda",
        "terça", "terca", "quarta",
        "quinta", "sábado", "sabado",
        "domingo", "urgente", "importante",
        "até", "ate", "para", "com",
        "de", "do", "da", "um", "uma"
    }

    for padrao in padroes:

        resultado = re.search(
            padrao,
            texto,
            re.IGNORECASE
        )

        if resultado:

            nome = resultado.group(1).strip()

            if nome.lower() not in palavras_proibidas:

                nome = re.sub(
                    r"[.,!?;:]+$",
                    "",
                    nome
                )

                return nome.title()

    # Para: João
    resultado = re.search(
        r"\bpara\s*:\s*([A-Za-zÀ-ÿ]+)",
        texto,
        re.IGNORECASE
    )

    if resultado:
        return resultado.group(1).title()

    return "Não definido"


# ============================================================
# PRAZO
# ============================================================

def formatar_data(data):
    return data.strftime("%d/%m/%Y")


def identificar_prazo(texto):

    texto = texto.lower().strip()

    hoje = date.today()

    # HOJE
    if re.search(r"\bhoje\b", texto):
        return formatar_data(hoje)

    # AMANHÃ
    if re.search(r"\bamanh[ãa]\b", texto):
        return formatar_data(
            hoje + timedelta(days=1)
        )

    # DATA COMPLETA
    resultado = re.search(
        r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b",
        texto
    )

    if resultado:

        dia = int(resultado.group(1))
        mes = int(resultado.group(2))
        ano = int(resultado.group(3))

        try:
            return formatar_data(
                date(ano, mes, dia)
            )
        except ValueError:
            return "Data inválida"

    # DATA SEM ANO
    resultado = re.search(
        r"\b(\d{1,2})[/-](\d{1,2})\b",
        texto
    )

    if resultado:

        dia = int(resultado.group(1))
        mes = int(resultado.group(2))
        ano = hoje.year

        try:

            data = date(
                ano,
                mes,
                dia
            )

            if data < hoje:
                data = date(
                    ano + 1,
                    mes,
                    dia
                )

            return formatar_data(data)

        except ValueError:
            return "Data inválida"

    # ATÉ DIA 20
    resultado = re.search(
        r"\b(?:até|ate)\s+(?:o\s+)?dia\s+(\d{1,2})",
        texto
    )

    if resultado:

        dia = int(resultado.group(1))

        mes = hoje.month
        ano = hoje.year

        try:

            data = date(
                ano,
                mes,
                dia
            )

            if data < hoje:

                if mes == 12:
                    data = date(
                        ano + 1,
                        1,
                        dia
                    )
                else:
                    data = date(
                        ano,
                        mes + 1,
                        dia
                    )

            return formatar_data(data)

        except ValueError:
            return "Data inválida"

    # DIAS DA SEMANA

    dias_semana = {
        "segunda": 0,
        "terça": 1,
        "terca": 1,
        "quarta": 2,
        "quinta": 3,
        "sexta": 4,
        "sábado": 5,
        "sabado": 5,
        "domingo": 6
    }

    for nome_dia, numero_dia in dias_semana.items():

        padrao = (
            r"\b(?:até\s+|ate\s+|na\s+|no\s+|para\s+|"
            r"nesta\s+|neste\s+|próxima\s+|proxima\s+|"
            r"próximo\s+|proximo\s+)?"
            + re.escape(nome_dia)
            + r"(?:-feira)?\b"
        )

        if re.search(
            padrao,
            texto
        ):

            diferenca = (
                numero_dia -
                hoje.weekday()
            ) % 7

            if diferenca == 0:
                diferenca = 7

            data = hoje + timedelta(
                days=diferenca
            )

            return formatar_data(data)

    # DATA POR EXTENSO

    meses = {
        "janeiro": 1,
        "fevereiro": 2,
        "março": 3,
        "marco": 3,
        "abril": 4,
        "maio": 5,
        "junho": 6,
        "julho": 7,
        "agosto": 8,
        "setembro": 9,
        "outubro": 10,
        "novembro": 11,
        "dezembro": 12
    }

    for nome_mes, numero_mes in meses.items():

        resultado = re.search(
            rf"\b(?:dia\s+)?(\d{{1,2}})\s+de\s+{nome_mes}\b",
            texto
        )

        if resultado:

            dia = int(resultado.group(1))
            ano = hoje.year

            try:

                data = date(
                    ano,
                    numero_mes,
                    dia
                )

                if data < hoje:

                    data = date(
                        ano + 1,
                        numero_mes,
                        dia
                    )

                return formatar_data(data)

            except ValueError:
                return "Data inválida"

    return "Não definido"


# ============================================================
# PRIORIDADE
# ============================================================

def identificar_prioridade(texto):

    texto = texto.lower()

    alta = [
        "urgente",
        "urgência",
        "urgencia",
        "imediato",
        "imediatamente",
        "agora",
        "crítico",
        "critico",
        "urgentemente",
        "pra ontem",
        "o quanto antes"
    ]

    media = [
        "importante",
        "prioridade",
        "atenção",
        "atencao"
    ]

    for palavra in alta:

        if palavra in texto:
            return "ALTA"

    for palavra in media:

        if palavra in texto:
            return "MÉDIA"

    return "BAIXA"


# ============================================================
# CATEGORIA
# ============================================================

def identificar_categoria(texto):

    texto = texto.lower()

    if any(p in texto for p in [
        "relatório",
        "relatorio",
        "documento",
        "planilha",
        "arquivo",
        "pdf"
    ]):
        return "DOCUMENTOS"

    if any(p in texto for p in [
        "reunião",
        "reuniao",
        "call",
        "meeting",
        "encontro"
    ]):
        return "REUNIÃO"

    if any(p in texto for p in [
        "cliente",
        "vendas",
        "venda",
        "proposta"
    ]):
        return "CLIENTE / VENDAS"

    if any(p in texto for p in [
        "pagamento",
        "cobrança",
        "cobranca",
        "financeiro",
        "dinheiro"
    ]):
        return "FINANCEIRO"

    if any(p in texto for p in [
        "programar",
        "programação",
        "programacao",
        "código",
        "codigo",
        "sistema",
        "software",
        "computador"
    ]):
        return "TECNOLOGIA"

    return "GERAL"


# ============================================================
# TÍTULO
# ============================================================

def criar_titulo(texto):

    titulo = texto.strip()

    remover = [
        "preciso que",
        "precisamos que",
        "por favor",
        "favor",
        "quero que"
    ]

    for palavra in remover:

        if titulo.lower().startswith(palavra):

            titulo = titulo[
                len(palavra):
            ].strip()

    titulo = titulo.rstrip(
        ".!?"
    )

    if len(titulo) > 70:
        titulo = titulo[:70] + "..."

    return titulo


# ============================================================
# INTERPRETAR
# ============================================================

def interpretar_solicitacao(texto):

    return {

        "texto_original": texto,

        "titulo": criar_titulo(texto),

        "responsavel":
            identificar_responsavel(texto),

        "prazo":
            identificar_prazo(texto),

        "prioridade":
            identificar_prioridade(texto),

        "categoria":
            identificar_categoria(texto),

        "status":
            "PENDENTE",

        "criada_em":
            datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )
    }


# ============================================================
# SQLITE - INSERIR
# ============================================================

def inserir_tarefa(tarefa):

    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO tarefas (
            texto_original,
            titulo,
            responsavel,
            prazo,
            prioridade,
            categoria,
            status,
            criada_em
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        tarefa["texto_original"],
        tarefa["titulo"],
        tarefa["responsavel"],
        tarefa["prazo"],
        tarefa["prioridade"],
        tarefa["categoria"],
        tarefa["status"],
        tarefa["criada_em"]

    ))

    conexao.commit()
    conexao.close()


# ============================================================
# SQLITE - BUSCAR
# ============================================================

def buscar_tarefas():

    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            titulo,
            responsavel,
            prazo,
            prioridade,
            categoria,
            status,
            criada_em
        FROM tarefas
        ORDER BY id DESC
    """)

    dados = cursor.fetchall()

    conexao.close()

    return dados


# ============================================================
# ESTATÍSTICAS
# ============================================================

def obter_estatisticas():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM tarefas"
    )

    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM tarefas
        WHERE status = 'PENDENTE'
    """)

    pendentes = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM tarefas
        WHERE status = 'CONCLUÍDA'
    """)

    concluidas = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM tarefas
        WHERE prioridade = 'ALTA'
    """)

    urgentes = cursor.fetchone()[0]

    conexao.close()

    return (
        total,
        pendentes,
        concluidas,
        urgentes
    )


# ============================================================
# ATUALIZAR TABELA
# ============================================================

def atualizar_tabela():

    for item in tabela.get_children():
        tabela.delete(item)

    tarefas = buscar_tarefas()

    termo = campo_busca.get().strip().lower()

    for tarefa in tarefas:

        if termo:

            texto = " ".join(
                str(valor)
                for valor in tarefa
            ).lower()

            if termo not in texto:
                continue

        tabela.insert(
            "",
            "end",
            values=tarefa
        )

    atualizar_cards()


# ============================================================
# CARDS
# ============================================================

def atualizar_cards():

    total, pendentes, concluidas, urgentes = \
        obter_estatisticas()

    valor_total.config(
        text=str(total)
    )

    valor_pendentes.config(
        text=str(pendentes)
    )

    valor_concluidas.config(
        text=str(concluidas)
    )

    valor_urgentes.config(
        text=str(urgentes)
    )


# ============================================================
# ADICIONAR
# ============================================================

def adicionar_tarefa():

    texto = campo_solicitacao.get(
        "1.0",
        tk.END
    ).strip()

    if not texto:

        messagebox.showwarning(
            "Atenção",
            "Digite uma solicitação."
        )

        return

    tarefa = interpretar_solicitacao(
        texto
    )

    inserir_tarefa(tarefa)

    campo_solicitacao.delete(
        "1.0",
        tk.END
    )

    atualizar_tabela()

    mostrar_resultado(tarefa)


# ============================================================
# RESULTADO DA ANÁLISE
# ============================================================

def mostrar_resultado(tarefa):

    janela_resultado = tk.Toplevel(
        janela
    )

    janela_resultado.title(
        "Tarefa criada"
    )

    janela_resultado.geometry(
        "500x430"
    )

    janela_resultado.configure(
        bg=WHITE
    )

    janela_resultado.resizable(
        False,
        False
    )

    tk.Label(
        janela_resultado,
        text="✓",
        font=("Arial", 40, "bold"),
        fg=GREEN,
        bg=WHITE
    ).pack(pady=(25, 0))

    tk.Label(
        janela_resultado,
        text="Tarefa criada com sucesso",
        font=("Arial", 18, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack(pady=5)

    tk.Label(
        janela_resultado,
        text="A solicitação foi analisada automaticamente.",
        font=("Arial", 10),
        fg=TEXT_LIGHT,
        bg=WHITE
    ).pack(pady=(0, 20))

    frame = tk.Frame(
        janela_resultado,
        bg=BG
    )

    frame.pack(
        fill="x",
        padx=35
    )

    informacoes = [
        ("Responsável", tarefa["responsavel"]),
        ("Prazo", tarefa["prazo"]),
        ("Prioridade", tarefa["prioridade"]),
        ("Categoria", tarefa["categoria"])
    ]

    for nome, valor in informacoes:

        linha = tk.Frame(
            frame,
            bg=BG
        )

        linha.pack(
            fill="x",
            padx=15,
            pady=9
        )

        tk.Label(
            linha,
            text=nome,
            font=("Arial", 10, "bold"),
            fg=TEXT_LIGHT,
            bg=BG
        ).pack(
            side="left"
        )

        tk.Label(
            linha,
            text=valor,
            font=("Arial", 10, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(
            side="right"
        )

    tk.Button(
        janela_resultado,
        text="Continuar",
        command=janela_resultado.destroy,
        bg=PRIMARY,
        fg=WHITE,
        activebackground=PRIMARY_HOVER,
        activeforeground=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=30,
        pady=10
    ).pack(
        pady=25
    )


# ============================================================
# CONCLUIR
# ============================================================

def concluir_tarefa():

    selecionado = tabela.selection()

    if not selecionado:

        messagebox.showwarning(
            "Atenção",
            "Selecione uma tarefa."
        )

        return

    item = tabela.item(
        selecionado[0]
    )

    id_tarefa = item["values"][0]

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE tarefas
        SET status = 'CONCLUÍDA'
        WHERE id = ?
    """, (id_tarefa,))

    conexao.commit()
    conexao.close()

    atualizar_tabela()


# ============================================================
# EXCLUIR
# ============================================================

def excluir_tarefa():

    selecionado = tabela.selection()

    if not selecionado:

        messagebox.showwarning(
            "Atenção",
            "Selecione uma tarefa."
        )

        return

    item = tabela.item(
        selecionado[0]
    )

    id_tarefa = item["values"][0]

    confirmar = messagebox.askyesno(
        "Excluir tarefa",
        "Tem certeza que deseja excluir esta tarefa?"
    )

    if not confirmar:
        return

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM tarefas WHERE id = ?",
        (id_tarefa,)
    )

    conexao.commit()
    conexao.close()

    atualizar_tabela()


# ============================================================
# JSON - EXPORTAR
# ============================================================

def exportar_json():

    tarefas = buscar_tarefas()

    dados = []

    for tarefa in tarefas:

        dados.append({

            "id": tarefa[0],

            "titulo": tarefa[1],

            "responsavel": tarefa[2],

            "prazo": tarefa[3],

            "prioridade": tarefa[4],

            "categoria": tarefa[5],

            "status": tarefa[6],

            "criada_em": tarefa[7]

        })

    arquivo = filedialog.asksaveasfilename(

        title="Exportar tarefas",

        defaultextension=".json",

        initialfile="tarefas.json",

        filetypes=[
            ("Arquivo JSON", "*.json")
        ]
    )

    if not arquivo:
        return

    with open(
        arquivo,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            dados,
            f,
            ensure_ascii=False,
            indent=4
        )

    messagebox.showinfo(
        "JSON",
        "Dados exportados com sucesso!"
    )


# ============================================================
# JSON - IMPORTAR
# ============================================================

def importar_json():

    arquivo = filedialog.askopenfilename(

        title="Importar tarefas",

        filetypes=[
            ("Arquivo JSON", "*.json")
        ]
    )

    if not arquivo:
        return

    try:

        with open(
            arquivo,
            "r",
            encoding="utf-8"
        ) as f:

            dados = json.load(f)

        conexao = conectar_banco()
        cursor = conexao.cursor()

        quantidade = 0

        for tarefa in dados:

            cursor.execute("""
                INSERT INTO tarefas (
                    texto_original,
                    titulo,
                    responsavel,
                    prazo,
                    prioridade,
                    categoria,
                    status,
                    criada_em
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (

                tarefa.get(
                    "titulo",
                    "Tarefa importada"
                ),

                tarefa.get(
                    "titulo",
                    "Tarefa importada"
                ),

                tarefa.get(
                    "responsavel",
                    "Não definido"
                ),

                tarefa.get(
                    "prazo",
                    "Não definido"
                ),

                tarefa.get(
                    "prioridade",
                    "BAIXA"
                ),

                tarefa.get(
                    "categoria",
                    "GERAL"
                ),

                tarefa.get(
                    "status",
                    "PENDENTE"
                ),

                tarefa.get(
                    "criada_em",
                    datetime.now().strftime(
                        "%d/%m/%Y %H:%M"
                    )
                )
            ))

            quantidade += 1

        conexao.commit()
        conexao.close()

        atualizar_tabela()

        messagebox.showinfo(
            "JSON",
            f"{quantidade} tarefa(s) importada(s)!"
        )

    except Exception as erro:

        messagebox.showerror(
            "Erro",
            f"Erro ao importar:\n{erro}"
        )


# ============================================================
# FAKER
# ============================================================

def gerar_dados_faker():

    atividades = [
        "entregar o relatório",
        "organizar o documento",
        "preparar a planilha",
        "enviar a proposta para o cliente",
        "finalizar o projeto"
    ]

    for atividade in atividades:

        nome = fake.first_name()

        data = fake.date_between(
            start_date="+1d",
            end_date="+30d"
        )

        data_formatada = data.strftime(
            "%d/%m/%Y"
        )

        texto = (
            f"{nome} precisa {atividade} "
            f"até {data_formatada}."
        )

        tarefa = interpretar_solicitacao(
            texto
        )

        inserir_tarefa(tarefa)

    atualizar_tabela()

    messagebox.showinfo(
        "Dados de teste",
        "5 tarefas foram geradas usando Faker."
    )


# ============================================================
# LIMPAR
# ============================================================

def limpar_campo():

    campo_solicitacao.delete(
        "1.0",
        tk.END
    )

    campo_solicitacao.focus()


# ============================================================
# TROCAR PÁGINA
# ============================================================

def mostrar_pagina(nome):

    if nome == "dashboard":

        titulo_pagina.config(
            text="Visão geral"
        )

        subtitulo_pagina.config(
            text="Acompanhe suas tarefas e atividades."
        )

        frame_nova.pack_forget()

        frame_lista.pack(
            fill="both",
            expand=True
        )

    elif nome == "nova":

        titulo_pagina.config(
            text="Nova solicitação"
        )

        subtitulo_pagina.config(
            text="Descreva a tarefa e deixe o sistema organizar."
        )

        frame_lista.pack_forget()

        frame_nova.pack(
            fill="both",
            expand=True
        )

        campo_solicitacao.focus()

    elif nome == "tarefas":

        titulo_pagina.config(
            text="Minhas tarefas"
        )

        subtitulo_pagina.config(
            text="Visualize e gerencie todas as tarefas."
        )

        frame_nova.pack_forget()

        frame_lista.pack(
            fill="both",
            expand=True
        )


# ============================================================
# JANELA PRINCIPAL
# ============================================================

criar_banco()

janela = tk.Tk()

janela.title(
    "Caixa de Entrada → Ação"
)

janela.geometry(
    "1280x760"
)

janela.minsize(
    1050,
    650
)

janela.configure(
    bg=BG
)


# ============================================================
# ESTILO
# ============================================================

style = ttk.Style()

style.theme_use(
    "clam"
)

style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT,
    rowheight=42,
    fieldbackground=WHITE,
    borderwidth=0,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=BG,
    foreground=TEXT_LIGHT,
    font=("Arial", 9, "bold"),
    borderwidth=0
)

style.map(
    "Treeview",
    background=[
        ("selected", "#E9EBFF")
    ],
    foreground=[
        ("selected", TEXT)
    ]
)


# ============================================================
# SIDEBAR
# ============================================================

sidebar = tk.Frame(
    janela,
    bg=SIDEBAR,
    width=240
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(
    False
)


# Logo

tk.Label(
    sidebar,
    text="C",
    font=("Arial", 22, "bold"),
    fg=WHITE,
    bg=PRIMARY,
    width=2,
    height=1
).pack(
    pady=(35, 8)
)

tk.Label(
    sidebar,
    text="CAIXA DE ENTRADA",
    font=("Arial", 10, "bold"),
    fg=WHITE,
    bg=SIDEBAR
).pack()

tk.Label(
    sidebar,
    text="→ AÇÃO",
    font=("Arial", 10),
    fg="#9CA5B5",
    bg=SIDEBAR
).pack(
    pady=(0, 40)
)


# ============================================================
# BOTÃO MENU
# ============================================================

def botao_menu(texto, comando):

    botao = tk.Button(
        sidebar,
        text=texto,
        command=comando,
        anchor="w",
        font=("Arial", 10, "bold"),
        fg="#C5CBD6",
        bg=SIDEBAR,
        activebackground=SIDEBAR_HOVER,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        padx=25,
        pady=14,
        cursor="hand2"
    )

    botao.pack(
        fill="x",
        padx=10,
        pady=3
    )

    return botao


botao_menu(
    "⌂   Visão geral",
    lambda: mostrar_pagina("dashboard")
)

botao_menu(
    "+   Nova solicitação",
    lambda: mostrar_pagina("nova")
)

botao_menu(
    "☷   Minhas tarefas",
    lambda: mostrar_pagina("tarefas")
)


# Espaço

tk.Frame(
    sidebar,
    bg=SIDEBAR
).pack(
    expand=True
)


# Informações

tk.Label(
    sidebar,
    text="AUTOMAÇÃO",
    font=("Arial", 8, "bold"),
    fg="#697386",
    bg=SIDEBAR
).pack(
    pady=(0, 5)
)

tk.Label(
    sidebar,
    text="Tkinter  •  SQLite\nJSON  •  Faker",
    font=("Arial", 8),
    fg="#697386",
    bg=SIDEBAR,
    justify="center"
).pack(
    pady=(0, 25)
)


# ============================================================
# CONTEÚDO
# ============================================================

conteudo = tk.Frame(
    janela,
    bg=BG
)

conteudo.pack(
    side="left",
    fill="both",
    expand=True
)


# ============================================================
# CABEÇALHO
# ============================================================

cabecalho = tk.Frame(
    conteudo,
    bg=BG
)

cabecalho.pack(
    fill="x",
    padx=35,
    pady=(30, 20)
)

titulo_pagina = tk.Label(
    cabecalho,
    text="Visão geral",
    font=("Arial", 24, "bold"),
    fg=TEXT,
    bg=BG
)

titulo_pagina.pack(
    anchor="w"
)

subtitulo_pagina = tk.Label(
    cabecalho,
    text="Acompanhe suas tarefas e atividades.",
    font=("Arial", 10),
    fg=TEXT_LIGHT,
    bg=BG
)

subtitulo_pagina.pack(
    anchor="w",
    pady=(5, 0)
)


# ============================================================
# CARDS
# ============================================================

cards = tk.Frame(
    conteudo,
    bg=BG
)

cards.pack(
    fill="x",
    padx=35,
    pady=(0, 20)
)


def criar_card(
    pai,
    titulo,
    valor_inicial,
    simbolo
):

    frame = tk.Frame(
        pai,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    tk.Label(
        frame,
        text=simbolo,
        font=("Arial", 18),
        fg=PRIMARY,
        bg=WHITE
    ).pack(
        anchor="w",
        padx=20,
        pady=(18, 5)
    )

    tk.Label(
        frame,
        text=titulo,
        font=("Arial", 9, "bold"),
        fg=TEXT_LIGHT,
        bg=WHITE
    ).pack(
        anchor="w",
        padx=20
    )

    valor = tk.Label(
        frame,
        text=valor_inicial,
        font=("Arial", 25, "bold"),
        fg=TEXT,
        bg=WHITE
    )

    valor.pack(
        anchor="w",
        padx=20,
        pady=(3, 18)
    )

    return valor


valor_total = criar_card(
    cards,
    "TOTAL DE TAREFAS",
    "0",
    "▣"
)

valor_pendentes = criar_card(
    cards,
    "PENDENTES",
    "0",
    "◷"
)

valor_concluidas = criar_card(
    cards,
    "CONCLUÍDAS",
    "0",
    "✓"
)

valor_urgentes = criar_card(
    cards,
    "ALTA PRIORIDADE",
    "0",
    "!"
)


# ============================================================
# FRAME NOVA TAREFA
# ============================================================

frame_nova = tk.Frame(
    conteudo,
    bg=BG
)

# Card principal

card_entrada = tk.Frame(
    frame_nova,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)

card_entrada.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=5
)


tk.Label(
    card_entrada,
    text="Descreva a solicitação",
    font=("Arial", 15, "bold"),
    fg=TEXT,
    bg=WHITE
).pack(
    anchor="w",
    padx=30,
    pady=(30, 5)
)

tk.Label(
    card_entrada,
    text=(
        "Escreva naturalmente. O sistema identifica "
        "responsável, prazo, prioridade e categoria."
    ),
    font=("Arial", 10),
    fg=TEXT_LIGHT,
    bg=WHITE
).pack(
    anchor="w",
    padx=30
)


campo_solicitacao = tk.Text(
    card_entrada,
    height=8,
    font=("Arial", 12),
    fg=TEXT,
    bg="#F8F9FC",
    insertbackground=TEXT,
    relief="flat",
    bd=0,
    wrap="word",
    padx=15,
    pady=15
)

campo_solicitacao.pack(
    fill="x",
    padx=30,
    pady=20
)

campo_solicitacao.insert(
    "1.0",
    "Exemplo: A Ana precisa fazer o relatório até sexta. É urgente."
)

campo_solicitacao.bind(
    "<FocusIn>",
    lambda e: (
        campo_solicitacao.delete(
            "1.0",
            tk.END
        )
        if campo_solicitacao.get(
            "1.0",
            tk.END
        ).strip().startswith("Exemplo:")
        else None
    )
)


# Botões

botoes_nova = tk.Frame(
    card_entrada,
    bg=WHITE
)

botoes_nova.pack(
    fill="x",
    padx=30,
    pady=(0, 30)
)


tk.Button(
    botoes_nova,
    text="🤖  Analisar solicitação",
    command=adicionar_tarefa,
    bg=PRIMARY,
    fg=WHITE,
    activebackground=PRIMARY_HOVER,
    activeforeground=WHITE,
    font=("Arial", 10, "bold"),
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=20,
    pady=12
).pack(
    side="left"
)

tk.Button(
    botoes_nova,
    text="Limpar",
    command=limpar_campo,
    bg=BG,
    fg=TEXT,
    activebackground=BORDER,
    font=("Arial", 10, "bold"),
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=20,
    pady=12
).pack(
    side="left",
    padx=10
)


# ============================================================
# FRAME LISTA
# ============================================================

frame_lista = tk.Frame(
    conteudo,
    bg=BG
)


# Busca

barra = tk.Frame(
    frame_lista,
    bg=BG
)

barra.pack(
    fill="x",
    padx=35,
    pady=(0, 15)
)


campo_busca = tk.Entry(
    barra,
    font=("Arial", 10),
    bg=WHITE,
    fg=TEXT,
    relief="flat",
    bd=0
)

campo_busca.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=11,
    padx=(0, 10)
)

campo_busca.insert(
    0,
    ""
)

campo_busca.bind(
    "<KeyRelease>",
    lambda event: atualizar_tabela()
)


tk.Button(
    barra,
    text="+ Nova tarefa",
    command=lambda: mostrar_pagina("nova"),
    bg=PRIMARY,
    fg=WHITE,
    activebackground=PRIMARY_HOVER,
    activeforeground=WHITE,
    font=("Arial", 10, "bold"),
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=18,
    pady=10
).pack(
    side="right"
)


# ============================================================
# TABELA
# ============================================================

card_tabela = tk.Frame(
    frame_lista,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)

card_tabela.pack(
    fill="both",
    expand=True,
    padx=35
)


colunas = (
    "ID",
    "Título",
    "Responsável",
    "Prazo",
    "Prioridade",
    "Categoria",
    "Status",
    "Criada em"
)

tabela = ttk.Treeview(
    card_tabela,
    columns=colunas,
    show="headings",
    selectmode="browse"
)


larguras = {
    "ID": 45,
    "Título": 270,
    "Responsável": 125,
    "Prazo": 105,
    "Prioridade": 95,
    "Categoria": 145,
    "Status": 105,
    "Criada em": 130
}


for coluna in colunas:

    tabela.heading(
        coluna,
        text=coluna
    )

    tabela.column(
        coluna,
        width=larguras[coluna],
        minwidth=60,
        anchor="center"
    )


# Tags de cores

tabela.tag_configure(
    "alta",
    foreground=RED
)

tabela.tag_configure(
    "media",
    foreground=ORANGE
)

tabela.tag_configure(
    "baixa",
    foreground=GREEN
)

tabela.tag_configure(
    "concluida",
    foreground=GREEN
)


# Scroll

scroll = ttk.Scrollbar(
    card_tabela,
    orient="vertical",
    command=tabela.yview
)

tabela.configure(
    yscrollcommand=scroll.set
)

scroll.pack(
    side="right",
    fill="y"
)

tabela.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# ============================================================
# AÇÕES DA TABELA
# ============================================================

acoes = tk.Frame(
    conteudo,
    bg=BG
)

acoes.pack(
    fill="x",
    padx=35,
    pady=15
)


tk.Button(
    acoes,
    text="✓  Concluir",
    command=concluir_tarefa,
    bg=GREEN_BG,
    fg=GREEN,
    activebackground="#D6F1E5",
    font=("Arial", 9, "bold"),
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=15,
    pady=9
).pack(
    side="left",
    padx=(0, 7)
)


tk.Button(
    acoes,
    text="🗑  Excluir",
    command=excluir_tarefa,
    bg=RED_BG,
    fg=RED,
    activebackground="#F7DADA",
    font=("Arial", 9, "bold"),
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=15,
    pady=9
).pack(
    side="left",
    padx=7
)


tk.Button(
    acoes,
    text="↓  Exportar JSON",
    command=exportar_json,
    bg=BLUE_BG,
    fg=BLUE,
    activebackground="#DCE7FC",
    font=("Arial", 9, "bold"),
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=15,
    pady=9
).pack(
    side="right",
    padx=5
)


tk.Button(
    acoes,
    text="↑  Importar JSON",
    command=importar_json,
    bg=WHITE,
    fg=TEXT,
    activebackground=BG,
    font=("Arial", 9, "bold"),
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=15,
    pady=9
).pack(
    side="right",
    padx=5
)


tk.Button(
    acoes,
    text="✦  Gerar testes",
    command=gerar_dados_faker,
    bg=ORANGE_BG,
    fg=ORANGE,
    activebackground="#FCE9C8",
    font=("Arial", 9, "bold"),
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=15,
    pady=9
).pack(
    side="right",
    padx=5
)


# ============================================================
# INICIALIZAÇÃO
# ============================================================

mostrar_pagina(
    "dashboard"
)

atualizar_tabela()


# ============================================================
# EXECUTAR
# ============================================================

janela.mainloop()