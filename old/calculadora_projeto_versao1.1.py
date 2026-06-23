"""
Exemplo simple de calculadora usado python e sendo exibido por pyinstaller
"""

# --- Documentação do Código ---
# Este programa é uma calculadora simples que realiza as quatro operações básicas.
# Ele foi projetado para ser didático, mostrando como interagir com o usuário,
# usar condicionais e lidar com erros básicos.

def calculadora():

    #Função principal da calculadora.
    #Gerencia a entrada de dados, a operação e a exibição do resultado.

    print("--- Calculadora Simples em Python ---")
    print("Bem-vindo(a! Escolha uma operação:")
    print("1. Adição      (+)")
    print("2. Subtração   (-)")
    print("3. Multiplicação(*)")
    print("4. Divisão     (/)")
    print("-----------------------------------")

    # Loop para garantir que o usuário escolha uma operação válida
    while True:
        escolha = input("Digite o número da operação (1/2/3/4): ")

        if escolha in ('1', '2', '3', '4'):
            break # Sai do loop se a escolha for válida
        else:
            print("Opção inválida. Por favor, digite 1, 2, 3 ou 4.")

    # Loop para garantir que os números inseridos são válidos
    while True:
        try:
            num1 = float(input("Digite o primeiro número: "))
            num2 = float(input("Digite o segundo número: "))
            break # Sai do loop se os números forem válidos
        except ValueError:
            print("Entrada inválida. Por favor, digite apenas números.")

    # Realiza a operação baseada na escolha do usuário
    if escolha == '1':
        resultado = num1 + num2
        print(f"O resultado da adição é: {resultado}")
    elif escolha == '2':
        resultado = num1 - num2
        print(f"O resultado da subtração é: {resultado}")
    elif escolha == '3':
        resultado = num1 * num2
        print(f"O resultado da multiplicação é: {resultado}")
    elif escolha == '4':
        # Tratamento especial para divisão por zero
        if num2 == 0:
            print("Erro: Não é possível dividir por zero!")
        else:
            resultado = num1 / num2
            print(f"O resultado da divisão é: {resultado}")

# Chama a função da calculadora para iniciar o programa
calculadora()

