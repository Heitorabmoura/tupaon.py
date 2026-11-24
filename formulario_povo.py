"""Formulário para adicionar ou editar as informações de um povo."""
import pygame
from configuracoes import (
    tela, FUNDO, BRANCO, VERDE, CINZA, CINZA_CLARO,
    fonte_titulo, fonte_pequena, fonte_menor
)
from interface import (botao, campo_texto, campo_multilinha, desenhar_centralizado,
                       desenhar_texto, desenhar_mensagem, encerrar)
from povos import salvar_povo
from validacao import LIMITES_POVO, MINIMOS_POVO

# (chave, rótulo, limite de caracteres)
CAMPOS = [
    ("nome", "Nome do povo", LIMITES_POVO["nome"]),
    ("regiao", "Região", LIMITES_POVO["regiao"]),
    ("sobre", "Sobre o povo", LIMITES_POVO["sobre"]),
    ("cuidado", "Para pesquisar mais (opcional)", LIMITES_POVO["cuidado"]),
]


def tela_formulario(usuario, povo=None):
    """Formulário de criação (povo=None) ou edição. Retorna True se salvou."""
    valores = [povo.get(chave, "") if povo else "" for chave, _, _ in CAMPOS]
    nome_original = povo["nome"] if povo else None
    campo_atual = 0
    mensagem = ""
    tentou = False
    botao_voltar = pygame.Rect(25, 22, 125, 42)
    botao_salvar = pygame.Rect(745, 22, 130, 42)
    caixas = [
        pygame.Rect(150, 105, 600, 40),
        pygame.Rect(150, 192, 600, 58),
        pygame.Rect(150, 289, 600, 100),
        pygame.Rect(150, 427, 600, 76),
    ]

    def tentar_salvar():
        v = valores
        return salvar_povo(usuario["email"], v[0], v[1], v[2], v[3],
                           nome_original=nome_original)

    while True:
        mouse = pygame.mouse.get_pos()
        salvar_agora = False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                if evento.key == pygame.K_TAB:
                    campo_atual = (campo_atual + 1) % len(CAMPOS)
                elif evento.key == pygame.K_RETURN:
                    if campo_atual < len(CAMPOS) - 1:
                        campo_atual += 1
                    else:
                        salvar_agora = True
                elif evento.key == pygame.K_BACKSPACE:
                    valores[campo_atual] = valores[campo_atual][:-1]
                elif evento.unicode and evento.unicode.isprintable():
                    if len(valores[campo_atual]) < CAMPOS[campo_atual][2]:
                        valores[campo_atual] += evento.unicode
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_voltar.collidepoint(evento.pos):
                    return False
                if botao_salvar.collidepoint(evento.pos):
                    salvar_agora = True
                else:
                    for i, caixa in enumerate(caixas):
                        if caixa.collidepoint(evento.pos):
                            campo_atual = i

        if salvar_agora:
            tentou = True
            sucesso, mensagem = tentar_salvar()
            if sucesso:
                tela.fill(FUNDO)
                desenhar_centralizado("MEUS POVOS", fonte_titulo, BRANCO, 60)
                desenhar_mensagem(mensagem, 290, VERDE)
                pygame.display.flip()
                pygame.time.wait(900)
                return True

        tela.fill(FUNDO)
        botao("VOLTAR", botao_voltar, mouse, fonte_pequena, CINZA)
        botao("SALVAR", botao_salvar, mouse, fonte_pequena, VERDE)
        titulo = "EDITAR POVO" if povo else "ADICIONAR POVO"
        desenhar_centralizado(titulo, fonte_titulo, BRANCO, 25)

        for i, (chave, rotulo, limite) in enumerate(CAMPOS):
            if i == 0:
                campo_texto(rotulo, valores[i], caixas[i], campo_atual == i)
            else:
                campo_multilinha(rotulo, valores[i], caixas[i], campo_atual == i)
            minimo = MINIMOS_POVO[chave]
            atual = len(valores[i].strip())
            if minimo and atual >= minimo:
                cor_contador = VERDE
            elif minimo and (atual or tentou):
                cor_contador = (255, 130, 130)
            else:
                cor_contador = CINZA_CLARO
            texto_contador = f"{len(valores[i])}/{limite}" + (f"  (mín. {minimo})" if minimo else "")
            contador = fonte_menor.render(texto_contador, True, cor_contador)
            tela.blit(contador, (caixas[i].right - contador.get_width(), caixas[i].y - 24))

        desenhar_mensagem(mensagem, 518)
        desenhar_texto("TAB/ENTER: próximo campo | ENTER no último: salvar | ESC: voltar",
                       fonte_menor, CINZA_CLARO, 150, 565)
        pygame.display.flip()
