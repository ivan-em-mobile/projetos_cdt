from datetime import date

from app.database.connection import obter_conexao
from app.models.assinatura import Assinatura


def cadastrar_assinatura(assinatura: Assinatura) -> Assinatura:
    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO assinaturas (
                aluno_id,
                plano_id,
                data_inicio,
                data_fim,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                assinatura.aluno_id,
                assinatura.plano_id,
                assinatura.data_inicio.isoformat(),
                assinatura.data_fim.isoformat()
                if assinatura.data_fim is not None
                else None,
                assinatura.status,
            ),
        )

        conexao.commit()

        assinatura.id = cursor.lastrowid

        return assinatura

    finally:
        conexao.close()


def listar_assinaturas() -> list[Assinatura]:
    conexao = obter_conexao()

    try:
        linhas = conexao.execute(
            """
            SELECT
                id,
                aluno_id,
                plano_id,
                data_inicio,
                data_fim,
                status
            FROM assinaturas
            ORDER BY id
            """
        ).fetchall()

        return [_linha_para_assinatura(linha) for linha in linhas]

    finally:
        conexao.close()


def buscar_assinatura_por_id(
    assinatura_id: int,
) -> Assinatura | None:
    conexao = obter_conexao()

    try:
        linha = conexao.execute(
            """
            SELECT
                id,
                aluno_id,
                plano_id,
                data_inicio,
                data_fim,
                status
            FROM assinaturas
            WHERE id = ?
            """,
            (assinatura_id,),
        ).fetchone()

        if linha is None:
            return None

        return _linha_para_assinatura(linha)

    finally:
        conexao.close()


def buscar_assinatura_ativa_por_aluno(
    aluno_id: int,
) -> Assinatura | None:
    conexao = obter_conexao()

    try:
        linha = conexao.execute(
            """
            SELECT
                id,
                aluno_id,
                plano_id,
                data_inicio,
                data_fim,
                status
            FROM assinaturas
            WHERE aluno_id = ?
              AND status = 'ativa'
            ORDER BY id DESC
            LIMIT 1
            """,
            (aluno_id,),
        ).fetchone()

        if linha is None:
            return None

        return _linha_para_assinatura(linha)

    finally:
        conexao.close()


def _linha_para_assinatura(linha) -> Assinatura:
    return Assinatura(
        id=linha["id"],
        aluno_id=linha["aluno_id"],
        plano_id=linha["plano_id"],
        data_inicio=date.fromisoformat(linha["data_inicio"]),
        data_fim=(
            date.fromisoformat(linha["data_fim"])
            if linha["data_fim"] is not None
            else None
        ),
        status=linha["status"],
    )