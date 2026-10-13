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
    tela.set_clip(area)
    tela.blit(imagem, (area.x, area.y))
    tela.set_clip(None)

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
