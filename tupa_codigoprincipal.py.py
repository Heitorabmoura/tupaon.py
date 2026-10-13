import pygame
import hashlib
import json
import os
import re
from pathlib import Path

pygame.init()

# CONFIGURAÇÕES

LARGURA = 900
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tupã")

FUNDO = (30, 30, 30)
BRANCO = (255, 255, 255)
VERMELHO = (150, 30, 30)
VERMELHO_CLARO = (200, 50, 50)
VERDE = (50, 160, 70)
CINZA = (90, 90, 90)
CINZA_CLARO = (190, 190, 190)

fonte_titulo = pygame.font.Font(None, 62)
fonte_texto = pygame.font.Font(None, 32)
fonte_pequena = pygame.font.Font(None, 25)
fonte_menor = pygame.font.Font(None, 21)

ARQUIVO = Path("usuarios.json")
REGEX_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")

# ARMAZENAMENTO E SEGURANÇA

class ErroDeArmazenamento(Exception):
    pass


def carregar_usuarios():
    if not ARQUIVO.exists():
        return []
    try:
        with ARQUIVO.open("r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)
        if not isinstance(usuarios, list):
            raise ErroDeArmazenamento("O arquivo usuarios.json precisa conter uma lista de usuários.")
        return usuarios
    except (json.JSONDecodeError, OSError) as erro:
        raise ErroDeArmazenamento(f"Não foi possível ler usuarios.json: {erro}")


def salvar_usuarios(usuarios):
    try:
        with ARQUIVO.open("w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, ensure_ascii=False, indent=2)
    except OSError as erro:
        raise ErroDeArmazenamento(f"Não foi possível salvar os usuários: {erro}")


def gerar_hash(senha, salt=None):
    if salt is None:
        salt = os.urandom(16)
    hash_senha = hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), salt, 100_000
    )
    return {"salt": salt.hex(), "hash": hash_senha.hex()}


def senha_confere(senha, dados_senha):
    salt = bytes.fromhex(dados_senha["salt"])
    hash_calculado = hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), salt, 100_000
    )
    return hash_calculado.hex() == dados_senha["hash"]


def validar_senha(senha):
    if len(senha) < 8:
        return "A senha deve ter pelo menos 8 caracteres."
    if not any(c.isdigit() for c in senha):
        return "A senha deve ter pelo menos um número."
    if not any(c.isalpha() for c in senha):
        return "A senha deve ter pelo menos uma letra."
    return None


def cadastrar_usuario(nome, email, senha):
    nome = nome.strip()
    email = email.strip().lower()

    if len(nome) < 3:
        return False, "O nome deve ter pelo menos 3 caracteres."
    if not REGEX_EMAIL.match(email):
        return False, "E-mail inválido. Exemplo: nome@dominio.com"
    erro_senha = validar_senha(senha)
    if erro_senha:
        return False, erro_senha
    try:
        usuarios = carregar_usuarios()
        if any(u.get("email", "").lower() == email for u in usuarios):
            return False, "Já existe uma conta com esse e-mail."
        usuarios.append({
            "nome": nome,
            "email": email,
            "senha": gerar_hash(senha)
        })
        salvar_usuarios(usuarios)
        return True, "Conta criada com sucesso!"
    except (ErroDeArmazenamento, KeyError, TypeError) as erro:
        return False, str(erro)


def verificar_login(email, senha):
    email = email.strip().lower()
    if not REGEX_EMAIL.match(email):
        return False, "Digite um e-mail válido."
    try:
        usuarios = carregar_usuarios()
        for usuario in usuarios:
            if not isinstance(usuario, dict):
                continue
            if usuario.get("email", "").lower() == email:
                if senha_confere(senha, usuario["senha"]):
                    return True, usuario.get("nome", "Usuário")
                return False, "Senha incorreta."
        return False, "Não existe conta com esse e-mail."
    except (ErroDeArmazenamento, KeyError, TypeError, ValueError) as erro:
        return False, str(erro)


# FUNÇÕES VISUAIS

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


# TELA DE CADASTRO

