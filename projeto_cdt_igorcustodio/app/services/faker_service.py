import random
import re
from datetime import date, datetime, timedelta

from faker import Faker

from app.models.acesso import Acesso
from app.models.aluno import Aluno
from app.models.assinatura import Assinatura
from app.models.pagamento import Pagamento
from app.models.plano import Plano

from app.services.acesso_service import registrar_acesso
from app.services.aluno_service import cadastrar_aluno
from app.services.assinatura_service import cadastrar_assinatura
from app.services.pagamento_service import cadastrar_pagamento
from app.services.plano_service import (
    buscar_plano_por_nome,
    cadastrar_plano,
)


fake = Faker("pt_BR")


PLANOS_DEMONSTRACAO = (
    {
        "nome": "Smart",
        "valor": 99.90,
        "descricao": "Plano Smart - dados de demonstração.",
    },
    {
        "nome": "Fit",
        "valor": 119.90,
        "descricao": "Plano Fit - dados de demonstração.",
    },
    {
        "nome": "Black",
        "valor": 149.90,
        "descricao": "Plano Black - dados de demonstração.",
    },
)


def limpar_numeros(texto: str) -> str:
    return re.sub(r"\D", "", texto)


def criar_planos_demonstracao() -> list[Plano]:
    planos = []

    for dados_plano in PLANOS_DEMONSTRACAO:
        plano = buscar_plano_por_nome(
            dados_plano["nome"]
        )

        if plano is None:
            plano = Plano(
                nome=dados_plano["nome"],
                valor=dados_plano["valor"],
                descricao=dados_plano["descricao"],
            )

            plano = cadastrar_plano(plano)

        planos.append(plano)

    return planos


def criar_aluno_ficticio() -> Aluno:
    while True:
        aluno = Aluno(
            nome=fake.name(),
            cpf=limpar_numeros(
                fake.unique.cpf()
            ),
            data_nascimento=fake.date_of_birth(
                minimum_age=16,
                maximum_age=70,
            ),
            email=fake.unique.email(),
            telefone=limpar_numeros(
                fake.phone_number()
            ),
            data_cadastro=(
                date.today()
                - timedelta(
                    days=random.randint(0, 365)
                )
            ),
        )

        try:
            return cadastrar_aluno(aluno)

        except ValueError:
            continue


def criar_pagamento_ficticio(
    assinatura: Assinatura,
    valor: float,
) -> Pagamento:
    situacao = random.choice(
        [
            "pago",
            "pago",
            "pago",
            "pendente",
            "atrasado",
        ]
    )

    hoje = date.today()

    if situacao == "pago":
        data_vencimento = (
            hoje
            - timedelta(
                days=random.randint(1, 45)
            )
        )

        data_pagamento = (
            data_vencimento
            + timedelta(
                days=random.randint(0, 5)
            )
        )

        pagamento = Pagamento(
            assinatura_id=assinatura.id,
            valor=valor,
            data_vencimento=data_vencimento,
            data_pagamento=data_pagamento,
            status="pago",
            forma_pagamento=random.choice(
                [
                    "Pix",
                    "Cartão de crédito",
                    "Cartão de débito",
                ]
            ),
        )

    elif situacao == "atrasado":
        pagamento = Pagamento(
            assinatura_id=assinatura.id,
            valor=valor,
            data_vencimento=(
                hoje
                - timedelta(
                    days=random.randint(1, 30)
                )
            ),
            status="atrasado",
        )

    else:
        pagamento = Pagamento(
            assinatura_id=assinatura.id,
            valor=valor,
            data_vencimento=(
                hoje
                + timedelta(
                    days=random.randint(1, 30)
                )
            ),
            status="pendente",
        )

    return cadastrar_pagamento(
        pagamento
    )


def criar_acessos_ficticios(
    aluno: Aluno,
    pagamento: Pagamento,
) -> int:
    quantidade = random.randint(1, 5)

    for _ in range(quantidade):
        dias_atras = random.randint(0, 30)

        horario = (
            datetime.now()
            - timedelta(
                days=dias_atras,
                hours=random.randint(0, 12),
                minutes=random.randint(0, 59),
            )
        )

        if pagamento.status == "atrasado":
            status = random.choice(
                [
                    "negado",
                    "negado",
                    "autorizado",
                ]
            )

            motivo = (
                "Pagamento em atraso."
                if status == "negado"
                else None
            )

        else:
            status = "autorizado"
            motivo = None

        acesso = Acesso(
            aluno_id=aluno.id,
            data_hora=horario,
            status=status,
            motivo=motivo,
        )

        registrar_acesso(acesso)

    return quantidade


def popular_dados_demonstracao(
    quantidade_alunos: int = 20,
) -> dict:
    if quantidade_alunos <= 0:
        raise ValueError(
            "A quantidade de alunos deve ser maior que zero."
        )

    planos = criar_planos_demonstracao()

    total_assinaturas = 0
    total_pagamentos = 0
    total_acessos = 0

    for _ in range(quantidade_alunos):
        aluno = criar_aluno_ficticio()

        plano = random.choice(
            planos
        )

        assinatura = Assinatura(
            aluno_id=aluno.id,
            plano_id=plano.id,
            data_inicio=aluno.data_cadastro,
            status="ativa",
        )

        assinatura = cadastrar_assinatura(
            assinatura
        )

        total_assinaturas += 1

        pagamento = criar_pagamento_ficticio(
            assinatura=assinatura,
            valor=plano.valor,
        )

        total_pagamentos += 1

        total_acessos += criar_acessos_ficticios(
            aluno=aluno,
            pagamento=pagamento,
        )

    return {
        "alunos": quantidade_alunos,
        "planos": len(planos),
        "assinaturas": total_assinaturas,
        "pagamentos": total_pagamentos,
        "acessos": total_acessos,
    }