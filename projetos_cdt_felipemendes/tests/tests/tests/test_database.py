import sqlite3


def test_tabelas_sao_criadas(
    banco_teste,
):
    conexao = sqlite3.connect(
        banco_teste
    )

    try:
        linhas = conexao.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

    finally:
        conexao.close()

    tabelas = {
        linha[0]
        for linha in linhas
    }

    tabelas_esperadas = {
        "alunos",
        "planos",
        "assinaturas",
        "pagamentos",
        "acessos",
        "treinos",
        "exercicios",
        "treino_exercicios",
        "usuarios",
    }

    assert tabelas_esperadas.issubset(
        tabelas
    )