import sqlite3
import sys
from pathlib import Path


def obter_raiz_dados() -> Path:
    """
    Retorna a pasta onde os dados persistentes
    da aplicação devem ser armazenados.

    Durante o desenvolvimento:
        raiz do projeto.

    Quando executado pelo PyInstaller:
        mesma pasta do arquivo .exe.
    """

    if getattr(
        sys,
        "frozen",
        False,
    ):
        return (
            Path(sys.executable)
            .resolve()
            .parent
        )

    return (
        Path(__file__)
        .resolve()
        .parents[2]
    )


RAIZ_PROJETO = obter_raiz_dados()

PASTA_DADOS = (
    RAIZ_PROJETO
    / "data"
)

CAMINHO_BANCO = (
    PASTA_DADOS
    / "academia.db"
)


def obter_conexao():
    PASTA_DADOS.mkdir(
        parents=True,
        exist_ok=True,
    )

    conexao = sqlite3.connect(
        CAMINHO_BANCO
    )

    conexao.row_factory = (
        sqlite3.Row
    )

    conexao.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conexao