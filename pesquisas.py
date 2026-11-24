"""Tela de pesquisa de povos indígenas, com favoritos para quem estiver logado."""
import pygame
from configuracoes import (
    tela, FUNDO, BRANCO, VERDE, VERMELHO, CINZA, CINZA_CLARO,
    fonte_titulo, fonte_texto, fonte_pequena, fonte_menor
)
from armazenamento import ErroDeArmazenamento
from favoritos import alternar_favorito, listar_favoritos
from interface import (botao, botao_estrela, cortar_texto, desenhar_estrela,
                       desenhar_texto, desenhar_centralizado, desenhar_mensagem, encerrar)
from painel_povo import desenhar_aba, desenhar_sobre, retangulos_abas, tem_extras, ABAS
from permissoes import eh_administrador
from povos import excluir_povo_como_admin, obter_povos

COR_ERRO = (255, 130, 130)


def tela_pesquisas(usuario=None, so_favoritos=False):
    """usuario: {"nome": ..., "email": ...} de quem está logado, ou None (visitante, sem favoritos).
    so_favoritos: abre a tela já filtrando apenas os povos favoritados."""
    todos = obter_povos()
    favoritos = set()          # nomes (em minúsculas) dos povos favoritados pela pessoa
    mensagem = ""
    cor_mensagem = COR_ERRO
    busca = ""
    selecionado = 0
    inicio = 0                 # primeiro povo visível na lista da esquerda
    aba = 0                    # 0 Sobre, 1 Palavras, 2 Narrativas
    povo_da_aba = None         # nome do povo a que a aba escolhida se refere
    e_admin = bool(usuario) and eh_administrador(usuario["email"])
    confirmando_remocao = False
    VISIVEIS = 4
    botao_voltar = pygame.Rect(25, 22, 125, 42)
    caixa_busca = pygame.Rect(210, 95, 480, 42)
    botao_filtro = pygame.Rect(705, 95, 170, 42)
    botao_fav = pygame.Rect(300, 168, 40, 40)
    botao_remover = pygame.Rect(45, 505, 210, 40)   # só aparece para administradores

    def recarregar_favoritos():
        nonlocal favoritos, mensagem, cor_mensagem
        if not usuario:
            return
        try:
            favoritos = {nome.casefold() for nome in listar_favoritos(usuario["email"])}
        except ErroDeArmazenamento as erro:
            favoritos = set()
            mensagem, cor_mensagem = str(erro), COR_ERRO

    recarregar_favoritos()

    while True:
        mouse = pygame.mouse.get_pos()
        encontrados = [p for p in todos
                       if busca.lower() in p["nome"].lower()
                       and (not so_favoritos or p["nome"].casefold() in favoritos)]
        total_favoritos = sum(1 for p in todos if p["nome"].casefold() in favoritos)
        if encontrados:
            selecionado = max(0, min(selecionado, len(encontrados) - 1))
        else:
            selecionado = 0
        if selecionado < inicio:
            inicio = selecionado
        elif selecionado >= inicio + VISIVEIS:
            inicio = selecionado - VISIVEIS + 1
        inicio = max(0, min(inicio, max(0, len(encontrados) - VISIVEIS)))

        povo_atual = encontrados[selecionado] if encontrados else None
        if povo_atual and povo_atual["nome"] != povo_da_aba:
            aba, povo_da_aba = 0, povo_atual["nome"]       # outro povo: volta para a aba Sobre
            confirmando_remocao = False
        abas_visiveis = bool(povo_atual) and tem_extras(povo_atual)
        mostra_remover = e_admin and bool(povo_atual) and povo_atual["comunidade"]

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
                elif evento.key == pygame.K_LEFT and abas_visiveis:
                    aba = (aba - 1) % len(ABAS)
                elif evento.key == pygame.K_RIGHT and abas_visiveis:
                    aba = (aba + 1) % len(ABAS)
                elif evento.unicode and evento.unicode.isprintable():
                    busca += evento.unicode
                    selecionado = inicio = 0
            if evento.type == pygame.MOUSEWHEEL and encontrados:
                selecionado = max(0, min(len(encontrados) - 1, selecionado - evento.y))
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                if botao_voltar.collidepoint(pos):
                    return
                if usuario and botao_filtro.collidepoint(pos):
                    so_favoritos = not so_favoritos
                    selecionado = inicio = 0
                    mensagem = ""
                elif mostra_remover and botao_remover.collidepoint(pos):
                    if not confirmando_remocao:
                        confirmando_remocao = True      # primeiro clique só pede confirmação
                    else:
                        sucesso, texto = excluir_povo_como_admin(usuario["email"], povo_atual["nome"])
                        confirmando_remocao = False
                        mensagem = texto
                        cor_mensagem = VERDE if sucesso else COR_ERRO
                        if sucesso:
                            todos = obter_povos()
                            recarregar_favoritos()
                elif encontrados and botao_fav.collidepoint(pos):
                    if not usuario:
                        mensagem, cor_mensagem = "Entre na sua conta (LOGIN) para favoritar povos.", COR_ERRO
                    else:
                        sucesso, texto = alternar_favorito(usuario["email"], encontrados[selecionado]["nome"])
                        mensagem = texto
                        cor_mensagem = VERDE if sucesso else COR_ERRO
                        recarregar_favoritos()
                else:
                    clicou_aba = False
                    if abas_visiveis:
                        for i, retangulo in enumerate(retangulos_abas()):
                            if retangulo.collidepoint(pos):
                                aba, clicou_aba = i, True
                    if not clicou_aba:
                        for caixa, indice in botoes_povos:
                            if caixa.collidepoint(pos):
                                selecionado = indice

        tela.fill(FUNDO)
        botao("VOLTAR", botao_voltar, mouse, fonte_pequena, CINZA)
        desenhar_centralizado("PESQUISAR POVOS", fonte_titulo, BRANCO, 25)
        desenhar_texto("Digite o nome de um povo:", fonte_pequena, BRANCO, 210, 65)
        pygame.draw.rect(tela, VERDE, caixa_busca, 2, border_radius=5)
        desenhar_texto(busca, fonte_pequena, BRANCO, caixa_busca.x + 10, caixa_busca.y + 8)
        if usuario:
            botao(f"FAVORITOS ({total_favoritos})", botao_filtro, mouse, fonte_pequena,
                  VERDE if so_favoritos else CINZA)

        for caixa, indice in botoes_povos:
            povo = encontrados[indice]
            cor = VERDE if indice == selecionado else VERMELHO
            favorito_item = povo["nome"].casefold() in favoritos
            largura_texto = caixa.width - (68 if favorito_item else 20)
            botao(cortar_texto(povo["nome"], fonte_pequena, largura_texto), caixa, mouse, fonte_pequena, cor)
            if favorito_item:
                desenhar_estrela((caixa.x + 20, caixa.centery), 9, True)
        if len(encontrados) > VISIVEIS:
            fim = min(inicio + VISIVEIS, len(encontrados))
            desenhar_texto(f"{inicio + 1}-{fim} de {len(encontrados)}", fonte_menor, CINZA_CLARO, 45, 478)
        if e_admin and encontrados and encontrados[selecionado]["comunidade"]:
            botao("CONFIRMAR REMOÇÃO?" if confirmando_remocao else "REMOVER POVO (ADM)",
                  botao_remover, mouse, fonte_menor)
            if confirmando_remocao:
                desenhar_texto("Clique de novo para remover.", fonte_menor, CINZA_CLARO, 45, 549)

        if encontrados:
            povo = encontrados[selecionado]
            com_abas = tem_extras(povo)
            botao_estrela(botao_fav, povo["nome"].casefold() in favoritos, mouse)
            x_nome = botao_fav.right + 12
            desenhar_texto(povo["nome"], fonte_texto, BRANCO, x_nome, 178)
            y = 220
            if com_abas:
                desenhar_aba(povo, aba, mouse)
            elif povo["comunidade"]:
                etiqueta = "adicionado por usuário"
                x_etiqueta = x_nome + fonte_texto.size(povo["nome"])[0] + 15
                if x_etiqueta + fonte_menor.size(etiqueta)[0] <= 890:
                    desenhar_texto(etiqueta, fonte_menor, CINZA_CLARO, x_etiqueta, 184)
                else:  # nome muito longo: a etiqueta vai para baixo dele
                    desenhar_texto(etiqueta, fonte_menor, CINZA_CLARO, x_nome, 208)
                    y = 232
            if not com_abas:
                desenhar_sobre(povo, y)
        elif so_favoritos and not busca:
            desenhar_texto("Você ainda não favoritou nenhum povo.", fonte_pequena, BRANCO, 300, 220)
            desenhar_texto("Desative o filtro FAVORITOS e clique na estrela ao lado do nome de um povo.",
                           fonte_menor, CINZA_CLARO, 300, 250)
        else:
            desenhar_texto("Nenhum povo encontrado com esse nome.", fonte_pequena, BRANCO, 300, 220)

        desenhar_mensagem(mensagem, 543, cor_mensagem)
        desenhar_texto("Cima/Baixo: povos | Esq/Dir: abas | Estrela: favoritar | ESC: voltar",
                       fonte_menor, CINZA_CLARO, 45, 570)
        pygame.display.flip()
