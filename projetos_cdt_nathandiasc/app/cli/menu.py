import msvcrt
from datetime import date, datetime

from app.models.aluno import Aluno
from app.models.assinatura import Assinatura
from app.models.exercicio import Exercicio
from app.models.plano import Plano
from app.models.treino import Treino

from app.services.acesso_service import (
    autorizar_acesso,
    listar_acessos,
)

from app.services.aluno_service import (
    buscar_aluno_por_id,
    cadastrar_aluno,
    listar_alunos,
)

from app.services.assinatura_service import (
    buscar_assinatura_ativa_por_aluno,
    buscar_assinatura_por_id,
    cadastrar_assinatura,
    listar_assinaturas,
)

from app.services.exercicio_service import (
    cadastrar_exercicio,
    listar_exercicios,
)

from app.services.export_service import (
    exportar_banco_json,
)

from app.services.faker_service import (
    popular_dados_demonstracao,
)

from app.services.pagamento_service import (
    gerar_cobranca_para_assinatura,
    listar_pagamentos,
    registrar_pagamento,
)

from app.services.plano_service import (
    buscar_plano_por_id,
    cadastrar_plano,
    listar_planos,
)

from app.services.relatorio_service import (
    relatorio_acessos,
    relatorio_financeiro,
    relatorio_geral,
    relatorio_planos,
)

from app.services.treino_service import (
    adicionar_exercicio_ao_treino,
    buscar_treino_por_id,
    cadastrar_treino,
    listar_exercicios_do_treino,
    listar_treinos_por_aluno,
)

from app.services.usuario_service import (
    USUARIO_ROOT,
    autenticar_usuario,
)


def ler_senha_mascarada(mensagem="Senha: ") -> str:
    print(mensagem, end="", flush=True)

    caracteres = []

    while True:
        tecla = msvcrt.getwch()

        if tecla in ("\r", "\n"):
            print()
            break

        if tecla == "\003":
            raise KeyboardInterrupt

        if tecla == "\b":
            if caracteres:
                caracteres.pop()
                print(
                    "\b \b",
                    end="",
                    flush=True,
                )

            continue

        if tecla in ("\x00", "\xe0"):
            msvcrt.getwch()
            continue

        caracteres.append(tecla)

        print(
            "*",
            end="",
            flush=True,
        )

    return "".join(caracteres)


def converter_data(data_texto: str) -> date:
    formatos = ("%d/%m/%Y", "%Y-%m-%d")

    for formato in formatos:
        try:
            return datetime.strptime(
                data_texto,
                formato,
            ).date()

        except ValueError:
            continue

    raise ValueError(
        "Data inválida. Use o formato DD/MM/AAAA."
    )


def exibir_menu():
    print()
    print("=" * 50)
    print("SMARTFIT GYM MANAGER")
    print("=" * 50)

    print("1 - Cadastrar aluno")
    print("2 - Listar alunos")

    print("3 - Cadastrar plano")
    print("4 - Listar planos")

    print("5 - Criar assinatura")
    print("6 - Listar assinaturas")

    print("7 - Gerar cobrança")
    print("8 - Listar pagamentos")
    print("9 - Registrar pagamento")

    print("10 - Registrar acesso")
    print("11 - Histórico de acessos")

    print("12 - Cadastrar exercício")
    print("13 - Listar exercícios")

    print("14 - Criar treino")
    print("15 - Listar treinos de um aluno")
    print("16 - Adicionar exercício ao treino")
    print("17 - Visualizar ficha de treino")

    print("18 - Exportar banco para JSON")
    print("19 - Gerar dados fictícios com Faker")
    print("20 - Relatórios")

    print("0 - Sair")

    print("=" * 50)


def cadastrar_novo_aluno():
    print()
    print("--- Cadastro de Aluno ---")

    nome = input("Nome: ").strip()
    cpf = input("CPF: ").strip()

    data_nascimento = input(
        "Data de nascimento (DD/MM/AAAA): "
    ).strip()

    email = input("E-mail: ").strip()
    telefone = input("Telefone: ").strip()

    try:
        aluno = Aluno(
            nome=nome,
            cpf=cpf,
            data_nascimento=converter_data(
                data_nascimento
            ),
            email=email,
            telefone=telefone,
            data_cadastro=date.today(),
        )

        aluno = cadastrar_aluno(aluno)

        print()
        print("Aluno cadastrado com sucesso!")
        print(f"ID: {aluno.id}")
        print(f"Nome: {aluno.nome}")

    except ValueError as erro:
        print()
        print(f"Erro: {erro}")


