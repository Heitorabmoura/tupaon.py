"""Lista dos povos que o usuário adicionou, com opções de adicionar, editar e excluir."""
import pygame
from configuracoes import (
    tela, FUNDO, BRANCO, VERDE, CINZA, CINZA_CLARO,
    fonte_titulo, fonte_texto, fonte_pequena, fonte_menor
)
from armazenamento import ErroDeArmazenamento
from formulario_povo import tela_formulario
from interface import (botao, desenhar_centralizado, desenhar_texto,
                       desenhar_mensagem, desenhar_bloco, encerrar)
from povos import listar_povos_do_usuario, excluir_povo


def tela_meus_povos(usuario):
    """Lista os povos que o usuário adicionou, com opções de adicionar, editar e excluir."""
    VISIVEIS = 5
    selecionado = 0
    inicio = 0
    mensagem = ""
    cor_mensagem = (255, 130, 130)
    confirmando = False
    meus = []

    def recarregar():
        nonlocal meus, mensagem, cor_mensagem
        try:
            meus = listar_povos_do_usuario(usuario["email"])
        except ErroDeArmazenamento as erro:
            meus = []
            mensagem, cor_mensagem = str(erro), (255, 130, 130)

    recarregar()
    botao_voltar = pygame.Rect(25, 22, 125, 42)
    botao_novo = pygame.Rect(45, 450, 300, 48)
    botao_editar = pygame.Rect(390, 450, 200, 48)
    botao_excluir = pygame.Rect(610, 450, 200, 48)

    def ajustar_lista():
        """Mantém a seleção válida e devolve os botões visíveis da lista."""
        nonlocal selecionado, inicio
        selecionado = max(0, min(selecionado, len(meus) - 1)) if meus else 0
        if selecionado < inicio:
            inicio = selecionado
        elif selecionado >= inicio + VISIVEIS:
            inicio = selecionado - VISIVEIS + 1
        inicio = max(0, min(inicio, max(0, len(meus) - VISIVEIS)))
        return [(pygame.Rect(45, 125 + pos * 58, 300, 48), indice)
                for pos, indice in enumerate(range(inicio, min(inicio + VISIVEIS, len(meus))))]

    while True:
        mouse = pygame.mouse.get_pos()
        itens = ajustar_lista()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                if evento.key in (pygame.K_UP, pygame.K_DOWN) and meus:
                    passo = -1 if evento.key == pygame.K_UP else 1
                    selecionado = (selecionado + passo) % len(meus)
                    confirmando = False
            if evento.type == pygame.MOUSEWHEEL and meus:
                selecionado = max(0, min(len(meus) - 1, selecionado - evento.y))
                confirmando = False
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                if botao_voltar.collidepoint(pos):
                    return
                if botao_novo.collidepoint(pos):
                    confirmando = False
                    if tela_formulario(usuario):
                        recarregar()
                        mensagem = ""
                elif meus and botao_editar.collidepoint(pos):
                    confirmando = False
                    nome_editado = meus[selecionado]["nome"]
                    if tela_formulario(usuario, meus[selecionado]):
                        recarregar()
                        mensagem = ""
                        # mantém selecionado o povo que acabou de ser editado
                        # (o nome pode ter mudado, então procura pelo mais parecido)
                        selecionado = next(
                            (i for i, p in enumerate(meus)
                             if p["nome"].casefold() == nome_editado.casefold()), selecionado)
                elif meus and botao_excluir.collidepoint(pos):
                    if not confirmando:
                        confirmando = True
                    else:
                        sucesso, texto = excluir_povo(usuario["email"], meus[selecionado]["nome"])
                        confirmando = False
                        mensagem = texto
                        cor_mensagem = VERDE if sucesso else (255, 130, 130)
                        recarregar()
                else:
                    for caixa, indice in itens:
                        if caixa.collidepoint(pos):
                            selecionado = indice
                            confirmando = False

        itens = ajustar_lista()  # a lista pode ter mudado durante os eventos (editar/excluir)

        tela.fill(FUNDO)
        botao("VOLTAR", botao_voltar, mouse, fonte_pequena, CINZA)
        desenhar_centralizado("MEUS POVOS", fonte_titulo, BRANCO, 25)
        desenhar_texto("Informações que você adicionou:", fonte_pequena, BRANCO, 45, 95)

        for caixa, indice in itens:
            botao(meus[indice]["nome"], caixa, mouse, fonte_pequena,
                  VERDE if indice == selecionado else CINZA)
        if len(meus) > VISIVEIS:
            fim = min(inicio + VISIVEIS, len(meus))
            desenhar_texto(f"{inicio + 1}-{fim} de {len(meus)}", fonte_menor, CINZA_CLARO, 45, 422)
        botao("+ ADICIONAR POVO", botao_novo, mouse, fonte_pequena, VERDE)

        if meus:
            povo = meus[selecionado]
            desenhar_texto(povo["nome"], fonte_texto, BRANCO, 390, 100)
            y = 135
            y = desenhar_bloco("Região:", povo["regiao"], 390, y, 460)
            desenhar_bloco("Sobre:", povo["sobre"], 390, y, 460)
            botao("EDITAR", botao_editar, mouse, fonte_pequena, VERDE)
            botao("CONFIRMAR?" if confirmando else "EXCLUIR", botao_excluir, mouse, fonte_pequena)
            if confirmando:
                desenhar_texto("Clique de novo para excluir. Isso não pode ser desfeito.",
                               fonte_menor, CINZA_CLARO, 390, 508)
        else:
            desenhar_texto("Você ainda não adicionou nenhum povo.", fonte_pequena, BRANCO, 390, 130)
            desenhar_texto("Clique em + ADICIONAR POVO para começar.", fonte_menor, CINZA_CLARO, 390, 165)

        desenhar_mensagem(mensagem, 540, cor_mensagem)
        desenhar_texto("Setas ou rodinha: navegar | ESC: voltar", fonte_menor, CINZA_CLARO, 45, 570)
        pygame.display.flip()
