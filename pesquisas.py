"""Pesquisa local de informações sobre povos indígenas."""
import pygame
from configuracoes import (
    tela, FUNDO, BRANCO, VERDE, VERMELHO, CINZA, CINZA_CLARO,
    fonte_titulo, fonte_texto, fonte_pequena, fonte_menor
)
from interface import (botao, desenhar_texto, desenhar_centralizado,
                       quebrar_texto, encerrar)

POVOS = [
    {
        "nome": "Guarani",
        "regiao": "Diferentes áreas do Brasil, além de países vizinhos.",
        "sobre": "Guarani é o nome de povos indígenas com línguas e identidades próprias. Há diferentes grupos Guarani.",
        "cuidado": "Evite tratar todos os povos indígenas como se tivessem a mesma cultura."
    },
    {
        "nome": "Yanomami",
        "regiao": "Territórios na região amazônica do Brasil e da Venezuela.",
        "sobre": "Os Yanomami são um povo indígena da região amazônica, com línguas, conhecimentos e modos de vida próprios.",
        "cuidado": "A proteção territorial e o respeito às comunidades são temas importantes."
    },
    {
        "nome": "Tikuna",
        "regiao": "Principalmente na região do Alto Solimões, no Amazonas.",
        "sobre": "Os Tikuna possuem língua e práticas culturais próprias, além de expressões artísticas e conhecimentos tradicionais.",
        "cuidado": "As tradições e experiências podem variar entre comunidades e gerações."
    },
    {
        "nome": "Pataxó",
        "regiao": "Principalmente no sul da Bahia e em Minas Gerais.",
        "sobre": "O povo Pataxó mantém ações de fortalecimento cultural, memória, língua e defesa de seus territórios.",
        "cuidado": "Consulte fontes indígenas e instituições confiáveis para aprofundar a pesquisa."
    },
]

def tela_pesquisas():
    busca = ""
    selecionado = 0
    botao_voltar = pygame.Rect(25, 22, 125, 42)
    caixa_busca = pygame.Rect(210, 95, 480, 42)

    while True:
        mouse = pygame.mouse.get_pos()
        encontrados = [p for p in POVOS if busca.lower() in p["nome"].lower()]
        if encontrados:
            selecionado = max(0, min(selecionado, len(encontrados) - 1))
        else:
            selecionado = 0

        botoes_povos = []
        for i, povo in enumerate(encontrados[:4]):
            botoes_povos.append((pygame.Rect(45, 185 + i * 72, 210, 55), i))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                elif evento.key == pygame.K_BACKSPACE:
                    busca = busca[:-1]
                elif evento.key == pygame.K_UP and encontrados:
                    selecionado = (selecionado - 1) % len(encontrados)
                elif evento.key == pygame.K_DOWN and encontrados:
                    selecionado = (selecionado + 1) % len(encontrados)
                elif evento.unicode and evento.unicode.isprintable():
                    busca += evento.unicode
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

        if encontrados:
            povo = encontrados[selecionado]
            desenhar_texto(povo["nome"], fonte_texto, BRANCO, 300, 175)
            desenhar_texto("Região:", fonte_pequena, VERDE, 300, 220)
            desenhar_texto(povo["regiao"], fonte_menor, BRANCO, 300, 250)
            desenhar_texto("Sobre:", fonte_pequena, VERDE, 300, 295)
            linhas = quebrar_texto(povo["sobre"], fonte_menor, 550)
            for i, linha in enumerate(linhas):
                desenhar_texto(linha, fonte_menor, BRANCO, 300, 325 + i * 25)
            desenhar_texto("Para pesquisar mais:", fonte_pequena, VERDE, 300, 405)
            for i, linha in enumerate(quebrar_texto(povo["cuidado"], fonte_menor, 550)):
                desenhar_texto(linha, fonte_menor, BRANCO, 300, 435 + i * 24)
        else:
            desenhar_texto("Nenhum povo encontrado com esse nome.", fonte_pequena, BRANCO, 300, 220)

        desenhar_texto("Use as setas para navegar | ESC para voltar", fonte_menor, CINZA_CLARO, 45, 535)
        pygame.display.flip()
