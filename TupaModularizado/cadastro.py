"""Tela de criação de conta, com verificação ao vivo dos requisitos de cada campo."""
import pygame
from configuracoes import (
    tela, FUNDO, BRANCO, VERDE, CINZA, CINZA_CLARO, fonte_titulo,
    fonte_pequena, fonte_menor
)
from usuarios import cadastrar_usuario
from validacao import (
    erros_cadastro, resumir_erros,
    regras_nome, regras_email, regras_senha, regras_confirmacao
)
from interface import (botao, campo_texto, desenhar_centralizado, desenhar_texto,
                       desenhar_mensagem, desenhar_regra, encerrar)


def desenhar_painel_requisitos(nome, email, senha, confirmar, tentou):
    """Mostra, para cada campo, quais requisitos já foram cumpridos (verde) e quais não (vermelho).
    Campo vazio fica cinza até a pessoa tentar criar a conta."""
    secoes = [
        ("Nome", nome, regras_nome(nome)),
        ("E-mail", email, regras_email(email)),
        ("Senha", senha, regras_senha(senha)),
        ("Confirmar senha", confirmar, regras_confirmacao(senha, confirmar)),
    ]
    x, y = 560, 120
    desenhar_texto("REQUISITOS", fonte_pequena, CINZA_CLARO, x, y)
    y += 32
    for titulo, valor, regras in secoes:
        desenhar_texto(titulo, fonte_pequena, BRANCO, x, y)
        y += 24
        for rotulo, ok in regras:
            if ok:
                estado = "ok"
            elif valor or tentou:
                estado = "erro"
            else:
                estado = "neutro"
            y = desenhar_regra(rotulo, estado, x, y)
        y += 10


def tela_cadastro():
    nome = ""
    email = ""
    senha = ""
    confirmar = ""
    campo_atual = 0
    mostrar_senha = False
    mensagem = ""
    tentou = False

    campos = [
        pygame.Rect(60, 135, 400, 42),
        pygame.Rect(60, 220, 400, 42),
        pygame.Rect(60, 305, 320, 42),
        pygame.Rect(60, 390, 320, 42),
    ]
    botao_voltar = pygame.Rect(30, 25, 130, 42)
    botao_mostrar = pygame.Rect(395, 305, 120, 42)
    botao_mostrar_confirmar = pygame.Rect(395, 390, 120, 42)
    botao_criar = pygame.Rect(140, 465, 240, 45)

    def tentar_cadastrar():
        """Confere todos os campos de uma vez. Retorna True se a conta foi criada."""
        nonlocal mensagem, tentou
        tentou = True
        erros = erros_cadastro(nome, email, senha, confirmar)
        if erros:
            mensagem = resumir_erros(erros)
            return False
        sucesso, mensagem = cadastrar_usuario(nome, email, senha)
        return sucesso

    def tela_sucesso():
        tela.fill(FUNDO)
        desenhar_centralizado("CRIAR CONTA", fonte_titulo, BRANCO, 60)
        desenhar_mensagem("Conta criada com sucesso!", 290, VERDE)
        pygame.display.flip()
        pygame.time.wait(900)

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
                    elif tentar_cadastrar():
                        tela_sucesso()
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
                    if tentar_cadastrar():
                        tela_sucesso()
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
        desenhar_painel_requisitos(nome, email, senha, confirmar, tentou)
        desenhar_texto("ENTER: próximo campo | ESC: voltar", fonte_menor, CINZA_CLARO, 60, 525)
        desenhar_mensagem(mensagem, 555)
        pygame.display.flip()
