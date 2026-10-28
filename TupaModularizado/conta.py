"""Tela de exclusão da própria conta."""
import pygame
from configuracoes import (
    tela, FUNDO, BRANCO, VERDE, CINZA, CINZA_CLARO, fonte_titulo,
    fonte_pequena, fonte_menor
)
from usuarios import excluir_usuario
from interface import (botao, campo_texto, desenhar_centralizado, desenhar_mensagem,
                       quebrar_texto, encerrar)

AVISO = ("Esta ação é permanente. Seu nome, e-mail e senha serão apagados e você não poderá "
         "mais entrar com esta conta. As informações sobre povos que você adicionou continuam "
         "no Tupã, mas deixam de estar ligadas a você.")


def tela_excluir_conta(usuario):
    """Pede a senha para confirmar. Retorna True se a conta foi excluída."""
    senha = ""
    mostrar_senha = False
    mensagem = ""
    botao_voltar = pygame.Rect(25, 22, 125, 42)
    caixa_senha = pygame.Rect(250, 300, 320, 45)
    botao_mostrar = pygame.Rect(585, 300, 120, 45)
    botao_cancelar = pygame.Rect(215, 385, 220, 48)
    botao_excluir = pygame.Rect(465, 385, 220, 48)

    while True:
        mouse = pygame.mouse.get_pos()
        excluir_agora = False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                elif evento.key == pygame.K_RETURN:
                    excluir_agora = True
                elif evento.key == pygame.K_BACKSPACE:
                    senha = senha[:-1]
                elif evento.unicode and evento.unicode.isprintable():
                    senha += evento.unicode
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                if botao_voltar.collidepoint(pos) or botao_cancelar.collidepoint(pos):
                    return False
                if botao_mostrar.collidepoint(pos):
                    mostrar_senha = not mostrar_senha
                elif botao_excluir.collidepoint(pos):
                    excluir_agora = True

        if excluir_agora:
            if not senha:
                mensagem = "Digite sua senha para confirmar."
            else:
                sucesso, resultado = excluir_usuario(usuario["email"], senha)
                if sucesso:
                    tela.fill(FUNDO)
                    desenhar_centralizado("CONTA EXCLUÍDA", fonte_titulo, BRANCO, 60)
                    desenhar_mensagem("Sua conta foi apagada. Voltando ao menu...", 290, VERDE)
                    pygame.display.flip()
                    pygame.time.wait(1400)
                    return True
                mensagem = resultado

        tela.fill(FUNDO)
        botao("VOLTAR", botao_voltar, mouse, fonte_pequena, CINZA)
        desenhar_centralizado("DELETAR CONTA", fonte_titulo, BRANCO, 75)
        for i, linha in enumerate(quebrar_texto(AVISO, fonte_pequena, 700)):
            desenhar_centralizado(linha, fonte_pequena, CINZA_CLARO, 150 + i * 27)
        campo_texto("Digite sua senha para confirmar", senha, caixa_senha, True,
                    ocultar=not mostrar_senha)
        botao("OCULTAR" if mostrar_senha else "MOSTRAR", botao_mostrar, mouse, fonte_menor, CINZA)
        botao("CANCELAR", botao_cancelar, mouse, fonte_pequena, CINZA)
        botao("DELETAR CONTA", botao_excluir, mouse, fonte_pequena)
        desenhar_mensagem(mensagem, 460)
        pygame.display.flip()