def tela_cadastro():
    nome = ""
    email = ""
    senha = ""
    confirmar = ""
    campo_atual = 0
    mostrar_senha = False
    mensagem = ""

    campos = [
        pygame.Rect(250, 135, 400, 42),
        pygame.Rect(250, 220, 400, 42),
        pygame.Rect(250, 305, 320, 42),
        pygame.Rect(250, 390, 320, 42),
    ]
    botao_voltar = pygame.Rect(30, 25, 130, 42)
    botao_mostrar = pygame.Rect(585, 305, 120, 42)
    botao_mostrar_confirmar = pygame.Rect(585, 390, 120, 42)
    botao_criar = pygame.Rect(330, 465, 240, 45)

    while True:
        mouse = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                if evento.key == pygame.K_TAB:
                    campo_atual = (campo_atual + 1) % 4
                elif evento.key == pygame.K_RETURN:
                    if campo_atual < 3:
                        campo_atual += 1
                    else:
                        if senha != confirmar:
                            mensagem = "As senhas não são iguais."
                        else:
                            sucesso, mensagem = cadastrar_usuario(nome, email, senha)
                            if sucesso:
                                mensagem = "Conta criada! Voltando ao menu..."
                                tela.fill(FUNDO)
                                desenhar_centralizado("CRIAR CONTA", fonte_titulo, BRANCO, 60)
                                desenhar_mensagem(mensagem, 290, VERDE)
                                pygame.display.flip()
                                pygame.time.wait(900)
                                return
                elif evento.key == pygame.K_BACKSPACE:
                    if campo_atual == 0:
                        nome = nome[:-1]
                    elif campo_atual == 1:
                        email = email[:-1]
                    elif campo_atual == 2:
                        senha = senha[:-1]
                    else:
                        confirmar = confirmar[:-1]
                elif evento.unicode and evento.unicode.isprintable():
                    if campo_atual == 0:
                        nome += evento.unicode
                    elif campo_atual == 1:
                        email += evento.unicode
                    elif campo_atual == 2:
                        senha += evento.unicode
                    else:
                        confirmar += evento.unicode

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                if botao_voltar.collidepoint(pos):
                    return
                if botao_mostrar.collidepoint(pos) or botao_mostrar_confirmar.collidepoint(pos):
                    mostrar_senha = not mostrar_senha
                elif botao_criar.collidepoint(pos):
                    if senha != confirmar:
                        mensagem = "As senhas não são iguais."
                    else:
                        sucesso, mensagem = cadastrar_usuario(nome, email, senha)
                        if sucesso:
                            tela.fill(FUNDO)
                            desenhar_centralizado("CRIAR CONTA", fonte_titulo, BRANCO, 60)
                            desenhar_mensagem("Conta criada com sucesso!", 290, VERDE)
                            pygame.display.flip()
                            pygame.time.wait(900)
                            return
                else:
                    for i, caixa in enumerate(campos):
                        if caixa.collidepoint(pos):
                            campo_atual = i

        tela.fill(FUNDO)
        botao("VOLTAR", botao_voltar, mouse, fonte_pequena, CINZA)
        desenhar_centralizado("CRIAR CONTA", fonte_titulo, BRANCO, 45)

        valores = [nome, email, senha, confirmar]
        rotulos = ["Nome", "E-mail", "Senha", "Confirmar senha"]
        for i, caixa in enumerate(campos):
            campo_texto(rotulos[i], valores[i], caixa, campo_atual == i,
                        ocultar=(i in (2, 3) and not mostrar_senha))

        botao("OCULTAR" if mostrar_senha else "MOSTRAR", botao_mostrar, mouse, fonte_menor, CINZA)
        botao("OCULTAR" if mostrar_senha else "MOSTRAR", botao_mostrar_confirmar, mouse, fonte_menor, CINZA)
        botao("CRIAR CONTA", botao_criar, mouse)
        desenhar_texto("ENTER: próximo campo | ESC: voltar", fonte_menor, CINZA_CLARO, 250, 525)
        desenhar_mensagem(mensagem, 555)
        pygame.display.flip()


# RF2 - TELA DE LOGIN

