import pygame
import random

# --- Configurações Iniciais ---
# Inicia o Pygame
pygame.init()

# Define as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 128, 0)
CINZA_CLARO = (200, 200, 200)

# Define o tamanho da tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo 21 (Blackjack)")

# --- Classes do Jogo ---

class Carta:
    """Representa uma carta individual."""
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe

    def __str__(self):
        return f"{self.valor} de {self.naipe}"

class Baralho:
    """Representa um baralho de cartas."""
    def __init__(self):
        self.cartas = []
        self.criar_baralho()
        self.embaralhar()

    def criar_baralho(self):
        """Cria um baralho completo com 52 cartas."""
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        naipes = ['Copas', 'Espadas', 'Ouros', 'Paus']
        for naipe in naipes:
            for valor in valores:
                self.cartas.append(Carta(valor, naipe))

    def embaralhar(self):
        """Embaralha as cartas do baralho."""
        random.shuffle(self.cartas)

    def distribuir(self):
        """Remove e retorna uma carta do topo do baralho."""
        if not self.cartas:
            # Se o baralho estiver vazio, cria e embaralha um novo
            self.criar_baralho()
            self.embaralhar()
        return self.cartas.pop()

class Mao:
    """Representa a mão de cartas de um jogador ou do dealer."""
    def __init__(self):
        self.cartas = []
        self.valor = 0
        self.ases = 0 # Contar ases para ajustar o valor

    def adicionar_carta(self, carta):
        """Adiciona uma carta à mão e calcula o valor."""
        self.cartas.append(carta)
        # Calcula o valor da carta
        if carta.valor.isdigit():
            self.valor += int(carta.valor)
        elif carta.valor in ['J', 'Q', 'K']:
            self.valor += 10
        elif carta.valor == 'A':
            self.valor += 11
            self.ases += 1

        # Ajusta o valor se a mão ultrapassar 21 e tiver ases
        while self.valor > 21 and self.ases:
            self.valor -= 10
            self.ases -= 1
    
    def __str__(self):
        """Representação em texto da mão."""
        return ", ".join([str(carta) for carta in self.cartas])

# --- Funções de Desenho ---

def desenhar_texto(texto, tamanho, cor, x, y):
    """Função para desenhar texto na tela."""
    fonte = pygame.font.Font(None, tamanho)
    superficie_texto = fonte.render(texto, True, cor)
    retangulo_texto = superficie_texto.get_rect(center=(x, y))
    tela.blit(superficie_texto, retangulo_texto)

def desenhar_cartas(mao, y_posicao, esconder_primeira=False):
    """Desenha as cartas de uma mão na tela."""
    x_posicao = 150
    for i, carta in enumerate(mao.cartas):
        if i == 0 and esconder_primeira:
            # Desenha a "costa" da carta para o dealer
            pygame.draw.rect(tela, PRETO, (x_posicao, y_posicao, 100, 150), 0, 5)
            pygame.draw.rect(tela, VERDE, (x_posicao + 5, y_posicao + 5, 90, 140), 0, 5)
        else:
            # Desenha a "frente" da carta
            pygame.draw.rect(tela, BRANCO, (x_posicao, y_posicao, 100, 150), 0, 5)
            desenhar_texto(str(carta.valor), 30, PRETO, x_posicao + 50, y_posicao + 40)
            desenhar_texto(str(carta.naipe), 20, PRETO, x_posicao + 50, y_posicao + 80)
        x_posicao += 120

def desenhar_botoes(estado_jogo):
    """Desenha os botões Pedir Carta e Manter."""
    global botao_pedir, botao_manter
    fonte = pygame.font.Font(None, 40)

    # Botão "Pedir Carta"
    cor_pedir = CINZA_CLARO if estado_jogo == "jogando" else (150, 150, 150)
    botao_pedir = pygame.Rect(LARGURA_TELA / 2 - 160, ALTURA_TELA - 100, 150, 50)
    pygame.draw.rect(tela, cor_pedir, botao_pedir, 0, 10)
    desenhar_texto("Pedir Carta", 30, PRETO, LARGURA_TELA / 2 - 85, ALTURA_TELA - 75)

    # Botão "Manter"
    cor_manter = CINZA_CLARO if estado_jogo == "jogando" else (150, 150, 150)
    botao_manter = pygame.Rect(LARGURA_TELA / 2 + 10, ALTURA_TELA - 100, 150, 50)
    pygame.draw.rect(tela, cor_manter, botao_manter, 0, 10)
    desenhar_texto("Manter", 30, PRETO, LARGURA_TELA / 2 + 85, ALTURA_TELA - 75)

