from app.database.connection import obter_conexao
from app.services.pagamento_service import (
    atualizar_pagamentos_atrasados,
)


def relatorio_geral() -> dict:
    conexao = obter_conexao()

    try:
        total_alunos = conexao.execute(
            """
            SELECT COUNT(*)
            FROM alunos
            """
        ).fetchone()[0]

        alunos_ativos = conexao.execute(
            """
            SELECT COUNT(*)
            FROM alunos
            WHERE status = 'ativo'
            """
        ).fetchone()[0]

        assinaturas_ativas = conexao.execute(
            """
            SELECT COUNT(*)
            FROM assinaturas
            WHERE status = 'ativa'
            """
        ).fetchone()[0]

        planos_ativos = conexao.execute(
            """
            SELECT COUNT(*)
            FROM planos
            WHERE ativo = 1
            """
        ).fetchone()[0]

        return {
            "total_alunos": total_alunos,
            "alunos_ativos": alunos_ativos,
            "assinaturas_ativas": assinaturas_ativas,
            "planos_ativos": planos_ativos,
        }

    finally:
        conexao.close()


def relatorio_financeiro() -> dict:
    atualizar_pagamentos_atrasados()

    conexao = obter_conexao()

    try:
        total_recebido = conexao.execute(
            """
            SELECT COALESCE(SUM(valor), 0)
            FROM pagamentos
            WHERE status = 'pago'
            """
        ).fetchone()[0]

        total_pendente = conexao.execute(
            """
            SELECT COALESCE(SUM(valor), 0)
            FROM pagamentos
            WHERE status = 'pendente'
            """
        ).fetchone()[0]

        total_atrasado = conexao.execute(
            """
            SELECT COALESCE(SUM(valor), 0)
            FROM pagamentos
            WHERE status = 'atrasado'
            """
        ).fetchone()[0]

        quantidade_pagos = conexao.execute(
            """
            SELECT COUNT(*)
            FROM pagamentos
            WHERE status = 'pago'
            """
        ).fetchone()[0]

        quantidade_pendentes = conexao.execute(
            """
            SELECT COUNT(*)
            FROM pagamentos
            WHERE status = 'pendente'
            """
        ).fetchone()[0]

        quantidade_atrasados = conexao.execute(
            """
            SELECT COUNT(*)
            FROM pagamentos
            WHERE status = 'atrasado'
            """
        ).fetchone()[0]

        return {
            "total_recebido": total_recebido,
            "total_pendente": total_pendente,
            "total_atrasado": total_atrasado,
            "quantidade_pagos": quantidade_pagos,
            "quantidade_pendentes": quantidade_pendentes,
            "quantidade_atrasados": quantidade_atrasados,
        }

    finally:
        conexao.close()


def relatorio_acessos() -> dict:
    conexao = obter_conexao()

    try:
        total_acessos = conexao.execute(
            """
            SELECT COUNT(*)
            FROM acessos
            """
        ).fetchone()[0]

        autorizados = conexao.execute(
            """
            SELECT COUNT(*)
            FROM acessos
            WHERE status = 'autorizado'
            """
        ).fetchone()[0]

        negados = conexao.execute(
            """
            SELECT COUNT(*)
            FROM acessos
            WHERE status = 'negado'
            """
        ).fetchone()[0]

        acessos_por_aluno = conexao.execute(
            """
            SELECT
                alunos.nome,
                COUNT(acessos.id) AS quantidade
            FROM alunos

            LEFT JOIN acessos
                ON acessos.aluno_id = alunos.id

            GROUP BY
                alunos.id,
                alunos.nome

            HAVING COUNT(acessos.id) > 0

            ORDER BY
                quantidade DESC,
                alunos.nome
            """
        ).fetchall()

        ranking = [
            {
                "nome": linha["nome"],
                "quantidade": linha["quantidade"],
            }
            for linha in acessos_por_aluno
        ]

        return {
            "total_acessos": total_acessos,
            "autorizados": autorizados,
            "negados": negados,
            "ranking_alunos": ranking,
        }

    finally:
        conexao.close()


def relatorio_planos() -> list[dict]:
    conexao = obter_conexao()

    try:
        linhas = conexao.execute(
            """
            SELECT
                planos.nome,
                planos.valor,
                COUNT(assinaturas.id) AS quantidade_assinaturas
            FROM planos

            LEFT JOIN assinaturas
                ON assinaturas.plano_id = planos.id
                AND assinaturas.status = 'ativa'

            GROUP BY
                planos.id,
                planos.nome,
                planos.valor

            ORDER BY
                quantidade_assinaturas DESC,
                planos.nome
            """
        ).fetchall()

        return [
            {
                "nome": linha["nome"],
                "valor": linha["valor"],
                "quantidade_assinaturas": (
                    linha["quantidade_assinaturas"]
                ),
            }
            for linha in linhas
        ]

    finally:
        conexao.close()