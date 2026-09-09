"""
pip install pygame, será necessario a instalação do pygame para o funcionamento do jogo.
"""

import pygame
import random

pygame.init()
tela = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Game Snake Run')

# corpo_cobra = [(100, 100), (90, 100), (80, 100)]
corpo_cobra = [(100, 50)]
# direcao = 'RIGHT'
direcao = (10, 0)

comida = (300, 200)

def desenhar():

    tela.fill((0, 0, 0))

    for parte in corpo_cobra:

        pygame.draw.rect(tela, (0, 255, 0), (*parte, 10, 10))

    pygame.draw.rect(tela, (255, 0, 0), (*comida, 10, 10))

    #pygame.display.flip()
    pygame.display.update()

rodando = True

relogio = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and direcao != (0, 10):
                direcao = (0, -10)
            elif evento.key == pygame.K_DOWN and direcao != (0, -10):
                direcao = (0, 10)
            elif evento.key == pygame.K_LEFT and direcao != (10, 0):
                direcao = (-10, 0)
            elif evento.key == pygame.K_RIGHT and direcao != (-10, 0):
                direcao = (10, 0)

    nova_cabeca = (corpo_cobra[0][0] + direcao[0], corpo_cobra[0][1] + direcao[1])
    corpo_cobra.insert(0, nova_cabeca)

    if nova_cabeca == comida:
        # comida = (random.randint(0, 60) * 10, random.randint(0, 40) * 10)

        comida = (random.randrange(0, 59) * 10, random.randrange(0, 39) * 10)
    else:
        corpo_cobra.pop()

    if nova_cabeca in corpo_cobra[1:]:
        rodando = False

    if nova_cabeca[0] < 0 or nova_cabeca[0] >= 600 or nova_cabeca[1] < 0 or nova_cabeca[1] >= 400:
        rodando = False

    desenhar()
    relogio.tick(15)

pygame.quit()