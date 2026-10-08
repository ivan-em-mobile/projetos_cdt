from datetime import datetime
import msvcrt


# ==========================================================
# FUNÇÃO PARA DIGITAR SENHA OCULTA COM ****
# ==========================================================

def senha_oculta(mensagem="Senha: "):
    print(mensagem, end="", flush=True)
    senha = ""

    while True:
        tecla = msvcrt.getch()

        # ENTER
        if tecla in (b"\r", b"\n"):
            print()
            break

        # BACKSPACE
        elif tecla == b"\x08":
            if senha:
                senha = senha[:-1]
                print("\b \b", end="", flush=True)

        # Teclas especiais
        elif tecla in (b"\x00", b"\xe0"):
            msvcrt.getch()

        # Caracteres normais
        else:
            try:
                caractere = tecla.decode("utf-8")
                senha += caractere
                print("*", end="", flush=True)
            except UnicodeDecodeError:
                pass

    return senha


# ==========================================================
# BANCO DE USUÁRIOS
# ==========================================================

usuarios = {
    "admin@email.com": {
        "nome": "Administrador",
        "senha": "1234"
    }
}


# ==========================================================
# CARDÁPIO
# ==========================================================

hamburgueres = {
    1: ("X-Burguer", 15.00),
    2: ("X-Salada", 18.00),
    3: ("X-Bacon", 22.00),
    4: ("X-Tudo", 27.00),
    5: ("Duplo Bacon", 30.00),
    6: ("Cheddar Burger", 25.00),
    7: ("Chicken Burger", 23.00),
    8: ("Monster Burger", 35.00)
}

bebidas = {
    1: ("Coca-Cola Lata", 6.00),
    2: ("Guaraná Lata", 5.00),
    3: ("Fanta Laranja", 5.00),
    4: ("Sprite Lata", 5.00),
    5: ("Suco de Laranja", 8.00),
    6: ("Suco de Maracujá", 8.00),
    7: ("Suco de Morango", 9.00),
    8: ("Água Mineral", 3.00)
}


# ==========================================================
# FUNÇÕES GERAIS
# ==========================================================

def linha():
    print("=" * 55)


def pausar():
    input("\nPressione ENTER para continuar...")


def dinheiro(valor):
    return f"R$ {valor:.2f}".replace(".", ",")


# ==========================================================
# CADASTRAR CONTA
# ==========================================================

def cadastrar():
    linha()
    print("CADASTRO DE CONTA")
    linha()

    nome = input("Digite seu nome: ")

    email = input("Digite seu e-mail: ").lower()

    if email in usuarios:
        print("\nEsse e-mail já está cadastrado!")
        pausar()
        return

    # Senha aparecendo como ****
    senha = senha_oculta("Crie uma senha: ")

    # Confirmação da senha também aparece como ****
    confirmar = senha_oculta("Confirme a senha: ")

    if senha != confirmar:
        print("\nAs senhas não são iguais!")
        pausar()
        return

    usuarios[email] = {
        "nome": nome,
        "senha": senha
    }

    print("\nConta cadastrada com sucesso!")
    pausar()


# ==========================================================
# LOGIN
# ==========================================================

def login():
    linha()
    print("LOGIN")
    linha()

    email = input("E-mail: ").lower()

    # Senha aparece como ****
    senha = senha_oculta("Senha: ")

    if email in usuarios and usuarios[email]["senha"] == senha:
        print("\nLogin realizado com sucesso!")
        print(f"Bem-vindo(a), {usuarios[email]['nome']}!")
        pausar()

        return usuarios[email]

    print("\nE-mail ou senha incorretos!")
    pausar()

    return None


# ==========================================================
# CARDÁPIO DE HAMBÚRGUERES
# ==========================================================

def mostrar_hamburgueres():
    linha()
    print("HAMBÚRGUERES")
    linha()

    for codigo, produto in hamburgueres.items():
        nome, preco = produto

        print(
            f"{codigo} - "
            f"{nome:<25} "
            f"{dinheiro(preco)}"
        )


# ==========================================================
# CARDÁPIO DE BEBIDAS
# ==========================================================

def mostrar_bebidas():
    linha()
    print("BEBIDAS")
    linha()

    for codigo, produto in bebidas.items():
        nome, preco = produto

        print(
            f"{codigo} - "
            f"{nome:<25} "
            f"{dinheiro(preco)}"
        )


# ==========================================================
# ADICIONAR PRODUTO
# ==========================================================

def adicionar_produto(carrinho, produtos, tipo):

    if tipo == "hamburguer":
        mostrar_hamburgueres()
    else:
        mostrar_bebidas()

    try:
        codigo = int(
            input("\nDigite o código do produto: ")
        )

        if codigo not in produtos:
            print("\nProduto inválido!")
            pausar()
            return

        quantidade = int(
            input("Digite a quantidade: ")
        )

        if quantidade <= 0:
            print("\nQuantidade inválida!")
            pausar()
            return

        nome, preco = produtos[codigo]

        carrinho.append({
            "nome": nome,
            "preco": preco,
            "quantidade": quantidade
        })

        print(
            f"\n{quantidade}x {nome} "
            "adicionado ao carrinho!"
        )

    except ValueError:
        print("\nDigite apenas números!")

    pausar()


