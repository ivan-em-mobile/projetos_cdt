import json
import os
from datetime import datetime

# Configurações
NOME_ARQUIVO = "tarefas_pro.json"

def carregar_tarefas():
    """Carrega tarefas usando o formato JSON para maior integridade."""
    if not os.path.exists(NOME_ARQUIVO):
        return []
    try:
        with open(NOME_ARQUIVO, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("⚠️ Aviso: Arquivo de dados corrompido. Iniciando nova lista.")
        return []

def salvar_tarefas(tarefas):
    """Salva a lista completa em formato estruturado JSON."""
    try:
        with open(NOME_ARQUIVO, 'w', encoding='utf-8') as file:
            json.dump(tarefas, file, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"❌ Erro ao salvar tarefas: {e}")

def adicionar_tarefa(tarefas):
    descricao = input("\n📝 Descrição da tarefa: ").strip()
    if descricao:
        nova_tarefa = {
            'id': len(tarefas) + 1,
            'descricao': descricao,
            'concluida': False,
            'data': datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        tarefas.append(nova_tarefa)
        salvar_tarefas(tarefas)
        print("✅ Tarefa adicionada!")
    else:
        print("⚠️ A descrição não pode estar vazia.")

def visualizar_tarefas(tarefas):
    if not tarefas:
        print("\n📭 Sua lista está limpa!")
        return

    print(f"\n{'ID':<3} | {'Status':<10} | {'Tarefa':<30} | {'Criada em'}")
    print("-" * 70)
    for t in tarefas:
        status = "✅ Pronta" if t['concluida'] else "⏳ Pendente"
        print(f"{t['id']:<3} | {status:<10} | {t['descricao']:<30} | {t['data']}")

def gerenciar_tarefa(tarefas, acao="marcar"):
    visualizar_tarefas(tarefas)
    if not tarefas: return

    try:
        idx_input = int(input(f"\nID da tarefa para {acao}: "))
        # Busca a tarefa pelo ID real, não apenas pelo índice da lista
        tarefa = next((t for t in tarefas if t['id'] == idx_input), None)
        
        if tarefa:
            if acao == "marcar":
                tarefa['concluida'] = not tarefa['concluida']
                print(f"🔄 Status de '{tarefa['descricao']}' atualizado!")
            elif acao == "remover":
                tarefas.remove(tarefa)
                print(f"🗑️ Tarefa removida!")
            salvar_tarefas(tarefas)
        else:
            print("❌ ID não encontrado.")
    except ValueError:
        print("⚠️ Digite um número válido.")

def menu_principal():
    tarefas = carregar_tarefas()

    while True:
        print("\n--- 📝 GESTOR DE TAREFAS PRO ---")
        print("1. Adicionar [A]")
        print("2. Listar    [L]")
        print("3. Concluir  [C]")
        print("4. Remover   [R]")
        print("5. Sair      [S]")
        
        opcao = input("\nEscolha uma opção: ").upper()

        if opcao in ['1', 'A']:
            adicionar_tarefa(tarefas)
        elif opcao in ['2', 'L']:
            visualizar_tarefas(tarefas)
        elif opcao in ['3', 'C']:
            gerenciar_tarefa(tarefas, "marcar")
        elif opcao in ['4', 'R']:
            gerenciar_tarefa(tarefas, "remover")
        elif opcao in ['5', 'S']:
            print("👋 Até logo!")
            break
        else:
            print("⚠️ Opção inválida!")

if __name__ == "__main__":
    menu_principal()