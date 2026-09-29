from datetime import datetime

from app.database.connection import obter_conexao
from app.models.acesso import Acesso

from app.services.aluno_service import buscar_aluno_por_id
from app.services.assinatura_service import (
    buscar_assinatura_ativa_por_aluno,
)
from app.services.pagamento_service import (
    existe_pagamento_atrasado,
)


def registrar_acesso(acesso: Acesso) -> Acesso:
    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO acessos (
                aluno_id,
                data_hora,
                status,
                motivo
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                acesso.aluno_id,
                acesso.data_hora.isoformat(),
                acesso.status,
                acesso.motivo,
            ),
        )

        conexao.commit()

        acesso.id = cursor.lastrowid

        return acesso

    finally:
        conexao.close()


def autorizar_acesso(aluno_id: int) -> Acesso:
    aluno = buscar_aluno_por_id(aluno_id)

    if aluno is None:
        return Acesso(
            aluno_id=aluno_id,
            data_hora=datetime.now(),
            status="negado",
            motivo="Aluno não encontrado.",
        )

    if aluno.status != "ativo":
        acesso = Acesso(
            aluno_id=aluno_id,
            data_hora=datetime.now(),
            status="negado",
            motivo="Aluno inativo.",
        )

        return registrar_acesso(acesso)

    assinatura = buscar_assinatura_ativa_por_aluno(
        aluno_id
    )

    if assinatura is None:
        acesso = Acesso(
            aluno_id=aluno_id,
            data_hora=datetime.now(),
            status="negado",
            motivo="Aluno sem assinatura ativa.",
        )

        return registrar_acesso(acesso)

    if existe_pagamento_atrasado(
        assinatura.id
    ):
        acesso = Acesso(
            aluno_id=aluno_id,
            data_hora=datetime.now(),
            status="negado",
            motivo="Pagamento em atraso.",
        )

        return registrar_acesso(acesso)

    acesso = Acesso(
        aluno_id=aluno_id,
        data_hora=datetime.now(),
        status="autorizado",
        motivo=None,
    )

    return registrar_acesso(acesso)


def listar_acessos() -> list[Acesso]:
    conexao = obter_conexao()

    try:
        linhas = conexao.execute(
            """
            SELECT
                id,
                aluno_id,
                data_hora,
                status,
                motivo
            FROM acessos
            ORDER BY data_hora DESC
            """
        ).fetchall()

        return [
            _linha_para_acesso(linha)
            for linha in linhas
        ]

    finally:
        conexao.close()


def listar_acessos_por_aluno(
    aluno_id: int,
) -> list[Acesso]:
    conexao = obter_conexao()

    try:
        linhas = conexao.execute(
            """
            SELECT
                id,
                aluno_id,
                data_hora,
                status,
                motivo
            FROM acessos
            WHERE aluno_id = ?
            ORDER BY data_hora DESC
            """,
            (aluno_id,),
        ).fetchall()

        return [
            _linha_para_acesso(linha)
            for linha in linhas
        ]

    finally:
        conexao.close()


def _linha_para_acesso(linha) -> Acesso:
    return Acesso(
        id=linha["id"],
        aluno_id=linha["aluno_id"],
        data_hora=datetime.fromisoformat(
            linha["data_hora"]
        ),
        status=linha["status"],
        motivo=linha["motivo"],
    )