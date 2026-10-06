import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from app.database.schema import criar_tabelas
from app.gui.tela_acesso import TelaAcesso
from app.gui.tela_alunos import TelaAlunos
from app.gui.tela_assinaturas import TelaAssinaturas
from app.gui.tela_exportacao import TelaExportacao
from app.gui.tela_pagamentos import TelaPagamentos
from app.gui.tela_planos import TelaPlanos
from app.gui.tela_relatorios import TelaRelatorios
from app.gui.tela_treinos import TelaTreinos

from app.services.relatorio_service import (
    relatorio_acessos,
    relatorio_financeiro,
    relatorio_geral,
)

from app.services.usuario_service import (
    criar_usuario_root,
)


def obter_caminho_version() -> Path:
    if getattr(
        sys,
        "frozen",
        False,
    ):
        pasta_recursos = Path(
            getattr(
                sys,
                "_MEIPASS",
                Path(sys.executable)
                .resolve()
                .parent,
            )
        )

        return (
            pasta_recursos
            / "VERSION"
        )

    raiz_projeto = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    return (
        raiz_projeto
        / "VERSION"
    )


def obter_versao():
    caminho_version = (
        obter_caminho_version()
    )

    with open(
        caminho_version,
        "r",
        encoding="utf-8",
    ) as arquivo:
        return arquivo.read().strip()


