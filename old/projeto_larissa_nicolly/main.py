import sqlite3

conexao = sqlite3.connect("cafeteria.db")

cursor = conexao.cursor()

cursor.execute("""
INSERT INTO Usuarios (usuario, senha, tipo)
VALUES (?, ?, ?)
""", ("amelie", "1234", "admin"))

conexao.commit()

print("=== LOGIN CAFÉ AMÉLIE ===")

usuario = input("Usuário: ")
senha = input("Senha: ")

cursor.execute("""
SELECT * FROM Usuarios
WHERE usuario = ? AND senha = ?
""", (usuario, senha))

login = cursor.fetchone()

if login:
    print("\nLogin realizado com sucesso!")

    if login[3] == "admin":
        print("\n=== ÁREA DO DONO ===")
        print("1 - Ver produtos")
        print("2 - Ver estoque")
        print("3 - Ver vendas")

opcao = input("\nEscolha uma opção: ")

while True:

    print("\n1 - Ver produtos")
    print("2 - Ver estoque")
    print("3 - Ver vendas")
    print("4 - Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":

        cursor.execute("SELECT * FROM Produtos")

        produtos = cursor.fetchall()

        print("\n=== PRODUTOS ===")

        for produto in produtos:
            print(produto)

    elif opcao == "2":

        print("\n=== ESTOQUE ===")

        cursor.execute("SELECT nome, estoque FROM Produtos")

        estoque = cursor.fetchall()

        for item in estoque:
            print(item)

    elif opcao == "3":

        print("\n=== VENDAS ===")
        print("Sistema de vendas em desenvolvimento...")

    elif opcao == "4":

        print("\nSaindo do sistema...")
        break

    else:
        print("\nOpção inválida!")

else:
    print("\nUsuário ou senha incorretos.")

conexao.close()