def mostrar_alunos():
    print()
    print("--- Alunos Cadastrados ---")

    alunos = listar_alunos()

    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    for aluno in alunos:
        print(
            f"ID: {aluno.id} | "
            f"Nome: {aluno.nome} | "
            f"CPF: {aluno.cpf} | "
            f"Status: {aluno.status}"
        )


def cadastrar_novo_plano():
    print()
    print("--- Cadastro de Plano ---")

    nome = input("Nome do plano: ").strip()

    valor_texto = input(
        "Valor mensal: R$ "
    ).strip()

    descricao = input(
        "Descrição: "
    ).strip()

    try:
        valor = float(
            valor_texto.replace(",", ".")
        )

        plano = Plano(
            nome=nome,
            valor=valor,
            descricao=descricao,
        )

        plano = cadastrar_plano(plano)

        print()
        print("Plano cadastrado com sucesso!")
        print(f"ID: {plano.id}")
        print(f"Plano: {plano.nome}")
        print(f"Valor: R$ {plano.valor:.2f}")

    except ValueError as erro:
        print()
        print(f"Erro: {erro}")


def mostrar_planos():
    print()
    print("--- Planos Cadastrados ---")

    planos = listar_planos()

    if not planos:
        print("Nenhum plano cadastrado.")
        return

    for plano in planos:
        status = (
            "Ativo"
            if plano.ativo
            else "Inativo"
        )

        print(
            f"ID: {plano.id} | "
            f"Nome: {plano.nome} | "
            f"Valor: R$ {plano.valor:.2f} | "
            f"Status: {status}"
        )


def criar_nova_assinatura():
    print()
    print("--- Nova Assinatura ---")

    try:
        aluno_id = int(
            input("ID do aluno: ")
        )

        plano_id = int(
            input("ID do plano: ")
        )

    except ValueError:
        print(
            "Erro: os IDs devem ser números inteiros."
        )
        return

    aluno = buscar_aluno_por_id(
        aluno_id
    )

    if aluno is None:
        print("Aluno não encontrado.")
        return

    plano = buscar_plano_por_id(
        plano_id
    )

    if plano is None:
        print("Plano não encontrado.")
        return

    assinatura_existente = (
        buscar_assinatura_ativa_por_aluno(
            aluno_id
        )
    )

    if assinatura_existente is not None:
        print(
            f"O aluno {aluno.nome} já possui "
            "uma assinatura ativa."
        )
        return

    assinatura = Assinatura(
        aluno_id=aluno_id,
        plano_id=plano_id,
        data_inicio=date.today(),
    )

    assinatura = cadastrar_assinatura(
        assinatura
    )

    print()
    print("Assinatura criada com sucesso!")
    print(
        f"ID da assinatura: "
        f"{assinatura.id}"
    )
    print(f"Aluno: {aluno.nome}")
    print(f"Plano: {plano.nome}")


def mostrar_assinaturas():
    print()
    print("--- Assinaturas Cadastradas ---")

    assinaturas = listar_assinaturas()

    if not assinaturas:
        print(
            "Nenhuma assinatura cadastrada."
        )
        return

    for assinatura in assinaturas:
        aluno = buscar_aluno_por_id(
            assinatura.aluno_id
        )

        plano = buscar_plano_por_id(
            assinatura.plano_id
        )

        nome_aluno = (
            aluno.nome
            if aluno is not None
            else "Aluno não encontrado"
        )

        nome_plano = (
            plano.nome
            if plano is not None
            else "Plano não encontrado"
        )

        print(
            f"ID: {assinatura.id} | "
            f"Aluno: {nome_aluno} | "
            f"Plano: {nome_plano} | "
            f"Status: {assinatura.status}"
        )


def gerar_nova_cobranca():
    print()
    print("--- Gerar Cobrança ---")

    try:
        assinatura_id = int(
            input("ID da assinatura: ")
        )

        vencimento_texto = input(
            "Data de vencimento "
            "(DD/MM/AAAA): "
        ).strip()

        data_vencimento = converter_data(
            vencimento_texto
        )

        pagamento = (
            gerar_cobranca_para_assinatura(
                assinatura_id,
                data_vencimento,
            )
        )

        print()
        print("Cobrança gerada com sucesso!")
        print(
            f"ID do pagamento: "
            f"{pagamento.id}"
        )
        print(
            f"Valor: "
            f"R$ {pagamento.valor:.2f}"
        )
        print(
            "Vencimento: "
            f"{pagamento.data_vencimento.strftime('%d/%m/%Y')}"
        )
        print(
            f"Status: {pagamento.status}"
        )

    except ValueError as erro:
        print()
        print(f"Erro: {erro}")


