from datetime import date

import pytest

from app.database.connection import obter_conexao


@pytest.fixture
def cliente_web(
    tmp_path,
    monkeypatch,
):
    import app.database.connection as connection

    caminho_banco_teste = (
        tmp_path
        / "academia_web_teste.db"
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

    import app.web.app_web as app_web

    monkeypatch.setattr(
        app_web,
        "obter_ip_local",
        lambda: "127.0.0.1",
    )

    app = app_web.criar_app()

    app.config.update(
        TESTING=True,
    )

    with app.test_client() as cliente:
        yield cliente


def test_paginas_web_abrem(
    cliente_web,
):
    rotas = [
        "/",
        "/alunos",
        "/planos",
        "/assinaturas",
        "/pagamentos",
        "/acesso",
        "/relatorios",
        "/exportacao",
        "/qr",
    ]

    for rota in rotas:
        resposta = cliente_web.get(
            rota
        )

        assert resposta.status_code == 200


def test_qr_code_retorna_imagem(
    cliente_web,
):
    resposta = cliente_web.get(
        "/qr/imagem"
    )

    assert resposta.status_code == 200

    assert (
        resposta.content_type
        == "image/png"
    )


def test_cadastro_aluno_pela_web(
    cliente_web,
):
    resposta = cliente_web.post(
        "/alunos",
        data={
            "nome": "Aluno Web Teste",
            "cpf": "12345678901",
            "data_nascimento": "2000-05-10",
            "email": "web.teste@email.com",
            "telefone": "11999999999",
        },
        follow_redirects=True,
    )

    texto = resposta.get_data(
        as_text=True
    )

    assert resposta.status_code == 200

    assert (
        "Aluno cadastrado com sucesso"
        in texto
    )

    conexao = obter_conexao()

    try:
        aluno = conexao.execute(
            """
            SELECT
                id,
                nome,
                cpf
            FROM alunos
            WHERE cpf = ?
            """,
            ("123.456.789-01",),
        ).fetchone()

        assert aluno is not None

        assert (
            aluno["nome"]
            == "Aluno Web Teste"
        )

        assert (
            aluno["cpf"]
            == "123.456.789-01"
        )

    finally:
        conexao.close()


def test_plano_duplicado_pela_web(
    cliente_web,
):
    cliente_web.post(
        "/planos",
        data={
            "nome": "Plano Web",
            "valor": "129,90",
            "descricao": (
                "Plano criado pelo teste Web."
            ),
        },
        follow_redirects=True,
    )

    resposta = cliente_web.post(
        "/planos",
        data={
            "nome": "plano web",
            "valor": "149,90",
            "descricao": (
                "Tentativa de duplicidade."
            ),
        },
        follow_redirects=True,
    )

    texto = resposta.get_data(
        as_text=True
    )

    assert resposta.status_code == 200

    assert (
        "Já existe um plano cadastrado "
        "com esse nome"
        in texto
    )

    conexao = obter_conexao()

    try:
        quantidade = conexao.execute(
            """
            SELECT COUNT(*)
            FROM planos
            WHERE LOWER(TRIM(nome))
                = LOWER(TRIM(?))
            """,
            ("Plano Web",),
        ).fetchone()[0]

        assert quantidade == 1

    finally:
        conexao.close()


def test_fluxo_principal_web(
    cliente_web,
):
    # ==========================================
    # ALUNO
    # ==========================================

    resposta_aluno = cliente_web.post(
        "/alunos",
        data={
            "nome": "Aluno Fluxo Web",
            "cpf": "123.456.789-01",
            "data_nascimento": "1999-08-15",
            "email": "fluxo@email.com",
            "telefone": "11988888888",
        },
        follow_redirects=True,
    )

    texto_aluno = (
        resposta_aluno
        .get_data(
            as_text=True
        )
    )

    assert (
        resposta_aluno.status_code
        == 200
    )

    assert (
        "Aluno cadastrado com sucesso"
        in texto_aluno
    )

    # ==========================================
    # PLANO
    # ==========================================

    resposta_plano = cliente_web.post(
        "/planos",
        data={
            "nome": "Plano Fluxo",
            "valor": "99,90",
            "descricao": (
                "Plano utilizado no "
                "teste de integração."
            ),
        },
        follow_redirects=True,
    )

    assert (
        resposta_plano.status_code
        == 200
    )

    conexao = obter_conexao()

    try:
        aluno = conexao.execute(
            """
            SELECT id
            FROM alunos
            WHERE cpf = ?
            """,
            ("123.456.789-01",),
        ).fetchone()

        plano = conexao.execute(
            """
            SELECT id
            FROM planos
            WHERE nome = ?
            """,
            ("Plano Fluxo",),
        ).fetchone()

        assert aluno is not None
        assert plano is not None

        aluno_id = aluno["id"]
        plano_id = plano["id"]

    finally:
        conexao.close()

    # ==========================================
    # ASSINATURA
    # ==========================================

    resposta_assinatura = (
        cliente_web.post(
            "/assinaturas",
            data={
                "aluno_id": str(
                    aluno_id
                ),
                "plano_id": str(
                    plano_id
                ),
                "data_inicio": (
                    date.today()
                    .isoformat()
                ),
                "data_fim": "",
            },
            follow_redirects=True,
        )
    )

    texto_assinatura = (
        resposta_assinatura
        .get_data(
            as_text=True
        )
    )

    assert (
        "Assinatura criada com sucesso"
        in texto_assinatura
    )

    conexao = obter_conexao()

    try:
        assinatura = conexao.execute(
            """
            SELECT id
            FROM assinaturas
            WHERE aluno_id = ?
              AND status = 'ativa'
            """,
            (aluno_id,),
        ).fetchone()

        assert assinatura is not None

        assinatura_id = (
            assinatura["id"]
        )

    finally:
        conexao.close()

    # ==========================================
    # COBRANÇA
    # ==========================================

    resposta_cobranca = (
        cliente_web.post(
            "/pagamentos",
            data={
                "acao": (
                    "gerar_cobranca"
                ),
                "assinatura_id": str(
                    assinatura_id
                ),
                "data_vencimento": (
                    "2099-12-31"
                ),
            },
            follow_redirects=True,
        )
    )

    texto_cobranca = (
        resposta_cobranca
        .get_data(
            as_text=True
        )
    )

    assert (
        "Cobrança gerada com sucesso"
        in texto_cobranca
    )

    conexao = obter_conexao()

    try:
        pagamento = conexao.execute(
            """
            SELECT id
            FROM pagamentos
            WHERE assinatura_id = ?
            """,
            (assinatura_id,),
        ).fetchone()

        assert pagamento is not None

        pagamento_id = (
            pagamento["id"]
        )

    finally:
        conexao.close()

    # ==========================================
    # PAGAMENTO
    # ==========================================

    resposta_pagamento = (
        cliente_web.post(
            "/pagamentos",
            data={
                "acao": (
                    "registrar_pagamento"
                ),
                "pagamento_id": str(
                    pagamento_id
                ),
                "forma_pagamento": "Pix",
                "data_pagamento": (
                    date.today()
                    .isoformat()
                ),
            },
            follow_redirects=True,
        )
    )

    texto_pagamento = (
        resposta_pagamento
        .get_data(
            as_text=True
        )
    )

    assert (
        "Pagamento registrado com sucesso"
        in texto_pagamento
    )

    # ==========================================
    # ACESSO
    # ==========================================

    resposta_acesso = cliente_web.post(
        "/acesso",
        data={
            "aluno_id": str(
                aluno_id
            ),
        },
        follow_redirects=True,
    )

    texto_acesso = (
        resposta_acesso
        .get_data(
            as_text=True
        )
    )

    assert (
        "ACESSO AUTORIZADO"
        in texto_acesso
    )

    conexao = obter_conexao()

    try:
        acesso = conexao.execute(
            """
            SELECT
                status,
                motivo
            FROM acessos
            WHERE aluno_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (aluno_id,),
        ).fetchone()

        assert acesso is not None

        assert (
            acesso["status"]
            == "autorizado"
        )

        assert acesso["motivo"] is None

    finally:
        conexao.close()