import sqlite3

def criar_banco():
    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            dia TEXT NOT NULL,
            mes TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

def add_data():
    while True:
        #Garante que o numero do dia seja válido
        dia = input("Digite o dia: ")
        try:
            if 1 <= int(dia) <= 31:
                break
            else:
                print("❌ Dia inválido! Digite um número entre 1 e 31.")
        except ValueError:
            print("⚠️ Erro: Digite apenas números inteiros para o dia!")

    while True:
        #garante que o mes seja válido
        mes = input("Digite o Mes: ")
        try:
            if 1 <= int(mes) <= 12:
                break
            else:
                print("❌ Mês inválido! Digite um número entre 1 e 12.")
        except ValueError:
            print("⚠️ Erro: Digite apenas números inteiros para o mês!")

    hora = input("Digite a Hora: ")
    nome = input("Digite o nome do compromisso: ")

    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()
    
    #coloca os dados em contatos
    cursor.execute("""
        INSERT INTO contatos (nome, dia, mes, hora) 
        VALUES (?, ?, ?, ?)
    """, (nome, dia, mes, hora))
    
    conexao.commit()
    conexao.close()
    print("✅ Data agendada com sucesso!")


def listar_datas():
    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM contatos")
    dados = cursor.fetchall()
    
    if not dados:
        print("Nenhuma data encontrada.")
    for linha in dados:
        print(f"ID: {linha[0]} | Nome: {linha[1]} | Data: {linha[2]}/{linha[3]} às {linha[4]}")
        
    conexao.close()

def editar_data():
    listar_datas()
    
    id_editar = input("Digite o ID da data que deseja editar: ")
    
    novo_nome = input("Digite o novo nome do compromisso: ")
    novo_dia = input("Digite o novo dia: ")
    novo_mes = input("Digite o novo Mês: ")
    nova_hora = input("Digite a nova Hora: ")
    
    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE contatos 
        SET nome = ?, dia = ?, mes = ?, hora = ? 
        WHERE id = ?
    """, (novo_nome, novo_dia, novo_mes, nova_hora, id_editar))
    
    conexao.commit()
    conexao.close()
    print("✅ Data editada com sucesso!")

def deletar_data():
    listar_datas()
    print("\n--- DELETAR COMPROMISSO ---")
    id_data = input("Digite o ID do compromisso que deseja APAGAR: ")
    
    conexao = sqlite3.connect("agenda.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM contatos WHERE id = ?", (id_data,))
    
    conexao.commit()
    conexao.close()
    print(f" ✅ Compromisso ID {id_data} deletado com sucesso!")

criar_banco()

while True:
    print("\n=== AGENDA ===")
    print("1 - Adicionar data")
    print("2 - Deletar data")
    print("3 - Editar data")
    print("4 - Listar datas")
    print("0 - Sair")

    escolha_menu = input("Escolha uma opção: ")

    if escolha_menu == '1':
        add_data()
    elif escolha_menu == '2':
        deletar_data()
    elif escolha_menu == '3':
        editar_data()
    elif escolha_menu == '4':
        listar_datas()
    elif escolha_menu == '0':
        print("Saindo do sistema...")
        break
    else:
        print("Opção inválida!")