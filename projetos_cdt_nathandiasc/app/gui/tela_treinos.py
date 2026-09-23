import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from app.models.exercicio import Exercicio
from app.models.treino import Treino

from app.services.aluno_service import (
    buscar_aluno_por_id,
    listar_alunos,
)

from app.services.exercicio_service import (
    cadastrar_exercicio,
    listar_exercicios,
)

from app.services.treino_service import (
    adicionar_exercicio_ao_treino,
    buscar_treino_por_id,
    cadastrar_treino,
    listar_exercicios_do_treino,
    listar_treinos_por_aluno,
)


class TelaTreinos:
    def __init__(self, container):
        self.container = container

        self.alunos = {}
        self.exercicios = {}
        self.treinos = {}

        self.criar_tela()

    def criar_tela(self):
        self.criar_cabecalho()
        self.criar_abas()

        self.criar_aba_exercicios()
        self.criar_aba_treinos()
        self.criar_aba_ficha()

        self.atualizar_tudo()

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
            text="Treinos",
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
            command=self.atualizar_tudo,
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

        self.aba_exercicios = tk.Frame(
            self.notebook,
            bg="#f4f4f4",
        )

        self.aba_treinos = tk.Frame(
            self.notebook,
            bg="#f4f4f4",
        )

        self.aba_ficha = tk.Frame(
            self.notebook,
            bg="#f4f4f4",
        )

        self.notebook.add(
            self.aba_exercicios,
            text="Exercícios",
        )

        self.notebook.add(
            self.aba_treinos,
            text="Criar Treino",
        )

        self.notebook.add(
            self.aba_ficha,
            text="Ficha de Treino",
        )

    # ==================================================
    # ABA EXERCÍCIOS
    # ==================================================

    def criar_aba_exercicios(self):
        formulario = tk.Frame(
            self.aba_exercicios,
            bg="white",
            padx=20,
            pady=20,
        )

        formulario.pack(
            fill="x",
            pady=(15, 10),
        )

        titulo = tk.Label(
            formulario,
            text="Cadastrar exercício",
            bg="white",
            fg="#111111",
            font=(
                "Arial",
                13,
                "bold",
            ),
        )

        titulo.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(0, 15),
        )

        for coluna in range(4):
            formulario.columnconfigure(
                coluna,
                weight=1,
            )

        self.entry_exercicio_nome = (
            self.criar_campo(
                formulario,
                "Nome",
                1,
                0,
            )
        )

        self.entry_grupo_muscular = (
            self.criar_campo(
                formulario,
                "Grupo muscular",
                1,
                1,
            )
        )

        self.entry_exercicio_descricao = (
            self.criar_campo(
                formulario,
                "Descrição",
                1,
                2,
            )
        )

        botao = tk.Button(
            formulario,
            text="Cadastrar exercício",
            command=self.cadastrar_novo_exercicio,
            bg="#111111",
            fg="white",
            activebackground="#ffd400",
            activeforeground="#111111",
            relief="flat",
            font=(
                "Arial",
                10,
                "bold",
            ),
            cursor="hand2",
        )

        botao.grid(
            row=1,
            column=3,
            sticky="sew",
            padx=5,
            pady=(21, 5),
        )

        lista_container = tk.Frame(
            self.aba_exercicios,
            bg="white",
            padx=20,
            pady=20,
        )

        lista_container.pack(
            fill="both",
            expand=True,
            pady=(10, 15),
        )

        colunas = (
            "id",
            "nome",
            "grupo",
            "descricao",
        )

        self.tabela_exercicios = ttk.Treeview(
            lista_container,
            columns=colunas,
            show="headings",
        )

        self.tabela_exercicios.heading(
            "id",
            text="ID",
        )

        self.tabela_exercicios.heading(
            "nome",
            text="Exercício",
        )

        self.tabela_exercicios.heading(
            "grupo",
            text="Grupo muscular",
        )

        self.tabela_exercicios.heading(
            "descricao",
            text="Descrição",
        )

        self.tabela_exercicios.column(
            "id",
            width=50,
            anchor="center",
        )

        self.tabela_exercicios.column(
            "nome",
            width=180,
        )

        self.tabela_exercicios.column(
            "grupo",
            width=160,
        )

        self.tabela_exercicios.column(
            "descricao",
            width=350,
        )

        barra = ttk.Scrollbar(
            lista_container,
            orient="vertical",
            command=self.tabela_exercicios.yview,
        )

        self.tabela_exercicios.configure(
            yscrollcommand=barra.set
        )

        self.tabela_exercicios.pack(
            side="left",
            fill="both",
            expand=True,
        )

        barra.pack(
            side="right",
            fill="y",
        )

    # ==================================================
    # ABA CRIAR TREINO
    # ==================================================

    def criar_aba_treinos(self):
        formulario = tk.Frame(
            self.aba_treinos,
            bg="white",
            padx=20,
            pady=20,
        )

        formulario.pack(
            fill="x",
            pady=(15, 10),
        )

        titulo = tk.Label(
            formulario,
            text="Criar novo treino",
            bg="white",
            fg="#111111",
            font=(
                "Arial",
                13,
                "bold",
            ),
        )

        titulo.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(0, 15),
        )

        for coluna in range(4):
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
        )

        tk.Label(
            bloco_aluno,
            text="Aluno",
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

        self.combo_aluno_treino = ttk.Combobox(
            bloco_aluno,
            state="readonly",
        )

        self.combo_aluno_treino.pack(
            fill="x",
            ipady=5,
        )

        self.entry_treino_nome = (
            self.criar_campo(
                formulario,
                "Nome do treino",
                1,
                1,
            )
        )

        self.entry_treino_objetivo = (
            self.criar_campo(
                formulario,
                "Objetivo",
                1,
                2,
            )
        )

        botao = tk.Button(
            formulario,
            text="Criar treino",
            command=self.criar_novo_treino,
            bg="#111111",
            fg="white",
            activebackground="#ffd400",
            activeforeground="#111111",
            relief="flat",
            font=(
                "Arial",
                10,
                "bold",
            ),
            cursor="hand2",
        )

        botao.grid(
            row=1,
            column=3,
            sticky="sew",
            padx=5,
            pady=(21, 5),
        )

        area_lista = tk.Frame(
            self.aba_treinos,
            bg="white",
            padx=20,
            pady=20,
        )

        area_lista.pack(
            fill="both",
            expand=True,
            pady=(10, 15),
        )

        filtro = tk.Frame(
            area_lista,
            bg="white",
        )

        filtro.pack(
            fill="x",
            pady=(0, 15),
        )

        tk.Label(
            filtro,
            text="Visualizar treinos do aluno:",
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                9,
                "bold",
            ),
        ).pack(
            side="left",
            padx=(0, 10),
        )

        self.combo_filtro_aluno = ttk.Combobox(
            filtro,
            state="readonly",
            width=35,
        )

        self.combo_filtro_aluno.pack(
            side="left"
        )

        self.combo_filtro_aluno.bind(
            "<<ComboboxSelected>>",
            lambda event: self.carregar_treinos_aluno(),
        )

        colunas = (
            "id",
            "nome",
            "objetivo",
            "criacao",
            "status",
        )

        self.tabela_treinos = ttk.Treeview(
            area_lista,
            columns=colunas,
            show="headings",
        )

        self.tabela_treinos.heading(
            "id",
            text="ID",
        )

        self.tabela_treinos.heading(
            "nome",
            text="Treino",
        )

        self.tabela_treinos.heading(
            "objetivo",
            text="Objetivo",
        )

        self.tabela_treinos.heading(
            "criacao",
            text="Criação",
        )

        self.tabela_treinos.heading(
            "status",
            text="Status",
        )

        self.tabela_treinos.column(
            "id",
            width=50,
            anchor="center",
        )

        self.tabela_treinos.column(
            "nome",
            width=180,
        )

        self.tabela_treinos.column(
            "objetivo",
            width=250,
        )

        self.tabela_treinos.column(
            "criacao",
            width=100,
            anchor="center",
        )

        self.tabela_treinos.column(
            "status",
            width=90,
            anchor="center",
        )

        self.tabela_treinos.pack(
            fill="both",
            expand=True,
        )

    # ==================================================
    # ABA FICHA
    # ==================================================

    def criar_aba_ficha(self):
        formulario = tk.Frame(
            self.aba_ficha,
            bg="white",
            padx=20,
            pady=20,
        )

        formulario.pack(
            fill="x",
            pady=(15, 10),
        )

        titulo = tk.Label(
            formulario,
            text="Adicionar exercício à ficha",
            bg="white",
            fg="#111111",
            font=(
                "Arial",
                13,
                "bold",
            ),
        )

        titulo.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(0, 15),
        )

        for coluna in range(4):
            formulario.columnconfigure(
                coluna,
                weight=1,
            )

        self.combo_treino_ficha = (
            self.criar_combo(
                formulario,
                "Treino",
                1,
                0,
            )
        )

        self.combo_exercicio_ficha = (
            self.criar_combo(
                formulario,
                "Exercício",
                1,
                1,
            )
        )

        self.entry_series = self.criar_campo(
            formulario,
            "Séries",
            1,
            2,
        )

        self.entry_repeticoes = (
            self.criar_campo(
                formulario,
                "Repetições",
                1,
                3,
            )
        )

        self.entry_carga = self.criar_campo(
            formulario,
            "Carga (kg)",
            2,
            0,
        )

        self.entry_descanso = (
            self.criar_campo(
                formulario,
                "Descanso (s)",
                2,
                1,
            )
        )

        self.entry_ordem = self.criar_campo(
            formulario,
            "Ordem",
            2,
            2,
        )

        botao = tk.Button(
            formulario,
            text="Adicionar à ficha",
            command=self.adicionar_exercicio,
            bg="#111111",
            fg="white",
            activebackground="#ffd400",
            activeforeground="#111111",
            relief="flat",
            font=(
                "Arial",
                10,
                "bold",
            ),
            cursor="hand2",
        )

        botao.grid(
            row=2,
            column=3,
            sticky="sew",
            padx=5,
            pady=(21, 5),
        )

        self.combo_treino_ficha.bind(
            "<<ComboboxSelected>>",
            lambda event: self.carregar_ficha(),
        )

        lista_container = tk.Frame(
            self.aba_ficha,
            bg="white",
            padx=20,
            pady=20,
        )

        lista_container.pack(
            fill="both",
            expand=True,
            pady=(10, 15),
        )

        self.label_ficha = tk.Label(
            lista_container,
            text="Selecione um treino",
            bg="white",
            fg="#111111",
            font=(
                "Arial",
                13,
                "bold",
            ),
        )

        self.label_ficha.pack(
            anchor="w",
            pady=(0, 15),
        )

        colunas = (
            "ordem",
            "exercicio",
            "grupo",
            "series",
            "repeticoes",
            "carga",
            "descanso",
        )

        self.tabela_ficha = ttk.Treeview(
            lista_container,
            columns=colunas,
            show="headings",
        )

        cabecalhos = {
            "ordem": "Ordem",
            "exercicio": "Exercício",
            "grupo": "Grupo",
            "series": "Séries",
            "repeticoes": "Repetições",
            "carga": "Carga",
            "descanso": "Descanso",
        }

        for coluna, texto in cabecalhos.items():
            self.tabela_ficha.heading(
                coluna,
                text=texto,
            )

        self.tabela_ficha.column(
            "ordem",
            width=60,
            anchor="center",
        )

        self.tabela_ficha.column(
            "exercicio",
            width=180,
        )

        self.tabela_ficha.column(
            "grupo",
            width=130,
        )

        self.tabela_ficha.column(
            "series",
            width=70,
            anchor="center",
        )

        self.tabela_ficha.column(
            "repeticoes",
            width=100,
            anchor="center",
        )

        self.tabela_ficha.column(
            "carga",
            width=90,
            anchor="center",
        )

        self.tabela_ficha.column(
            "descanso",
            width=90,
            anchor="center",
        )

        self.tabela_ficha.pack(
            fill="both",
            expand=True,
        )

    # ==================================================
    # HELPERS VISUAIS
    # ==================================================

    def criar_campo(
        self,
        container,
        texto,
        linha,
        coluna,
    ):
        bloco = tk.Frame(
            container,
            bg="white",
        )

        bloco.grid(
            row=linha,
            column=coluna,
            sticky="ew",
            padx=5,
            pady=5,
        )

        tk.Label(
            bloco,
            text=texto,
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

        entry = tk.Entry(
            bloco,
            relief="solid",
            borderwidth=1,
        )

        entry.pack(
            fill="x",
            ipady=6,
        )

        return entry

    def criar_combo(
        self,
        container,
        texto,
        linha,
        coluna,
    ):
        bloco = tk.Frame(
            container,
            bg="white",
        )

        bloco.grid(
            row=linha,
            column=coluna,
            sticky="ew",
            padx=5,
            pady=5,
        )

        tk.Label(
            bloco,
            text=texto,
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

        combo = ttk.Combobox(
            bloco,
            state="readonly",
        )

        combo.pack(
            fill="x",
            ipady=5,
        )

        return combo

    # ==================================================
    # EXERCÍCIOS
    # ==================================================

    def cadastrar_novo_exercicio(self):
        nome = (
            self.entry_exercicio_nome
            .get()
            .strip()
        )

        grupo = (
            self.entry_grupo_muscular
            .get()
            .strip()
        )

        descricao = (
            self.entry_exercicio_descricao
            .get()
            .strip()
        )

        if not nome or not grupo:
            messagebox.showwarning(
                "Campos obrigatórios",
                (
                    "Informe o nome e o "
                    "grupo muscular."
                ),
            )

            return

        try:
            exercicio = Exercicio(
                nome=nome,
                grupo_muscular=grupo,
                descricao=(
                    descricao
                    if descricao
                    else None
                ),
            )

            exercicio = cadastrar_exercicio(
                exercicio
            )

            messagebox.showinfo(
                "Exercício cadastrado",
                (
                    "Exercício cadastrado "
                    "com sucesso!\n\n"
                    f"ID: {exercicio.id}\n"
                    f"Nome: {exercicio.nome}"
                ),
            )

            self.entry_exercicio_nome.delete(
                0,
                tk.END,
            )

            self.entry_grupo_muscular.delete(
                0,
                tk.END,
            )

            self.entry_exercicio_descricao.delete(
                0,
                tk.END,
            )

            self.carregar_exercicios()

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível cadastrar "
                    "o exercício.\n\n"
                    f"{erro}"
                ),
            )

    def carregar_exercicios(self):
        for item in (
            self.tabela_exercicios
            .get_children()
        ):
            self.tabela_exercicios.delete(
                item
            )

        try:
            exercicios = listar_exercicios()

            self.exercicios = {}

            for exercicio in exercicios:
                descricao = (
                    exercicio.descricao
                    if exercicio.descricao
                    else "-"
                )

                self.tabela_exercicios.insert(
                    "",
                    "end",
                    values=(
                        exercicio.id,
                        exercicio.nome,
                        exercicio.grupo_muscular,
                        descricao,
                    ),
                )

                texto = (
                    f"{exercicio.id} - "
                    f"{exercicio.nome}"
                )

                self.exercicios[
                    texto
                ] = exercicio.id

            self.combo_exercicio_ficha[
                "values"
            ] = list(
                self.exercicios.keys()
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "os exercícios.\n\n"
                    f"{erro}"
                ),
            )

    # ==================================================
    # TREINOS
    # ==================================================

    def carregar_alunos(self):
        try:
            alunos = listar_alunos()

            self.alunos = {
                (
                    f"{aluno.id} - "
                    f"{aluno.nome}"
                ): aluno.id
                for aluno in alunos
                if aluno.status == "ativo"
            }

            valores = list(
                self.alunos.keys()
            )

            self.combo_aluno_treino[
                "values"
            ] = valores

            self.combo_filtro_aluno[
                "values"
            ] = valores

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "os alunos.\n\n"
                    f"{erro}"
                ),
            )

    def criar_novo_treino(self):
        aluno_texto = (
            self.combo_aluno_treino
            .get()
            .strip()
        )

        nome = (
            self.entry_treino_nome
            .get()
            .strip()
        )

        objetivo = (
            self.entry_treino_objetivo
            .get()
            .strip()
        )

        if not aluno_texto:
            messagebox.showwarning(
                "Aluno obrigatório",
                "Selecione um aluno.",
            )

            return

        if not nome or not objetivo:
            messagebox.showwarning(
                "Campos obrigatórios",
                (
                    "Informe o nome e "
                    "o objetivo do treino."
                ),
            )

            return

        try:
            aluno_id = self.alunos[
                aluno_texto
            ]

            treino = Treino(
                aluno_id=aluno_id,
                nome=nome,
                objetivo=objetivo,
                data_criacao=date.today(),
            )

            treino = cadastrar_treino(
                treino
            )

            aluno = buscar_aluno_por_id(
                aluno_id
            )

            messagebox.showinfo(
                "Treino criado",
                (
                    "Treino criado "
                    "com sucesso!\n\n"
                    f"ID: {treino.id}\n"
                    f"Aluno: {aluno.nome}\n"
                    f"Treino: {treino.nome}"
                ),
            )

            self.entry_treino_nome.delete(
                0,
                tk.END,
            )

            self.entry_treino_objetivo.delete(
                0,
                tk.END,
            )

            self.combo_aluno_treino.set("")

            self.carregar_todos_treinos()

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível criar "
                    "o treino.\n\n"
                    f"{erro}"
                ),
            )

    def carregar_treinos_aluno(self):
        for item in (
            self.tabela_treinos
            .get_children()
        ):
            self.tabela_treinos.delete(
                item
            )

        aluno_texto = (
            self.combo_filtro_aluno
            .get()
            .strip()
        )

        if not aluno_texto:
            return

        try:
            aluno_id = self.alunos[
                aluno_texto
            ]

            treinos = listar_treinos_por_aluno(
                aluno_id
            )

            for treino in treinos:
                status = (
                    "Ativo"
                    if treino.ativo
                    else "Inativo"
                )

                self.tabela_treinos.insert(
                    "",
                    "end",
                    values=(
                        treino.id,
                        treino.nome,
                        treino.objetivo,
                        treino.data_criacao.strftime(
                            "%d/%m/%Y"
                        ),
                        status,
                    ),
                )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "os treinos.\n\n"
                    f"{erro}"
                ),
            )

    def carregar_todos_treinos(self):
        try:
            self.treinos = {}

            for aluno_texto, aluno_id in (
                self.alunos.items()
            ):
                treinos = listar_treinos_por_aluno(
                    aluno_id
                )

                for treino in treinos:
                    if not treino.ativo:
                        continue

                    texto = (
                        f"{treino.id} - "
                        f"{treino.nome} - "
                        f"{aluno_texto.split(' - ', 1)[1]}"
                    )

                    self.treinos[
                        texto
                    ] = treino.id

            self.combo_treino_ficha[
                "values"
            ] = list(
                self.treinos.keys()
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "os treinos disponíveis.\n\n"
                    f"{erro}"
                ),
            )

    # ==================================================
    # FICHA
    # ==================================================

    def adicionar_exercicio(self):
        treino_texto = (
            self.combo_treino_ficha
            .get()
            .strip()
        )

        exercicio_texto = (
            self.combo_exercicio_ficha
            .get()
            .strip()
        )

        if not treino_texto:
            messagebox.showwarning(
                "Treino obrigatório",
                "Selecione um treino.",
            )

            return

        if not exercicio_texto:
            messagebox.showwarning(
                "Exercício obrigatório",
                "Selecione um exercício.",
            )

            return

        try:
            series = int(
                self.entry_series
                .get()
                .strip()
            )

            repeticoes = (
                self.entry_repeticoes
                .get()
                .strip()
            )

            if not repeticoes:
                raise ValueError(
                    "Informe as repetições."
                )

            carga_texto = (
                self.entry_carga
                .get()
                .strip()
            )

            descanso_texto = (
                self.entry_descanso
                .get()
                .strip()
            )

            ordem_texto = (
                self.entry_ordem
                .get()
                .strip()
            )

            carga = (
                float(
                    carga_texto.replace(
                        ",",
                        ".",
                    )
                )
                if carga_texto
                else None
            )

            descanso = (
                int(descanso_texto)
                if descanso_texto
                else None
            )

            ordem = (
                int(ordem_texto)
                if ordem_texto
                else None
            )

            treino_id = self.treinos[
                treino_texto
            ]

            exercicio_id = self.exercicios[
                exercicio_texto
            ]

            item_id = (
                adicionar_exercicio_ao_treino(
                    treino_id=treino_id,
                    exercicio_id=exercicio_id,
                    series=series,
                    repeticoes=repeticoes,
                    carga=carga,
                    descanso_segundos=descanso,
                    ordem=ordem,
                )
            )

            messagebox.showinfo(
                "Ficha atualizada",
                (
                    "Exercício adicionado "
                    "com sucesso!\n\n"
                    f"ID do item: {item_id}"
                ),
            )

            self.limpar_campos_ficha()
            self.carregar_ficha()

        except ValueError as erro:
            messagebox.showerror(
                "Dados inválidos",
                str(erro),
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível adicionar "
                    "o exercício à ficha.\n\n"
                    f"{erro}"
                ),
            )

    def carregar_ficha(self):
        for item in (
            self.tabela_ficha
            .get_children()
        ):
            self.tabela_ficha.delete(
                item
            )

        treino_texto = (
            self.combo_treino_ficha
            .get()
            .strip()
        )

        if not treino_texto:
            self.label_ficha.configure(
                text="Selecione um treino"
            )

            return

        try:
            treino_id = self.treinos[
                treino_texto
            ]

            treino = buscar_treino_por_id(
                treino_id
            )

            itens = listar_exercicios_do_treino(
                treino_id
            )

            self.label_ficha.configure(
                text=(
                    f"Ficha: {treino.nome} "
                    f"| Objetivo: {treino.objetivo}"
                )
            )

            for item in itens:
                carga = (
                    f"{item['carga']:.1f} kg"
                    if item["carga"] is not None
                    else "-"
                )

                descanso = (
                    f"{item['descanso_segundos']} s"
                    if (
                        item[
                            "descanso_segundos"
                        ]
                        is not None
                    )
                    else "-"
                )

                ordem = (
                    item["ordem"]
                    if item["ordem"] is not None
                    else "-"
                )

                self.tabela_ficha.insert(
                    "",
                    "end",
                    values=(
                        ordem,
                        item["nome"],
                        item[
                            "grupo_muscular"
                        ],
                        item["series"],
                        item["repeticoes"],
                        carga,
                        descanso,
                    ),
                )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "a ficha de treino.\n\n"
                    f"{erro}"
                ),
            )

    def limpar_campos_ficha(self):
        self.combo_exercicio_ficha.set("")

        campos = (
            self.entry_series,
            self.entry_repeticoes,
            self.entry_carga,
            self.entry_descanso,
            self.entry_ordem,
        )

        for campo in campos:
            campo.delete(
                0,
                tk.END,
            )

    # ==================================================
    # ATUALIZAÇÃO
    # ==================================================

    def atualizar_tudo(self):
        self.carregar_alunos()
        self.carregar_exercicios()
        self.carregar_todos_treinos()

        if (
            self.combo_filtro_aluno
            .get()
            .strip()
        ):
            self.carregar_treinos_aluno()

        if (
            self.combo_treino_ficha
            .get()
            .strip()
        ):
            self.carregar_ficha()