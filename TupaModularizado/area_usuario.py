"""Tela exibida após o login bem-sucedido."""
import pygame
from configuracoes import tela, FUNDO, BRANCO, VERDE, CINZA, fonte_titulo, fonte_texto
from interface import botao, desenhar_centralizado, encerrar
from meus_povos import tela_meus_povos
from conta import tela_excluir_conta


def tela_principal_usuario(usuario):
    """usuario é o dicionário {"nome": ..., "email": ...} devolvido pelo login."""
    botao_povos = pygame.Rect(280, 260, 340, 55)
    botao_excluir = pygame.Rect(280, 330, 340, 55)
    botao_sair = pygame.Rect(280, 400, 340, 55)

    while True:
        mouse = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_povos.collidepoint(evento.pos):
                    tela_meus_povos(usuario)
                elif botao_excluir.collidepoint(evento.pos):
                    if tela_excluir_conta(usuario):
                        return  # conta apagada: volta ao menu principal
                elif botao_sair.collidepoint(evento.pos):
                    return

        tela.fill(FUNDO)
        desenhar_centralizado(f"OLÁ, {usuario['nome'].upper()}!", fonte_titulo, BRANCO, 110)
        desenhar_centralizado("Login realizado com sucesso.", fonte_texto, VERDE, 190)
        botao("ADICIONAR INFORMAÇÕES", botao_povos, mouse, cor=VERDE)
        botao("DELETAR CONTA", botao_excluir, mouse)
        botao("VOLTAR AO MENU", botao_sair, mouse, cor=CINZA)
        pygame.display.flip()
