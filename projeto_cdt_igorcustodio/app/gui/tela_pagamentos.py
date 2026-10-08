import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from app.services.aluno_service import (
    buscar_aluno_por_id,
)

from app.services.assinatura_service import (
    buscar_assinatura_por_id,
    listar_assinaturas,
)

from app.services.pagamento_service import (
    gerar_cobranca_para_assinatura,
    listar_pagamentos,
    registrar_pagamento,
)

from app.services.plano_service import (
    buscar_plano_por_id,
)


class TelaPagamentos:
    def __init__(self, container):
        self.container = container

        self.assinaturas = {}
        self.pagamentos = {}

        self.criar_tela()

    def criar_tela(self):
        self.criar_cabecalho()
        self.criar_area_cobranca()
        self.criar_area_pagamento()
        self.criar_lista()

        self.atualizar_tela()

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
            text="Pagamentos",
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
            command=self.atualizar_tela,
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

    def criar_area_cobranca(self):
        area = tk.Frame(
            self.container,
            bg="#f4f4f4",
        )

        area.pack(
            fill="x",
            padx=30,
            pady=(30, 8),
        )

        formulario = tk.Frame(
            area,
            bg="white",
            padx=25,
            pady=20,
        )

        formulario.pack(
            fill="x"
        )

        titulo = tk.Label(
            formulario,
            text="Gerar cobrança",
            bg="white",
            fg="#111111",
            font=(
                "Arial",
                14,
                "bold",
            ),
        )

        titulo.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(0, 20),
        )

        for coluna in range(3):
            formulario.columnconfigure(
                coluna,
                weight=1,
            )

        bloco_assinatura = tk.Frame(
            formulario,
            bg="white",
        )

        bloco_assinatura.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=5,
        )

        tk.Label(
            bloco_assinatura,
            text="Assinatura",
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                9,
                "bold",
            ),
        ).pack(
            anchor="w",
            pady=(0, 5),
        )

        self.combo_assinatura = ttk.Combobox(
            bloco_assinatura,
            state="readonly",
            font=(
                "Arial",
                10,
            ),
        )

        self.combo_assinatura.pack(
            fill="x",
            ipady=5,
        )

        bloco_vencimento = tk.Frame(
            formulario,
            bg="white",
        )

        bloco_vencimento.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
        )

        tk.Label(
            bloco_vencimento,
            text="Vencimento (DD/MM/AAAA)",
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                9,
                "bold",
            ),
        ).pack(
            anchor="w",
            pady=(0, 5),
        )

        self.entry_vencimento = tk.Entry(
            bloco_vencimento,
            font=(
                "Arial",
                10,
            ),
            relief="solid",
            borderwidth=1,
        )

        self.entry_vencimento.pack(
            fill="x",
            ipady=6,
        )

        botao_gerar = tk.Button(
            formulario,
            text="Gerar cobrança",
            command=self.gerar_cobranca,
            bg="#111111",
            fg="white",
            activebackground="#ffd400",
            activeforeground="#111111",
            relief="flat",
            padx=20,
            pady=9,
            font=(
                "Arial",
                10,
                "bold",
            ),
            cursor="hand2",
        )

        botao_gerar.grid(
            row=1,
            column=2,
            sticky="sew",
            padx=5,
        )

    def criar_area_pagamento(self):
        area = tk.Frame(
            self.container,
            bg="#f4f4f4",
        )

        area.pack(
            fill="x",
            padx=30,
            pady=8,
        )

        formulario = tk.Frame(
            area,
            bg="white",
            padx=25,
            pady=20,
        )

        formulario.pack(
            fill="x"
        )

        titulo = tk.Label(
            formulario,
            text="Registrar pagamento",
            bg="white",
            fg="#111111",
            font=(
                "Arial",
                14,
                "bold",
            ),
        )

        titulo.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(0, 20),
        )

        for coluna in range(3):
            formulario.columnconfigure(
                coluna,
                weight=1,
            )

        bloco_pagamento = tk.Frame(
            formulario,
            bg="white",
        )

        bloco_pagamento.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=5,
        )

        tk.Label(
            bloco_pagamento,
            text="Cobrança",
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                9,
                "bold",
            ),
        ).pack(
            anchor="w",
            pady=(0, 5),
        )

        self.combo_pagamento = ttk.Combobox(
            bloco_pagamento,
            state="readonly",
            font=(
                "Arial",
                10,
            ),
        )

        self.combo_pagamento.pack(
            fill="x",
            ipady=5,
        )

        bloco_forma = tk.Frame(
            formulario,
            bg="white",
        )

        bloco_forma.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
        )

        tk.Label(
            bloco_forma,
            text="Forma de pagamento",
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                9,
                "bold",
            ),
        ).pack(
            anchor="w",
            pady=(0, 5),
        )

        self.combo_forma_pagamento = ttk.Combobox(
            bloco_forma,
            state="readonly",
            values=(
                "Pix",
                "Cartão de crédito",
                "Cartão de débito",
                "Dinheiro",
            ),
            font=(
                "Arial",
                10,
            ),
        )

        self.combo_forma_pagamento.pack(
            fill="x",
            ipady=5,
        )

        botao_pagar = tk.Button(
            formulario,
            text="Registrar pagamento",
            command=self.registrar_pagamento_selecionado,
            bg="#111111",
            fg="white",
            activebackground="#ffd400",
            activeforeground="#111111",
            relief="flat",
            padx=20,
            pady=9,
            font=(
                "Arial",
                10,
                "bold",
            ),
            cursor="hand2",
        )

        botao_pagar.grid(
            row=1,
            column=2,
            sticky="sew",
            padx=5,
        )

    def criar_lista(self):
        area = tk.Frame(
            self.container,
            bg="#f4f4f4",
        )

        area.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(8, 30),
        )

        container_lista = tk.Frame(
            area,
            bg="white",
            padx=20,
            pady=20,
        )

        container_lista.pack(
            fill="both",
            expand=True,
        )

        titulo = tk.Label(
            container_lista,
            text="Histórico financeiro",
            bg="white",
            fg="#111111",
            font=(
                "Arial",
                14,
                "bold",
            ),
        )

        titulo.pack(
            anchor="w",
            pady=(0, 15),
        )

        colunas = (
            "id",
            "aluno",
            "plano",
            "valor",
            "vencimento",
            "pagamento",
            "forma",
            "status",
        )

        self.tabela = ttk.Treeview(
            container_lista,
            columns=colunas,
            show="headings",
            height=9,
        )

        cabecalhos = {
            "id": "ID",
            "aluno": "Aluno",
            "plano": "Plano",
            "valor": "Valor",
            "vencimento": "Vencimento",
            "pagamento": "Pagamento",
            "forma": "Forma",
            "status": "Status",
        }

        for coluna, texto in cabecalhos.items():
            self.tabela.heading(
                coluna,
                text=texto,
            )

        self.tabela.column(
            "id",
            width=45,
            anchor="center",
        )

        self.tabela.column(
            "aluno",
            width=160,
        )

        self.tabela.column(
            "plano",
            width=100,
        )

        self.tabela.column(
            "valor",
            width=90,
            anchor="center",
        )

        self.tabela.column(
            "vencimento",
            width=100,
            anchor="center",
        )

        self.tabela.column(
            "pagamento",
            width=100,
            anchor="center",
        )

        self.tabela.column(
            "forma",
            width=120,
            anchor="center",
        )

        self.tabela.column(
            "status",
            width=90,
            anchor="center",
        )

        barra_vertical = ttk.Scrollbar(
            container_lista,
            orient="vertical",
            command=self.tabela.yview,
        )

        barra_horizontal = ttk.Scrollbar(
            container_lista,
            orient="horizontal",
            command=self.tabela.xview,
        )

        self.tabela.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set,
        )

        self.tabela.pack(
            side="top",
            fill="both",
            expand=True,
        )

        barra_horizontal.pack(
            side="bottom",
            fill="x",
        )

        barra_vertical.place(
            relx=1,
            rely=0,
            relheight=0.9,
            anchor="ne",
        )

    def converter_data(self, texto):
        try:
            return datetime.strptime(
                texto,
                "%d/%m/%Y",
            ).date()

        except ValueError:
            raise ValueError(
                "Data inválida. "
                "Use o formato DD/MM/AAAA."
            )

    def carregar_assinaturas(self):
        try:
            assinaturas = listar_assinaturas()

            self.assinaturas = {}

            for assinatura in assinaturas:
                if assinatura.status != "ativa":
                    continue

                aluno = buscar_aluno_por_id(
                    assinatura.aluno_id
                )

                plano = buscar_plano_por_id(
                    assinatura.plano_id
                )

                if aluno is None or plano is None:
                    continue

                texto = (
                    f"{assinatura.id} - "
                    f"{aluno.nome} - "
                    f"{plano.nome}"
                )

                self.assinaturas[
                    texto
                ] = assinatura.id

            self.combo_assinatura[
                "values"
            ] = list(
                self.assinaturas.keys()
            )

            self.combo_assinatura.set("")

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "as assinaturas.\n\n"
                    f"{erro}"
                ),
            )

    def carregar_pagamentos(self):
        for item in self.tabela.get_children():
            self.tabela.delete(
                item
            )

        try:
            pagamentos = listar_pagamentos()

            self.pagamentos = {}

            for pagamento in pagamentos:
                assinatura = (
                    buscar_assinatura_por_id(
                        pagamento.assinatura_id
                    )
                )

                nome_aluno = "Não encontrado"
                nome_plano = "Não encontrado"

                if assinatura is not None:
                    aluno = buscar_aluno_por_id(
                        assinatura.aluno_id
                    )

                    plano = buscar_plano_por_id(
                        assinatura.plano_id
                    )

                    if aluno is not None:
                        nome_aluno = aluno.nome

                    if plano is not None:
                        nome_plano = plano.nome

                data_pagamento = (
                    pagamento.data_pagamento.strftime(
                        "%d/%m/%Y"
                    )
                    if pagamento.data_pagamento
                    else "-"
                )

                forma = (
                    pagamento.forma_pagamento
                    if pagamento.forma_pagamento
                    else "-"
                )

                self.tabela.insert(
                    "",
                    "end",
                    values=(
                        pagamento.id,
                        nome_aluno,
                        nome_plano,
                        f"R$ {pagamento.valor:.2f}",
                        pagamento.data_vencimento.strftime(
                            "%d/%m/%Y"
                        ),
                        data_pagamento,
                        forma,
                        pagamento.status,
                    ),
                )

                if pagamento.status in (
                    "pendente",
                    "atrasado",
                ):
                    texto = (
                        f"{pagamento.id} - "
                        f"{nome_aluno} - "
                        f"R$ {pagamento.valor:.2f} - "
                        f"{pagamento.status}"
                    )

                    self.pagamentos[
                        texto
                    ] = pagamento.id

            self.combo_pagamento[
                "values"
            ] = list(
                self.pagamentos.keys()
            )

            self.combo_pagamento.set("")

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "os pagamentos.\n\n"
                    f"{erro}"
                ),
            )

    def gerar_cobranca(self):
        assinatura_texto = (
            self.combo_assinatura
            .get()
            .strip()
        )

        vencimento_texto = (
            self.entry_vencimento
            .get()
            .strip()
        )

        if not assinatura_texto:
            messagebox.showwarning(
                "Assinatura obrigatória",
                "Selecione uma assinatura.",
            )

            return

        if not vencimento_texto:
            messagebox.showwarning(
                "Vencimento obrigatório",
                "Informe a data de vencimento.",
            )

            return

        try:
            assinatura_id = (
                self.assinaturas[
                    assinatura_texto
                ]
            )

            vencimento = self.converter_data(
                vencimento_texto
            )

            pagamento = (
                gerar_cobranca_para_assinatura(
                    assinatura_id,
                    vencimento,
                )
            )

            messagebox.showinfo(
                "Cobrança gerada",
                (
                    "Cobrança gerada "
                    "com sucesso!\n\n"
                    f"ID: {pagamento.id}\n"
                    f"Valor: R$ "
                    f"{pagamento.valor:.2f}\n"
                    f"Vencimento: "
                    f"{pagamento.data_vencimento.strftime('%d/%m/%Y')}"
                ),
            )

            self.combo_assinatura.set("")

            self.entry_vencimento.delete(
                0,
                tk.END,
            )

            self.carregar_pagamentos()

        except ValueError as erro:
            messagebox.showerror(
                "Erro",
                str(erro),
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível gerar "
                    "a cobrança.\n\n"
                    f"{erro}"
                ),
            )

    def registrar_pagamento_selecionado(self):
        pagamento_texto = (
            self.combo_pagamento
            .get()
            .strip()
        )

        forma_pagamento = (
            self.combo_forma_pagamento
            .get()
            .strip()
        )

        if not pagamento_texto:
            messagebox.showwarning(
                "Cobrança obrigatória",
                (
                    "Selecione uma cobrança "
                    "pendente ou atrasada."
                ),
            )

            return

        if not forma_pagamento:
            messagebox.showwarning(
                "Forma de pagamento",
                (
                    "Selecione a forma "
                    "de pagamento."
                ),
            )

            return

        try:
            pagamento_id = (
                self.pagamentos[
                    pagamento_texto
                ]
            )

            pagamento = registrar_pagamento(
                pagamento_id,
                forma_pagamento,
            )

            if pagamento is None:
                messagebox.showerror(
                    "Erro",
                    "Pagamento não encontrado.",
                )

                return

            messagebox.showinfo(
                "Pagamento registrado",
                (
                    "Pagamento registrado "
                    "com sucesso!\n\n"
                    f"ID: {pagamento.id}\n"
                    f"Valor: R$ "
                    f"{pagamento.valor:.2f}\n"
                    f"Forma: "
                    f"{pagamento.forma_pagamento}"
                ),
            )

            self.combo_pagamento.set("")
            self.combo_forma_pagamento.set("")

            self.carregar_pagamentos()

        except ValueError as erro:
            messagebox.showerror(
                "Erro",
                str(erro),
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível registrar "
                    "o pagamento.\n\n"
                    f"{erro}"
                ),
            )

    def atualizar_tela(self):
        self.carregar_assinaturas()
        self.carregar_pagamentos()