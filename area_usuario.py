"""Tela exibida após o login bem-sucedido."""
import pygame
from configuracoes import tela, FUNDO, BRANCO, VERDE, fonte_titulo, fonte_texto
from interface import botao, desenhar_centralizado, encerrar

def tela_principal_usuario(nome):
    while True:
        mouse = pygame.mouse.get_pos()
        botao_sair = pygame.Rect(330, 360, 240, 50)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_sair.collidepoint(evento.pos):
                    return

        tela.fill(FUNDO)
        desenhar_centralizado(f"OLÁ, {nome.upper()}!", fonte_titulo, BRANCO, 145)
        desenhar_centralizado("Login realizado com sucesso.", fonte_texto, VERDE, 235)
        botao("VOLTAR AO MENU", botao_sair, mouse)
        pygame.display.flip()