def mostrar_pagamentos():
    print()
    print("--- Pagamentos ---")

    pagamentos = listar_pagamentos()

    if not pagamentos:
        print(
            "Nenhum pagamento cadastrado."
        )
        return

    for pagamento in pagamentos:
        assinatura = (
            buscar_assinatura_por_id(
                pagamento.assinatura_id
            )
        )

        nome_aluno = "Não encontrado"
        nome_plano = "Não encontrado"

        if assinatura is not None:
            aluno = buscar_aluno_por_id(
                assinatura.aluno_id
            )

            plano = buscar_plano_por_id(
                assinatura.plano_id
            )

            if aluno is not None:
                nome_aluno = aluno.nome

            if plano is not None:
                nome_plano = plano.nome

        data_pagamento = (
            pagamento.data_pagamento.strftime(
                "%d/%m/%Y"
            )
            if pagamento.data_pagamento
            is not None
            else "-"
        )

        print(
            f"ID: {pagamento.id} | "
            f"Aluno: {nome_aluno} | "
            f"Plano: {nome_plano} | "
            f"Valor: R$ {pagamento.valor:.2f} | "
            f"Vencimento: "
            f"{pagamento.data_vencimento.strftime('%d/%m/%Y')} | "
            f"Pagamento: {data_pagamento} | "
            f"Status: {pagamento.status}"
        )


def registrar_novo_pagamento():
    print()
    print("--- Registrar Pagamento ---")

    try:
        pagamento_id = int(
            input("ID do pagamento: ")
        )

        forma_pagamento = input(
            "Forma de pagamento: "
        ).strip()

        pagamento = registrar_pagamento(
            pagamento_id,
            forma_pagamento,
        )

        if pagamento is None:
            print(
                "Pagamento não encontrado."
            )
            return

        print()
        print(
            "Pagamento registrado com sucesso!"
        )
        print(f"ID: {pagamento.id}")
        print(
            f"Valor: R$ "
            f"{pagamento.valor:.2f}"
        )
        print(
            "Data do pagamento: "
            f"{pagamento.data_pagamento.strftime('%d/%m/%Y')}"
        )
        print(
            f"Forma: "
            f"{pagamento.forma_pagamento}"
        )
        print(
            f"Status: "
            f"{pagamento.status}"
        )

    except ValueError as erro:
        print()
        print(f"Erro: {erro}")


def registrar_novo_acesso():
    print()
    print("--- Controle de Acesso ---")

    try:
        aluno_id = int(
            input("ID do aluno: ")
        )

    except ValueError:
        print(
            "Erro: o ID deve ser um número inteiro."
        )
        return

    aluno = buscar_aluno_por_id(
        aluno_id
    )

    acesso = autorizar_acesso(
        aluno_id
    )

    print()

    if acesso.status == "autorizado":
        print("ACESSO AUTORIZADO")

    else:
        print("ACESSO NEGADO")

    if aluno is not None:
        print(f"Aluno: {aluno.nome}")

    else:
        print(
            f"Aluno ID: {aluno_id}"
        )

    print(
        "Data e hora: "
        f"{acesso.data_hora.strftime('%d/%m/%Y %H:%M:%S')}"
    )

    if acesso.motivo is not None:
        print(
            f"Motivo: {acesso.motivo}"
        )


def mostrar_acessos():
    print()
    print("--- Histórico de Acessos ---")

    acessos = listar_acessos()

    if not acessos:
        print(
            "Nenhum acesso registrado."
        )
        return

    for acesso in acessos:
        aluno = buscar_aluno_por_id(
            acesso.aluno_id
        )

        nome_aluno = (
            aluno.nome
            if aluno is not None
            else f"Aluno ID {acesso.aluno_id}"
        )

        motivo = (
            acesso.motivo
            if acesso.motivo is not None
            else "-"
        )

        print(
            f"ID: {acesso.id} | "
            f"Aluno: {nome_aluno} | "
            f"Data: "
            f"{acesso.data_hora.strftime('%d/%m/%Y %H:%M:%S')} | "
            f"Status: {acesso.status} | "
            f"Motivo: {motivo}"
        )


