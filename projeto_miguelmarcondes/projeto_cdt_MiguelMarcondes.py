'''

Sistema de Barbearia

'''

while True:

    print("\n Barbearia Andrades - Seja Bem Vindo!")

    print("\nPara escolher o serviço digite o número correspondente...")

    print("\n1 - Agendar horário")
    print("\n2 - Serviços disponíveis")
    print("\n3 - Localização e contato")
    print("\n4 - Avalie nosso serviço")
    print("\n0 - Sair")

    escolha_servico = input("\nEscolha o serviço desejado: ")

    if escolha_servico == '1':

        print("\n=== Agendamento de Horário ===")

        nome = input("\nDigite seu nome: ")

        dia = input("Digite o dia do agendamento: ")

        horario = input("Digite o horário desejado: ")

        print("\nAgendamento realizado com sucesso!")

        print(f"\nCliente: {nome}")

        print(f"Dia: {dia}")

        print(f"Horário: {horario}")

        print("\nObrigado pela preferência!")

    elif escolha_servico == '2':

        print("\nCorte masculino - 30R$")

        print("\nCorte de barba - 25R$")

        print("\nSobrancelha - 20R$")

        print("\nLuzes - 80R$")

        print("\nProgressiva - 100R$")

    elif escolha_servico == '3':

        print("\nEndereço: Jardim Macedônia - Rua Póva de Varzim - Nº67")

        print("\nContato: +55 11 91539-7314")

    elif escolha_servico == '4':

        print("\nAvalie nossos serviços de 1 a 5:")

        print("\n1 - Péssimo")

        print("\n2 - Ruim")

        print("\n3 - Médio")

        print("\n4 - Bom")

        print("\n5 - Muito bom")

        avaliar_servico = input("\nSua avaliação: ")

        if avaliar_servico == '1':

            print("\nSentimos muito, vamos procurar melhorar :(")

        elif avaliar_servico == '2':

            print("\nSentimos muito, vamos procurar melhorar :(")

        elif avaliar_servico == '3':

            print("\nVamos nos esforçar mais, obrigado!")

        elif avaliar_servico == '4':

            print("\nObrigado, volte sempre!")

        elif avaliar_servico == '5':

            print("\nMuito obrigado, volte sempre!")

        else:

            print("\nAvaliação inválida!")

    elif escolha_servico == '0':

        print("\nSistema encerrado.")

        break

    else:

        print("\nOpção inválida!")





           

