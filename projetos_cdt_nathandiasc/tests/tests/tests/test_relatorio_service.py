from datetime import date, timedelta

from app.models.aluno import Aluno
from app.models.assinatura import Assinatura
from app.models.plano import Plano

from app.services.acesso_service import (
    autorizar_acesso,
)

from app.services.aluno_service import (
    cadastrar_aluno,
)

from app.services.assinatura_service import (
    cadastrar_assinatura,
)

from app.services.pagamento_service import (
    gerar_cobranca_para_assinatura,
    registrar_pagamento,
)

from app.services.plano_service import (
    cadastrar_plano,
)

from app.services.relatorio_service import (
    relatorio_acessos,
    relatorio_financeiro,
    relatorio_geral,
    relatorio_planos,
)


def criar_aluno(
    nome,
    cpf,
    email,
):
    aluno = Aluno(
        nome=nome,
        cpf=cpf,
        data_nascimento=date(
            2000,
            1,
            1,
        ),
        email=email,
        telefone="11999999999",
        data_cadastro=date.today(),
    )

    return cadastrar_aluno(
        aluno
    )


def criar_plano(
    nome,
    valor=99.90,
):
    plano = Plano(
        nome=nome,
        valor=valor,
        descricao="Plano criado para testes.",
    )

    return cadastrar_plano(
        plano
    )


def criar_assinatura(
    aluno_id,
    plano_id,
):
    assinatura = Assinatura(
        aluno_id=aluno_id,
        plano_id=plano_id,
        data_inicio=date.today(),
    )

    return cadastrar_assinatura(
        assinatura
    )


def test_relatorio_geral(
    banco_teste,
):
    aluno_1 = criar_aluno(
        nome="Aluno Um",
        cpf="11111111111",
        email="um@teste.com",
    )

    criar_aluno(
        nome="Aluno Dois",
        cpf="22222222222",
        email="dois@teste.com",
    )

    plano = criar_plano(
        nome="Plano Geral",
    )

    criar_assinatura(
        aluno_1.id,
        plano.id,
    )

    dados = relatorio_geral()

    assert dados["total_alunos"] == 2
    assert dados["alunos_ativos"] == 2
    assert dados["assinaturas_ativas"] == 1
    assert dados["planos_ativos"] == 1


def test_relatorio_financeiro(
    banco_teste,
):
    aluno = criar_aluno(
        nome="Aluno Financeiro",
        cpf="33333333333",
        email="financeiro@teste.com",
    )

    plano = criar_plano(
        nome="Plano Financeiro",
        valor=100.00,
    )

    assinatura = criar_assinatura(
        aluno.id,
        plano.id,
    )

    pagamento_pago = (
        gerar_cobranca_para_assinatura(
            assinatura.id,
            date.today() + timedelta(days=10),
        )
    )

    registrar_pagamento(
        pagamento_pago.id,
        "Pix",
    )

    gerar_cobranca_para_assinatura(
        assinatura.id,
        date.today() + timedelta(days=20),
    )

    gerar_cobranca_para_assinatura(
        assinatura.id,
        date.today() - timedelta(days=5),
    )

    dados = relatorio_financeiro()

    assert dados["total_recebido"] == 100.00
    assert dados["total_pendente"] == 100.00
    assert dados["total_atrasado"] == 100.00

    assert dados["quantidade_pagos"] == 1
    assert dados["quantidade_pendentes"] == 1
    assert dados["quantidade_atrasados"] == 1


def test_relatorio_acessos(
    banco_teste,
):
    plano = criar_plano(
        nome="Plano Acesso",
    )

    aluno_regular = criar_aluno(
        nome="Aluno Regular",
        cpf="44444444444",
        email="regular@teste.com",
    )

    assinatura_regular = criar_assinatura(
        aluno_regular.id,
        plano.id,
    )

    gerar_cobranca_para_assinatura(
        assinatura_regular.id,
        date.today() + timedelta(days=10),
    )

    autorizar_acesso(
        aluno_regular.id
    )

    autorizar_acesso(
        aluno_regular.id
    )

    aluno_inadimplente = criar_aluno(
        nome="Aluno Inadimplente",
        cpf="55555555555",
        email="inadimplente@teste.com",
    )

    assinatura_inadimplente = (
        criar_assinatura(
            aluno_inadimplente.id,
            plano.id,
        )
    )

    gerar_cobranca_para_assinatura(
        assinatura_inadimplente.id,
        date.today() - timedelta(days=10),
    )

    autorizar_acesso(
        aluno_inadimplente.id
    )

    dados = relatorio_acessos()

    assert dados["total_acessos"] == 3
    assert dados["autorizados"] == 2
    assert dados["negados"] == 1

    assert len(
        dados["ranking_alunos"]
    ) == 2

    assert (
        dados["ranking_alunos"][0]["nome"]
        == "Aluno Regular"
    )

    assert (
        dados["ranking_alunos"][0]["quantidade"]
        == 2
    )


def test_relatorio_planos(
    banco_teste,
):
    plano_a = criar_plano(
        nome="Plano A",
        valor=99.90,
    )

    plano_b = criar_plano(
        nome="Plano B",
        valor=149.90,
    )

    aluno_1 = criar_aluno(
        nome="Aluno Plano 1",
        cpf="66666666666",
        email="plano1@teste.com",
    )

    aluno_2 = criar_aluno(
        nome="Aluno Plano 2",
        cpf="77777777777",
        email="plano2@teste.com",
    )

    criar_assinatura(
        aluno_1.id,
        plano_a.id,
    )

    criar_assinatura(
        aluno_2.id,
        plano_a.id,
    )

    dados = relatorio_planos()

    planos = {
        plano["nome"]: plano
        for plano in dados
    }

    assert (
        planos["Plano A"]["quantidade_assinaturas"]
        == 2
    )

    assert (
        planos["Plano B"]["quantidade_assinaturas"]
        == 0
    )

    assert planos["Plano A"]["valor"] == 99.90
    assert planos["Plano B"]["valor"] == 149.90