def cadastrar_novo_exercicio():
    print()
    print("--- Cadastro de Exercício ---")

    nome = input(
        "Nome do exercício: "
    ).strip()

    grupo_muscular = input(
        "Grupo muscular: "
    ).strip()

    descricao = input(
        "Descrição: "
    ).strip()

    if not descricao:
        descricao = None

    exercicio = Exercicio(
        nome=nome,
        grupo_muscular=grupo_muscular,
        descricao=descricao,
    )

    exercicio = cadastrar_exercicio(
        exercicio
    )

    print()
    print("Exercício cadastrado com sucesso!")
    print(f"ID: {exercicio.id}")
    print(f"Nome: {exercicio.nome}")
    print(
        f"Grupo muscular: "
        f"{exercicio.grupo_muscular}"
    )


def mostrar_exercicios():
    print()
    print("--- Catálogo de Exercícios ---")

    exercicios = listar_exercicios()

    if not exercicios:
        print(
            "Nenhum exercício cadastrado."
        )
        return

    for exercicio in exercicios:
        descricao = (
            exercicio.descricao
            if exercicio.descricao
            else "-"
        )

        print(
            f"ID: {exercicio.id} | "
            f"Nome: {exercicio.nome} | "
            f"Grupo: {exercicio.grupo_muscular} | "
            f"Descrição: {descricao}"
        )


def criar_novo_treino():
    print()
    print("--- Criar Treino ---")

    try:
        aluno_id = int(
            input("ID do aluno: ")
        )

    except ValueError:
        print(
            "Erro: o ID deve ser um número inteiro."
        )
        return

    aluno = buscar_aluno_por_id(
        aluno_id
    )

    if aluno is None:
        print("Aluno não encontrado.")
        return

    nome = input(
        "Nome do treino: "
    ).strip()

    objetivo = input(
        "Objetivo: "
    ).strip()

    try:
        treino = Treino(
            aluno_id=aluno_id,
            nome=nome,
            objetivo=objetivo,
            data_criacao=date.today(),
        )

        treino = cadastrar_treino(
            treino
        )

        print()
        print("Treino criado com sucesso!")
        print(f"ID: {treino.id}")
        print(f"Aluno: {aluno.nome}")
        print(f"Treino: {treino.nome}")
        print(f"Objetivo: {treino.objetivo}")

    except ValueError as erro:
        print()
        print(f"Erro: {erro}")


def mostrar_treinos_do_aluno():
    print()
    print("--- Treinos do Aluno ---")

    try:
        aluno_id = int(
            input("ID do aluno: ")
        )

    except ValueError:
        print(
            "Erro: o ID deve ser um número inteiro."
        )
        return

    aluno = buscar_aluno_por_id(
        aluno_id
    )

    if aluno is None:
        print("Aluno não encontrado.")
        return

    treinos = listar_treinos_por_aluno(
        aluno_id
    )

    if not treinos:
        print(
            f"{aluno.nome} não possui "
            "treinos cadastrados."
        )
        return

    print()
    print(f"Aluno: {aluno.nome}")

    for treino in treinos:
        status = (
            "Ativo"
            if treino.ativo
            else "Inativo"
        )

        print(
            f"ID: {treino.id} | "
            f"Nome: {treino.nome} | "
            f"Objetivo: {treino.objetivo} | "
            f"Status: {status}"
        )


def adicionar_exercicio_na_ficha():
    print()
    print("--- Adicionar Exercício ao Treino ---")

    try:
        treino_id = int(
            input("ID do treino: ")
        )

        exercicio_id = int(
            input("ID do exercício: ")
        )

        series = int(
            input("Número de séries: ")
        )

        repeticoes = input(
            "Repetições (ex.: 8-12): "
        ).strip()

        carga_texto = input(
            "Carga em kg "
            "(deixe vazio se não houver): "
        ).strip()

        descanso_texto = input(
            "Descanso em segundos "
            "(deixe vazio se não houver): "
        ).strip()

        ordem_texto = input(
            "Ordem do exercício "
            "(deixe vazio para não definir): "
        ).strip()

        carga = (
            float(
                carga_texto.replace(",", ".")
            )
            if carga_texto
            else None
        )

        descanso_segundos = (
            int(descanso_texto)
            if descanso_texto
            else None
        )

        ordem = (
            int(ordem_texto)
            if ordem_texto
            else None
        )

        item_id = adicionar_exercicio_ao_treino(
            treino_id=treino_id,
            exercicio_id=exercicio_id,
            series=series,
            repeticoes=repeticoes,
            carga=carga,
            descanso_segundos=descanso_segundos,
            ordem=ordem,
        )

        print()
        print(
            "Exercício adicionado ao treino "
            "com sucesso!"
        )
        print(
            f"ID do item da ficha: {item_id}"
        )

    except ValueError as erro:
        print()
        print(f"Erro: {erro}")


