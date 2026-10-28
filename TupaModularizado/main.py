"""Ponto de entrada e menu principal do Tupã."""
import pygame
from configuracoes import (
    tela, FUNDO, BRANCO, CINZA, CINZA_CLARO, fonte_titulo, fonte_pequena, fonte_menor
)
from interface import botao, desenhar_centralizado, encerrar
from cadastro import tela_cadastro
from login import tela_login
from pesquisas import tela_pesquisas
from quiz import tela_quiz

def menu_principal():
    botoes = {
        "cadastro": pygame.Rect(300, 205, 300, 55),
        "login": pygame.Rect(300, 275, 300, 55),
        "pesquisas": pygame.Rect(300, 345, 300, 55),
        "quiz": pygame.Rect(300, 415, 300, 55),
        "sair": pygame.Rect(300, 485, 300, 50),
    }

    while True:
        mouse = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botoes["cadastro"].collidepoint(evento.pos):
                    tela_cadastro()
                elif botoes["login"].collidepoint(evento.pos):
                    tela_login()
                elif botoes["pesquisas"].collidepoint(evento.pos):
                    tela_pesquisas()
                elif botoes["quiz"].collidepoint(evento.pos):
                    tela_quiz()
                elif botoes["sair"].collidepoint(evento.pos):
                    return

        tela.fill(FUNDO)
        desenhar_centralizado("TUPÃ", fonte_titulo, BRANCO, 65)
        desenhar_centralizado("Conhecimento e valorização dos povos originários", fonte_menor, CINZA_CLARO, 135)
        botao("CRIAR CONTA", botoes["cadastro"], mouse)
        botao("LOGIN", botoes["login"], mouse)
        botao("PESQUISAR POVOS", botoes["pesquisas"], mouse)
        botao("QUIZ", botoes["quiz"], mouse)
        botao("SAIR", botoes["sair"], mouse, fonte_pequena, CINZA)
        pygame.display.flip()


if __name__ == "__main__":
    try:
        menu_principal()
    finally:
        pygame.quit()
