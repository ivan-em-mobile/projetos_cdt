import os
import json
from datetime import datetime

ARQUIVO_BANCO = "agendamentos.json"

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

def carregar_agendamentos():

    if not os.path.exists(ARQUIVO_BANCO):
        with open(ARQUIVO_BANCO, "w") as arquivo:
            json.dump([], arquivo)

    with open(ARQUIVO_BANCO, "r") as arquivo:
        return json.load(arquivo)

def salvar_agendamentos(lista_agendamentos):

    with open(ARQUIVO_BANCO, "w") as arquivo:
        json.dump(lista_agendamentos, arquivo, indent=4)

while True:

    limpar_tela()

    print("\nBarbearia Andrades - Seja Bem Vindo!")

    print("\n1 - Agendar horário")
    print("2 - Cancelar agendamento")
    print("3 - Ver agendamentos")
    print("4 - Serviços e preços")
    print("5 - Localização e contato")
    print("0 - Sair")

    escolha = input("\nEscolha: ").strip()

    if escolha == "1":

        mostrar_cabecalho("Agendamento")

        nome = input("\nDigite seu nome: ").strip()

        print("\nServiços:\n")

        for cod, (nome_serv, preco) in SERVICOS.items():
            print(f"{cod} - {nome_serv} (R$ {preco})")

        cod_servico = input("\nEscolha o serviço: ").strip()

        if cod_servico not in SERVICOS:
            print("\nServiço inválido.")
            input("\nPressione Enter...")
            continue

        while True:

            data_input = input("\nDigite a data (DD/MM/AAAA): ").strip()

            try:
                data_validada = datetime.strptime(data_input, "%d/%m/%Y")

                if data_validada.date() < datetime.now().date():
                    print("Data inválida.")
                    continue

                break

            except ValueError:
                print("Formato inválido.")

        print("\nHorários:\n")

        for hr, disponivel in HORARIOS_DISPONIVEIS.items():

            if disponivel:
                print(f"{hr} -> Disponível")
            else:
                print(f"{hr} -> Ocupado")

        horario = input("\nDigite o horário: ").strip()

        if horario not in HORARIOS_DISPONIVEIS:
            print("\nHorário inválido.")
            input("\nPressione Enter...")
            continue

        if not HORARIOS_DISPONIVEIS[horario]:
            print("\nHorário ocupado.")
            input("\nPressione Enter...")
            continue

        HORARIOS_DISPONIVEIS[horario] = False

        agendamento = {
            "nome": nome,
            "servico": SERVICOS[cod_servico][0],
            "data": data_input,
            "horario": horario
        }

        lista = carregar_agendamentos()
        lista.append(agendamento)
        salvar_agendamentos(lista)

        print("\nAgendamento realizado com sucesso!")

        input("\nPressione Enter para voltar...")

    elif escolha == "2":

        mostrar_cabecalho("Cancelar Agendamento")

        nome = input("\nDigite seu nome: ").strip()

        lista = carregar_agendamentos()

        novo_banco = []
        removido = False

        for agendamento in lista:

            if agendamento["nome"].lower() == nome.lower():

                HORARIOS_DISPONIVEIS[agendamento["horario"]] = True
                removido = True

            else:
                novo_banco.append(agendamento)

        salvar_agendamentos(novo_banco)

        if removido:
            print("\nAgendamento cancelado.")
        else:
            print("\nNenhum agendamento encontrado.")

        input("\nPressione Enter para voltar...")

    elif escolha == "3":

        mostrar_cabecalho("Agendamentos")

        lista = carregar_agendamentos()

        if len(lista) == 0:
            print("\nNenhum agendamento encontrado.")

        else:

            for agendamento in lista:

                print("\nNome:", agendamento["nome"])
                print("Serviço:", agendamento["servico"])
                print("Data:", agendamento["data"])
                print("Horário:", agendamento["horario"])
                print("-" * 30)

        input("\nPressione Enter para voltar...")

    elif escolha == "4":

        mostrar_cabecalho("Serviços e Preços")

        print()

        for cod, (nome_serv, preco) in SERVICOS.items():
            print(f"{nome_serv} - R$ {preco}")

        input("\nPressione Enter para voltar...")

    elif escolha == "5":

        mostrar_cabecalho("Contato")

        print("\nEndereço: Jardim Macedônia - Rua Póva de Varzim - Nº67")
        print("Contato: +55 11 91539-7314")

        input("\nPressione Enter para voltar...")

    elif escolha == "0":

        print("\nSistema encerrado.")
        break

    else:

        print("\nOpção inválida.")
        input("\nPressione Enter...")