def visualizar_ficha_treino():
    print()
    print("--- Ficha de Treino ---")

    try:
        treino_id = int(
            input("ID do treino: ")
        )

    except ValueError:
        print(
            "Erro: o ID deve ser um número inteiro."
        )
        return

    treino = buscar_treino_por_id(
        treino_id
    )

    if treino is None:
        print("Treino não encontrado.")
        return

    aluno = buscar_aluno_por_id(
        treino.aluno_id
    )

    exercicios = listar_exercicios_do_treino(
        treino_id
    )

    print()
    print(
        f"Aluno: "
        f"{aluno.nome if aluno else 'Não encontrado'}"
    )
    print(
        f"Treino: {treino.nome}"
    )
    print(
        f"Objetivo: {treino.objetivo}"
    )
    print(
        "Data de criação: "
        f"{treino.data_criacao.strftime('%d/%m/%Y')}"
    )

    print()
    print("--- Exercícios ---")

    if not exercicios:
        print(
            "Nenhum exercício adicionado "
            "a este treino."
        )
        return

    for item in exercicios:
        carga = (
            f"{item['carga']:.1f} kg"
            if item["carga"] is not None
            else "-"
        )

        descanso = (
            f"{item['descanso_segundos']} s"
            if item["descanso_segundos"]
            is not None
            else "-"
        )

        ordem = (
            item["ordem"]
            if item["ordem"] is not None
            else "-"
        )

        print(
            f"Ordem: {ordem} | "
            f"{item['nome']} | "
            f"Grupo: {item['grupo_muscular']} | "
            f"{item['series']} séries | "
            f"{item['repeticoes']} reps | "
            f"Carga: {carga} | "
            f"Descanso: {descanso}"
        )


def exportar_dados_json():
    print()
    print("--- Exportação para JSON ---")
    print("Acesso restrito ao usuário root master.")
    print()

    nome_usuario = input(
        "Usuário: "
    ).strip()

    senha = ler_senha_mascarada(
        "Senha: "
    )

    usuario = autenticar_usuario(
        nome_usuario,
        senha,
    )

    if (
        usuario is None
        or usuario.usuario != USUARIO_ROOT
    ):
        print()
        print("ACESSO NEGADO")
        print(
            "Usuário ou senha inválidos."
        )
        return

    print()
    print(
        "Autenticação realizada com sucesso."
    )

    try:
        caminho_arquivo = exportar_banco_json()

        print()
        print("Banco exportado com sucesso!")
        print(
            f"Arquivo: "
            f"{caminho_arquivo.name}"
        )
        print(
            f"Local: "
            f"{caminho_arquivo}"
        )

    except Exception as erro:
        print()
        print(
            "Não foi possível exportar o banco."
        )
        print(
            f"Erro: {erro}"
        )


def gerar_dados_ficticios():
    print()
    print("--- Geração de Dados com Faker ---")

    quantidade_texto = input(
        "Quantidade de alunos a gerar: "
    ).strip()

    try:
        quantidade = int(
            quantidade_texto
        )

        resultado = popular_dados_demonstracao(
            quantidade
        )

        print()
        print(
            "Dados fictícios gerados com sucesso!"
        )

        print(
            f"Alunos: "
            f"{resultado['alunos']}"
        )

        print(
            f"Planos disponíveis: "
            f"{resultado['planos']}"
        )

        print(
            f"Assinaturas: "
            f"{resultado['assinaturas']}"
        )

        print(
            f"Pagamentos: "
            f"{resultado['pagamentos']}"
        )

        print(
            f"Acessos: "
            f"{resultado['acessos']}"
        )

    except ValueError as erro:
        print()
        print(
            f"Erro: {erro}"
        )

    except Exception as erro:
        print()
        print(
            "Não foi possível gerar "
            "os dados fictícios."
        )
        print(
            f"Erro: {erro}"
        )


def mostrar_relatorio_geral():
    dados = relatorio_geral()

    print()
    print("=" * 45)
    print("RELATÓRIO GERAL")
    print("=" * 45)

    print(
        f"Total de alunos: "
        f"{dados['total_alunos']}"
    )

    print(
        f"Alunos ativos: "
        f"{dados['alunos_ativos']}"
    )

    print(
        f"Assinaturas ativas: "
        f"{dados['assinaturas_ativas']}"
    )

    print(
        f"Planos ativos: "
        f"{dados['planos_ativos']}"
    )


