"""Elementos visuais reutilizáveis nas telas do Tupã."""
import pygame
from configuracoes import (
    LARGURA, tela, BRANCO, VERMELHO, VERMELHO_CLARO, VERDE, CINZA,
    CINZA_CLARO, fonte_texto, fonte_pequena, fonte_menor
)

def desenhar_texto(texto, fonte, cor, x, y):
    imagem = fonte.render(str(texto), True, cor)
    tela.blit(imagem, (x, y))

def desenhar_centralizado(texto, fonte, cor, y):
    imagem = fonte.render(str(texto), True, cor)
    tela.blit(imagem, (LARGURA // 2 - imagem.get_width() // 2, y))

def botao(texto, retangulo, mouse, fonte=fonte_texto, cor=VERMELHO):
    cor_atual = VERMELHO_CLARO if retangulo.collidepoint(mouse) else cor
    pygame.draw.rect(tela, cor_atual, retangulo, border_radius=8)
    imagem = fonte.render(texto, True, BRANCO)
    tela.blit(imagem, (
        retangulo.centerx - imagem.get_width() // 2,
        retangulo.centery - imagem.get_height() // 2
    ))

def campo_texto(rotulo, valor, retangulo, ativo, ocultar=False):
    desenhar_texto(rotulo, fonte_pequena, BRANCO, retangulo.x, retangulo.y - 27)
    pygame.draw.rect(tela, VERDE if ativo else CINZA_CLARO, retangulo, 2, border_radius=5)
    texto = "*" * len(valor) if ocultar else valor
    imagem = fonte_pequena.render(texto, True, BRANCO)
    area = pygame.Rect(retangulo.x + 8, retangulo.y + 5, retangulo.width - 16, retangulo.height - 10)
    deslocamento = min(0, area.width - imagem.get_width())
    tela.set_clip(area)
    tela.blit(imagem, (area.x + deslocamento, area.y))
    tela.set_clip(None)

def campo_multilinha(rotulo, valor, retangulo, ativo, fonte=fonte_pequena):
    """Caixa de texto que quebra linhas; mostra as últimas linhas se o texto não couber."""
    desenhar_texto(rotulo, fonte_pequena, BRANCO, retangulo.x, retangulo.y - 27)
    pygame.draw.rect(tela, VERDE if ativo else CINZA_CLARO, retangulo, 2, border_radius=5)
    altura_linha = fonte.get_linesize() + 2
    max_linhas = max(1, (retangulo.height - 10) // altura_linha)
    linhas = quebrar_texto(valor, fonte, retangulo.width - 16)[-max_linhas:]
    tela.set_clip(retangulo.inflate(-4, -4))
    for i, linha in enumerate(linhas):
        desenhar_texto(linha, fonte, BRANCO, retangulo.x + 8, retangulo.y + 5 + i * altura_linha)
    tela.set_clip(None)

def desenhar_bloco(titulo, texto, x, y, largura):
    """Título verde + texto quebrado em linhas. Retorna o y onde o próximo bloco pode começar."""
    desenhar_texto(titulo, fonte_pequena, VERDE, x, y)
    y += 28
    for linha in quebrar_texto(texto, fonte_menor, largura):
        desenhar_texto(linha, fonte_menor, BRANCO, x, y)
        y += 23
    return y + 14

def desenhar_regra(texto, estado, x, y):
    """Uma linha de requisito. estado: 'ok' (verde), 'erro' (vermelho) ou 'neutro' (cinza).
    Devolve o y da próxima linha. Os ícones são desenhados porque a fonte padrão não tem ✓/✗."""
    cor = {"ok": VERDE, "erro": (255, 130, 130)}.get(estado, CINZA_CLARO)
    cx, cy = x + 9, y + 9
    pygame.draw.circle(tela, cor, (cx, cy), 9, 2)
    if estado == "ok":
        pygame.draw.lines(tela, cor, False, [(cx - 4, cy), (cx - 1, cy + 4), (cx + 5, cy - 4)], 2)
    elif estado == "erro":
        pygame.draw.line(tela, cor, (cx - 4, cy - 4), (cx + 4, cy + 4), 2)
        pygame.draw.line(tela, cor, (cx - 4, cy + 4), (cx + 4, cy - 4), 2)
    desenhar_texto(texto, fonte_menor, cor, x + 26, y + 2)
    return y + 24

def desenhar_mensagem(mensagem, y=525, cor=(255, 130, 130)):
    if mensagem:
        imagem = fonte_menor.render(mensagem, True, cor)
        tela.blit(imagem, (LARGURA // 2 - imagem.get_width() // 2, y))

def encerrar():
    pygame.quit()
    raise SystemExit

def quebrar_texto(texto, fonte, largura_maxima):
    palavras = texto.split()
    linhas = []
    linha = ""
    for palavra in palavras:
        tentativa = palavra if not linha else linha + " " + palavra
        if fonte.size(tentativa)[0] <= largura_maxima:
            linha = tentativa
        else:
            if linha:
                linhas.append(linha)
            linha = palavra
    if linha:
        linhas.append(linha)
    return linhas
