"""Quiz educativo sobre diversidade e respeito aos povos indígenas."""
import pygame
from configuracoes import (
    tela, FUNDO, BRANCO, VERDE, VERMELHO, CINZA, CINZA_CLARO,
    fonte_titulo, fonte_texto, fonte_pequena, fonte_menor
)
from interface import botao, desenhar_centralizado, quebrar_texto, encerrar

def tela_quiz():
    perguntas = [
        {
            "pergunta": "Por que é importante falar em povos indígenas, no plural?",
            "opcoes": [
                "Porque existem muitos povos com culturas e línguas diversas.",
                "Porque todos vivem exatamente da mesma maneira.",
                "Porque todos têm a mesma língua.",
                "Porque só existe um povo indígena no Brasil."
            ],
            "correta": 0
        },
        {
            "pergunta": "Qual atitude ajuda a pesquisar com respeito?",
            "opcoes": [
                "Usar apenas estereótipos.",
                "Consultar fontes confiáveis e, quando possível, fontes dos próprios povos.",
                "Supor que todas as tradições são iguais.",
                "Ignorar a diversidade entre comunidades."
            ],
            "correta": 1
        }
    ]
    indice = 0
    pontos = 0
    respondidas = set()
    mensagem = ""
    botao_voltar = pygame.Rect(25, 22, 125, 42)
    botoes = [pygame.Rect(140, 260 + i * 62, 620, 48) for i in range(4)]

    while True:
        mouse = pygame.mouse.get_pos()
        if indice >= len(perguntas):
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    encerrar()
                if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if botao_voltar.collidepoint(evento.pos):
                        return
                    return
            tela.fill(FUNDO)
            desenhar_centralizado("QUIZ CONCLUÍDO!", fonte_titulo, BRANCO, 130)
            desenhar_centralizado(f"Sua pontuação: {pontos} de {len(perguntas)}", fonte_texto, VERDE, 240)
            desenhar_centralizado("Clique ou pressione ENTER para voltar ao menu.", fonte_pequena, CINZA_CLARO, 320)
            botao("VOLTAR", botao_voltar, mouse, fonte_pequena, CINZA)
            pygame.display.flip()
            continue

        pergunta = perguntas[indice]
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_voltar.collidepoint(evento.pos):
                    return
                if indice not in respondidas:
                    for i, caixa in enumerate(botoes):
                        if caixa.collidepoint(evento.pos):
                            if i == pergunta["correta"]:
                                pontos += 1
                                mensagem = "Resposta correta!"
                            else:
                                mensagem = "Não foi dessa vez. Vamos para a próxima!"
                            respondidas.add(indice)
                            break
                else:
                    indice += 1
                    mensagem = ""

        tela.fill(FUNDO)
        botao("VOLTAR", botao_voltar, mouse, fonte_pequena, CINZA)
        desenhar_centralizado(f"QUIZ - PERGUNTA {indice + 1}/{len(perguntas)}", fonte_titulo, BRANCO, 70)
        for i, linha in enumerate(quebrar_texto(pergunta["pergunta"], fonte_texto, 700)):
            desenhar_centralizado(linha, fonte_texto, BRANCO, 160 + i * 35)
        for i, caixa in enumerate(botoes):
            botao(pergunta["opcoes"][i], caixa, mouse, fonte_menor,
                  VERDE if indice in respondidas and i == pergunta["correta"] else VERMELHO)
        desenhar_centralizado(mensagem, fonte_pequena, VERDE if "correta" in mensagem else BRANCO, 525)
        if indice in respondidas:
            desenhar_centralizado("Clique novamente para continuar.", fonte_menor, CINZA_CLARO, 555)
        pygame.display.flip()
