from app.database.connection import obter_conexao
from app.models.exercicio import Exercicio


def cadastrar_exercicio(exercicio: Exercicio) -> Exercicio:
    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO exercicios (
                nome,
                grupo_muscular,
                descricao
            )
            VALUES (?, ?, ?)
            """,
            (
                exercicio.nome,
                exercicio.grupo_muscular,
                exercicio.descricao,
            ),
        )

        conexao.commit()

        exercicio.id = cursor.lastrowid

        return exercicio

    finally:
        conexao.close()


def buscar_exercicio_por_id(
    exercicio_id: int,
) -> Exercicio | None:
    conexao = obter_conexao()

    try:
        linha = conexao.execute(
            """
            SELECT
                id,
                nome,
                grupo_muscular,
                descricao
            FROM exercicios
            WHERE id = ?
            """,
            (exercicio_id,),
        ).fetchone()

        if linha is None:
            return None

        return _linha_para_exercicio(linha)

    finally:
        conexao.close()


def listar_exercicios() -> list[Exercicio]:
    conexao = obter_conexao()

    try:
        linhas = conexao.execute(
            """
            SELECT
                id,
                nome,
                grupo_muscular,
                descricao
            FROM exercicios
            ORDER BY grupo_muscular, nome
            """
        ).fetchall()

        return [
            _linha_para_exercicio(linha)
            for linha in linhas
        ]

    finally:
        conexao.close()


def listar_exercicios_por_grupo(
    grupo_muscular: str,
) -> list[Exercicio]:
    conexao = obter_conexao()

    try:
        linhas = conexao.execute(
            """
            SELECT
                id,
                nome,
                grupo_muscular,
                descricao
            FROM exercicios
            WHERE LOWER(grupo_muscular) = LOWER(?)
            ORDER BY nome
            """,
            (grupo_muscular,),
        ).fetchall()

        return [
            _linha_para_exercicio(linha)
            for linha in linhas
        ]

    finally:
        conexao.close()


def _linha_para_exercicio(linha) -> Exercicio:
    return Exercicio(
        id=linha["id"],
        nome=linha["nome"],
        grupo_muscular=linha["grupo_muscular"],
        descricao=linha["descricao"],
    )