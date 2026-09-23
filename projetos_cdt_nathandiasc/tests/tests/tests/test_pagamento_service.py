from datetime import date, timedelta

from app.models.aluno import Aluno
from app.models.assinatura import Assinatura
from app.models.plano import Plano

from app.services.aluno_service import (
    cadastrar_aluno,
)

from app.services.assinatura_service import (
    cadastrar_assinatura,
)

from app.services.pagamento_service import (
    existe_pagamento_atrasado,
    gerar_cobranca_para_assinatura,
    listar_pagamentos,
    registrar_pagamento,
)

from app.services.plano_service import (
    cadastrar_plano,
)


def criar_assinatura_teste():
    aluno = Aluno(
        nome="Aluno Financeiro",
        cpf="98765432100",
        data_nascimento=date(
            1998,
            5,
            10,
        ),
        email="financeiro@teste.com",
        telefone="11988887777",
        data_cadastro=date.today(),
    )

    aluno = cadastrar_aluno(
        aluno
    )

    plano = Plano(
        nome="Plano Financeiro",
        valor=119.90,
        descricao="Plano para testes financeiros.",
    )

    plano = cadastrar_plano(
        plano
    )

    assinatura = Assinatura(
        aluno_id=aluno.id,
        plano_id=plano.id,
        data_inicio=date.today(),
    )

    assinatura = cadastrar_assinatura(
        assinatura
    )

    return aluno, plano, assinatura


def test_gerar_cobranca(
    banco_teste,
):
    _, plano, assinatura = (
        criar_assinatura_teste()
    )

    vencimento = (
        date.today()
        + timedelta(days=10)
    )

    pagamento = (
        gerar_cobranca_para_assinatura(
            assinatura.id,
            vencimento,
        )
    )

    assert pagamento.id is not None
    assert pagamento.assinatura_id == assinatura.id
    assert pagamento.valor == plano.valor
    assert pagamento.data_vencimento == vencimento
    assert pagamento.status == "pendente"


def test_listar_pagamentos(
    banco_teste,
):
    _, _, assinatura = (
        criar_assinatura_teste()
    )

    gerar_cobranca_para_assinatura(
        assinatura.id,
        date.today() + timedelta(days=5),
    )

    pagamentos = listar_pagamentos()

    assert len(pagamentos) == 1
    assert pagamentos[0].assinatura_id == assinatura.id


def test_registrar_pagamento(
    banco_teste,
):
    _, _, assinatura = (
        criar_assinatura_teste()
    )

    pagamento = (
        gerar_cobranca_para_assinatura(
            assinatura.id,
            date.today() + timedelta(days=5),
        )
    )

    pagamento_pago = registrar_pagamento(
        pagamento.id,
        "Pix",
    )

    assert pagamento_pago is not None
    assert pagamento_pago.status == "pago"
    assert pagamento_pago.data_pagamento == date.today()
    assert pagamento_pago.forma_pagamento == "Pix"


def test_pagamento_vencido_vira_atrasado(
    banco_teste,
):
    _, _, assinatura = (
        criar_assinatura_teste()
    )

    pagamento = (
        gerar_cobranca_para_assinatura(
            assinatura.id,
            date.today() - timedelta(days=5),
        )
    )

    assert pagamento.status == "pendente"

    pagamentos = listar_pagamentos()

    assert len(pagamentos) == 1
    assert pagamentos[0].status == "atrasado"


def test_detectar_inadimplencia(
    banco_teste,
):
    _, _, assinatura = (
        criar_assinatura_teste()
    )

    gerar_cobranca_para_assinatura(
        assinatura.id,
        date.today() - timedelta(days=10),
    )

    possui_atraso = existe_pagamento_atrasado(
        assinatura.id
    )

    assert possui_atraso is True