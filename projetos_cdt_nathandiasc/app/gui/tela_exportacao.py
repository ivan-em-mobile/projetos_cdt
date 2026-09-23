import tkinter as tk
from tkinter import messagebox

from app.services.export_service import (
    exportar_banco_json,
)

from app.services.usuario_service import (
    USUARIO_ROOT,
    autenticar_usuario,
)


class TelaExportacao:
    def __init__(self, container):
        self.container = container

        self.criar_tela()

    def criar_tela(self):
        self.criar_cabecalho()
        self.criar_conteudo()

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
            text="Exportar banco de dados",
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

    def criar_conteudo(self):
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

        card = tk.Frame(
            area,
            bg="white",
            padx=35,
            pady=30,
        )

        card.pack(
            fill="x"
        )

        titulo = tk.Label(
            card,
            text="Exportação JSON",
            bg="white",
            fg="#111111",
            font=(
                "Arial",
                16,
                "bold",
            ),
        )

        titulo.pack(
            anchor="w"
        )

        descricao = tk.Label(
            card,
            text=(
                "Esta funcionalidade exporta os dados "
                "da academia para um arquivo JSON.\n\n"
                "Por segurança, a operação exige "
                "autenticação administrativa."
            ),
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                10,
            ),
            justify="left",
        )

        descricao.pack(
            anchor="w",
            pady=(10, 25),
        )

        formulario = tk.Frame(
            card,
            bg="white",
        )

        formulario.pack(
            fill="x"
        )

        formulario.columnconfigure(
            0,
            weight=1,
        )

        formulario.columnconfigure(
            1,
            weight=1,
        )

        bloco_usuario = tk.Frame(
            formulario,
            bg="white",
        )

        bloco_usuario.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10),
        )

        label_usuario = tk.Label(
            bloco_usuario,
            text="Usuário",
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                9,
                "bold",
            ),
        )

        label_usuario.pack(
            anchor="w",
            pady=(0, 5),
        )

        self.entry_usuario = tk.Entry(
            bloco_usuario,
            font=(
                "Arial",
                10,
            ),
            relief="solid",
            borderwidth=1,
        )

        self.entry_usuario.pack(
            fill="x",
            ipady=7,
        )

        bloco_senha = tk.Frame(
            formulario,
            bg="white",
        )

        bloco_senha.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(10, 0),
        )

        label_senha = tk.Label(
            bloco_senha,
            text="Senha",
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                9,
                "bold",
            ),
        )

        label_senha.pack(
            anchor="w",
            pady=(0, 5),
        )

        self.entry_senha = tk.Entry(
            bloco_senha,
            font=(
                "Arial",
                10,
            ),
            relief="solid",
            borderwidth=1,
            show="*",
        )

        self.entry_senha.pack(
            fill="x",
            ipady=7,
        )

        botoes = tk.Frame(
            card,
            bg="white",
        )

        botoes.pack(
            fill="x",
            pady=(25, 0),
        )

        botao_exportar = tk.Button(
            botoes,
            text="Autenticar e exportar JSON",
            command=self.exportar,
            bg="#111111",
            fg="white",
            activebackground="#ffd400",
            activeforeground="#111111",
            relief="flat",
            padx=25,
            pady=10,
            font=(
                "Arial",
                10,
                "bold",
            ),
            cursor="hand2",
        )

        botao_exportar.pack(
            side="left"
        )

        botao_limpar = tk.Button(
            botoes,
            text="Limpar",
            command=self.limpar_campos,
            bg="#dddddd",
            fg="#111111",
            activebackground="#cccccc",
            relief="flat",
            padx=25,
            pady=10,
            font=(
                "Arial",
                10,
                "bold",
            ),
            cursor="hand2",
        )

        botao_limpar.pack(
            side="left",
            padx=(10, 0),
        )

        self.status = tk.Frame(
            area,
            bg="white",
            padx=30,
            pady=25,
        )

        self.status.pack(
            fill="x",
            pady=(20, 0),
        )

        self.label_status = tk.Label(
            self.status,
            text="Nenhuma exportação realizada nesta sessão.",
            bg="white",
            fg="#666666",
            font=(
                "Arial",
                11,
            ),
            justify="left",
        )

        self.label_status.pack(
            anchor="w"
        )

        informacao = tk.Frame(
            area,
            bg="white",
            padx=30,
            pady=25,
        )

        informacao.pack(
            fill="x",
            pady=(20, 0),
        )

        titulo_info = tk.Label(
            informacao,
            text="Destino dos arquivos",
            bg="white",
            fg="#111111",
            font=(
                "Arial",
                13,
                "bold",
            ),
        )

        titulo_info.pack(
            anchor="w"
        )

        texto_info = tk.Label(
            informacao,
            text=(
                "Os arquivos exportados são armazenados em:\n\n"
                "data/exports/\n\n"
                "Cada exportação recebe data e horário "
                "no nome do arquivo."
            ),
            bg="white",
            fg="#555555",
            font=(
                "Arial",
                10,
            ),
            justify="left",
        )

        texto_info.pack(
            anchor="w",
            pady=(10, 0),
        )

    def exportar(self):
        nome_usuario = (
            self.entry_usuario
            .get()
            .strip()
        )

        senha = (
            self.entry_senha
            .get()
        )

        if not nome_usuario or not senha:
            messagebox.showwarning(
                "Autenticação",
                (
                    "Informe o usuário e a senha "
                    "antes de continuar."
                ),
            )

            return

        if nome_usuario != USUARIO_ROOT:
            self.exibir_falha()

            messagebox.showerror(
                "Acesso negado",
                (
                    "Somente o usuário administrativo "
                    "root pode realizar a exportação."
                ),
            )

            return

        try:
            usuario = autenticar_usuario(
                nome_usuario,
                senha,
            )

            if usuario is None:
                self.exibir_falha()

                messagebox.showerror(
                    "Acesso negado",
                    "Usuário ou senha inválidos.",
                )

                self.entry_senha.delete(
                    0,
                    tk.END,
                )

                return

            caminho = exportar_banco_json()

            self.status.configure(
                bg="#dff5e1"
            )

            self.label_status.configure(
                text=(
                    "EXPORTAÇÃO CONCLUÍDA\n\n"
                    f"Arquivo: {caminho.name}\n"
                    f"Local: {caminho}"
                ),
                bg="#dff5e1",
                fg="#156b25",
                font=(
                    "Arial",
                    11,
                    "bold",
                ),
            )

            messagebox.showinfo(
                "Exportação concluída",
                (
                    "Banco de dados exportado "
                    "com sucesso!\n\n"
                    f"Arquivo:\n{caminho.name}"
                ),
            )

            self.limpar_campos()

        except Exception as erro:
            self.status.configure(
                bg="#fde2e2"
            )

            self.label_status.configure(
                text=(
                    "FALHA NA EXPORTAÇÃO\n\n"
                    f"{erro}"
                ),
                bg="#fde2e2",
                fg="#a51f1f",
                font=(
                    "Arial",
                    11,
                    "bold",
                ),
            )

            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível exportar "
                    "o banco de dados.\n\n"
                    f"{erro}"
                ),
            )

    def exibir_falha(self):
        self.status.configure(
            bg="#fde2e2"
        )

        self.label_status.configure(
            text=(
                "AUTENTICAÇÃO NEGADA\n\n"
                "A exportação não foi realizada."
            ),
            bg="#fde2e2",
            fg="#a51f1f",
            font=(
                "Arial",
                11,
                "bold",
            ),
        )

    def limpar_campos(self):
        self.entry_usuario.delete(
            0,
            tk.END,
        )

        self.entry_senha.delete(
            0,
            tk.END,
        )

        self.entry_usuario.focus()