"""Tela de criação de conta."""
import pygame
from configuracoes import (
    tela, FUNDO, BRANCO, VERDE, CINZA, CINZA_CLARO, fonte_titulo,
    fonte_pequena, fonte_menor
)
from armazenamento import cadastrar_usuario
from interface import (botao, campo_texto, desenhar_centralizado,
                       desenhar_texto, desenhar_mensagem, encerrar)

def tela_cadastro():
    nome = ""
    email = ""
    senha = ""
    confirmar = ""
    campo_atual = 0
    mostrar_senha = False
    mensagem = ""

    campos = [
        pygame.Rect(250, 135, 400, 42),
        pygame.Rect(250, 220, 400, 42),
        pygame.Rect(250, 305, 320, 42),
        pygame.Rect(250, 390, 320, 42),
    ]
    botao_voltar = pygame.Rect(30, 25, 130, 42)
    botao_mostrar = pygame.Rect(585, 305, 120, 42)
    botao_mostrar_confirmar = pygame.Rect(585, 390, 120, 42)
    botao_criar = pygame.Rect(330, 465, 240, 45)

    while True:
        mouse = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                if evento.key == pygame.K_TAB:
                    campo_atual = (campo_atual + 1) % 4
                elif evento.key == pygame.K_RETURN:
                    if campo_atual < 3:
                        campo_atual += 1
                    else:
                        if senha != confirmar:
                            mensagem = "As senhas não são iguais."
                        else:
                            sucesso, mensagem = cadastrar_usuario(nome, email, senha)
                            if sucesso:
                                mensagem = "Conta criada! Voltando ao menu..."
                                tela.fill(FUNDO)
                                desenhar_centralizado("CRIAR CONTA", fonte_titulo, BRANCO, 60)
                                desenhar_mensagem(mensagem, 290, VERDE)
                                pygame.display.flip()
                                pygame.time.wait(900)
                                return
                elif evento.key == pygame.K_BACKSPACE:
                    if campo_atual == 0:
                        nome = nome[:-1]
                    elif campo_atual == 1:
                        email = email[:-1]
                    elif campo_atual == 2:
                        senha = senha[:-1]
                    else:
                        confirmar = confirmar[:-1]
                elif evento.unicode and evento.unicode.isprintable():
                    if campo_atual == 0:
                        nome += evento.unicode
                    elif campo_atual == 1:
                        email += evento.unicode
                    elif campo_atual == 2:
                        senha += evento.unicode
                    else:
                        confirmar += evento.unicode

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                if botao_voltar.collidepoint(pos):
                    return
                if botao_mostrar.collidepoint(pos) or botao_mostrar_confirmar.collidepoint(pos):
                    mostrar_senha = not mostrar_senha
                elif botao_criar.collidepoint(pos):
                    if senha != confirmar:
                        mensagem = "As senhas não são iguais."
                    else:
                        sucesso, mensagem = cadastrar_usuario(nome, email, senha)
                        if sucesso:
                            tela.fill(FUNDO)
                            desenhar_centralizado("CRIAR CONTA", fonte_titulo, BRANCO, 60)
                            desenhar_mensagem("Conta criada com sucesso!", 290, VERDE)
                            pygame.display.flip()
                            pygame.time.wait(900)
                            return
                else:
                    for i, caixa in enumerate(campos):
                        if caixa.collidepoint(pos):
                            campo_atual = i

        tela.fill(FUNDO)
        botao("VOLTAR", botao_voltar, mouse, fonte_pequena, CINZA)
        desenhar_centralizado("CRIAR CONTA", fonte_titulo, BRANCO, 45)

        valores = [nome, email, senha, confirmar]
        rotulos = ["Nome", "E-mail", "Senha", "Confirmar senha"]
        for i, caixa in enumerate(campos):
            campo_texto(rotulos[i], valores[i], caixa, campo_atual == i,
                        ocultar=(i in (2, 3) and not mostrar_senha))

        botao("OCULTAR" if mostrar_senha else "MOSTRAR", botao_mostrar, mouse, fonte_menor, CINZA)
        botao("OCULTAR" if mostrar_senha else "MOSTRAR", botao_mostrar_confirmar, mouse, fonte_menor, CINZA)
        botao("CRIAR CONTA", botao_criar, mouse)
        desenhar_texto("ENTER: próximo campo | ESC: voltar", fonte_menor, CINZA_CLARO, 250, 525)
        desenhar_mensagem(mensagem, 555)
        pygame.display.flip()
