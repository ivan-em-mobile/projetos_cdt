from datetime import date

import pytest

from app.models.aluno import Aluno
from app.services.aluno_service import (
    buscar_aluno_por_cpf,
    buscar_aluno_por_id,
    cadastrar_aluno,
    listar_alunos,
)


def criar_aluno_teste(
    nome="Aluno Teste",
    cpf="12345678901",
    email="aluno@teste.com",
):
    return Aluno(
        nome=nome,
        cpf=cpf,
        data_nascimento=date(
            2000,
            1,
            15,
        ),
        email=email,
        telefone="11999999999",
        data_cadastro=date.today(),
    )


def test_cadastrar_aluno(
    banco_teste,
):
    aluno = criar_aluno_teste()

    aluno_cadastrado = cadastrar_aluno(
        aluno
    )

    assert (
        aluno_cadastrado.id
        is not None
    )

    assert (
        aluno_cadastrado.nome
        == "Aluno Teste"
    )

    assert (
        aluno_cadastrado.cpf
        == "123.456.789-01"
    )

    assert (
        aluno_cadastrado.status
        == "ativo"
    )


def test_buscar_aluno_por_id_e_cpf(
    banco_teste,
):
    aluno = cadastrar_aluno(
        criar_aluno_teste()
    )

    aluno_por_id = buscar_aluno_por_id(
        aluno.id
    )

    aluno_por_cpf = buscar_aluno_por_cpf(
        "12345678901"
    )

    aluno_por_cpf_formatado = (
        buscar_aluno_por_cpf(
            "123.456.789-01"
        )
    )

    assert aluno_por_id is not None

    assert aluno_por_cpf is not None

    assert (
        aluno_por_cpf_formatado
        is not None
    )

    assert (
        aluno_por_id.id
        == aluno.id
    )

    assert (
        aluno_por_cpf.id
        == aluno.id
    )

    assert (
        aluno_por_cpf_formatado.id
        == aluno.id
    )

    assert (
        aluno_por_id.nome
        == "Aluno Teste"
    )

    assert (
        aluno_por_cpf.cpf
        == "123.456.789-01"
    )


def test_listar_alunos(
    banco_teste,
):
    cadastrar_aluno(
        criar_aluno_teste(
            nome="Aluno Um",
            cpf="11111111111",
            email="aluno1@teste.com",
        )
    )

    cadastrar_aluno(
        criar_aluno_teste(
            nome="Aluno Dois",
            cpf="22222222222",
            email="aluno2@teste.com",
        )
    )

    alunos = listar_alunos()

    assert len(alunos) == 2

    nomes = [
        aluno.nome
        for aluno in alunos
    ]

    assert "Aluno Um" in nomes
    assert "Aluno Dois" in nomes


def test_nao_permite_cpf_duplicado(
    banco_teste,
):
    primeiro_aluno = criar_aluno_teste(
        nome="Primeiro Aluno",
        cpf="33333333333",
        email="primeiro@teste.com",
    )

    segundo_aluno = criar_aluno_teste(
        nome="Segundo Aluno",
        cpf="333.333.333-33",
        email="segundo@teste.com",
    )

    cadastrar_aluno(
        primeiro_aluno
    )

    with pytest.raises(
        ValueError
    ):
        cadastrar_aluno(
            segundo_aluno
        )


def test_nao_permite_email_duplicado(
    banco_teste,
):
    primeiro_aluno = criar_aluno_teste(
        nome="Primeiro Aluno",
        cpf="44444444444",
        email="duplicado@teste.com",
    )

    segundo_aluno = criar_aluno_teste(
        nome="Segundo Aluno",
        cpf="55555555555",
        email="duplicado@teste.com",
    )

    cadastrar_aluno(
        primeiro_aluno
    )

    with pytest.raises(
        ValueError
    ):
        cadastrar_aluno(
            segundo_aluno
        )


def test_nao_permite_cpf_com_menos_de_11_digitos(
    banco_teste,
):
    aluno = criar_aluno_teste(
        cpf="1234567890",
    )

    with pytest.raises(
        ValueError,
        match="CPF inválido",
    ):
        cadastrar_aluno(
            aluno
        )


def test_nao_permite_cpf_com_mais_de_11_digitos(
    banco_teste,
):
    aluno = criar_aluno_teste(
        cpf="123456789012",
    )

    with pytest.raises(
        ValueError,
        match="CPF inválido",
    ):
        cadastrar_aluno(
            aluno
        )


def test_nao_permite_cpf_com_caracteres_invalidos(
    banco_teste,
):
    aluno = criar_aluno_teste(
        cpf="123.456.789-0A",
    )

    with pytest.raises(
        ValueError,
        match="CPF inválido",
    ):
        cadastrar_aluno(
            aluno
        )