def tela_login():
    email = ""
    senha = ""
    campo_atual = 0
    mostrar_senha = False
    mensagem = ""
    botao_voltar = pygame.Rect(30, 25, 130, 42)
    caixa_email = pygame.Rect(250, 220, 400, 45)
    caixa_senha = pygame.Rect(250, 315, 320, 45)
    botao_mostrar = pygame.Rect(585, 315, 120, 45)
    botao_entrar = pygame.Rect(330, 405, 240, 48)

    while True:
        mouse = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                if evento.key == pygame.K_TAB:
                    campo_atual = 1 - campo_atual
                elif evento.key == pygame.K_RETURN:
                    if campo_atual == 0:
                        campo_atual = 1
                    else:
                        sucesso, resultado = verificar_login(email, senha)
                        if sucesso:
                            tela_principal_usuario(resultado)
                            return
                        mensagem = resultado
                elif evento.key == pygame.K_BACKSPACE:
                    if campo_atual == 0:
                        email = email[:-1]
                    else:
                        senha = senha[:-1]
                elif evento.unicode and evento.unicode.isprintable():
                    if campo_atual == 0:
                        email += evento.unicode
                    else:
                        senha += evento.unicode

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                if botao_voltar.collidepoint(pos):
                    return
                if botao_mostrar.collidepoint(pos):
                    mostrar_senha = not mostrar_senha
                elif botao_entrar.collidepoint(pos):
                    sucesso, resultado = verificar_login(email, senha)
                    if sucesso:
                        tela_principal_usuario(resultado)
                        return
                    mensagem = resultado
                elif caixa_email.collidepoint(pos):
                    campo_atual = 0
                elif caixa_senha.collidepoint(pos):
                    campo_atual = 1

        tela.fill(FUNDO)
        botao("VOLTAR", botao_voltar, mouse, fonte_pequena, CINZA)
        desenhar_centralizado("LOGIN", fonte_titulo, BRANCO, 75)
        campo_texto("E-mail", email, caixa_email, campo_atual == 0)
        campo_texto("Senha", senha, caixa_senha, campo_atual == 1, ocultar=not mostrar_senha)
        botao("OCULTAR" if mostrar_senha else "MOSTRAR", botao_mostrar, mouse, fonte_menor, CINZA)
        botao("ENTRAR", botao_entrar, mouse)
        desenhar_texto("ENTER: avançar/entrar | ESC: voltar", fonte_menor, CINZA_CLARO, 250, 480)
        desenhar_mensagem(mensagem, 530)
        pygame.display.flip()


def tela_principal_usuario(nome):
    while True:
        mouse = pygame.mouse.get_pos()
        botao_sair = pygame.Rect(330, 360, 240, 50)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_sair.collidepoint(evento.pos):
                    return

        tela.fill(FUNDO)
        desenhar_centralizado(f"OLÁ, {nome.upper()}!", fonte_titulo, BRANCO, 145)
        desenhar_centralizado("Login realizado com sucesso.", fonte_texto, VERDE, 235)
        botao("VOLTAR AO MENU", botao_sair, mouse)
        pygame.display.flip()


# Área de pesquisa

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


# Quiz

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


# MENU PRINCIPAL

def menu_principal():
    botoes = {
        "cadastro": pygame.Rect(300, 205, 300, 55),
        "login": pygame.Rect(300, 275, 300, 55),
        "pesquisas": pygame.Rect(300, 345, 300, 55),
        "quiz": pygame.Rect(300, 415, 300, 55),
        "sair": pygame.Rect(300, 485, 300, 50),
    }

    while True:
        mouse = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                encerrar()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botoes["cadastro"].collidepoint(evento.pos):
                    tela_cadastro()
                elif botoes["login"].collidepoint(evento.pos):
                    tela_login()
                elif botoes["pesquisas"].collidepoint(evento.pos):
                    tela_pesquisas()
                elif botoes["quiz"].collidepoint(evento.pos):
                    tela_quiz()
                elif botoes["sair"].collidepoint(evento.pos):
                    return

        tela.fill(FUNDO)
        desenhar_centralizado("TUPÃ", fonte_titulo, BRANCO, 65)
        desenhar_centralizado("Conhecimento e valorização dos povos originários", fonte_menor, CINZA_CLARO, 135)
        botao("CRIAR CONTA", botoes["cadastro"], mouse)
        botao("LOGIN", botoes["login"], mouse)
        botao("PESQUISAR POVOS", botoes["pesquisas"], mouse)
        botao("QUIZ", botoes["quiz"], mouse)
        botao("SAIR", botoes["sair"], mouse, fonte_pequena, CINZA)
        pygame.display.flip()


if __name__ == "__main__":
    try:
        menu_principal()
    finally:
        pygame.quit()
