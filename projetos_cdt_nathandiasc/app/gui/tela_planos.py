import tkinter as tk
from tkinter import messagebox, ttk

from app.models.plano import Plano
from app.services.plano_service import (
    cadastrar_plano,
    listar_planos,
)


class TelaPlanos:
    def __init__(self, container):
        self.container = container

        self.criar_tela()

    def criar_tela(self):
        self.criar_cabecalho()
        self.criar_formulario()
        self.criar_lista()

        self.carregar_planos()

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
            text="Planos",
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
            command=self.carregar_planos,
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

    def criar_formulario(self):
        area_formulario = tk.Frame(
            self.container,
            bg="#f4f4f4",
        )

        area_formulario.pack(
            fill="x",
            padx=30,
            pady=(30, 15),
        )

        formulario = tk.Frame(
            area_formulario,
            bg="white",
            padx=25,
            pady=20,
        )

        formulario.pack(
            fill="x"
        )

        titulo = tk.Label(
            formulario,
            text="Cadastrar novo plano",
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
            columnspan=4,
            sticky="w",
            pady=(0, 20),
        )

        for coluna in range(4):
            formulario.columnconfigure(
                coluna,
                weight=1,
            )

        self.entry_nome = self.criar_campo(
            formulario,
            "Nome do plano",
            linha=1,
            coluna=0,
        )

        self.entry_valor = self.criar_campo(
            formulario,
            "Valor mensal (R$)",
            linha=1,
            coluna=1,
        )

        self.entry_descricao = self.criar_campo(
            formulario,
            "Descrição",
            linha=1,
            coluna=2,
            coluna_span=2,
        )

        botao_cadastrar = tk.Button(
            formulario,
            text="Cadastrar plano",
            command=self.cadastrar_novo_plano,
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

        botao_cadastrar.grid(
            row=2,
            column=3,
            sticky="ew",
            padx=5,
            pady=(18, 5),
        )

    def criar_campo(
        self,
        container,
        texto,
        linha,
        coluna,
        coluna_span=1,
    ):
        bloco = tk.Frame(
            container,
            bg="white",
        )

        bloco.grid(
            row=linha,
            column=coluna,
            columnspan=coluna_span,
            sticky="ew",
            padx=5,
            pady=5,
        )

        label = tk.Label(
            bloco,
            text=texto,
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                9,
                "bold",
            ),
        )

        label.pack(
            anchor="w",
            pady=(0, 5),
        )

        entry = tk.Entry(
            bloco,
            font=(
                "Arial",
                10,
            ),
            relief="solid",
            borderwidth=1,
        )

        entry.pack(
            fill="x",
            ipady=6,
        )

        return entry

    def criar_lista(self):
        area_lista = tk.Frame(
            self.container,
            bg="#f4f4f4",
        )

        area_lista.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(15, 30),
        )

        lista_container = tk.Frame(
            area_lista,
            bg="white",
            padx=20,
            pady=20,
        )

        lista_container.pack(
            fill="both",
            expand=True,
        )

        titulo = tk.Label(
            lista_container,
            text="Planos cadastrados",
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
            "nome",
            "valor",
            "descricao",
            "status",
        )

        self.tabela = ttk.Treeview(
            lista_container,
            columns=colunas,
            show="headings",
            height=10,
        )

        self.tabela.heading(
            "id",
            text="ID",
        )

        self.tabela.heading(
            "nome",
            text="Plano",
        )

        self.tabela.heading(
            "valor",
            text="Valor mensal",
        )

        self.tabela.heading(
            "descricao",
            text="Descrição",
        )

        self.tabela.heading(
            "status",
            text="Status",
        )

        self.tabela.column(
            "id",
            width=50,
            anchor="center",
        )

        self.tabela.column(
            "nome",
            width=160,
        )

        self.tabela.column(
            "valor",
            width=120,
            anchor="center",
        )

        self.tabela.column(
            "descricao",
            width=330,
        )

        self.tabela.column(
            "status",
            width=90,
            anchor="center",
        )

        barra_vertical = ttk.Scrollbar(
            lista_container,
            orient="vertical",
            command=self.tabela.yview,
        )

        self.tabela.configure(
            yscrollcommand=barra_vertical.set
        )

        self.tabela.pack(
            side="left",
            fill="both",
            expand=True,
        )

        barra_vertical.pack(
            side="right",
            fill="y",
        )

    def cadastrar_novo_plano(self):
        nome = (
            self.entry_nome
            .get()
            .strip()
        )

        valor_texto = (
            self.entry_valor
            .get()
            .strip()
        )

        descricao = (
            self.entry_descricao
            .get()
            .strip()
        )

        if not nome or not valor_texto:
            messagebox.showwarning(
                "Campos obrigatórios",
                (
                    "Preencha o nome e o valor "
                    "do plano."
                ),
            )

            return

        try:
            valor = float(
                valor_texto.replace(
                    ",",
                    ".",
                )
            )

            if valor <= 0:
                raise ValueError(
                    "O valor do plano deve "
                    "ser maior que zero."
                )

            plano = Plano(
                nome=nome,
                valor=valor,
                descricao=descricao,
            )

            plano = cadastrar_plano(
                plano
            )

            messagebox.showinfo(
                "Cadastro realizado",
                (
                    "Plano cadastrado "
                    "com sucesso!\n\n"
                    f"ID: {plano.id}\n"
                    f"Plano: {plano.nome}\n"
                    f"Valor: R$ {plano.valor:.2f}"
                ),
            )

            self.limpar_formulario()
            self.carregar_planos()

        except ValueError as erro:
            messagebox.showerror(
                "Erro no cadastro",
                str(erro),
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível cadastrar "
                    "o plano.\n\n"
                    f"{erro}"
                ),
            )

    def limpar_formulario(self):
        campos = (
            self.entry_nome,
            self.entry_valor,
            self.entry_descricao,
        )

        for campo in campos:
            campo.delete(
                0,
                tk.END,
            )

        self.entry_nome.focus()

    def carregar_planos(self):
        for item in self.tabela.get_children():
            self.tabela.delete(
                item
            )

        try:
            planos = listar_planos()

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "os planos.\n\n"
                    f"{erro}"
                ),
            )

            return

        for plano in planos:
            status = (
                "Ativo"
                if plano.ativo
                else "Inativo"
            )

            descricao = (
                plano.descricao
                if plano.descricao
                else "-"
            )

            self.tabela.insert(
                "",
                "end",
                values=(
                    plano.id,
                    plano.nome,
                    f"R$ {plano.valor:.2f}",
                    descricao,
                    status,
                ),
            )