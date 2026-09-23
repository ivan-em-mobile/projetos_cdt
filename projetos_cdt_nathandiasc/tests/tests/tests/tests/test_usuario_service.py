from app.services.usuario_service import (
    USUARIO_ROOT,
    autenticar_usuario,
    buscar_usuario_por_nome,
)


def test_usuario_root_e_criado(
    banco_teste,
):
    usuario = buscar_usuario_por_nome(
        USUARIO_ROOT
    )

    assert usuario is not None
    assert usuario.usuario == "root master"
    assert usuario.perfil == "administrador"


def test_root_autentica_com_senha_correta(
    banco_teste,
):
    usuario = autenticar_usuario(
        "root master",
        "root",
    )

    assert usuario is not None
    assert usuario.usuario == "root master"


def test_root_nao_autentica_com_senha_errada(
    banco_teste,
):
    usuario = autenticar_usuario(
        "root master",
        "senha_errada",
    )

    assert usuario is None


def test_usuario_inexistente_nao_autentica(
    banco_teste,
):
    usuario = autenticar_usuario(
        "usuario inexistente",
        "root",
    )

    assert usuario is None