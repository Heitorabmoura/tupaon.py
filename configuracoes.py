"""Configurações gerais e recursos compartilhados do Tupã."""
import pygame

pygame.init()

LARGURA = 900
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tupã")

FUNDO = (30, 30, 30)
BRANCO = (255, 255, 255)
VERMELHO = (150, 30, 30)
VERMELHO_CLARO = (200, 50, 50)
VERDE = (50, 160, 70)
CINZA = (90, 90, 90)
CINZA_CLARO = (190, 190, 190)

fonte_titulo = pygame.font.Font(None, 62)
fonte_texto = pygame.font.Font(None, 32)
fonte_pequena = pygame.font.Font(None, 25)
fonte_menor = pygame.font.Font(None, 21)
