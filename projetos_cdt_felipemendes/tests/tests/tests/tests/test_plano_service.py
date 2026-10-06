import pytest

from app.models.plano import Plano
from app.services.plano_service import (
    buscar_plano_por_id,
    buscar_plano_por_nome,
    cadastrar_plano,
    listar_planos,
)


def criar_plano_teste(
    nome="Plano Teste",
    valor=99.90,
):
    return Plano(
        nome=nome,
        valor=valor,
        descricao="Plano criado para testes.",
    )


def test_cadastrar_plano(
    banco_teste,
):
    plano = criar_plano_teste()

    plano_cadastrado = cadastrar_plano(
        plano
    )

    assert plano_cadastrado.id is not None
    assert plano_cadastrado.nome == "Plano Teste"
    assert plano_cadastrado.valor == 99.90
    assert plano_cadastrado.ativo is True


def test_buscar_plano_por_id(
    banco_teste,
):
    plano = cadastrar_plano(
        criar_plano_teste()
    )

    plano_encontrado = buscar_plano_por_id(
        plano.id
    )

    assert plano_encontrado is not None
    assert plano_encontrado.id == plano.id
    assert plano_encontrado.nome == "Plano Teste"


def test_buscar_plano_por_nome(
    banco_teste,
):
    cadastrar_plano(
        criar_plano_teste(
            nome="Plano Especial",
            valor=129.90,
        )
    )

    plano = buscar_plano_por_nome(
        "Plano Especial"
    )

    assert plano is not None
    assert plano.nome == "Plano Especial"
    assert plano.valor == 129.90


def test_listar_planos(
    banco_teste,
):
    cadastrar_plano(
        criar_plano_teste(
            nome="Plano A",
            valor=89.90,
        )
    )

    cadastrar_plano(
        criar_plano_teste(
            nome="Plano B",
            valor=119.90,
        )
    )

    planos = listar_planos()

    assert len(planos) == 2

    nomes = [
        plano.nome
        for plano in planos
    ]

    assert "Plano A" in nomes
    assert "Plano B" in nomes


def test_nao_permite_nome_de_plano_duplicado(
    banco_teste,
):
    primeiro_plano = criar_plano_teste(
        nome="Plano Duplicado",
        valor=99.90,
    )

    segundo_plano = criar_plano_teste(
        nome="Plano Duplicado",
        valor=149.90,
    )

    cadastrar_plano(
        primeiro_plano
    )

    with pytest.raises(ValueError):
        cadastrar_plano(
            segundo_plano
        )


def test_nao_permite_plano_duplicado_ignorando_maiusculas(
    banco_teste,
):
    primeiro_plano = criar_plano_teste(
        nome="Plano Web",
        valor=129.90,
    )

    segundo_plano = criar_plano_teste(
        nome="plano web",
        valor=149.90,
    )

    cadastrar_plano(
        primeiro_plano
    )

    with pytest.raises(
        ValueError,
        match="Já existe um plano cadastrado com esse nome",
    ):
        cadastrar_plano(
            segundo_plano
        )


def test_buscar_plano_por_nome_ignora_maiusculas_e_espacos(
    banco_teste,
):
    plano = cadastrar_plano(
        criar_plano_teste(
            nome="Plano Premium",
            valor=199.90,
        )
    )

    plano_encontrado = buscar_plano_por_nome(
        "  PLANO PREMIUM  "
    )

    assert plano_encontrado is not None
    assert plano_encontrado.id == plano.id
    assert plano_encontrado.nome == "Plano Premium"