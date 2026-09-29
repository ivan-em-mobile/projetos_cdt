import tkinter as tk
from datetime import date, datetime
from tkinter import messagebox, ttk

from app.models.aluno import Aluno
from app.services.aluno_service import (
    cadastrar_aluno,
    listar_alunos,
)


class TelaAlunos:
    def __init__(
        self,
        container,
    ):
        self.container = container

        self.criar_tela()

    def criar_tela(self):
        self.criar_cabecalho()
        self.criar_formulario()
        self.criar_lista()

        self.carregar_alunos()

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
            text="Alunos",
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
            command=self.carregar_alunos,
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
            text="Cadastrar novo aluno",
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

        formulario.columnconfigure(
            0,
            weight=1,
        )

        formulario.columnconfigure(
            1,
            weight=1,
        )

        formulario.columnconfigure(
            2,
            weight=1,
        )

        formulario.columnconfigure(
            3,
            weight=1,
        )

        self.entry_nome = self.criar_campo(
            formulario,
            "Nome",
            linha=1,
            coluna=0,
            coluna_span=2,
        )

        self.entry_cpf = self.criar_campo(
            formulario,
            "CPF (000.000.000-00)",
            linha=1,
            coluna=2,
        )

        self.entry_cpf.bind(
            "<KeyRelease>",
            self.aplicar_mascara_cpf,
        )

        self.entry_data_nascimento = (
            self.criar_campo(
                formulario,
                "Nascimento (DD/MM/AAAA)",
                linha=1,
                coluna=3,
            )
        )

        self.entry_email = self.criar_campo(
            formulario,
            "E-mail",
            linha=2,
            coluna=0,
            coluna_span=2,
        )

        self.entry_telefone = (
            self.criar_campo(
                formulario,
                "Telefone",
                linha=2,
                coluna=2,
            )
        )

        botao_cadastrar = tk.Button(
            formulario,
            text="Cadastrar aluno",
            command=self.cadastrar_novo_aluno,
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
            pady=(22, 5),
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

    def aplicar_mascara_cpf(
        self,
        event=None,
    ):
        digitos = "".join(
            caractere
            for caractere
            in self.entry_cpf.get()
            if caractere.isdigit()
        )[:11]

        if len(digitos) <= 3:
            cpf_formatado = digitos

        elif len(digitos) <= 6:
            cpf_formatado = (
                f"{digitos[:3]}."
                f"{digitos[3:]}"
            )

        elif len(digitos) <= 9:
            cpf_formatado = (
                f"{digitos[:3]}."
                f"{digitos[3:6]}."
                f"{digitos[6:]}"
            )

        else:
            cpf_formatado = (
                f"{digitos[:3]}."
                f"{digitos[3:6]}."
                f"{digitos[6:9]}-"
                f"{digitos[9:]}"
            )

        if (
            self.entry_cpf.get()
            != cpf_formatado
        ):
            self.entry_cpf.delete(
                0,
                tk.END,
            )

            self.entry_cpf.insert(
                0,
                cpf_formatado,
            )

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
            text="Alunos cadastrados",
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
            "cpf",
            "email",
            "telefone",
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
            text="Nome",
        )

        self.tabela.heading(
            "cpf",
            text="CPF",
        )

        self.tabela.heading(
            "email",
            text="E-mail",
        )

        self.tabela.heading(
            "telefone",
            text="Telefone",
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
            width=190,
        )

        self.tabela.column(
            "cpf",
            width=120,
        )

        self.tabela.column(
            "email",
            width=210,
        )

        self.tabela.column(
            "telefone",
            width=120,
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
            yscrollcommand=(
                barra_vertical.set
            )
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

    def converter_data(
        self,
        texto,
    ) -> date:
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

    def cadastrar_novo_aluno(self):
        nome = (
            self.entry_nome
            .get()
            .strip()
        )

        cpf = (
            self.entry_cpf
            .get()
            .strip()
        )

        data_nascimento = (
            self.entry_data_nascimento
            .get()
            .strip()
        )

        email = (
            self.entry_email
            .get()
            .strip()
        )

        telefone = (
            self.entry_telefone
            .get()
            .strip()
        )

        if not all(
            (
                nome,
                cpf,
                data_nascimento,
                email,
                telefone,
            )
        ):
            messagebox.showwarning(
                "Campos obrigatórios",
                (
                    "Preencha todos os campos "
                    "antes de cadastrar o aluno."
                ),
            )

            return

        try:
            aluno = Aluno(
                nome=nome,
                cpf=cpf,
                data_nascimento=(
                    self.converter_data(
                        data_nascimento
                    )
                ),
                email=email,
                telefone=telefone,
                data_cadastro=date.today(),
            )

            aluno = cadastrar_aluno(
                aluno
            )

            messagebox.showinfo(
                "Cadastro realizado",
                (
                    "Aluno cadastrado "
                    "com sucesso!\n\n"
                    f"ID: {aluno.id}\n"
                    f"Nome: {aluno.nome}"
                ),
            )

            self.limpar_formulario()
            self.carregar_alunos()

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
                    "o aluno.\n\n"
                    f"{erro}"
                ),
            )

    def limpar_formulario(self):
        campos = (
            self.entry_nome,
            self.entry_cpf,
            self.entry_data_nascimento,
            self.entry_email,
            self.entry_telefone,
        )

        for campo in campos:
            campo.delete(
                0,
                tk.END,
            )

        self.entry_nome.focus()

    def carregar_alunos(self):
        for item in (
            self.tabela
            .get_children()
        ):
            self.tabela.delete(
                item
            )

        try:
            alunos = listar_alunos()

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "os alunos.\n\n"
                    f"{erro}"
                ),
            )

            return

        for aluno in alunos:
            self.tabela.insert(
                "",
                "end",
                values=(
                    aluno.id,
                    aluno.nome,
                    aluno.cpf,
                    aluno.email,
                    aluno.telefone,
                    aluno.status,
                ),
            )