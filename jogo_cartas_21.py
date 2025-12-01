import pygame
import random
import os
import sys

# --- Funções de Ajuda de Caminho (Para PyInstaller, opcional) ---
def resolver_caminho_recurso(caminho_relativo):
    """Garante que o caminho do recurso funciona como script ou empacotado."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, caminho_relativo)

# --- Configurações Iniciais ---
pygame.init()

# Define as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 128, 0)
CINZA_CLARO = (200, 200, 200)
AMARELO = (255, 255, 0) 
PRETO_TRANSPARENTE = (0, 0, 0, 150) # Usado para escurecer a tela no final do jogo

# Define o tamanho da tela
LARGURA_TELA = 920
ALTURA_TELA = 620
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo 21 (Blackjack)")

# Variáveis globais dos botões (serão definidas em desenhar_botoes)
botao_pedir = pygame.Rect(0, 0, 0, 0)
botao_manter = pygame.Rect(0, 0, 0, 0)

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
        naipes = ['♥', '♠', '♦', '♣']
        for naipe in naipes:
            for valor in valores:
                self.cartas.append(Carta(valor, naipe))

    def embaralhar(self):
        """Embaralha as cartas do baralho."""
        random.shuffle(self.cartas)

    def distribuir(self):
        """Remove e retorna uma carta do topo do baralho."""
        if not self.cartas:
            self.criar_baralho()
            self.embaralhar()
        return self.cartas.pop()

class Mao:
    """Representa a mão de cartas de um jogador ou do dealer."""
    def __init__(self):
        self.cartas = []
        self.valor = 0
        self.ases = 0 

    def adicionar_carta(self, carta):
        """Adiciona uma carta à mão e calcula o valor."""
        self.cartas.append(carta)
        
        if carta.valor.isdigit():
            self.valor += int(carta.valor)
        elif carta.valor in ['J', 'Q', 'K']:
            self.valor += 10
        elif carta.valor == 'A':
            self.valor += 11
            self.ases += 1

        while self.valor > 21 and self.ases:
            self.valor -= 10
            self.ases -= 1
    
    def __str__(self):
        """Representação em texto da mão."""
        return ", ".join([str(carta) for carta in self.cartas])

# --- Funções de Desenho ---

def desenhar_texto(texto, tamanho, cor, x, y):
    """
    Função para desenhar texto na tela. 
    CORREÇÃO APLICADA: Tenta usar SysFont para garantir suporte a Unicode (naipes).
    """
    # Tenta carregar uma fonte do sistema que suporta Unicode (ex: Arial)
    try:
        fonte = pygame.font.SysFont('arial', tamanho)
    except:
        # Se a fonte do sistema falhar, volta para a fonte padrão do Pygame
        fonte = pygame.font.Font(None, tamanho) 
        
    superficie_texto = fonte.render(texto, True, cor)
    retangulo_texto = superficie_texto.get_rect(center=(x, y))
    tela.blit(superficie_texto, retangulo_texto)

def desenhar_cartas(mao, y_posicao, esconder_primeira=False):
    """Desenha as cartas de uma mão na tela, centralizando-as."""
    largura_carta = 100
    espaco_entre_cartas = 20
    
    largura_total_cartas = len(mao.cartas) * largura_carta + (len(mao.cartas) - 1) * espaco_entre_cartas
    x_posicao_inicial = (LARGURA_TELA - largura_total_cartas) / 2
    
    for i, carta in enumerate(mao.cartas):
        x_posicao = x_posicao_inicial + i * (largura_carta + espaco_entre_cartas)
        rect_carta = pygame.Rect(x_posicao, y_posicao, largura_carta, 150)
        
        if i == 0 and esconder_primeira:
            # Desenha a "costa" da carta para o dealer
            pygame.draw.rect(tela, PRETO, rect_carta, 0, 5)
            pygame.draw.rect(tela, VERDE, (x_posicao + 5, y_posicao + 5, 90, 140), 0, 5)
        else:
            # Desenha a "frente" da carta
            pygame.draw.rect(tela, BRANCO, rect_carta, 0, 5)
            cor_naipe = PRETO
            if carta.naipe in ['♥', '♦']:
                cor_naipe = (255, 0, 0)
            
            # Desenha o VALOR 
            desenhar_texto(str(carta.valor), 30, cor_naipe, x_posicao + 50, y_posicao + 40)
            
            # Desenha o NAIPE (Tamanho da fonte 45)
            desenhar_texto(str(carta.naipe), 45, cor_naipe, x_posicao + 50, y_posicao + 80) 

def desenhar_botoes(estado_jogo):
    """Desenha os botões Pedir Carta e Manter e define seus Rects globais."""
    global botao_pedir, botao_manter
    
    cor_pedir = CINZA_CLARO if estado_jogo == "jogando" else (150, 150, 150)
    botao_pedir = pygame.Rect(LARGURA_TELA / 2 - 160, ALTURA_TELA - 100, 150, 50)
    pygame.draw.rect(tela, cor_pedir, botao_pedir, 0, 10)
    desenhar_texto("Pedir Carta", 30, PRETO, LARGURA_TELA / 2 - 85, ALTURA_TELA - 75)

    cor_manter = CINZA_CLARO if estado_jogo == "jogando" else (150, 150, 150)
    botao_manter = pygame.Rect(LARGURA_TELA / 2 + 10, ALTURA_TELA - 100, 150, 50)
    pygame.draw.rect(tela, cor_manter, botao_manter, 0, 10)
    desenhar_texto("Manter", 30, PRETO, LARGURA_TELA / 2 + 85, ALTURA_TELA - 75)

# --- Funções de Controle do Jogo ---
def iniciar_jogo():
    """Reinicia o estado do jogo para uma nova rodada."""
    global baralho, mao_jogador, mao_dealer, estado_jogo, mensagem_vitoria
    baralho = Baralho()
    mao_jogador = Mao()
    mao_dealer = Mao()
    estado_jogo = "jogando" 
    mensagem_vitoria = ""

    mao_jogador.adicionar_carta(baralho.distribuir())
    mao_dealer.adicionar_carta(baralho.distribuir())
    mao_jogador.adicionar_carta(baralho.distribuir())
    mao_dealer.adicionar_carta(baralho.distribuir())
    
    if mao_jogador.valor == 21:
        estado_jogo = "manter" 

# --- Loop Principal do Jogo ---
iniciar_jogo()

rodando = True
while rodando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_pos = evento.pos
            
            if estado_jogo == "jogando":
                if botao_pedir.collidepoint(mouse_pos):
                    mao_jogador.adicionar_carta(baralho.distribuir())
                    if mao_jogador.valor > 21:
                        estado_jogo = "manter" 
                
                elif botao_manter.collidepoint(mouse_pos):
                    estado_jogo = "manter"
            
            elif estado_jogo == "jogo_finalizado":
                iniciar_jogo()
                
    if estado_jogo == "manter":
        
        if mao_jogador.valor <= 21:
            while mao_dealer.valor < 17:
                mao_dealer.adicionar_carta(baralho.distribuir())
        
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
        
        estado_jogo = "jogo_finalizado" 

    # --- Desenho na Tela ---
    tela.fill(VERDE) 

    desenhar_texto("Dealer", 35, BRANCO, LARGURA_TELA/2, 50)
    desenhar_cartas(mao_dealer, 70, esconder_primeira=(estado_jogo != "jogo_finalizado"))
    
    # desenhar_texto("Jogador", 35, BRANCO, LARGURA_TELA/2, 300)
    desenhar_texto("Jogador", 35, BRANCO, LARGURA_TELA/2, 295)
    desenhar_cartas(mao_jogador, 320)
    desenhar_texto(f"Sua Pontuação: {mao_jogador.valor}", 30, BRANCO, LARGURA_TELA/2, 500)

    # Lógica de exibição final (MENSAGEM, ESCURECIMENTO E REINÍCIO)
    if estado_jogo == "jogo_finalizado":
        # Desenha o fundo escurecido
        s = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA) 
        s.fill(PRETO_TRANSPARENTE) 
        tela.blit(s, (0,0)) 

        desenhar_texto(f"Valor do Dealer: {mao_dealer.valor}", 30, BRANCO, LARGURA_TELA/2, 250)
        
        desenhar_texto(mensagem_vitoria, 50, AMARELO, LARGURA_TELA/2, ALTURA_TELA/2 + 50) 
        desenhar_texto("Clique para jogar novamente", 30, BRANCO, LARGURA_TELA/2, ALTURA_TELA/2 + 100) 
        
    else:
        desenhar_botoes(estado_jogo)

    pygame.display.flip()

pygame.quit()