from datetime import date

from app.database.connection import obter_conexao
from app.models.pagamento import Pagamento
from app.services.assinatura_service import buscar_assinatura_por_id
from app.services.plano_service import buscar_plano_por_id


def cadastrar_pagamento(pagamento: Pagamento) -> Pagamento:
    conexao = obter_conexao()

    try:
        cursor = conexao.execute(
            """
            INSERT INTO pagamentos (
                assinatura_id,
                valor,
                data_vencimento,
                data_pagamento,
                status,
                forma_pagamento
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                pagamento.assinatura_id,
                pagamento.valor,
                pagamento.data_vencimento.isoformat(),
                (
                    pagamento.data_pagamento.isoformat()
                    if pagamento.data_pagamento is not None
                    else None
                ),
                pagamento.status,
                pagamento.forma_pagamento,
            ),
        )

        conexao.commit()

        pagamento.id = cursor.lastrowid

        return pagamento

    finally:
        conexao.close()


def gerar_cobranca_para_assinatura(
    assinatura_id: int,
    data_vencimento: date,
) -> Pagamento:
    assinatura = buscar_assinatura_por_id(assinatura_id)

    if assinatura is None:
        raise ValueError("Assinatura não encontrada.")

    if assinatura.status != "ativa":
        raise ValueError(
            "Não é possível gerar cobrança para uma assinatura inativa."
        )

    plano = buscar_plano_por_id(assinatura.plano_id)

    if plano is None:
        raise ValueError(
            "O plano associado à assinatura não foi encontrado."
        )

    cobranca_existente = buscar_cobranca_por_assinatura_e_vencimento(
        assinatura_id,
        data_vencimento,
    )

    if cobranca_existente is not None:
        raise ValueError(
            "Já existe uma cobrança para esta assinatura "
            "com esse vencimento."
        )

    pagamento = Pagamento(
        assinatura_id=assinatura_id,
        valor=plano.valor,
        data_vencimento=data_vencimento,
    )

    return cadastrar_pagamento(pagamento)


def buscar_pagamento_por_id(
    pagamento_id: int,
) -> Pagamento | None:
    conexao = obter_conexao()

    try:
        linha = conexao.execute(
            """
            SELECT
                id,
                assinatura_id,
                valor,
                data_vencimento,
                data_pagamento,
                status,
                forma_pagamento
            FROM pagamentos
            WHERE id = ?
            """,
            (pagamento_id,),
        ).fetchone()

        if linha is None:
            return None

        return _linha_para_pagamento(linha)

    finally:
        conexao.close()


def buscar_cobranca_por_assinatura_e_vencimento(
    assinatura_id: int,
    data_vencimento: date,
) -> Pagamento | None:
    conexao = obter_conexao()

    try:
        linha = conexao.execute(
            """
            SELECT
                id,
                assinatura_id,
                valor,
                data_vencimento,
                data_pagamento,
                status,
                forma_pagamento
            FROM pagamentos
            WHERE assinatura_id = ?
              AND data_vencimento = ?
            LIMIT 1
            """,
            (
                assinatura_id,
                data_vencimento.isoformat(),
            ),
        ).fetchone()

        if linha is None:
            return None

        return _linha_para_pagamento(linha)

    finally:
        conexao.close()


def listar_pagamentos() -> list[Pagamento]:
    atualizar_pagamentos_atrasados()

    conexao = obter_conexao()

    try:
        linhas = conexao.execute(
            """
            SELECT
                id,
                assinatura_id,
                valor,
                data_vencimento,
                data_pagamento,
                status,
                forma_pagamento
            FROM pagamentos
            ORDER BY data_vencimento
            """
        ).fetchall()

        return [
            _linha_para_pagamento(linha)
            for linha in linhas
        ]

    finally:
        conexao.close()


def listar_pagamentos_por_assinatura(
    assinatura_id: int,
) -> list[Pagamento]:
    atualizar_pagamentos_atrasados()

    conexao = obter_conexao()

    try:
        linhas = conexao.execute(
            """
            SELECT
                id,
                assinatura_id,
                valor,
                data_vencimento,
                data_pagamento,
                status,
                forma_pagamento
            FROM pagamentos
            WHERE assinatura_id = ?
            ORDER BY data_vencimento
            """,
            (assinatura_id,),
        ).fetchall()

        return [
            _linha_para_pagamento(linha)
            for linha in linhas
        ]

    finally:
        conexao.close()


def registrar_pagamento(
    pagamento_id: int,
    forma_pagamento: str,
    data_pagamento: date | None = None,
) -> Pagamento | None:
    pagamento = buscar_pagamento_por_id(
        pagamento_id
    )

    if pagamento is None:
        return None

    if pagamento.status == "pago":
        raise ValueError(
            "Este pagamento já foi registrado como pago."
        )

    if data_pagamento is None:
        data_pagamento = date.today()

    conexao = obter_conexao()

    try:
        conexao.execute(
            """
            UPDATE pagamentos
            SET
                data_pagamento = ?,
                status = 'pago',
                forma_pagamento = ?
            WHERE id = ?
            """,
            (
                data_pagamento.isoformat(),
                forma_pagamento,
                pagamento_id,
            ),
        )

        conexao.commit()

    finally:
        conexao.close()

    return buscar_pagamento_por_id(pagamento_id)


def atualizar_pagamentos_atrasados():
    hoje = date.today().isoformat()

    conexao = obter_conexao()

    try:
        conexao.execute(
            """
            UPDATE pagamentos
            SET status = 'atrasado'
            WHERE status = 'pendente'
              AND data_pagamento IS NULL
              AND data_vencimento < ?
            """,
            (hoje,),
        )

        conexao.commit()

    finally:
        conexao.close()


def existe_pagamento_atrasado(
    assinatura_id: int,
) -> bool:
    atualizar_pagamentos_atrasados()

    conexao = obter_conexao()

    try:
        linha = conexao.execute(
            """
            SELECT 1
            FROM pagamentos
            WHERE assinatura_id = ?
              AND status = 'atrasado'
            LIMIT 1
            """,
            (assinatura_id,),
        ).fetchone()

        return linha is not None

    finally:
        conexao.close()


def _linha_para_pagamento(linha) -> Pagamento:
    return Pagamento(
        id=linha["id"],
        assinatura_id=linha["assinatura_id"],
        valor=linha["valor"],
        data_vencimento=date.fromisoformat(
            linha["data_vencimento"]
        ),
        data_pagamento=(
            date.fromisoformat(linha["data_pagamento"])
            if linha["data_pagamento"] is not None
            else None
        ),
        status=linha["status"],
        forma_pagamento=linha["forma_pagamento"],
    )