import tkinter as tk
from tkinter import messagebox, ttk

from app.services.relatorio_service import (
    relatorio_acessos,
    relatorio_financeiro,
    relatorio_geral,
    relatorio_planos,
)


class TelaRelatorios:
    def __init__(self, container):
        self.container = container

        self.criar_tela()

    def criar_tela(self):
        self.criar_cabecalho()
        self.criar_abas()

        self.criar_aba_geral()
        self.criar_aba_financeiro()
        self.criar_aba_acessos()
        self.criar_aba_planos()

        self.atualizar_relatorios()

    def criar_cabecalho(self):
        cabecalho = tk.Frame(
            self.container,
            bg="white",
            height=85,
        )

        cabecalho.pack(
            fill="x"
        )

        cabecalho.pack_propagate(
            False
        )

        titulo = tk.Label(
            cabecalho,
            text="Relatórios",
            bg="white",
            fg="#111111",
            font=(
                "Arial",
                22,
                "bold",
            ),
        )

        titulo.pack(
            side="left",
            padx=30,
            pady=25,
        )

        botao_atualizar = tk.Button(
            cabecalho,
            text="Atualizar",
            command=self.atualizar_relatorios,
            bg="#ffd400",
            fg="#111111",
            activebackground="#e5bf00",
            relief="flat",
            padx=20,
            pady=8,
            font=(
                "Arial",
                10,
                "bold",
            ),
            cursor="hand2",
        )

        botao_atualizar.pack(
            side="right",
            padx=30,
        )

    def criar_abas(self):
        area = tk.Frame(
            self.container,
            bg="#f4f4f4",
        )

        area.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30,
        )

        self.notebook = ttk.Notebook(
            area
        )

        self.notebook.pack(
            fill="both",
            expand=True,
        )

        self.aba_geral = tk.Frame(
            self.notebook,
            bg="#f4f4f4",
        )

        self.aba_financeiro = tk.Frame(
            self.notebook,
            bg="#f4f4f4",
        )

        self.aba_acessos = tk.Frame(
            self.notebook,
            bg="#f4f4f4",
        )

        self.aba_planos = tk.Frame(
            self.notebook,
            bg="#f4f4f4",
        )

        self.notebook.add(
            self.aba_geral,
            text="Geral",
        )

        self.notebook.add(
            self.aba_financeiro,
            text="Financeiro",
        )

        self.notebook.add(
            self.aba_acessos,
            text="Acessos",
        )

        self.notebook.add(
            self.aba_planos,
            text="Planos",
        )

    # ==================================================
    # RELATÓRIO GERAL
    # ==================================================

    def criar_aba_geral(self):
        titulo = tk.Label(
            self.aba_geral,
            text="Visão geral da academia",
            bg="#f4f4f4",
            fg="#111111",
            font=(
                "Arial",
                16,
                "bold",
            ),
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(25, 20),
        )

        self.cards_geral = tk.Frame(
            self.aba_geral,
            bg="#f4f4f4",
        )

        self.cards_geral.pack(
            fill="x",
            padx=15,
        )

        for coluna in range(4):
            self.cards_geral.columnconfigure(
                coluna,
                weight=1,
            )

        self.valor_total_alunos = (
            self.criar_card(
                self.cards_geral,
                0,
                "Total de alunos",
            )
        )

        self.valor_alunos_ativos = (
            self.criar_card(
                self.cards_geral,
                1,
                "Alunos ativos",
            )
        )

        self.valor_assinaturas_ativas = (
            self.criar_card(
                self.cards_geral,
                2,
                "Assinaturas ativas",
            )
        )

        self.valor_planos_ativos = (
            self.criar_card(
                self.cards_geral,
                3,
                "Planos ativos",
            )
        )

    # ==================================================
    # RELATÓRIO FINANCEIRO
    # ==================================================

    def criar_aba_financeiro(self):
        titulo = tk.Label(
            self.aba_financeiro,
            text="Resumo financeiro",
            bg="#f4f4f4",
            fg="#111111",
            font=(
                "Arial",
                16,
                "bold",
            ),
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(25, 20),
        )

        primeira_linha = tk.Frame(
            self.aba_financeiro,
            bg="#f4f4f4",
        )

        primeira_linha.pack(
            fill="x",
            padx=15,
        )

        for coluna in range(3):
            primeira_linha.columnconfigure(
                coluna,
                weight=1,
            )

        self.valor_recebido = self.criar_card(
            primeira_linha,
            0,
            "Total recebido",
        )

        self.valor_pendente = self.criar_card(
            primeira_linha,
            1,
            "Valor pendente",
        )

        self.valor_atrasado = self.criar_card(
            primeira_linha,
            2,
            "Valor em atraso",
        )

        segunda_linha = tk.Frame(
            self.aba_financeiro,
            bg="#f4f4f4",
        )

        segunda_linha.pack(
            fill="x",
            padx=15,
            pady=(15, 0),
        )

        for coluna in range(3):
            segunda_linha.columnconfigure(
                coluna,
                weight=1,
            )

        self.qtd_pagos = self.criar_card(
            segunda_linha,
            0,
            "Pagamentos realizados",
        )

        self.qtd_pendentes = self.criar_card(
            segunda_linha,
            1,
            "Pagamentos pendentes",
        )

        self.qtd_atrasados = self.criar_card(
            segunda_linha,
            2,
            "Pagamentos atrasados",
        )

    # ==================================================
    # RELATÓRIO DE ACESSOS
    # ==================================================

    def criar_aba_acessos(self):
        titulo = tk.Label(
            self.aba_acessos,
            text="Controle de acessos",
            bg="#f4f4f4",
            fg="#111111",
            font=(
                "Arial",
                16,
                "bold",
            ),
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(25, 20),
        )

        cards = tk.Frame(
            self.aba_acessos,
            bg="#f4f4f4",
        )

        cards.pack(
            fill="x",
            padx=15,
        )

        for coluna in range(3):
            cards.columnconfigure(
                coluna,
                weight=1,
            )

        self.valor_total_acessos = (
            self.criar_card(
                cards,
                0,
                "Total de acessos",
            )
        )

        self.valor_autorizados = (
            self.criar_card(
                cards,
                1,
                "Autorizados",
            )
        )

        self.valor_negados = (
            self.criar_card(
                cards,
                2,
                "Negados",
            )
        )

        ranking_container = tk.Frame(
            self.aba_acessos,
            bg="white",
            padx=20,
            pady=20,
        )

        ranking_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20,
        )

        titulo_ranking = tk.Label(
            ranking_container,
            text="Ranking de frequência",
            bg="white",
            fg="#111111",
            font=(
                "Arial",
                13,
                "bold",
            ),
        )

        titulo_ranking.pack(
            anchor="w",
            pady=(0, 15),
        )

        colunas = (
            "posicao",
            "aluno",
            "acessos",
        )

        self.tabela_ranking = ttk.Treeview(
            ranking_container,
            columns=colunas,
            show="headings",
        )

        self.tabela_ranking.heading(
            "posicao",
            text="Posição",
        )

        self.tabela_ranking.heading(
            "aluno",
            text="Aluno",
        )

        self.tabela_ranking.heading(
            "acessos",
            text="Acessos",
        )

        self.tabela_ranking.column(
            "posicao",
            width=100,
            anchor="center",
        )

        self.tabela_ranking.column(
            "aluno",
            width=350,
        )

        self.tabela_ranking.column(
            "acessos",
            width=120,
            anchor="center",
        )

        self.tabela_ranking.pack(
            fill="both",
            expand=True,
        )

    # ==================================================
    # RELATÓRIO DE PLANOS
    # ==================================================

    def criar_aba_planos(self):
        titulo = tk.Label(
            self.aba_planos,
            text="Desempenho dos planos",
            bg="#f4f4f4",
            fg="#111111",
            font=(
                "Arial",
                16,
                "bold",
            ),
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(25, 20),
        )

        container = tk.Frame(
            self.aba_planos,
            bg="white",
            padx=20,
            pady=20,
        )

        container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20),
        )

        colunas = (
            "plano",
            "valor",
            "assinaturas",
        )

        self.tabela_planos = ttk.Treeview(
            container,
            columns=colunas,
            show="headings",
        )

        self.tabela_planos.heading(
            "plano",
            text="Plano",
        )

        self.tabela_planos.heading(
            "valor",
            text="Valor mensal",
        )

        self.tabela_planos.heading(
            "assinaturas",
            text="Assinaturas ativas",
        )

        self.tabela_planos.column(
            "plano",
            width=300,
        )

        self.tabela_planos.column(
            "valor",
            width=160,
            anchor="center",
        )

        self.tabela_planos.column(
            "assinaturas",
            width=180,
            anchor="center",
        )

        self.tabela_planos.pack(
            fill="both",
            expand=True,
        )

    # ==================================================
    # COMPONENTES
    # ==================================================

    def criar_card(
        self,
        container,
        coluna,
        titulo,
    ):
        card = tk.Frame(
            container,
            bg="white",
            padx=20,
            pady=20,
        )

        card.grid(
            row=0,
            column=coluna,
            sticky="nsew",
            padx=7,
        )

        label_titulo = tk.Label(
            card,
            text=titulo,
            bg="white",
            fg="#777777",
            font=(
                "Arial",
                9,
                "bold",
            ),
        )

        label_titulo.pack(
            anchor="w"
        )

        label_valor = tk.Label(
            card,
            text="-",
            bg="white",
            fg="#111111",
            font=(
                "Arial",
                20,
                "bold",
            ),
        )

        label_valor.pack(
            anchor="w",
            pady=(8, 0),
        )

        return label_valor

    def obter_valor(
        self,
        dados,
        *chaves,
        padrao=0,
    ):
        for chave in chaves:
            if chave in dados:
                return dados[chave]

        return padrao

    # ==================================================
    # CARREGAMENTO
    # ==================================================

    def carregar_geral(self):
        dados = relatorio_geral()

        self.valor_total_alunos.configure(
            text=str(
                self.obter_valor(
                    dados,
                    "total_alunos",
                )
            )
        )

        self.valor_alunos_ativos.configure(
            text=str(
                self.obter_valor(
                    dados,
                    "alunos_ativos",
                )
            )
        )

        self.valor_assinaturas_ativas.configure(
            text=str(
                self.obter_valor(
                    dados,
                    "assinaturas_ativas",
                )
            )
        )

        self.valor_planos_ativos.configure(
            text=str(
                self.obter_valor(
                    dados,
                    "planos_ativos",
                )
            )
        )

    def carregar_financeiro(self):
        dados = relatorio_financeiro()

        total_recebido = self.obter_valor(
            dados,
            "total_recebido",
        )

        valor_pendente = self.obter_valor(
            dados,
            "valor_pendente",
            "total_pendente",
        )

        valor_atrasado = self.obter_valor(
            dados,
            "valor_atrasado",
            "total_atrasado",
        )

        quantidade_pagos = self.obter_valor(
            dados,
            "quantidade_pagos",
            "quantidade_realizados",
            "pagamentos_realizados",
        )

        quantidade_pendentes = self.obter_valor(
            dados,
            "quantidade_pendentes",
        )

        quantidade_atrasados = self.obter_valor(
            dados,
            "quantidade_atrasados",
        )

        self.valor_recebido.configure(
            text=f"R$ {total_recebido:.2f}"
        )

        self.valor_pendente.configure(
            text=f"R$ {valor_pendente:.2f}"
        )

        self.valor_atrasado.configure(
            text=f"R$ {valor_atrasado:.2f}"
        )

        self.qtd_pagos.configure(
            text=str(
                quantidade_pagos
            )
        )

        self.qtd_pendentes.configure(
            text=str(
                quantidade_pendentes
            )
        )

        self.qtd_atrasados.configure(
            text=str(
                quantidade_atrasados
            )
        )

    def carregar_acessos(self):
        dados = relatorio_acessos()

        total = self.obter_valor(
            dados,
            "total_acessos",
        )

        autorizados = self.obter_valor(
            dados,
            "autorizados",
            "acessos_autorizados",
        )

        negados = self.obter_valor(
            dados,
            "negados",
            "acessos_negados",
        )

        self.valor_total_acessos.configure(
            text=str(total)
        )

        self.valor_autorizados.configure(
            text=str(autorizados)
        )

        self.valor_negados.configure(
            text=str(negados)
        )

        for item in (
            self.tabela_ranking.get_children()
        ):
            self.tabela_ranking.delete(
                item
            )

        ranking = self.obter_valor(
            dados,
            "ranking_frequencia",
            "ranking",
            padrao=[],
        )

        for posicao, registro in enumerate(
            ranking,
            start=1,
        ):
            nome = self.obter_valor(
                registro,
                "nome",
                "aluno",
                "nome_aluno",
                padrao="-",
            )

            quantidade = self.obter_valor(
                registro,
                "quantidade_acessos",
                "total_acessos",
                "acessos",
                padrao=0,
            )

            self.tabela_ranking.insert(
                "",
                "end",
                values=(
                    posicao,
                    nome,
                    quantidade,
                ),
            )

    def carregar_planos(self):
        for item in (
            self.tabela_planos.get_children()
        ):
            self.tabela_planos.delete(
                item
            )

        dados = relatorio_planos()

        if isinstance(
            dados,
            dict,
        ):
            planos = self.obter_valor(
                dados,
                "planos",
                "relatorio",
                padrao=[],
            )

        else:
            planos = dados

        for registro in planos:
            nome = self.obter_valor(
                registro,
                "nome",
                "plano",
                padrao="-",
            )

            valor = self.obter_valor(
                registro,
                "valor",
                "valor_mensal",
                padrao=0,
            )

            assinaturas = self.obter_valor(
                registro,
                "assinaturas_ativas",
                "quantidade_assinaturas",
                "total_assinaturas",
                padrao=0,
            )

            self.tabela_planos.insert(
                "",
                "end",
                values=(
                    nome,
                    f"R$ {valor:.2f}",
                    assinaturas,
                ),
            )

    def atualizar_relatorios(self):
        try:
            self.carregar_geral()
            self.carregar_financeiro()
            self.carregar_acessos()
            self.carregar_planos()

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "os relatórios.\n\n"
                    f"{erro}"
                ),
            )