while True:

    print("\n===== SISTEMA =====")
    print("1 - Agendar Aula")
    print("0 - Sair")

    acesso_menu = input("\nEscolha uma opção: ")

    if acesso_menu == '1':

        print("\nAGENDANDO AULA...")

        nome_aluno = input("Digite seu nome: ")
        idade_aluno = input("Digite sua idade: ")
        numero_aluno = input("Digite se whatsapp: ")

        print("\nAULA AGENDADA COM SUCESSO!")

        print("Aluno:", nome_aluno)
        print("Turma:", idade_aluno)
        print("E-mail:", numero_aluno)

    elif acesso_menu == '0':

        print("\nSAINDO DO SISTEMA...")
        break

    else:

        print("\nOPÇÃO INVÁLIDA.")
        