from datetime import date, timedelta

from app.models.aluno import Aluno
from app.models.assinatura import Assinatura
from app.models.plano import Plano

from app.services.acesso_service import (
    autorizar_acesso,
    listar_acessos,
)

from app.services.aluno_service import (
    cadastrar_aluno,
)

from app.services.assinatura_service import (
    cadastrar_assinatura,
)

from app.services.pagamento_service import (
    gerar_cobranca_para_assinatura,
)

from app.services.plano_service import (
    cadastrar_plano,
)


def criar_aluno_com_assinatura():
    aluno = Aluno(
        nome="Aluno Acesso",
        cpf="12312312312",
        data_nascimento=date(
            1995,
            8,
            20,
        ),
        email="acesso@teste.com",
        telefone="11977776666",
        data_cadastro=date.today(),
    )

    aluno = cadastrar_aluno(
        aluno
    )

    plano = Plano(
        nome="Plano Acesso",
        valor=99.90,
        descricao="Plano para testes de acesso.",
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


def test_acesso_autorizado_para_aluno_regular(
    banco_teste,
):
    aluno, _, assinatura = (
        criar_aluno_com_assinatura()
    )

    gerar_cobranca_para_assinatura(
        assinatura.id,
        date.today() + timedelta(days=10),
    )

    acesso = autorizar_acesso(
        aluno.id
    )

    assert acesso.id is not None
    assert acesso.aluno_id == aluno.id
    assert acesso.status == "autorizado"
    assert acesso.motivo is None


def test_acesso_negado_por_inadimplencia(
    banco_teste,
):
    aluno, _, assinatura = (
        criar_aluno_com_assinatura()
    )

    gerar_cobranca_para_assinatura(
        assinatura.id,
        date.today() - timedelta(days=10),
    )

    acesso = autorizar_acesso(
        aluno.id
    )

    assert acesso.id is not None
    assert acesso.status == "negado"
    assert acesso.motivo == "Pagamento em atraso."


def test_acesso_negado_sem_assinatura(
    banco_teste,
):
    aluno = Aluno(
        nome="Aluno Sem Assinatura",
        cpf="99988877766",
        data_nascimento=date(
            2001,
            3,
            15,
        ),
        email="semassinatura@teste.com",
        telefone="11966665555",
        data_cadastro=date.today(),
    )

    aluno = cadastrar_aluno(
        aluno
    )

    acesso = autorizar_acesso(
        aluno.id
    )

    assert acesso.id is not None
    assert acesso.status == "negado"
    assert acesso.motivo == "Aluno sem assinatura ativa."


def test_historico_de_acessos(
    banco_teste,
):
    aluno, _, assinatura = (
        criar_aluno_com_assinatura()
    )

    gerar_cobranca_para_assinatura(
        assinatura.id,
        date.today() + timedelta(days=10),
    )

    autorizar_acesso(
        aluno.id
    )

    autorizar_acesso(
        aluno.id
    )

    acessos = listar_acessos()

    assert len(acessos) == 2

    assert all(
        acesso.aluno_id == aluno.id
        for acesso in acessos
    )

    assert all(
        acesso.status == "autorizado"
        for acesso in acessos
    )