"""Tela de autenticação."""
import pygame
from configuracoes import (
    tela, FUNDO, BRANCO, CINZA, CINZA_CLARO, fonte_titulo, fonte_pequena, fonte_menor
)
from usuarios import verificar_login
from area_usuario import tela_principal_usuario
from interface import (botao, campo_texto, desenhar_centralizado,
                       desenhar_texto, desenhar_mensagem, encerrar)

def tela_login():
    email = ""
    senha = ""
    campo_atual = 0
    mostrar_senha = False
    mensagem = ""
    botao_voltar = pygame.Rect(30, 25, 130, 42)
    caixa_email = pygame.Rect(250, 220, 400, 45)
    caixa_senha = pygame.Rect(250, 315, 320, 45)
    botao_mostrar = pygame.Rect(585, 315, 120, 45)
    botao_entrar = pygame.Rect(330, 405, 240, 48)

    while True:
        mouse = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                if evento.key == pygame.K_TAB:
                    campo_atual = 1 - campo_atual
                elif evento.key == pygame.K_RETURN:
                    if campo_atual == 0:
                        campo_atual = 1
                    else:
                        sucesso, resultado = verificar_login(email, senha)
                        if sucesso:
                            tela_principal_usuario(resultado)
                            return
                        mensagem = resultado
                elif evento.key == pygame.K_BACKSPACE:
                    if campo_atual == 0:
                        email = email[:-1]
                    else:
                        senha = senha[:-1]
                elif evento.unicode and evento.unicode.isprintable():
                    if campo_atual == 0:
                        email += evento.unicode
                    else:
                        senha += evento.unicode

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                if botao_voltar.collidepoint(pos):
                    return
                if botao_mostrar.collidepoint(pos):
                    mostrar_senha = not mostrar_senha
                elif botao_entrar.collidepoint(pos):
                    sucesso, resultado = verificar_login(email, senha)
                    if sucesso:
                        tela_principal_usuario(resultado)
                        return
                    mensagem = resultado
                elif caixa_email.collidepoint(pos):
                    campo_atual = 0
                elif caixa_senha.collidepoint(pos):
                    campo_atual = 1

        tela.fill(FUNDO)
        botao("VOLTAR", botao_voltar, mouse, fonte_pequena, CINZA)
        desenhar_centralizado("LOGIN", fonte_titulo, BRANCO, 75)
        campo_texto("E-mail", email, caixa_email, campo_atual == 0)
        campo_texto("Senha", senha, caixa_senha, campo_atual == 1, ocultar=not mostrar_senha)
        botao("OCULTAR" if mostrar_senha else "MOSTRAR", botao_mostrar, mouse, fonte_menor, CINZA)
        botao("ENTRAR", botao_entrar, mouse)
        desenhar_texto("ENTER: avançar/entrar | ESC: voltar", fonte_menor, CINZA_CLARO, 250, 480)
        desenhar_mensagem(mensagem, 530)
        pygame.display.flip()
