import os

nome_salvo = ""
data_salva = ""
horario_salvo = ""

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:

    limpar_tela()

    print("\n Barbearia Andrades - Seja Bem Vindo!")

    print("\nPara escolher o serviço digite o número correspondente...")

    print("\n1 - Agendar horário")
    print("\n2 - Cancelar agendamento")
    print("\n3 - Serviços disponíveis")
    print("\n4 - Localização e contato")
    print("\n5 - Avalie nosso serviço")
    print("\n0 - Sair")

    escolha_servico = input("\nEscolha o serviço desejado: ")

    if escolha_servico == '1':

        limpar_tela()

        print("\n=== Agendamento de Horário ===")

        nome_salvo = input("\nDigite seu nome: ")
        data_salva = input("\nDigite a data do agendamento | EX:09/10/2026 : ")
        horario_salvo = input("\nDigite o horário desejado | EX:17:30 : ")

        print(f"\nCliente: {nome_salvo}")
        print(f"\nData: {data_salva}")
        print(f"\nHorário: {horario_salvo}")

        print(f"\nAgendamento realizado com sucesso {nome_salvo}, Obrigado pela preferência!")

        print("\n>.<")

        input("\nPressione [Enter] para voltar ao menu...")

    elif escolha_servico == '2':

        limpar_tela()

        if nome_salvo == "":

            print("\nVocê ainda não possui um agendamento ativo.")
            print("\nPor favor, selecione a opção 1 no menu para agendar o seu horário!")

        else:

            print("\nPara cancelar seu agendamento preencha os campos a seguir:")

            nome = input("\nDigite seu nome: ")

            if nome != nome_salvo:

                print("\nNome diferente, tente novamente!")

                nome = input("\nDIGITE SEU NOME NOVAMENTE!:")

                if nome != nome_salvo:

                    print("\nNOME DIFERENTE, TENTE NOVAMENTE!")

            if nome == nome_salvo:

                print(f"\nCliente: {nome_salvo}")
                print(f"\nData: {data_salva}")
                print(f"\nHorário: {horario_salvo}")

                print(f"\nAgendamento cancelado com sucesso {nome_salvo}!")

                nome_salvo = ""
                data_salva = ""
                horario_salvo = ""

        input("\nPressione [Enter] para voltar ao menu...")

    elif escolha_servico == '3':

        limpar_tela()

        print("\nDegradê - 35R$")
        print("\nCorte social - 30R$")
        print("\nBarba completa - 25R$")
        print("\nPigmentação - 40R$")
        print("\nHidratação capilar - 50R$")
        print("\nPlatinado - 120R$")
        print("\nCombo corte + barba - 50R$")

        input("\nPressione [Enter] para voltar ao menu...")

    elif escolha_servico == '4':

        limpar_tela()

        print("\nEndereço: Jardim Macedônia - Rua Póva de Varzim - Nº67")
        print("\nContato: +55 11 91539-7314")

        input("\nPressione [Enter] para voltar ao menu...")

    elif escolha_servico == '5':

        limpar_tela()

        print("\nAvalie nossos serviços de 1 a 5:")

        print("\n1 - Péssimo")
        print("\n2 - Ruim")
        print("\n3 - Médio")
        print("\n4 - Bom")
        print("\n5 - Muito bom")

        avaliar_servico = input("\nSua avaliação: ")

        if avaliar_servico == '1':

            print("\nSentimos MUITO, vamos procurar melhorar :(")

        elif avaliar_servico == '2':

            print("\nVamos procurar melhorar :(")

        elif avaliar_servico == '3':

            print("\nVamos nos esforçar mais, Obrigado!")

        elif avaliar_servico == '4':

            print("\nObrigado, Volte sempre!")

        elif avaliar_servico == '5':

            print("\nMuito obrigado, Volte sempre!")

        else:

            print("\nAvaliação inválida!")

        input("\nPressione [Enter] para voltar ao menu...")

    elif escolha_servico == '0':

        limpar_tela()

        print("\nSistema encerrado.")

        break

    else:

        print("\nOpção inválida, tente novamente!")

        input("\nPressione [Enter] para continuar...")