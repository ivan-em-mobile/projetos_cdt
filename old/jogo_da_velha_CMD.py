# --- Documentação do Código ---
# Este programa implementa o clássico jogo da velha (Tic-Tac-Toe) para dois jogadores.
# Ele demonstra como usar listas para representar um tabuleiro, funções para organizar
# o código, loops para o fluxo do jogo e condicionais para verificar vitórias e empates.

def exibir_tabuleiro(tabuleiro):
    """
    Exibe o tabuleiro do jogo no terminal.
    O tabuleiro é uma lista de 9 elementos, representando as posições.
    """
    print("\n")
    print(f" {tabuleiro[0]} | {tabuleiro[1]} | {tabuleiro[2]} ")
    print("---|---|---")
    print(f" {tabuleiro[3]} | {tabuleiro[4]} | {tabuleiro[5]} ")
    print("---|---|---")
    print(f" {tabuleiro[6]} | {tabuleiro[7]} | {tabuleiro[8]} ")
    print("\n")

def verificar_vitoria(tabuleiro, jogador):
    """
    Verifica se o jogador atual venceu.
    Checa todas as combinações possíveis de vitória (linhas, colunas, diagonais).
    """
    # Combinações de vitória (índices das posições no tabuleiro)
    vitorias = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6]              # Diagonais
    ]
    for combo in vitorias:
        if all(tabuleiro[i] == jogador for i in combo):
            return True
    return False

def verificar_empate(tabuleiro):
    """
    Verifica se o jogo terminou em empate.
    Isso ocorre se todas as posições estiverem preenchidas e não houver um vencedor.
    """
    # Se não houver '_' (posição vazia) no tabuleiro, significa que está cheio
    return '_' not in tabuleiro

def jogar_tic_tac_toe():
    """
    Função principal do jogo da velha.
    Gerencia o fluxo do jogo, turnos, entradas e verificação de condições de fim de jogo.
    """
    print("--- Bem-vindo ao Jogo da Velha! ---")
    
    while True: # Loop principal para jogar múltiplas partidas
        # Inicializa o tabuleiro com posições vazias
        # As posições são de 0 a 8, correspondendo a:
        # 0 | 1 | 2
        #---|---|---
        # 3 | 4 | 5
        #---|---|---
        # 6 | 7 | 8
        tabuleiro = ['_' for _ in range(9)]
        jogador_atual = 'X' # 'X' sempre começa
        jogo_ativo = True

        print("As posições são numeradas de 0 a 8:")
        exibir_tabuleiro(['0', '1', '2', '3', '4', '5', '6', '7', '8']) # Mostra os números das posições

        while jogo_ativo:
            exibir_tabuleiro(tabuleiro)
            print(f"Vez do jogador {jogador_atual}")

            # Loop para garantir uma jogada válida
            while True:
                try:
                    posicao = int(input("Escolha uma posição (0-8): "))
                    if 0 <= posicao <= 8 and tabuleiro[posicao] == '_':
                        break # Posição válida e vazia
                    elif not (0 <= posicao <= 8):
                        print("Posição inválida. Digite um número entre 0 e 8.")
                    else:
                        print("Essa posição já está ocupada. Escolha outra.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")

            tabuleiro[posicao] = jogador_atual # Marca a posição com o símbolo do jogador

            # Verifica se o jogador atual venceu
            if verificar_vitoria(tabuleiro, jogador_atual):
                exibir_tabuleiro(tabuleiro)
                print(f"Parabéns! O jogador {jogador_atual} venceu!")
                jogo_ativo = False
            # Verifica se houve empate
            elif verificar_empate(tabuleiro):
                exibir_tabuleiro(tabuleiro)
                print("O jogo terminou em empate!")
                jogo_ativo = False
            else:
                # Troca de jogador para o próximo turno
                jogador_atual = 'O' if jogador_atual == 'X' else 'X'
        
        # Pergunta se os jogadores querem jogar novamente
        while True:
            jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower()
            if jogar_novamente in ('s', 'n'):
                break
            else:
                print("Opção inválida. Digite 's' para sim ou 'n' para não.")
        
        if jogar_novamente == 'n':
            print("Obrigado por jogar! Até a próxima!")
            break # Sai do loop principal, encerrando o programa

# Chama a função principal para iniciar o jogo
jogar_tic_tac_toe()