class JanelaPrincipal:
    def __init__(
        self,
        root,
    ):
        self.root = root

        self.root.title(
            "SmartFit Gym Manager"
        )

        self.root.geometry(
            "1100x700"
        )

        self.root.minsize(
            900,
            600,
        )

        self.root.configure(
            bg="#f4f4f4"
        )

        self.criar_layout()
        self.carregar_dashboard()

    def criar_layout(self):
        self.criar_menu_lateral()
        self.criar_area_principal()

    def criar_menu_lateral(self):
        self.menu_lateral = tk.Frame(
            self.root,
            bg="#111111",
            width=230,
        )

        self.menu_lateral.pack(
            side="left",
            fill="y",
        )

        self.menu_lateral.pack_propagate(
            False
        )

        titulo = tk.Label(
            self.menu_lateral,
            text="SMARTFIT\nGYM MANAGER",
            bg="#111111",
            fg="#ffd400",
            font=(
                "Arial",
                18,
                "bold",
            ),
            justify="left",
        )

        titulo.pack(
            anchor="w",
            padx=25,
            pady=(30, 35),
        )

        self.criar_botao_menu(
            "Dashboard",
            self.carregar_dashboard,
        )

        self.criar_botao_menu(
            "Alunos",
            self.carregar_alunos,
        )

        self.criar_botao_menu(
            "Planos",
            self.carregar_planos,
        )

        self.criar_botao_menu(
            "Assinaturas",
            self.carregar_assinaturas,
        )

        self.criar_botao_menu(
            "Pagamentos",
            self.carregar_pagamentos,
        )

        self.criar_botao_menu(
            "Controle de Acesso",
            self.carregar_acesso,
        )

        self.criar_botao_menu(
            "Treinos",
            self.carregar_treinos,
        )

        self.criar_botao_menu(
            "Relatórios",
            self.carregar_relatorios,
        )

        self.criar_botao_menu(
            "Exportar JSON",
            self.carregar_exportacao,
        )

        versao = obter_versao()

        label_versao = tk.Label(
            self.menu_lateral,
            text=f"Versão {versao}",
            bg="#111111",
            fg="#aaaaaa",
            font=(
                "Arial",
                9,
            ),
        )

        label_versao.pack(
            side="bottom",
            pady=20,
        )

    def criar_botao_menu(
        self,
        texto,
        comando,
    ):
        botao = tk.Button(
            self.menu_lateral,
            text=texto,
            command=comando,
            bg="#111111",
            fg="white",
            activebackground="#ffd400",
            activeforeground="#111111",
            relief="flat",
            borderwidth=0,
            anchor="w",
            padx=25,
            pady=11,
            font=(
                "Arial",
                10,
                "bold",
            ),
            cursor="hand2",
        )

        botao.pack(
            fill="x"
        )

    def criar_area_principal(self):
        self.area_principal = tk.Frame(
            self.root,
            bg="#f4f4f4",
        )

        self.area_principal.pack(
            side="left",
            fill="both",
            expand=True,
        )

    def limpar_area_principal(self):
        for widget in (
            self.area_principal
            .winfo_children()
        ):
            widget.destroy()

    def carregar_alunos(self):
        self.limpar_area_principal()

        TelaAlunos(
            self.area_principal
        )

    def carregar_planos(self):
        self.limpar_area_principal()

        TelaPlanos(
            self.area_principal
        )

    def carregar_assinaturas(self):
        self.limpar_area_principal()

        TelaAssinaturas(
            self.area_principal
        )

    def carregar_pagamentos(self):
        self.limpar_area_principal()

        TelaPagamentos(
            self.area_principal
        )

    def carregar_acesso(self):
        self.limpar_area_principal()

        TelaAcesso(
            self.area_principal
        )

    def carregar_treinos(self):
        self.limpar_area_principal()

        TelaTreinos(
            self.area_principal
        )

    def carregar_relatorios(self):
        self.limpar_area_principal()

        TelaRelatorios(
            self.area_principal
        )

    def carregar_exportacao(self):
        self.limpar_area_principal()

        TelaExportacao(
            self.area_principal
        )

    def carregar_dashboard(self):
        self.limpar_area_principal()

        cabecalho = tk.Frame(
            self.area_principal,
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
            text="Dashboard",
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
            command=self.carregar_dashboard,
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

        conteudo = tk.Frame(
            self.area_principal,
            bg="#f4f4f4",
        )

        conteudo.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30,
        )

        try:
            geral = relatorio_geral()
            financeiro = relatorio_financeiro()
            acessos = relatorio_acessos()

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível carregar "
                    "os dados do dashboard.\n\n"
                    f"{erro}"
                ),
            )

            return

        cards = tk.Frame(
            conteudo,
            bg="#f4f4f4",
        )

        cards.pack(
            fill="x"
        )

        for coluna in range(4):
            cards.columnconfigure(
                coluna,
                weight=1,
            )

        self.criar_card(
            cards,
            coluna=0,
            titulo="Alunos",
            valor=geral[
                "total_alunos"
            ],
        )

        self.criar_card(
            cards,
            coluna=1,
            titulo="Assinaturas Ativas",
            valor=geral[
                "assinaturas_ativas"
            ],
        )

        self.criar_card(
            cards,
            coluna=2,
            titulo="Recebido",
            valor=(
                "R$ "
                f"{financeiro['total_recebido']:.2f}"
            ),
        )

        self.criar_card(
            cards,
            coluna=3,
            titulo="Acessos",
            valor=acessos[
                "total_acessos"
            ],
        )

        titulo_resumo = tk.Label(
            conteudo,
            text="Resumo da Operação",
            bg="#f4f4f4",
            fg="#111111",
            font=(
                "Arial",
                16,
                "bold",
            ),
        )

        titulo_resumo.pack(
            anchor="w",
            pady=(35, 15),
        )

        resumo = tk.Frame(
            conteudo,
            bg="white",
            padx=25,
            pady=25,
        )

        resumo.pack(
            fill="x"
        )

        textos = [
            (
                "Alunos ativos",
                geral[
                    "alunos_ativos"
                ],
            ),
            (
                "Planos ativos",
                geral[
                    "planos_ativos"
                ],
            ),
            (
                "Pagamentos pendentes",
                financeiro[
                    "quantidade_pendentes"
                ],
            ),
            (
                "Pagamentos atrasados",
                financeiro[
                    "quantidade_atrasados"
                ],
            ),
            (
                "Acessos autorizados",
                acessos[
                    "autorizados"
                ],
            ),
            (
                "Acessos negados",
                acessos[
                    "negados"
                ],
            ),
        ]

        for descricao, valor in textos:
            linha = tk.Frame(
                resumo,
                bg="white",
            )

            linha.pack(
                fill="x",
                pady=4,
            )

            label_descricao = tk.Label(
                linha,
                text=descricao,
                bg="white",
                fg="#555555",
                font=(
                    "Arial",
                    10,
                ),
            )

            label_descricao.pack(
                side="left"
            )

            label_valor = tk.Label(
                linha,
                text=str(valor),
                bg="white",
                fg="#111111",
                font=(
                    "Arial",
                    10,
                    "bold",
                ),
            )

            label_valor.pack(
                side="right"
            )

    def criar_card(
        self,
        container,
        coluna,
        titulo,
        valor,
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
            text=str(valor),
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


def executar_gui():
    criar_tabelas()
    criar_usuario_root()

    root = tk.Tk()

    JanelaPrincipal(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    executar_gui()