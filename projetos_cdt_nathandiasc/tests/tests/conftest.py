import pytest

import app.database.connection as connection
from app.database.schema import criar_tabelas
from app.services.usuario_service import criar_usuario_root


@pytest.fixture
def banco_teste(tmp_path, monkeypatch):
    caminho_banco_teste = (
        tmp_path
        / "academia_teste.db"
    )

    monkeypatch.setattr(
        connection,
        "PASTA_DADOS",
        tmp_path,
    )

    monkeypatch.setattr(
        connection,
        "CAMINHO_BANCO",
        caminho_banco_teste,
    )

    criar_tabelas()
    criar_usuario_root()

    return caminho_banco_teste