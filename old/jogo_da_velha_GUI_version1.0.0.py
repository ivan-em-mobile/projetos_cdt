import tkinter as tk
from tkinter import messagebox

# --- CONFIGURAÇÕES DE ESTILO RETRO ---
COR_FUNDO = 'black'
COR_TEXTO_PADRAO = '#00FF00'  # Verde brilhante (como um monitor de fósforo)
COR_X = '#FF0000'           # Vermelho para 'X'
COR_O = '#00FFFF'           # Ciano para 'O'
FONTE_RETRO = ('Courier', 20, 'bold') # Fonte monoespaçada para simular terminal

# --- Lógica do Jogo ---

class JogoDaVelhaRetro:
    def __init__(self, master):
        self.master = master
        master.title("TIC-TAC-TOE [RETRO MODE]")
        master.config(bg=COR_FUNDO) # Define o fundo da janela como preto
        
        self.tabuleiro_logico = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.jogador_atual = "X"
        self.rodada = 0
        self.botoes = []
        
        # 1. Cria a interface do placar e status (Retro Style)
        self.label_status = tk.Label(master, 
                                     text=f"[STATUS] VEZ DO JOGADOR: {self.jogador_atual}", 
                                     font=FONTE_RETRO, 
                                     bg=COR_FUNDO, 
                                     fg=COR_TEXTO_PADRAO)
        self.label_status.grid(row=0, column=0, columnspan=3, pady=7)

        # 2. Cria os Botões do Tabuleiro
        self.criar_botoes()
        
        # 3. Cria o botão de Novo Jogo (uma boa prática em GUIs)
        self.botao_reiniciar = tk.Button(master, 
                                         text="[REINICIAR JOGO]", 
                                         font=FONTE_RETRO, 
                                         bg=COR_TEXTO_PADRAO, 
                                         fg=COR_FUNDO, 
                                         command=self.reiniciar_jogo)
        self.botao_reiniciar.grid(row=4, column=0, columnspan=3, pady=20)


    def criar_botoes(self):
        """Cria e posiciona os 9 botões do tabuleiro com estilo retro."""
        for linha in range(3):
            linha_botoes = []
            for coluna in range(3):
                botao = tk.Button(self.master, 
                                   text="", 
                                   font=('Courier', 35, 'bold'), # Fonte maior para os símbolos
                                   width=4, 
                                   height=2,
                                   bg=COR_FUNDO,
                                   fg=COR_TEXTO_PADRAO,
                                   relief=tk.RAISED, # Borda levantada/3D para visual retro
                                   bd=5, # Espessura da borda
                                   command=lambda r=linha, c=coluna: self.fazer_jogada(r, c))
                
                # Posiciona o botão (linhas 1, 2, 3 do grid)
                botao.grid(row=linha + 1, column=coluna, sticky="nsew", padx=2, pady=2)
                linha_botoes.append(botao)
            self.botoes.append(linha_botoes)

    def verificar_vitoria(self, tab, jogador):
        """Verifica se o jogador atual venceu o jogo (lógica original)."""
        # (Lógica mantida do código anterior)
        # Verifica Linhas, Colunas, Diagonais Principal e Secundária
        for r in range(3):
            if all(tab[r][c] == jogador for c in range(3)): return True # Linhas
            if all(tab[c][r] == jogador for c in range(3)): return True # Colunas
        if all(tab[i][i] == jogador for i in range(3)): return True # Diagonal Principal
        if all(tab[i][2 - i] == jogador for i in range(3)): return True # Diagonal Secundária
        return False

    def fazer_jogada(self, linha, coluna):
        """Processa a jogada do jogador."""
        if self.tabuleiro_logico[linha][coluna] == "":
            
            # 1. Atualiza o tabuleiro lógico e visual
            self.tabuleiro_logico[linha][coluna] = self.jogador_atual
            
            cor_simbolo = COR_X if self.jogador_atual == 'X' else COR_O
            
            self.botoes[linha][coluna].config(text=self.jogador_atual, 
                                              state=tk.DISABLED, 
                                              fg=cor_simbolo) # Cor do símbolo
            self.rodada += 1

            # 2. Verifica a Vitória
            if self.verificar_vitoria(self.tabuleiro_logico, self.jogador_atual):
                self.label_status.config(text=f"[VENCEDOR] JOGADOR {self.jogador_atual} GANHOU!", fg='yellow')
                self.desabilitar_todos_botoes()
                return

            # 3. Verifica o Empate
            if self.rodada == 9:
                self.label_status.config(text="[FIM] JOGO EMPATADO!", fg='orange')
                return

            # 4. Alterna o Jogador
            self.jogador_atual = "O" if self.jogador_atual == "X" else "X"
            self.label_status.config(text=f"[STATUS] VEZ DO JOGADOR: {self.jogador_atual}", fg=COR_TEXTO_PADRAO)

    def desabilitar_todos_botoes(self):
        """Desabilita os botões após o fim do jogo."""
        for linha in self.botoes:
            for botao in linha:
                botao.config(state=tk.DISABLED)
                
    def reiniciar_jogo(self):
        """Reinicia o estado do jogo e a interface."""
        # Reinicia as variáveis lógicas
        self.tabuleiro_logico = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.jogador_atual = "X"
        self.rodada = 0
        
        # Reinicia a interface dos botões
        for linha in range(3):
            for coluna in range(3):
                self.botoes[linha][coluna].config(text="", 
                                                  state=tk.NORMAL, # Reabilita o botão
                                                  fg=COR_TEXTO_PADRAO) # Reseta a cor
                                                  
        # Reinicia o status
        self.label_status.config(text=f"[STATUS] VEZ DO JOGADOR: {self.jogador_atual}", fg=COR_TEXTO_PADRAO)


# --- Inicialização da Aplicação ---
if __name__ == "__main__":
    root = tk.Tk()
    app = JogoDaVelhaRetro(root)
    root.mainloop()