# --- Loop Principal do Jogo ---
def iniciar_jogo():
    """Reinicia o estado do jogo para uma nova rodada."""
    global baralho, mao_jogador, mao_dealer, estado_jogo, mensagem_vitoria
    baralho = Baralho()
    mao_jogador = Mao()
    mao_dealer = Mao()
    estado_jogo = "jogando" # pode ser "jogando", "vitoria", "derrota", "empate"
    mensagem_vitoria = ""

    # Distribui as cartas iniciais
    mao_jogador.adicionar_carta(baralho.distribuir())
    mao_dealer.adicionar_carta(baralho.distribuir())
    mao_jogador.adicionar_carta(baralho.distribuir())
    mao_dealer.adicionar_carta(baralho.distribuir())
    
    # Checa por Blackjack inicial
    if mao_jogador.valor == 21:
        estado_jogo = "manter" # Faz o jogador "manter" se tiver blackjack

iniciar_jogo()

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_pos = evento.pos
            # Lógica dos botões
            if estado_jogo == "jogando":
                if botao_pedir.collidepoint(mouse_pos):
                    # Lógica para "Pedir Carta"
                    mao_jogador.adicionar_carta(baralho.distribuir())
                    if mao_jogador.valor > 21:
                        estado_jogo = "manter" # Passa a vez para o dealer, mesmo que estourou
                
                if botao_manter.collidepoint(mouse_pos):
                    # Lógica para "Manter"
                    estado_jogo = "manter"

    # Lógica do dealer após o jogador "manter" ou "estourar"
    if estado_jogo == "manter":
        # Dealer revela sua carta e joga
        while mao_dealer.valor < 17:
            mao_dealer.adicionar_carta(baralho.distribuir())
        
        # Determina o resultado
        if mao_jogador.valor > 21:
            mensagem_vitoria = "Você estourou! O Dealer vence."
        elif mao_dealer.valor > 21:
            mensagem_vitoria = "O Dealer estourou! Você vence."
        elif mao_jogador.valor > mao_dealer.valor:
            mensagem_vitoria = "Você vence!"
        elif mao_jogador.valor < mao_dealer.valor:
            mensagem_vitoria = "Você perdeu! O Dealer vence."
        else:
            mensagem_vitoria = "Empate!"
        
        # Mudar o estado para "jogo_finalizado" para poder reiniciar
        estado_jogo = "jogo_finalizado"

    # --- Desenho na Tela ---
    tela.fill(VERDE) # Cor de fundo da mesa de jogo

    # Desenha a mão do Dealer
    desenhar_texto("Dealer", 35, BRANCO, 100, 50)
    desenhar_cartas(mao_dealer, 70, esconder_primeira=(estado_jogo != "jogo_finalizado"))
    if estado_jogo == "jogo_finalizado":
        desenhar_texto(f"Valor do Dealer: {mao_dealer.valor}", 30, BRANCO, LARGURA_TELA/2, 250)

    # Desenha a mão do Jogador
    desenhar_texto("Jogador", 35, BRANCO, 100, 300)
    desenhar_cartas(mao_jogador, 320)
    desenhar_texto(f"Sua Pontuação: {mao_jogador.valor}", 30, BRANCO, LARGURA_TELA/2, 500)
    
    # Desenha a mensagem de vitória/derrota
    if estado_jogo == "jogo_finalizado":
        desenhar_texto(mensagem_vitoria, 50, BRANCO, LARGURA_TELA/2, ALTURA_TELA/2)
        desenhar_texto("Clique para jogar novamente", 30, BRANCO, LARGURA_TELA/2, ALTURA_TELA/2 + 50)
        
        # Espera por um clique do mouse para reiniciar
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                iniciar_jogo()
                
    else:
        # Desenha os botões de ação enquanto o jogo está em andamento
        desenhar_botoes(estado_jogo)

    pygame.display.flip()

pygame.quit()