def mostrar_relatorio_financeiro():
    dados = relatorio_financeiro()

    print()
    print("=" * 45)
    print("RELATÓRIO FINANCEIRO")
    print("=" * 45)

    print(
        f"Total recebido: "
        f"R$ {dados['total_recebido']:.2f}"
    )

    print(
        f"Total pendente: "
        f"R$ {dados['total_pendente']:.2f}"
    )

    print(
        f"Total em atraso: "
        f"R$ {dados['total_atrasado']:.2f}"
    )

    print()

    print(
        f"Pagamentos realizados: "
        f"{dados['quantidade_pagos']}"
    )

    print(
        f"Pagamentos pendentes: "
        f"{dados['quantidade_pendentes']}"
    )

    print(
        f"Pagamentos atrasados: "
        f"{dados['quantidade_atrasados']}"
    )


def mostrar_relatorio_acessos():
    dados = relatorio_acessos()

    print()
    print("=" * 45)
    print("RELATÓRIO DE ACESSOS")
    print("=" * 45)

    print(
        f"Total de acessos: "
        f"{dados['total_acessos']}"
    )

    print(
        f"Acessos autorizados: "
        f"{dados['autorizados']}"
    )

    print(
        f"Acessos negados: "
        f"{dados['negados']}"
    )

    print()
    print("--- Ranking de Frequência ---")

    if not dados["ranking_alunos"]:
        print(
            "Nenhum acesso registrado."
        )
        return

    for posicao, aluno in enumerate(
        dados["ranking_alunos"],
        start=1,
    ):
        print(
            f"{posicao}º - "
            f"{aluno['nome']} | "
            f"{aluno['quantidade']} acesso(s)"
        )


def mostrar_relatorio_planos():
    planos = relatorio_planos()

    print()
    print("=" * 45)
    print("RELATÓRIO DE PLANOS")
    print("=" * 45)

    if not planos:
        print(
            "Nenhum plano cadastrado."
        )
        return

    for plano in planos:
        print(
            f"Plano: {plano['nome']} | "
            f"Valor: R$ {plano['valor']:.2f} | "
            f"Assinaturas ativas: "
            f"{plano['quantidade_assinaturas']}"
        )


def menu_relatorios():
    while True:
        print()
        print("=" * 45)
        print("RELATÓRIOS")
        print("=" * 45)

        print("1 - Relatório geral")
        print("2 - Relatório financeiro")
        print("3 - Relatório de acessos")
        print("4 - Relatório de planos")
        print("0 - Voltar")

        print("=" * 45)

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":
            mostrar_relatorio_geral()

        elif opcao == "2":
            mostrar_relatorio_financeiro()

        elif opcao == "3":
            mostrar_relatorio_acessos()

        elif opcao == "4":
            mostrar_relatorio_planos()

        elif opcao == "0":
            break

        else:
            print()
            print(
                "Opção inválida. "
                "Tente novamente."
            )


def iniciar_menu():
    while True:
        exibir_menu()

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":
            cadastrar_novo_aluno()

        elif opcao == "2":
            mostrar_alunos()

        elif opcao == "3":
            cadastrar_novo_plano()

        elif opcao == "4":
            mostrar_planos()

        elif opcao == "5":
            criar_nova_assinatura()

        elif opcao == "6":
            mostrar_assinaturas()

        elif opcao == "7":
            gerar_nova_cobranca()

        elif opcao == "8":
            mostrar_pagamentos()

        elif opcao == "9":
            registrar_novo_pagamento()

        elif opcao == "10":
            registrar_novo_acesso()

        elif opcao == "11":
            mostrar_acessos()

        elif opcao == "12":
            cadastrar_novo_exercicio()

        elif opcao == "13":
            mostrar_exercicios()

        elif opcao == "14":
            criar_novo_treino()

        elif opcao == "15":
            mostrar_treinos_do_aluno()

        elif opcao == "16":
            adicionar_exercicio_na_ficha()

        elif opcao == "17":
            visualizar_ficha_treino()

        elif opcao == "18":
            exportar_dados_json()

        elif opcao == "19":
            gerar_dados_ficticios()

        elif opcao == "20":
            menu_relatorios()

        elif opcao == "0":
            print()
            print(
                "Encerrando o "
                "SmartFit Gym Manager."
            )
            break

        else:
            print()
            print(
                "Opção inválida. "
                "Tente novamente."
            )