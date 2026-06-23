# --- Documentação do Código ---
# Este programa é um aplicativo de lista de tarefas (To-Do List) baseado em terminal.
# Ele permite adicionar, visualizar, marcar como concluída e remover tarefas.
# As tarefas são salvas e carregadas de um arquivo de texto para que não sejam perdidas
# quando o programa é encerrado, demonstrando persistência de dados.

NOME_ARQUIVO = "tarefas.txt" # Define o nome do arquivo onde as tarefas serão salvas

def carregar_tarefas():
    """
    Carrega as tarefas de um arquivo de texto.
    Cada linha do arquivo representa uma tarefa.
    Retorna uma lista de dicionários, onde cada dicionário tem 'descricao' e 'concluida'.
    """
    tarefas = []
    try:
        with open(NOME_ARQUIVO, 'r', encoding='utf-8') as file:
            for linha in file:
                linha = linha.strip() # Remove espaços e quebras de linha
                if linha: # Garante que a linha não está vazia
                    # Formato esperado: [X] Minha Tarefa ou [ ] Outra Tarefa
                    if linha.startswith('[X] '):
                        tarefas.append({'descricao': linha[4:], 'concluida': True})
                    elif linha.startswith('[ ] '):
                        tarefas.append({'descricao': linha[4:], 'concluida': False})
                    else:
                        # Para tarefas antigas que talvez não sigam o formato [ ]
                        tarefas.append({'descricao': linha, 'concluida': False})
    except FileNotFoundError:
        # Se o arquivo não existe (primeira vez que o programa roda), retorna lista vazia
        pass
    return tarefas

def salvar_tarefas(tarefas):
    """
    Salva as tarefas em um arquivo de texto.
    Formato: [X] Descrição da Tarefa (se concluída) ou [ ] Descrição da Tarefa (se pendente).
    """
    with open(NOME_ARQUIVO, 'w', encoding='utf-8') as file:
        for tarefa in tarefas:
            status = '[X]' if tarefa['concluida'] else '[ ]'
            file.write(f"{status} {tarefa['descricao']}\n")

def adicionar_tarefa(tarefas):
    """Adiciona uma nova tarefa à lista."""
    descricao = input("Digite a descrição da nova tarefa: ").strip()
    if descricao:
        tarefas.append({'descricao': descricao, 'concluida': False})
        salvar_tarefas(tarefas)
        print(f"Tarefa '{descricao}' adicionada com sucesso!")
    else:
        print("A descrição da tarefa não pode ser vazia.")

def visualizar_tarefas(tarefas):
    """Exibe todas as tarefas na lista."""
    if not tarefas:
        print("\nSua lista de tarefas está vazia!")
        return

    print("\n--- Suas Tarefas ---")
    for i, tarefa in enumerate(tarefas):
        status = "[X]" if tarefa['concluida'] else "[ ]"
        print(f"{i + 1}. {status} {tarefa['descricao']}")
    print("--------------------")

def marcar_tarefa_concluida(tarefas):
    """Marca uma tarefa como concluída ou pendente."""
    visualizar_tarefas(tarefas) # Mostra a lista para o usuário escolher
    if not tarefas:
        return

    while True:
        try:
            num_tarefa = int(input("Digite o número da tarefa para marcar/desmarcar: "))
            if 1 <= num_tarefa <= len(tarefas):
                tarefa_index = num_tarefa - 1
                tarefas[tarefa_index]['concluida'] = not tarefas[tarefa_index]['concluida'] # Inverte o status
                salvar_tarefas(tarefas)
                print(f"Status da tarefa '{tarefas[tarefa_index]['descricao']}' atualizado!")
                break
            else:
                print("Número de tarefa inválido. Por favor, digite um número da lista.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def remover_tarefa(tarefas):
    """Remove uma tarefa da lista."""
    visualizar_tarefas(tarefas) # Mostra a lista para o usuário escolher
    if not tarefas:
        return

    while True:
        try:
            num_tarefa = int(input("Digite o número da tarefa para remover: "))
            if 1 <= num_tarefa <= len(tarefas):
                tarefa_removida = tarefas.pop(num_tarefa - 1) # Remove pelo índice
                salvar_tarefas(tarefas)
                print(f"Tarefa '{tarefa_removida['descricao']}' removida com sucesso!")
                break
            else:
                print("Número de tarefa inválido. Por favor, digite um número da lista.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def menu_principal():
    """Exibe o menu principal do aplicativo e gerencia as opções."""
    tarefas = carregar_tarefas() # Carrega as tarefas ao iniciar o programa

    while True:
        print("\n--- Menu da Lista de Tarefas ---")
        print("1. Adicionar tarefa")
        print("2. Visualizar tarefas")
        print("3. Marcar/Desmarcar tarefa como concluída")
        print("4. Remover tarefa")
        print("5. Sair")
        print("--------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_tarefa(tarefas)
        elif opcao == '2':
            visualizar_tarefas(tarefas)
        elif opcao == '3':
            marcar_tarefa_concluida(tarefas)
        elif opcao == '4':
            remover_tarefa(tarefas)
        elif opcao == '5':
            print("Saindo do aplicativo. Suas tarefas foram salvas!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção de 1 a 5.")

# Inicia o aplicativo
if __name__ == "__main__":
    menu_principal()