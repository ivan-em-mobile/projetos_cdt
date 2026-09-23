import sqlite3

from app.database.connection import obter_conexao
from app.models.plano import Plano


def cadastrar_plano(plano: Plano) -> Plano:
    conexao = obter_conexao()

    try:
        nome_normalizado = plano.nome.strip()

        if not nome_normalizado:
            raise ValueError(
                "O nome do plano não pode ficar vazio."
            )

        plano_existente = conexao.execute(
            """
            SELECT id
            FROM planos
            WHERE LOWER(TRIM(nome)) = LOWER(TRIM(?))
            """,
            (nome_normalizado,),
        ).fetchone()

        if plano_existente is not None:
            raise ValueError(
                "Já existe um plano cadastrado com esse nome."
            )

        plano.nome = nome_normalizado

        cursor = conexao.execute(
            """
            INSERT INTO planos (
                nome,
                valor,
                descricao,
                ativo
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                plano.nome,
                plano.valor,
                plano.descricao,
                int(plano.ativo),
            ),
        )

        conexao.commit()

        plano.id = cursor.lastrowid

        return plano

    except sqlite3.IntegrityError as erro:
        raise ValueError(
            "Não foi possível cadastrar o plano. "
            "Verifique se já existe um plano com esse nome."
        ) from erro

    finally:
        conexao.close()


def listar_planos() -> list[Plano]:
    conexao = obter_conexao()

    try:
        linhas = conexao.execute(
            """
            SELECT
                id,
                nome,
                valor,
                descricao,
                ativo
            FROM planos
            ORDER BY nome
            """
        ).fetchall()

        return [
            _linha_para_plano(linha)
            for linha in linhas
        ]

    finally:
        conexao.close()


def buscar_plano_por_id(
    plano_id: int,
) -> Plano | None:
    conexao = obter_conexao()

    try:
        linha = conexao.execute(
            """
            SELECT
                id,
                nome,
                valor,
                descricao,
                ativo
            FROM planos
            WHERE id = ?
            """,
            (plano_id,),
        ).fetchone()

        if linha is None:
            return None

        return _linha_para_plano(linha)

    finally:
        conexao.close()


def buscar_plano_por_nome(
    nome: str,
) -> Plano | None:
    conexao = obter_conexao()

    try:
        linha = conexao.execute(
            """
            SELECT
                id,
                nome,
                valor,
                descricao,
                ativo
            FROM planos
            WHERE LOWER(TRIM(nome)) = LOWER(TRIM(?))
            """,
            (nome,),
        ).fetchone()

        if linha is None:
            return None

        return _linha_para_plano(linha)

    finally:
        conexao.close()


def _linha_para_plano(linha) -> Plano:
    return Plano(
        id=linha["id"],
        nome=linha["nome"],
        valor=linha["valor"],
        descricao=linha["descricao"],
        ativo=bool(linha["ativo"]),
    )