"""Painel de detalhes de um povo na tela de pesquisa, com abas.

Abas: Sobre, Palavras, Mitologia (criação do mundo, divindades e seres), Narrativas (histórias,
memória e tradições vividas) e Culinária.
"""
import pygame
from configuracoes import BRANCO, VERDE, CINZA, CINZA_CLARO, fonte_pequena, fonte_menor
from interface import botao, cortar_texto, desenhar_bloco, desenhar_texto, quebrar_texto

ABAS = ["SOBRE", "PALAVRAS", "MITOLOGIA", "NARRATIVAS", "CULINÁRIA"]
SOBRE, PALAVRAS, MITOLOGIA, NARRATIVAS, CULINARIA = range(5)

X = 300                 # coluna do painel
LARGURA = 550           # largura do texto
X_FIM = 850             # limite direito do conteúdo
Y_ABAS = 215
Y_CONTEUDO = 258        # onde começa o conteúdo quando há abas


def tem_extras(povo):
    """Só os povos do conteúdo base têm as demais abas; os dos usuários têm apenas 'Sobre'."""
    return any(povo.get(chave) for chave in ("palavras", "mitologia", "narrativa", "culinaria"))


def retangulos_abas():
    return [pygame.Rect(X + i * 108, Y_ABAS, 102, 30) for i in range(len(ABAS))]


def desenhar_abas(aba_atual, mouse):
    for i, (retangulo, nome) in enumerate(zip(retangulos_abas(), ABAS)):
        botao(nome, retangulo, mouse, fonte_menor, VERDE if i == aba_atual else CINZA)


def _rodape(textos, y):
    """Textos em cinza (observações e fontes) abaixo do conteúdo."""
    for texto in textos:
        for linha in quebrar_texto(texto, fonte_menor, LARGURA):
            desenhar_texto(linha, fonte_menor, CINZA_CLARO, X, y)
            y += 21


def desenhar_sobre(povo, y):
    y = desenhar_bloco("Região:", povo["regiao"], X, y, LARGURA)
    y = desenhar_bloco("Sobre:", povo["sobre"], X, y, LARGURA)
    if povo["cuidado"]:
        desenhar_bloco("Para pesquisar mais:", povo["cuidado"], X, y, LARGURA)


def _desenhar_lista(povo, chave, campo_1, campo_2, largura_1, vazio, y):
    """Lista de duas colunas (ex.: palavra e significado) seguida de observação e fontes."""
    itens = povo.get(chave) or []
    if not itens:
        desenhar_texto(vazio, fonte_pequena, BRANCO, X, y)
        return
    x_2 = X + largura_1 + 10
    for item in itens:
        desenhar_texto(cortar_texto(item[campo_1], fonte_pequena, largura_1), fonte_pequena, VERDE, X, y)
        desenhar_texto(cortar_texto(item[campo_2], fonte_menor, X_FIM - x_2), fonte_menor, BRANCO, x_2, y + 3)
        y += 24
    sufixo = chave if chave == "palavras" else "culinaria"
    rodape = []
    if povo.get("observacao_" + sufixo):
        rodape.append(povo["observacao_" + sufixo])
    if povo.get("fonte_" + sufixo):
        rodape.append("Fontes: " + povo["fonte_" + sufixo])
    _rodape(rodape, y + 8)


def desenhar_palavras(povo, y):
    _desenhar_lista(povo, "palavras", "palavra", "significado", 150,
                    "Este povo ainda não tem palavras cadastradas.", y)


def desenhar_culinaria(povo, y):
    _desenhar_lista(povo, "culinaria", "prato", "descricao", 180,
                    "Este povo ainda não tem culinária cadastrada.", y)


def _desenhar_relato(povo, chave, vazio, y):
    """Título + texto corrido + nota e fontes (usado por Mitologia e Narrativas)."""
    relato = povo.get(chave)
    if not relato:
        desenhar_texto(vazio, fonte_pequena, BRANCO, X, y)
        return
    desenhar_texto(cortar_texto(relato["titulo"], fonte_pequena, LARGURA), fonte_pequena, VERDE, X, y)
    y += 30
    for linha in quebrar_texto(relato["texto"], fonte_menor, LARGURA):
        desenhar_texto(linha, fonte_menor, BRANCO, X, y)
        y += 23
    _rodape(["Versão resumida: as tradições variam entre comunidades.",
             "Fontes: " + relato["fonte"]], y + 8)


def desenhar_mitologia(povo, y):
    _desenhar_relato(povo, "mitologia", "Este povo ainda não tem mitologia cadastrada.", y)


def desenhar_narrativa(povo, y):
    _desenhar_relato(povo, "narrativa", "Este povo ainda não tem narrativas cadastradas.", y)


def desenhar_aba(povo, aba, mouse):
    """Desenha as abas e o conteúdo da aba escolhida."""
    desenhar_abas(aba, mouse)
    desenhar = {
        SOBRE: desenhar_sobre, PALAVRAS: desenhar_palavras, MITOLOGIA: desenhar_mitologia,
        NARRATIVAS: desenhar_narrativa, CULINARIA: desenhar_culinaria,
    }.get(aba, desenhar_sobre)
    desenhar(povo, Y_CONTEUDO)
