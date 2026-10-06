import tkinter as tk
from tkinter import messagebox, ttk

from app.services.acesso_service import (
    autorizar_acesso,
    listar_acessos,
)

from app.services.aluno_service import (
    buscar_aluno_por_id,
    listar_alunos,
)


class TelaAcesso:
    def __init__(self, container):
        self.container = container

        self.alunos = {}

        self.criar_tela()

    def criar_tela(self):
        self.criar_cabecalho()
        self.criar_area_acesso()
        self.criar_area_resultado()
        self.criar_historico()

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
            text="Controle de Acesso",
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

    def criar_area_acesso(self):
        area = tk.Frame(
            self.container,
            bg="#f4f4f4",
        )

        area.pack(
            fill="x",
            padx=30,
            pady=(30, 10),
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
            text="Registrar tentativa de entrada",
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
            columnspan=2,
            sticky="w",
            pady=(0, 20),
        )

        formulario.columnconfigure(
            0,
            weight=3,
        )

        formulario.columnconfigure(
            1,
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
            padx=(0, 10),
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

        botao_acesso = tk.Button(
            formulario,
            text="Registrar acesso",
            command=self.registrar_acesso,
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

        botao_acesso.grid(
            row=1,
            column=1,
            sticky="sew",
        )

    def criar_area_resultado(self):
        area = tk.Frame(
            self.container,
            bg="#f4f4f4",
        )

        area.pack(
            fill="x",
            padx=30,
            pady=10,
        )

        self.resultado = tk.Frame(
            area,
            bg="white",
            padx=25,
            pady=20,
        )

        self.resultado.pack(
            fill="x"
        )

        self.label_status = tk.Label(
            self.resultado,
            text="Aguardando tentativa de acesso",
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                16,
                "bold",
            ),
        )

        self.label_status.pack(
            anchor="w"
        )

        self.label_detalhes = tk.Label(
            self.resultado,
            text=(
                "Selecione um aluno e registre "
                "uma tentativa de entrada."
            ),
            bg="white",
            fg="#777777",
            font=(
                "Arial",
                10,
            ),
            justify="left",
        )

        self.label_detalhes.pack(
            anchor="w",
            pady=(8, 0),
        )

    def criar_historico(self):
        area = tk.Frame(
            self.container,
            bg="#f4f4f4",
        )

        area.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(10, 30),
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
            text="Histórico de acessos",
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
            "data_hora",
            "status",
            "motivo",
        )

        self.tabela = ttk.Treeview(
            container_lista,
            columns=colunas,
            show="headings",
            height=11,
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
            "data_hora",
            text="Data / Hora",
        )

        self.tabela.heading(
            "status",
            text="Status",
        )

        self.tabela.heading(
            "motivo",
            text="Motivo",
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
            "data_hora",
            width=150,
            anchor="center",
        )

        self.tabela.column(
            "status",
            width=110,
            anchor="center",
        )

        self.tabela.column(
            "motivo",
            width=280,
        )

        barra_vertical = ttk.Scrollbar(
            container_lista,
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

    def carregar_alunos(self):
        try:
            alunos = listar_alunos()

            self.alunos = {
                (
                    f"{aluno.id} - "
                    f"{aluno.nome} "
                    f"({aluno.status})"
                ): aluno.id
                for aluno in alunos
            }

            self.combo_aluno[
                "values"
            ] = list(
                self.alunos.keys()
            )

            self.combo_aluno.set("")

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "os alunos.\n\n"
                    f"{erro}"
                ),
            )

    def registrar_acesso(self):
        aluno_texto = (
            self.combo_aluno
            .get()
            .strip()
        )

        if not aluno_texto:
            messagebox.showwarning(
                "Aluno obrigatório",
                (
                    "Selecione um aluno antes "
                    "de registrar o acesso."
                ),
            )

            return

        try:
            aluno_id = self.alunos[
                aluno_texto
            ]

            aluno = buscar_aluno_por_id(
                aluno_id
            )

            acesso = autorizar_acesso(
                aluno_id
            )

            if acesso.status == "autorizado":
                self.exibir_autorizado(
                    aluno,
                    acesso,
                )

            else:
                self.exibir_negado(
                    aluno,
                    acesso,
                )

            self.carregar_historico()

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível registrar "
                    "a tentativa de acesso.\n\n"
                    f"{erro}"
                ),
            )

    def exibir_autorizado(
        self,
        aluno,
        acesso,
    ):
        self.resultado.configure(
            bg="#dff5e1"
        )

        self.label_status.configure(
            text="ACESSO AUTORIZADO",
            bg="#dff5e1",
            fg="#156b25",
        )

        self.label_detalhes.configure(
            text=(
                f"Aluno: {aluno.nome}\n"
                f"Horário: "
                f"{acesso.data_hora.strftime('%d/%m/%Y %H:%M:%S')}"
            ),
            bg="#dff5e1",
            fg="#333333",
        )

    def exibir_negado(
        self,
        aluno,
        acesso,
    ):
        self.resultado.configure(
            bg="#fde2e2"
        )

        self.label_status.configure(
            text="ACESSO NEGADO",
            bg="#fde2e2",
            fg="#a51f1f",
        )

        motivo = (
            acesso.motivo
            if acesso.motivo
            else "Motivo não informado."
        )

        self.label_detalhes.configure(
            text=(
                f"Aluno: {aluno.nome}\n"
                f"Motivo: {motivo}\n"
                f"Horário: "
                f"{acesso.data_hora.strftime('%d/%m/%Y %H:%M:%S')}"
            ),
            bg="#fde2e2",
            fg="#333333",
        )

    def carregar_historico(self):
        for item in self.tabela.get_children():
            self.tabela.delete(
                item
            )

        try:
            acessos = listar_acessos()

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "o histórico de acessos.\n\n"
                    f"{erro}"
                ),
            )

            return

        for acesso in acessos:
            aluno = buscar_aluno_por_id(
                acesso.aluno_id
            )

            nome_aluno = (
                aluno.nome
                if aluno is not None
                else f"Aluno ID {acesso.aluno_id}"
            )

            motivo = (
                acesso.motivo
                if acesso.motivo
                else "-"
            )

            self.tabela.insert(
                "",
                "end",
                values=(
                    acesso.id,
                    nome_aluno,
                    acesso.data_hora.strftime(
                        "%d/%m/%Y %H:%M:%S"
                    ),
                    acesso.status,
                    motivo,
                ),
            )

    def atualizar_tela(self):
        self.carregar_alunos()
        self.carregar_historico()