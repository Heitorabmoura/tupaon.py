import pygame

pygame.init()

# Tamanho da janela
LARGURA = 900
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tupã")

# Cores
FUNDO = (30, 30, 30)
BRANCO = (255, 255, 255)
VERMELHO = (150, 30, 30)
VERMELHO_CLARO = (200, 50, 50)

# Fontes
fonte_titulo = pygame.font.Font(None, 80)
fonte_botao = pygame.font.Font(None, 40)

# Botões
botao_cadastro = pygame.Rect(300, 250, 300, 60)
botao_login = pygame.Rect(300, 330, 300, 60)
botao_sair = pygame.Rect(300, 410, 300, 60)

rodando = True

while rodando:

    # Verifica eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        # Clique do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:

            if botao_cadastro.collidepoint(evento.pos):
                print ("RF1 - Criar conta")

            if botao_login.collidepoint(evento.pos):
                print ("RF2 - Login")

            if botao_sair.collidepoint(evento.pos):
                rodando = False

    # Fundo
    tela.fill(FUNDO)

    # Título
    titulo = fonte_titulo.render("TUPÃ", True, BRANCO)
    tela.blit(titulo, (350, 100))

    # Mouse
    mouse = pygame.mouse.get_pos()

    # Botão cadastro
    cor = VERMELHO_CLARO if botao_cadastro.collidepoint(mouse) else VERMELHO
    pygame.draw.rect(tela, cor, botao_cadastro)

    texto = fonte_botao.render("CRIAR CONTA", True, BRANCO)
    tela.blit(texto, (365, 265))

    # Botão login
    cor = VERMELHO_CLARO if botao_login.collidepoint(mouse) else VERMELHO
    pygame.draw.rect(tela, cor, botao_login)

    texto = fonte_botao.render("LOGIN", True, BRANCO)
    tela.blit(texto, (410, 345))

    # Botão sair
    cor = VERMELHO_CLARO if botao_sair.collidepoint(mouse) else VERMELHO
    pygame.draw.rect(tela, cor, botao_sair)

    texto = fonte_botao.render("SAIR", True, BRANCO)
    tela.blit(texto, (425, 425))

    pygame.display.update()

pygame.quit()