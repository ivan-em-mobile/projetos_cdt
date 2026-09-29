import sqlite3
import os

# ============================================================
# CONFIGURAÇÃO
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "power_up.db")


# ============================================================
# CONEXÃO COM O BANCO
# ============================================================

def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    return conexao


# ============================================================
# PAUSA
# ============================================================

def pausar():
    input("\nPressione ENTER para voltar ao menu...")


# ============================================================
# LISTAR EXERCÍCIOS
# ============================================================

def listar_exercicios():
    try:
        conexao = conectar()

        exercicios = conexao.execute("""
            SELECT nome, grupo_muscular, musculos, execucao
            FROM exercicios
            ORDER BY grupo_muscular, nome
        """).fetchall()

        conexao.close()

        print("\n" + "=" * 60)
        print("                 EXERCÍCIOS")
        print("=" * 60)

        print(f"\nTotal de exercícios encontrados: {len(exercicios)}\n")

        for i, exercicio in enumerate(exercicios, start=1):
            print(f"{i}. {exercicio['nome']}")
            print(f"   Grupo muscular: {exercicio['grupo_muscular']}")
            print(f"   Músculos: {exercicio['musculos']}")
            print(f"   Execução: {exercicio['execucao']}")
            print("-" * 60)

        input("\nPressione ENTER para voltar ao menu...")

    except Exception as erro:
        print("\nErro ao listar exercícios:")
        print(erro)
        input("\nPressione ENTER para voltar ao menu...")

# ============================================================
# PESQUISAR EXERCÍCIO
# ============================================================

def pesquisar_exercicio():
    nome = input("\nDigite o nome do exercício: ").strip()

    if not nome:
        print("\nVocê não digitou nenhum exercício.")
        pausar()
        return

    try:
        conexao = conectar()

        exercicios = conexao.execute("""
            SELECT nome, grupo_muscular, musculos, execucao
            FROM exercicios
            WHERE nome LIKE ?
            ORDER BY nome
        """, (f"%{nome}%",)).fetchall()

        conexao.close()

        print("\n" + "=" * 60)
        print("                 RESULTADO")
        print("=" * 60)

        if not exercicios:
            print("\nNenhum exercício encontrado.")
            pausar()
            return

        for exercicio in exercicios:
            print(f"\nExercício: {exercicio['nome']}")
            print(f"Grupo muscular: {exercicio['grupo_muscular']}")
            print(f"Músculos: {exercicio['musculos']}")
            print(f"Execução: {exercicio['execucao']}")
            print("-" * 60)

        pausar()

    except Exception as erro:
        print("\nErro ao pesquisar exercício:")
        print(erro)
        pausar()


# ============================================================
# LISTAR GRUPOS MUSCULARES
# ============================================================

def listar_grupos():
    try:
        conexao = conectar()

        grupos = conexao.execute("""
            SELECT DISTINCT grupo_muscular
            FROM exercicios
            ORDER BY grupo_muscular
        """).fetchall()

        conexao.close()

        print("\n" + "=" * 60)
        print("              GRUPOS MUSCULARES")
        print("=" * 60)

        if not grupos:
            print("\nNenhum grupo muscular encontrado.")
            pausar()
            return

        for grupo in grupos:
            print(f"- {grupo['grupo_muscular']}")

        pausar()

    except Exception as erro:
        print("\nErro ao listar grupos musculares:")
        print(erro)
        pausar()


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu():

    while True:

        print("\n")
        print("=" * 60)
        print("                     POWER UP")
        print("              CLI - TREINOS E EXERCÍCIOS")
        print("=" * 60)

        print("\n1 - Listar exercícios")
        print("2 - Pesquisar exercício")
        print("3 - Ver grupos musculares")
        print("4 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            listar_exercicios()

        elif opcao == "2":
            pesquisar_exercicio()

        elif opcao == "3":
            listar_grupos()

        elif opcao == "4":
            print("\nEncerrando o Power Up...")
            break

        else:
            print("\nOpção inválida. Tente novamente.")
            pausar()


# ============================================================
# INÍCIO DO PROGRAMA
# ============================================================

if __name__ == "__main__":
    print("\nCLI INICIADO")
    menu()