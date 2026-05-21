import getpass
import json
import sqlite3
from datetime import datetime

def inicializar_banco():
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            plano TEXT NOT NULL,
            valor TEXT NOT NULL,
            horario TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracoes (
            chave TEXT PRIMARY KEY,
            valor TEXT NOT NULL
        )
    """)

    cursor.execute("INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES ('senha', '123456')")
    
    conexao.commit()
    conexao.close()

def obter_senha():
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT valor FROM configuracoes WHERE chave = 'senha'")
    senha = cursor.fetchone()[0]
    conexao.close()
    return senha

def atualizar_senha(nova_senha):
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE configuracoes SET valor = ? WHERE chave = 'senha'", (nova_senha,))
    conexao.commit()
    conexao.close()

def configurar_login():
    print("\n--- Configurações de Login ---")
    nova_senha = getpass.getpass('Digite a nova senha (os caracteres não aparecerão): ')
    confirmacao_senha = getpass.getpass('Confirme a nova senha: ')

    if nova_senha == confirmacao_senha:
        atualizar_senha(nova_senha)
        print('\n[SUCESSO] Senha alterada com sucesso!')
        return True
    else:
        print('\n[ERRO] As senhas não coincidem! A senha não foi alterada.')
        return False

def realizar_login_com_tentativas():
    tentativas_restantes = 5
    senha_padrao = obter_senha()
    
    print('\n--- Sistema de Login ---')
    nome_usuario = input('Digite seu login: ')
    
    while tentativas_restantes > 0:
        print(f'\nTentativas restantes: {tentativas_restantes}')
        senha_digitada = getpass.getpass('Digite sua senha (os caracteres não aparecerão): ')

        if senha_digitada == senha_padrao:
            print(f'\n[SUCESSO] Bem-vindo, {nome_usuario}!')
            return True
        else:
            tentativas_restantes -= 1
            if tentativas_restantes > 0:
                print('\n[ERRO] Senha incorreta! Tente novamente.')
            else:
                print('\n[BLOQUEADO] Número de tentativas excedido!')
    
    return False

def mostrar_planos():
    print("\n===== PLANOS DISPONÍVEIS =====")
    print("1 - Plano Gratuito")
    print("2 - Plano Básico - R$ 4,99 por mês")
    print("3 - Plano Premium - R$ 9,99 por mês")
    print("==============================")

def cadastrar_cliente():
    nome = input("\nDigite o nome do cliente: ")
    mostrar_planos()
    escolha = input("Escolha o plano do cliente: ")

    if escolha == "1":
        plano = "Gratuito"
        valor = "R$ 0,00"
    elif escolha == "2":
        plano = "Básico"
        valor = "R$ 4,99"
    elif escolha == "3":
        plano = "Premium"
        valor = "R$ 9,99"
    else:
        print("Plano inválido!")
        return

    horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, plano, valor, horario) 
        VALUES (?, ?, ?, ?)
    """, (nome, plano, valor, horario))
    conexao.commit()
    conexao.close()

    print("\nCliente cadastrado com sucesso!")

def listar_clientes():
    print("\n========= CLIENTES CADASTRADOS =========")
    
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, plano, valor, horario FROM clientes")
    clientes = cursor.fetchall()
    conexao.close()

    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    for i, cliente in enumerate(clientes, start=1):
        print(f"\nCliente {i}")
        print(f"Nome: {cliente[0]}")
        print(f"Plano: {cliente[1]}")
        print(f"Valor Mensal: {cliente[2]}")
        print(f"Horário do Cadastro: {cliente[3]}")
        print("-----------------------------------")

def mostrar_total():
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total = cursor.fetchone()[0]
    conexao.close()
    
    print(f"\nTotal de clientes cadastrados: {total}")

def exportar_para_json():
    conexao = sqlite3.connect("sistema.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, plano, valor, horario FROM clientes")
    linhas = cursor.fetchall()
    conexao.close()

    if not linhas:
        print("\n[AVISO] Não há clientes cadastrados para exportar.")
        return

    clientes_lista = [dict(linha) for linha in linhas]
    nome_arquivo = "clientes.json"
    
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(clientes_lista, arquivo, indent=4, ensure_ascii=False)
        
        print(f"\n[SUCESSO] Tudo pronto! Arquivo '{nome_arquivo}' gerado com sucesso.")
    except Exception as e:
        print(f"\n[ERRO] Falha ao gerar o arquivo JSON: {e}")

inicializar_banco()

if realizar_login_com_tentativas():
    while True:
        print("\n=========== MENU ===========")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Mostrar total de clientes")
        print("4 - Configurações (Alterar Senha)")
        print("5 - Exportar dados para JSON 💾")
        print("6 - Sair")
        print("============================")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            listar_clientes()
        elif opcao == "3":
            mostrar_total()
        elif opcao == "4":
            configurar_login()
        elif opcao == "5":
            exportar_para_json() 
        elif opcao == "6":
            print("\nSistema encerrado.")
            break
        else:
            print("\nOpção inválida. Tente novamente.")
else:
    print("\nNão foi possível acessar o sistema.")