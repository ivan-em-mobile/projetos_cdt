import socket
from datetime import date
from io import BytesIO
from pathlib import Path

import qrcode

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from app.database.schema import criar_tabelas

from app.models.aluno import Aluno
from app.models.assinatura import Assinatura
from app.models.plano import Plano

from app.services.acesso_service import (
    autorizar_acesso,
    listar_acessos,
)

from app.services.aluno_service import (
    cadastrar_aluno,
    listar_alunos,
)

from app.services.assinatura_service import (
    buscar_assinatura_ativa_por_aluno,
    cadastrar_assinatura,
    listar_assinaturas,
)

from app.services.export_service import (
    exportar_banco_json,
)

from app.services.pagamento_service import (
    gerar_cobranca_para_assinatura,
    listar_pagamentos,
    registrar_pagamento,
)

from app.services.plano_service import (
    cadastrar_plano,
    listar_planos,
)

from app.services.relatorio_service import (
    relatorio_acessos,
    relatorio_financeiro,
    relatorio_geral,
    relatorio_planos,
)

from app.services.usuario_service import (
    USUARIO_ROOT,
    autenticar_usuario,
    criar_usuario_root,
)


RAIZ_PROJETO = Path(
    __file__
).resolve().parents[2]

CAMINHO_VERSION = (
    RAIZ_PROJETO
    / "VERSION"
)


def obter_versao():
    with open(
        CAMINHO_VERSION,
        "r",
        encoding="utf-8",
    ) as arquivo:
        return arquivo.read().strip()


def obter_ip_local():
    socket_rede = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
    )

    try:
        socket_rede.connect(
            ("8.8.8.8", 80)
        )

        return socket_rede.getsockname()[0]

    except OSError:
        return "127.0.0.1"

    finally:
        socket_rede.close()


def obter_url_aplicacao():
    host_atual = (
        request.host
        .split(":")[0]
        .lower()
    )

    if host_atual in (
        "127.0.0.1",
        "localhost",
    ):
        ip_local = obter_ip_local()

        return (
            f"http://{ip_local}:5000"
        )

    return request.url_root.rstrip("/")


