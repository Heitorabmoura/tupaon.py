"""Tela de pesquisa de povos indígenas."""
import pygame
from configuracoes import (
    tela, FUNDO, BRANCO, VERDE, VERMELHO, CINZA, CINZA_CLARO,
    fonte_titulo, fonte_texto, fonte_pequena, fonte_menor
)
from interface import (botao, desenhar_texto, desenhar_centralizado,
                       desenhar_bloco, encerrar)
from povos import obter_povos


def tela_pesquisas():
    todos = obter_povos()
    busca = ""
    selecionado = 0
    inicio = 0          # primeiro povo visível na lista da esquerda
    VISIVEIS = 4
    botao_voltar = pygame.Rect(25, 22, 125, 42)
    caixa_busca = pygame.Rect(210, 95, 480, 42)

    while True:
        mouse = pygame.mouse.get_pos()
        encontrados = [p for p in todos if busca.lower() in p["nome"].lower()]
        if encontrados:
            selecionado = max(0, min(selecionado, len(encontrados) - 1))
        else:
            selecionado = 0
        if selecionado < inicio:
            inicio = selecionado
        elif selecionado >= inicio + VISIVEIS:
            inicio = selecionado - VISIVEIS + 1
        inicio = max(0, min(inicio, max(0, len(encontrados) - VISIVEIS)))

        botoes_povos = []
        for pos_visivel, indice in enumerate(range(inicio, min(inicio + VISIVEIS, len(encontrados)))):
            botoes_povos.append((pygame.Rect(45, 185 + pos_visivel * 72, 210, 55), indice))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                elif evento.key == pygame.K_BACKSPACE:
                    busca = busca[:-1]
                    selecionado = inicio = 0
                elif evento.key == pygame.K_UP and encontrados:
                    selecionado = (selecionado - 1) % len(encontrados)
                elif evento.key == pygame.K_DOWN and encontrados:
                    selecionado = (selecionado + 1) % len(encontrados)
                elif evento.unicode and evento.unicode.isprintable():
                    busca += evento.unicode
                    selecionado = inicio = 0
            if evento.type == pygame.MOUSEWHEEL and encontrados:
                selecionado = max(0, min(len(encontrados) - 1, selecionado - evento.y))
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_voltar.collidepoint(evento.pos):
                    return
                for caixa, indice in botoes_povos:
                    if caixa.collidepoint(evento.pos):
                        selecionado = indice

        tela.fill(FUNDO)
        botao("VOLTAR", botao_voltar, mouse, fonte_pequena, CINZA)
        desenhar_centralizado("PESQUISAR POVOS", fonte_titulo, BRANCO, 25)
        desenhar_texto("Digite o nome de um povo:", fonte_pequena, BRANCO, 210, 65)
        pygame.draw.rect(tela, VERDE, caixa_busca, 2, border_radius=5)
        desenhar_texto(busca, fonte_pequena, BRANCO, caixa_busca.x + 10, caixa_busca.y + 8)

        for caixa, indice in botoes_povos:
            povo = encontrados[indice]
            cor = VERDE if indice == selecionado else VERMELHO
            botao(povo["nome"], caixa, mouse, fonte_pequena, cor)
        if len(encontrados) > VISIVEIS:
            fim = min(inicio + VISIVEIS, len(encontrados))
            desenhar_texto(f"{inicio + 1}-{fim} de {len(encontrados)}", fonte_menor, CINZA_CLARO, 45, 478)

        if encontrados:
            povo = encontrados[selecionado]
            desenhar_texto(povo["nome"], fonte_texto, BRANCO, 300, 175)
            if povo["comunidade"]:
                largura_nome = fonte_texto.size(povo["nome"])[0]
                desenhar_texto("adicionado por usuário", fonte_menor, CINZA_CLARO, 300 + largura_nome + 15, 182)
            y = 215
            y = desenhar_bloco("Região:", povo["regiao"], 300, y, 550)
            y = desenhar_bloco("Sobre:", povo["sobre"], 300, y, 550)
            if povo["cuidado"]:
                desenhar_bloco("Para pesquisar mais:", povo["cuidado"], 300, y, 550)
        else:
            desenhar_texto("Nenhum povo encontrado com esse nome.", fonte_pequena, BRANCO, 300, 220)

        desenhar_texto("Use as setas ou a rodinha do mouse para navegar | ESC para voltar", fonte_menor, CINZA_CLARO, 45, 565)
        pygame.display.flip()
