import os
from datetime import datetime

agendamento_ativo = {
    "nome": "",
    "data": "",
    "horario": "",
    "servico": ""
}

SERVICOS = {
    "1": ("Degradê", 35),
    "2": ("Corte social", 30),
    "3": ("Barba completa", 25),
    "4": ("Pigmentação", 40),
    "5": ("Hidratação capilar", 50),
    "6": ("Platinado", 120),
    "7": ("Combo corte + barba", 50)
}

HORARIOS_DISPONIVEIS = {
    "09:00": True,
    "10:00": True,
    "11:00": True,
    "13:00": True,
    "14:00": True,
    "15:00": True,
    "16:00": True,
    "17:30": True
}

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_cabecalho(titulo):
    limpar_tela()
    print("=" * 45)
    print(f"      Barbearia Andrades - {titulo}")
    print("=" * 45)

while True:

    limpar_tela()

    print("\nBarbearia Andrades - Seja Bem Vindo!")

    print("\nSelecione a opção desejada:")
    print("1 - Agendar horário")
    print("2 - Cancelar agendamento")
    print("3 - Serviços e preços")
    print("4 - Localização e contato")
    print("5 - Avalie nosso serviço")
    print("0 - Sair")

    escolha_servico = input("\nEscolha: ").strip()

    if escolha_servico == '1':

        if agendamento_ativo["nome"] != "":
            mostrar_cabecalho("ALERTA")
            print("\nVocê já possui um agendamento ativo.")
            print("Cancele o atual antes de marcar outro.")
            input("\nPressione Enter para voltar...")
            continue

        mostrar_cabecalho("Agendamento")

        while True:
            nome = input("\nDigite seu nome completo: ").strip()

            if len(nome) >= 3 and nome.replace(" ", "").isalpha():
                agendamento_ativo["nome"] = nome
                break

            print("Nome inválido.")

        print("\nServiços disponíveis:\n")

        for cod, (nome_serv, preco) in SERVICOS.items():
            print(f"{cod} - {nome_serv} (R$ {preco:.2f})")

        while True:
            cod_servico = input("\nDigite o número do serviço: ").strip()

            if cod_servico in SERVICOS:
                agendamento_ativo["servico"] = SERVICOS[cod_servico][0]
                break

            print("Serviço inválido.")

        while True:
            data_input = input("\nDigite a data (DD/MM/AAAA): ").strip()

            try:
                data_validada = datetime.strptime(data_input, "%d/%m/%Y")

                if data_validada.date() < datetime.now().date():
                    print("Não é possível agendar no passado.")
                    continue

                agendamento_ativo["data"] = data_input
                break

            except ValueError:
                print("Data inválida.")

        print("\nHorários disponíveis:\n")

        for hr, disponivel in HORARIOS_DISPONIVEIS.items():

            if disponivel:
                status = "Disponível"
            else:
                status = "Ocupado"

            print(f"{hr} -> {status}")

        while True:

            horario_input = input("\nDigite o horário desejado: ").strip()

            horario_input = (
                horario_input
                .replace(".", ":")
                .replace("/", ":")
                .replace(";", ":")
            )

            if horario_input in HORARIOS_DISPONIVEIS:

                if HORARIOS_DISPONIVEIS[horario_input]:

                    agendamento_ativo["horario"] = horario_input
                    HORARIOS_DISPONIVEIS[horario_input] = False
                    break

                else:
                    print("Esse horário já está ocupado.")

            else:
                print("Horário inválido.")

        mostrar_cabecalho("Sucesso")

        print(f"\nAgendamento confirmado para {agendamento_ativo['nome']}")
        print(f"Serviço: {agendamento_ativo['servico']}")
        print(f"Data: {agendamento_ativo['data']}")
        print(f"Horário: {agendamento_ativo['horario']}")

        input("\nPressione Enter para voltar ao menu...")

    elif escolha_servico == '2':

        mostrar_cabecalho("Cancelar Agendamento")

        if agendamento_ativo["nome"] == "":
            print("\nNenhum agendamento encontrado.")

        else:

            nome_confirma = input("\nDigite seu nome: ").strip()

            if nome_confirma.lower() == agendamento_ativo["nome"].lower():

                hr_liberar = agendamento_ativo["horario"]
                HORARIOS_DISPONIVEIS[hr_liberar] = True

                print(f"\nAgendamento de {agendamento_ativo['nome']} cancelado.")

                agendamento_ativo = {
                    "nome": "",
                    "data": "",
                    "horario": "",
                    "servico": ""
                }

            else:
                print("\nNome incorreto.")

        input("\nPressione Enter para voltar...")

    elif escolha_servico == '3':

        mostrar_cabecalho("Serviços e Preços")

        print()

        for cod, (nome_serv, preco) in SERVICOS.items():
            print(f"{nome_serv.ljust(22)} - R$ {preco},00")

        input("\nPressione Enter para voltar...")

    elif escolha_servico == '4':

        mostrar_cabecalho("Contato e Endereço")

        print("\nEndereço: Jardim Macedônia - Rua Póva de Varzim - Nº67")
        print("Contato: +55 11 91539-7314")

        input("\nPressione Enter para voltar...")

    elif escolha_servico == '5':

        mostrar_cabecalho("Avaliação")

        print("\nQual nota você dá para o atendimento?")
        print("1 - Péssimo")
        print("2 - Ruim")
        print("3 - Médio")
        print("4 - Bom")
        print("5 - Excelente")

        avaliar_servico = input("\nSua nota: ").strip()

        respostas_avaliacao = {
            "1": "Sentimos muito. Vamos melhorar.",
            "2": "Obrigado pelo feedback.",
            "3": "Vamos nos esforçar mais.",
            "4": "Ficamos felizes com sua avaliação.",
            "5": "Muito obrigado pela excelente avaliação."
        }

        if avaliar_servico in respostas_avaliacao:
            print(f"\n{respostas_avaliacao[avaliar_servico]}")

        else:
            print("\nNota inválida.")

        input("\nPressione Enter para voltar...")

    elif escolha_servico == '0':

        limpar_tela()

        print("\nSistema encerrado.")
        break

    else:

        print("\nOpção inválida.")
        input("\nPressione Enter para continuar...")