# Importa a biblioteca Tkinter, usada para criar interfaces gráficas.
import tkinter as tk
# Importa a caixa de mensagem para exibir mensagens pop-up.
from tkinter import messagebox

# --- Lógica do Jogo ---

# Inicializa as variáveis do jogo.
jogador_atual = "X"
tabuleiro = [["" for _ in range(3)] for _ in range(3)]

def verificar_vitoria(tab, jogador):
    """
    Verifica se o jogador atual venceu o jogo.
    """
    # Verifica todas as linhas
    for i in range(3):
        if all([celula == jogador for celula in tab[i]]):
            return True
            
    # Verifica todas as colunas
    for i in range(3):
        if all([tab[j][i] == jogador for j in range(3)]):
            return True
            
    # Verifica a diagonal principal
    if all([tab[i][i] == jogador for i in range(3)]):
        return True
        
    # Verifica a diagonal secundária
    if all([tab[i][2 - i] == jogador for i in range(3)]):
        return True
        
    return False

def verificar_empate():
    """
    Verifica se o jogo terminou em empate.
    """
    # Retorna True se não houver mais espaços vazios no tabuleiro.
    for linha in tabuleiro:
        if "" in linha:
            return False
    return True

# --- Funções da Interface Gráfica ---

def clique_botao(linha, coluna):
    """
    Função chamada quando um botão é clicado.
    Responsável por processar a jogada.
    """
    global jogador_atual

    # Ação só ocorre se o botão estiver vazio.
    if tabuleiro[linha][coluna] == "":
        # Atualiza a matriz do tabuleiro e o texto do botão.
        tabuleiro[linha][coluna] = jogador_atual
        botoes[linha][coluna]["text"] = jogador_atual
        
        # Verifica se houve um vencedor.
        if verificar_vitoria(tabuleiro, jogador_atual):
            messagebox.showinfo("Fim de Jogo", f"Parabéns! O jogador {jogador_atual} venceu!")
            desabilitar_botoes()
            return
        
        # Verifica se houve um empate.
        if verificar_empate():
            messagebox.showinfo("Fim de Jogo", "Fim do Jogo! Empate!")
            return

        # Alterna o jogador.
        jogador_atual = "O" if jogador_atual == "X" else "X"
        rotulo_status["text"] = f"Vez do jogador: {jogador_atual}"

def reiniciar_jogo():
    """
    Reinicia todas as variáveis e a interface para um novo jogo.
    """
    global jogador_atual
    
    jogador_atual = "X"
    rotulo_status["text"] = f"Vez do jogador: {jogador_atual}"
    
    # Limpa o tabuleiro lógico e os textos dos botões.
    for i in range(3):
        for j in range(3):
            tabuleiro[i][j] = ""
            botoes[i][j]["text"] = ""
            botoes[i][j]["state"] = "normal"

def desabilitar_botoes():
    """
    Desabilita todos os botões após o fim do jogo.
    """
    for i in range(3):
        for j in range(3):
            botoes[i][j]["state"] = "disabled"

# --- Configuração da Janela Principal ---

# Cria a janela principal do Tkinter.
janela = tk.Tk()
janela.title("Jogo da Velha")

# Define o rótulo de status.
rotulo_status = tk.Label(janela, text=f"Vez do jogador: {jogador_atual}", font=("Arial", 16))
rotulo_status.grid(row=0, column=0, columnspan=3, pady=10)

# Cria e posiciona os botões do tabuleiro.
botoes = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        # Cria um botão para cada posição do tabuleiro.
        # Usa uma função lambda para passar os argumentos (i e j) para clique_botao.
        botao = tk.Button(janela, text="", font=("Arial", 30), width=5, height=2,
                          command=lambda i=i, j=j: clique_botao(i, j))
        botao.grid(row=i+1, column=j, padx=5, pady=5)
        botoes[i][j] = botao

# Cria o botão de reiniciar o jogo.
botao_reiniciar = tk.Button(janela, text="Reiniciar Jogo", font=("Arial", 12), command=reiniciar_jogo)
botao_reiniciar.grid(row=4, column=0, columnspan=3, pady=10)

# Inicia o loop principal do Tkinter.
janela.mainloop()