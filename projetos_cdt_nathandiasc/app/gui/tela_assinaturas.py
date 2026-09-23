import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from app.models.assinatura import Assinatura

from app.services.aluno_service import (
    buscar_aluno_por_id,
    listar_alunos,
)

from app.services.assinatura_service import (
    buscar_assinatura_ativa_por_aluno,
    cadastrar_assinatura,
    listar_assinaturas,
)

from app.services.plano_service import (
    buscar_plano_por_id,
    listar_planos,
)


class TelaAssinaturas:
    def __init__(self, container):
        self.container = container

        self.alunos = {}
        self.planos = {}

        self.criar_tela()

    def criar_tela(self):
        self.criar_cabecalho()
        self.criar_formulario()
        self.criar_lista()

        self.carregar_opcoes()
        self.carregar_assinaturas()

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
            text="Assinaturas",
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
            text="Criar nova assinatura",
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

        bloco_aluno = tk.Frame(
            formulario,
            bg="white",
        )

        bloco_aluno.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=5,
            pady=5,
        )

        label_aluno = tk.Label(
            bloco_aluno,
            text="Aluno",
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                9,
                "bold",
            ),
        )

        label_aluno.pack(
            anchor="w",
            pady=(0, 5),
        )

        self.combo_aluno = ttk.Combobox(
            bloco_aluno,
            state="readonly",
            font=(
                "Arial",
                10,
            ),
        )

        self.combo_aluno.pack(
            fill="x",
            ipady=5,
        )

        bloco_plano = tk.Frame(
            formulario,
            bg="white",
        )

        bloco_plano.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
            pady=5,
        )

        label_plano = tk.Label(
            bloco_plano,
            text="Plano",
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                9,
                "bold",
            ),
        )

        label_plano.pack(
            anchor="w",
            pady=(0, 5),
        )

        self.combo_plano = ttk.Combobox(
            bloco_plano,
            state="readonly",
            font=(
                "Arial",
                10,
            ),
        )

        self.combo_plano.pack(
            fill="x",
            ipady=5,
        )

        botao_criar = tk.Button(
            formulario,
            text="Criar assinatura",
            command=self.criar_assinatura,
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

        botao_criar.grid(
            row=1,
            column=2,
            sticky="sew",
            padx=5,
            pady=5,
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
            text="Assinaturas cadastradas",
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
            "inicio",
            "fim",
            "status",
        )

        self.tabela = ttk.Treeview(
            lista_container,
            columns=colunas,
            show="headings",
            height=12,
        )

        self.tabela.heading(
            "id",
            text="ID",
        )

        self.tabela.heading(
            "aluno",
            text="Aluno",
        )

        self.tabela.heading(
            "plano",
            text="Plano",
        )

        self.tabela.heading(
            "inicio",
            text="Início",
        )

        self.tabela.heading(
            "fim",
            text="Fim",
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
            "aluno",
            width=200,
        )

        self.tabela.column(
            "plano",
            width=150,
        )

        self.tabela.column(
            "inicio",
            width=100,
            anchor="center",
        )

        self.tabela.column(
            "fim",
            width=100,
            anchor="center",
        )

        self.tabela.column(
            "status",
            width=100,
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

    def carregar_opcoes(self):
        try:
            alunos = listar_alunos()
            planos = listar_planos()

            self.alunos = {
                f"{aluno.id} - {aluno.nome}": aluno.id
                for aluno in alunos
                if aluno.status == "ativo"
            }

            self.planos = {
                (
                    f"{plano.id} - "
                    f"{plano.nome} "
                    f"(R$ {plano.valor:.2f})"
                ): plano.id
                for plano in planos
                if plano.ativo
            }

            self.combo_aluno[
                "values"
            ] = list(
                self.alunos.keys()
            )

            self.combo_plano[
                "values"
            ] = list(
                self.planos.keys()
            )

            self.combo_aluno.set("")
            self.combo_plano.set("")

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "alunos e planos.\n\n"
                    f"{erro}"
                ),
            )

    def criar_assinatura(self):
        aluno_texto = (
            self.combo_aluno
            .get()
            .strip()
        )

        plano_texto = (
            self.combo_plano
            .get()
            .strip()
        )

        if not aluno_texto:
            messagebox.showwarning(
                "Aluno obrigatório",
                "Selecione um aluno.",
            )

            return

        if not plano_texto:
            messagebox.showwarning(
                "Plano obrigatório",
                "Selecione um plano.",
            )

            return

        aluno_id = self.alunos[
            aluno_texto
        ]

        plano_id = self.planos[
            plano_texto
        ]

        try:
            assinatura_existente = (
                buscar_assinatura_ativa_por_aluno(
                    aluno_id
                )
            )

            if assinatura_existente is not None:
                aluno = buscar_aluno_por_id(
                    aluno_id
                )

                messagebox.showwarning(
                    "Assinatura existente",
                    (
                        f"{aluno.nome} já possui "
                        "uma assinatura ativa."
                    ),
                )

                return

            assinatura = Assinatura(
                aluno_id=aluno_id,
                plano_id=plano_id,
                data_inicio=date.today(),
            )

            assinatura = cadastrar_assinatura(
                assinatura
            )

            aluno = buscar_aluno_por_id(
                aluno_id
            )

            plano = buscar_plano_por_id(
                plano_id
            )

            messagebox.showinfo(
                "Assinatura criada",
                (
                    "Assinatura criada "
                    "com sucesso!\n\n"
                    f"ID: {assinatura.id}\n"
                    f"Aluno: {aluno.nome}\n"
                    f"Plano: {plano.nome}"
                ),
            )

            self.combo_aluno.set("")
            self.combo_plano.set("")

            self.carregar_assinaturas()

        except ValueError as erro:
            messagebox.showerror(
                "Erro",
                str(erro),
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível criar "
                    "a assinatura.\n\n"
                    f"{erro}"
                ),
            )

    def carregar_assinaturas(self):
        for item in self.tabela.get_children():
            self.tabela.delete(
                item
            )

        try:
            assinaturas = listar_assinaturas()

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "as assinaturas.\n\n"
                    f"{erro}"
                ),
            )

            return

        for assinatura in assinaturas:
            aluno = buscar_aluno_por_id(
                assinatura.aluno_id
            )

            plano = buscar_plano_por_id(
                assinatura.plano_id
            )

            nome_aluno = (
                aluno.nome
                if aluno
                else "Não encontrado"
            )

            nome_plano = (
                plano.nome
                if plano
                else "Não encontrado"
            )

            data_inicio = (
                assinatura.data_inicio.strftime(
                    "%d/%m/%Y"
                )
            )

            data_fim = (
                assinatura.data_fim.strftime(
                    "%d/%m/%Y"
                )
                if assinatura.data_fim
                else "-"
            )

            self.tabela.insert(
                "",
                "end",
                values=(
                    assinatura.id,
                    nome_aluno,
                    nome_plano,
                    data_inicio,
                    data_fim,
                    assinatura.status,
                ),
            )

    def atualizar_tela(self):
        self.carregar_opcoes()
        self.carregar_assinaturas()