# ==========================================================
# MOSTRAR CARRINHO
# ==========================================================

def mostrar_carrinho(carrinho):

    linha()
    print("SEU CARRINHO")
    linha()

    if not carrinho:
        print("Seu carrinho está vazio.")
        pausar()
        return 0

    total = 0

    for item in carrinho:

        subtotal = (
            item["preco"] *
            item["quantidade"]
        )

        total += subtotal

        print(
            f"{item['quantidade']}x "
            f"{item['nome']:<25} "
            f"{dinheiro(subtotal)}"
        )

    linha()

    print(
        f"TOTAL: {dinheiro(total)}"
    )

    pausar()

    return total


# ==========================================================
# FINALIZAR COMPRA
# ==========================================================

def finalizar_compra(carrinho, usuario):

    if not carrinho:

        linha()
        print("SEU CARRINHO ESTÁ VAZIO!")
        linha()

        pausar()

        return

    linha()
    print("FINALIZAR COMPRA")
    linha()

    total = 0

    for item in carrinho:

        subtotal = (
            item["preco"] *
            item["quantidade"]
        )

        total += subtotal

        print(
            f"{item['quantidade']}x "
            f"{item['nome']} = "
            f"{dinheiro(subtotal)}"
        )

    linha()

    print(
        f"TOTAL: {dinheiro(total)}"
    )

    print("\nFORMAS DE PAGAMENTO")

    print("1 - Dinheiro")
    print("2 - Pix")
    print("3 - Cartão de Débito")
    print("4 - Cartão de Crédito")

    opcao = input(
        "\nEscolha o pagamento: "
    )

    pagamentos = {
        "1": "Dinheiro",
        "2": "Pix",
        "3": "Cartão de Débito",
        "4": "Cartão de Crédito"
    }

    if opcao not in pagamentos:

        print(
            "\nForma de pagamento inválida!"
        )

        pausar()

        return

    pagamento = pagamentos[opcao]

    print("\n" + "=" * 55)

    print("PEDIDO FINALIZADO!")

    print("=" * 55)

    print(
        f"Cliente: {usuario['nome']}"
    )

    print(
        f"Pagamento: {pagamento}"
    )

    print(
        f"Total: {dinheiro(total)}"
    )

    data = datetime.now()

    print(
        "Data:",
        data.strftime(
            "%d/%m/%Y %H:%M:%S"
        )
    )

    print(
        "\n🍔 Obrigado pela preferência!"
    )

    print(
        "Seu pedido está sendo preparado!"
    )

    # Limpa o carrinho
    carrinho.clear()

    pausar()


# ==========================================================
# MENU DA HAMBURGUERIA
# ==========================================================

def menu_hamburgueria(usuario):

    carrinho = []

    while True:

        print("\n")

        linha()

        print("🍔 HAMBURGUERIA")

        linha()

        print(
            f"Cliente: {usuario['nome']}"
        )

        print("\n1 - Ver hambúrgueres")
        print("2 - Adicionar hambúrguer")
        print("3 - Ver bebidas")
        print("4 - Adicionar bebida")
        print("5 - Ver carrinho")
        print("6 - Finalizar compra")
        print("7 - Sair da conta")

        opcao = input(
            "\nEscolha uma opção: "
        )

        # Ver hambúrgueres
        if opcao == "1":

            mostrar_hamburgueres()

            pausar()

        # Adicionar hambúrguer
        elif opcao == "2":

            adicionar_produto(
                carrinho,
                hamburgueres,
                "hamburguer"
            )

        # Ver bebidas
        elif opcao == "3":

            mostrar_bebidas()

            pausar()

        # Adicionar bebida
        elif opcao == "4":

            adicionar_produto(
                carrinho,
                bebidas,
                "bebida"
            )

        # Ver carrinho
        elif opcao == "5":

            mostrar_carrinho(carrinho)

        # Finalizar compra
        elif opcao == "6":

            finalizar_compra(
                carrinho,
                usuario
            )

        # Sair da conta
        elif opcao == "7":

            print(
                "\nSaindo da conta..."
            )

            pausar()

            break

        else:

            print(
                "\nOpção inválida!"
            )

            pausar()


# ==========================================================
# MENU INICIAL
# ==========================================================

def menu_inicial():

    while True:

        print("\n")

        linha()

        print(
            "🍔 BEM-VINDO À HAMBURGUERIA 🍔"
        )

        linha()

        print("1 - Fazer Login")
        print("2 - Cadastrar Conta")
        print("3 - Sair")

        opcao = input(
            "\nEscolha uma opção: "
        )

        # Login
        if opcao == "1":

            usuario = login()

            if usuario:

                menu_hamburgueria(
                    usuario
                )

        # Cadastro
        elif opcao == "2":

            cadastrar()

        # Sair
        elif opcao == "3":

            print(
                "\nObrigado por utilizar "
                "nosso sistema!"
            )

            print(
                "Até logo! 🍔"
            )

            break

        else:

            print(
                "\nOpção inválida!"
            )

            pausar()


# ==========================================================
# EXECUTAR PROGRAMA
# ==========================================================

if __name__ == "__main__":
    menu_inicial()