def criar_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    app.config["SECRET_KEY"] = (
        "smartfit-gym-manager-dev"
    )

    criar_tabelas()
    criar_usuario_root()

    # ==========================================
    # DASHBOARD
    # ==========================================

    @app.route("/")
    def dashboard():
        geral = relatorio_geral()
        financeiro = relatorio_financeiro()
        acessos = relatorio_acessos()

        return render_template(
            "dashboard.html",
            versao=obter_versao(),
            geral=geral,
            financeiro=financeiro,
            acessos=acessos,
        )

    # ==========================================
    # ALUNOS
    # ==========================================

    @app.route(
        "/alunos",
        methods=[
            "GET",
            "POST",
        ],
    )
    def alunos():
        if request.method == "POST":
            nome = (
                request.form
                .get("nome", "")
                .strip()
            )

            cpf = (
                request.form
                .get("cpf", "")
                .strip()
            )

            data_nascimento_texto = (
                request.form
                .get(
                    "data_nascimento",
                    "",
                )
                .strip()
            )

            email = (
                request.form
                .get("email", "")
                .strip()
            )

            telefone = (
                request.form
                .get("telefone", "")
                .strip()
            )

            if not all(
                (
                    nome,
                    cpf,
                    data_nascimento_texto,
                    email,
                    telefone,
                )
            ):
                flash(
                    (
                        "Preencha todos os campos "
                        "antes de cadastrar o aluno."
                    ),
                    "erro",
                )

                return redirect(
                    url_for("alunos")
                )

            try:
                data_nascimento = (
                    date.fromisoformat(
                        data_nascimento_texto
                    )
                )

                aluno = Aluno(
                    nome=nome,
                    cpf=cpf,
                    data_nascimento=data_nascimento,
                    email=email,
                    telefone=telefone,
                    data_cadastro=date.today(),
                )

                aluno = cadastrar_aluno(
                    aluno
                )

                flash(
                    (
                        "Aluno cadastrado com "
                        "sucesso! "
                        f"ID: {aluno.id}"
                    ),
                    "sucesso",
                )

            except ValueError as erro:
                flash(
                    str(erro),
                    "erro",
                )

            except Exception as erro:
                flash(
                    (
                        "Não foi possível "
                        "cadastrar o aluno. "
                        f"{erro}"
                    ),
                    "erro",
                )

            return redirect(
                url_for("alunos")
            )

        alunos_cadastrados = (
            listar_alunos()
        )

        return render_template(
            "alunos.html",
            versao=obter_versao(),
            alunos=alunos_cadastrados,
        )

    # ==========================================
    # PLANOS
    # ==========================================

    @app.route(
        "/planos",
        methods=[
            "GET",
            "POST",
        ],
    )
    def planos():
        if request.method == "POST":
            nome = (
                request.form
                .get("nome", "")
                .strip()
            )

            valor_texto = (
                request.form
                .get("valor", "")
                .strip()
            )

            descricao = (
                request.form
                .get("descricao", "")
                .strip()
            )

            if not nome or not valor_texto:
                flash(
                    (
                        "Informe o nome e o "
                        "valor do plano."
                    ),
                    "erro",
                )

                return redirect(
                    url_for("planos")
                )

            try:
                valor = float(
                    valor_texto.replace(
                        ",",
                        ".",
                    )
                )

                if valor <= 0:
                    raise ValueError(
                        (
                            "O valor do plano deve "
                            "ser maior que zero."
                        )
                    )

                plano = Plano(
                    nome=nome,
                    valor=valor,
                    descricao=descricao,
                )

                plano = cadastrar_plano(
                    plano
                )

                flash(
                    (
                        "Plano cadastrado com "
                        "sucesso! "
                        f"ID: {plano.id}"
                    ),
                    "sucesso",
                )

            except ValueError as erro:
                flash(
                    str(erro),
                    "erro",
                )

            except Exception as erro:
                flash(
                    (
                        "Não foi possível "
                        "cadastrar o plano. "
                        f"{erro}"
                    ),
                    "erro",
                )

            return redirect(
                url_for("planos")
            )

        planos_cadastrados = (
            listar_planos()
        )

        return render_template(
            "planos.html",
            versao=obter_versao(),
            planos=planos_cadastrados,
        )

    # ==========================================
    # ASSINATURAS
    # ==========================================

    @app.route(
        "/assinaturas",
        methods=[
            "GET",
            "POST",
        ],
    )
    def assinaturas():
        alunos_cadastrados = (
            listar_alunos()
        )

        planos_cadastrados = (
            listar_planos()
        )

        if request.method == "POST":
            aluno_id_texto = (
                request.form
                .get("aluno_id", "")
                .strip()
            )

            plano_id_texto = (
                request.form
                .get("plano_id", "")
                .strip()
            )

            data_inicio_texto = (
                request.form
                .get("data_inicio", "")
                .strip()
            )

            data_fim_texto = (
                request.form
                .get("data_fim", "")
                .strip()
            )

            if not all(
                (
                    aluno_id_texto,
                    plano_id_texto,
                    data_inicio_texto,
                )
            ):
                flash(
                    (
                        "Selecione o aluno, o plano "
                        "e informe a data de início."
                    ),
                    "erro",
                )

                return redirect(
                    url_for("assinaturas")
                )

            try:
                aluno_id = int(
                    aluno_id_texto
                )

                plano_id = int(
                    plano_id_texto
                )

                aluno_selecionado = next(
                    (
                        aluno
                        for aluno
                        in alunos_cadastrados
                        if aluno.id == aluno_id
                    ),
                    None,
                )

                plano_selecionado = next(
                    (
                        plano
                        for plano
                        in planos_cadastrados
                        if plano.id == plano_id
                    ),
                    None,
                )

                if aluno_selecionado is None:
                    raise ValueError(
                        "Aluno não encontrado."
                    )

                if plano_selecionado is None:
                    raise ValueError(
                        "Plano não encontrado."
                    )

                if (
                    aluno_selecionado.status
                    != "ativo"
                ):
                    raise ValueError(
                        (
                            "Não é possível criar "
                            "uma assinatura para "
                            "um aluno inativo."
                        )
                    )

                if not plano_selecionado.ativo:
                    raise ValueError(
                        (
                            "Não é possível criar "
                            "uma assinatura com "
                            "um plano inativo."
                        )
                    )

                assinatura_ativa = (
                    buscar_assinatura_ativa_por_aluno(
                        aluno_id
                    )
                )

                if assinatura_ativa is not None:
                    raise ValueError(
                        (
                            "Este aluno já possui "
                            "uma assinatura ativa."
                        )
                    )

                data_inicio = (
                    date.fromisoformat(
                        data_inicio_texto
                    )
                )

                data_fim = None

                if data_fim_texto:
                    data_fim = (
                        date.fromisoformat(
                            data_fim_texto
                        )
                    )

                    if data_fim < data_inicio:
                        raise ValueError(
                            (
                                "A data final não pode "
                                "ser anterior à data "
                                "de início."
                            )
                        )

                assinatura = Assinatura(
                    aluno_id=aluno_id,
                    plano_id=plano_id,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                )

                assinatura = (
                    cadastrar_assinatura(
                        assinatura
                    )
                )

                flash(
                    (
                        "Assinatura criada com "
                        "sucesso! "
                        f"ID: {assinatura.id}"
                    ),
                    "sucesso",
                )

            except ValueError as erro:
                flash(
                    str(erro),
                    "erro",
                )

            except Exception as erro:
                flash(
                    (
                        "Não foi possível criar "
                        "a assinatura. "
                        f"{erro}"
                    ),
                    "erro",
                )

            return redirect(
                url_for("assinaturas")
            )

        assinaturas_cadastradas = (
            listar_assinaturas()
        )

        nomes_alunos = {
            aluno.id: aluno.nome
            for aluno in alunos_cadastrados
        }

        nomes_planos = {
            plano.id: plano.nome
            for plano in planos_cadastrados
        }

        alunos_ativos = [
            aluno
            for aluno in alunos_cadastrados
            if aluno.status == "ativo"
        ]

        planos_ativos = [
            plano
            for plano in planos_cadastrados
            if plano.ativo
        ]

        return render_template(
            "assinaturas.html",
            versao=obter_versao(),
            assinaturas=assinaturas_cadastradas,
            alunos=alunos_ativos,
            planos=planos_ativos,
            nomes_alunos=nomes_alunos,
            nomes_planos=nomes_planos,
            hoje=date.today().isoformat(),
        )

    # ==========================================
    # PAGAMENTOS
    # ==========================================

    @app.route(
        "/pagamentos",
        methods=[
            "GET",
            "POST",
        ],
    )
    def pagamentos():
        assinaturas_cadastradas = (
            listar_assinaturas()
        )

        alunos_cadastrados = (
            listar_alunos()
        )

        planos_cadastrados = (
            listar_planos()
        )

        if request.method == "POST":
            acao = (
                request.form
                .get("acao", "")
                .strip()
            )

            try:
                if acao == "gerar_cobranca":
                    assinatura_id_texto = (
                        request.form
                        .get(
                            "assinatura_id",
                            "",
                        )
                        .strip()
                    )

                    vencimento_texto = (
                        request.form
                        .get(
                            "data_vencimento",
                            "",
                        )
                        .strip()
                    )

                    if (
                        not assinatura_id_texto
                        or not vencimento_texto
                    ):
                        raise ValueError(
                            (
                                "Selecione uma assinatura "
                                "e informe a data de "
                                "vencimento."
                            )
                        )

                    assinatura_id = int(
                        assinatura_id_texto
                    )

                    data_vencimento = (
                        date.fromisoformat(
                            vencimento_texto
                        )
                    )

                    pagamento = (
                        gerar_cobranca_para_assinatura(
                            assinatura_id,
                            data_vencimento,
                        )
                    )

                    flash(
                        (
                            "Cobrança gerada com "
                            "sucesso! "
                            f"ID: {pagamento.id}"
                        ),
                        "sucesso",
                    )

                elif acao == "registrar_pagamento":
                    pagamento_id_texto = (
                        request.form
                        .get(
                            "pagamento_id",
                            "",
                        )
                        .strip()
                    )

                    forma_pagamento = (
                        request.form
                        .get(
                            "forma_pagamento",
                            "",
                        )
                        .strip()
                    )

                    data_pagamento_texto = (
                        request.form
                        .get(
                            "data_pagamento",
                            "",
                        )
                        .strip()
                    )

                    if (
                        not pagamento_id_texto
                        or not forma_pagamento
                    ):
                        raise ValueError(
                            (
                                "Selecione uma cobrança "
                                "e informe a forma de "
                                "pagamento."
                            )
                        )

                    pagamento_id = int(
                        pagamento_id_texto
                    )

                    data_pagamento = None

                    if data_pagamento_texto:
                        data_pagamento = (
                            date.fromisoformat(
                                data_pagamento_texto
                            )
                        )

                    pagamento = (
                        registrar_pagamento(
                            pagamento_id,
                            forma_pagamento,
                            data_pagamento,
                        )
                    )

                    if pagamento is None:
                        raise ValueError(
                            "Pagamento não encontrado."
                        )

                    flash(
                        (
                            "Pagamento registrado "
                            "com sucesso! "
                            f"ID: {pagamento.id}"
                        ),
                        "sucesso",
                    )

                else:
                    raise ValueError(
                        "Operação de pagamento inválida."
                    )

            except ValueError as erro:
                flash(
                    str(erro),
                    "erro",
                )

            except Exception as erro:
                flash(
                    (
                        "Não foi possível concluir "
                        "a operação financeira. "
                        f"{erro}"
                    ),
                    "erro",
                )

            return redirect(
                url_for("pagamentos")
            )

        pagamentos_cadastrados = (
            listar_pagamentos()
        )

        alunos_por_id = {
            aluno.id: aluno
            for aluno in alunos_cadastrados
        }

        planos_por_id = {
            plano.id: plano
            for plano in planos_cadastrados
        }

        assinaturas_por_id = {
            assinatura.id: assinatura
            for assinatura
            in assinaturas_cadastradas
        }

        assinaturas_ativas = [
            assinatura
            for assinatura
            in assinaturas_cadastradas
            if assinatura.status == "ativa"
        ]

        pagamentos_em_aberto = [
            pagamento
            for pagamento
            in pagamentos_cadastrados
            if pagamento.status
            in (
                "pendente",
                "atrasado",
            )
        ]

        return render_template(
            "pagamentos.html",
            versao=obter_versao(),
            assinaturas=assinaturas_ativas,
            pagamentos=pagamentos_cadastrados,
            pagamentos_em_aberto=pagamentos_em_aberto,
            assinaturas_por_id=assinaturas_por_id,
            alunos_por_id=alunos_por_id,
            planos_por_id=planos_por_id,
            hoje=date.today().isoformat(),
        )

    # ==========================================
    # CONTROLE DE ACESSO
    # ==========================================

    @app.route(
        "/acesso",
        methods=[
            "GET",
            "POST",
        ],
    )
    def acesso():
        alunos_cadastrados = (
            listar_alunos()
        )

        if request.method == "POST":
            aluno_id_texto = (
                request.form
                .get("aluno_id", "")
                .strip()
            )

            if not aluno_id_texto:
                flash(
                    "Selecione um aluno.",
                    "erro",
                )

                return redirect(
                    url_for("acesso")
                )

            try:
                aluno_id = int(
                    aluno_id_texto
                )

                aluno_selecionado = next(
                    (
                        aluno
                        for aluno
                        in alunos_cadastrados
                        if aluno.id == aluno_id
                    ),
                    None,
                )

                if aluno_selecionado is None:
                    raise ValueError(
                        "Aluno não encontrado."
                    )

                resultado = autorizar_acesso(
                    aluno_id
                )

                if resultado.status == "autorizado":
                    flash(
                        (
                            "ACESSO AUTORIZADO - "
                            f"{aluno_selecionado.nome}"
                        ),
                        "sucesso",
                    )

                else:
                    motivo = (
                        resultado.motivo
                        or "Motivo não informado."
                    )

                    flash(
                        (
                            "ACESSO NEGADO - "
                            f"{aluno_selecionado.nome}. "
                            f"Motivo: {motivo}"
                        ),
                        "erro",
                    )

            except ValueError as erro:
                flash(
                    str(erro),
                    "erro",
                )

            except Exception as erro:
                flash(
                    (
                        "Não foi possível registrar "
                        "a tentativa de acesso. "
                        f"{erro}"
                    ),
                    "erro",
                )

            return redirect(
                url_for("acesso")
            )

        acessos_registrados = (
            listar_acessos()
        )

        alunos_por_id = {
            aluno.id: aluno
            for aluno in alunos_cadastrados
        }

        return render_template(
            "acesso.html",
            versao=obter_versao(),
            alunos=alunos_cadastrados,
            acessos=acessos_registrados,
            alunos_por_id=alunos_por_id,
        )

    # ==========================================
    # RELATÓRIOS
    # ==========================================

    @app.route("/relatorios")
    def relatorios():
        geral = relatorio_geral()
        financeiro = relatorio_financeiro()
        acessos = relatorio_acessos()
        planos = relatorio_planos()

        return render_template(
            "relatorios.html",
            versao=obter_versao(),
            geral=geral,
            financeiro=financeiro,
            acessos=acessos,
            planos=planos,
        )

    # ==========================================
    # EXPORTAÇÃO JSON
    # ==========================================

    @app.route(
        "/exportacao",
        methods=[
            "GET",
            "POST",
        ],
    )
    def exportacao():
        if request.method == "POST":
            nome_usuario = (
                request.form
                .get("usuario", "")
                .strip()
            )

            senha = (
                request.form
                .get("senha", "")
            )

            if not nome_usuario or not senha:
                flash(
                    (
                        "Informe o usuário e a senha "
                        "para realizar a exportação."
                    ),
                    "erro",
                )

                return redirect(
                    url_for("exportacao")
                )

            try:
                usuario = autenticar_usuario(
                    nome_usuario,
                    senha,
                )

                if usuario is None:
                    raise ValueError(
                        "Usuário ou senha inválidos."
                    )

                if usuario.usuario != USUARIO_ROOT:
                    raise ValueError(
                        (
                            "Somente o usuário root master "
                            "pode exportar o banco de dados."
                        )
                    )

                caminho_arquivo = (
                    exportar_banco_json()
                )

                return send_file(
                    caminho_arquivo,
                    as_attachment=True,
                    download_name=caminho_arquivo.name,
                    mimetype="application/json",
                )

            except ValueError as erro:
                flash(
                    str(erro),
                    "erro",
                )

            except Exception as erro:
                flash(
                    (
                        "Não foi possível exportar "
                        "o banco de dados. "
                        f"{erro}"
                    ),
                    "erro",
                )

            return redirect(
                url_for("exportacao")
            )

        return render_template(
            "exportacao.html",
            versao=obter_versao(),
            usuario_root=USUARIO_ROOT,
        )

    # ==========================================
    # QR CODE
    # ==========================================

    @app.route("/qr")
    def qr_code():
        url_aplicacao = (
            obter_url_aplicacao()
        )

        return render_template(
            "qr_code.html",
            versao=obter_versao(),
            url_aplicacao=url_aplicacao,
        )

    @app.route("/qr/imagem")
    def qr_code_imagem():
        url_aplicacao = (
            obter_url_aplicacao()
        )

        imagem_qr = qrcode.make(
            url_aplicacao
        )

        arquivo_memoria = BytesIO()

        imagem_qr.save(
            arquivo_memoria,
            format="PNG",
        )

        arquivo_memoria.seek(0)

        return send_file(
            arquivo_memoria,
            mimetype="image/png",
        )

    return app


app = criar_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )