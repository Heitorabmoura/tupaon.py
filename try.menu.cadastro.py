 
import pygame
import hashlib
import json
import os
import re
from pathlib import Path


# ============================================================
# CONFIGURAÇÕES
# ============================================================

pygame.init()

LARGURA = 900
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tupã")

FUNDO = (30, 30, 30)
BRANCO = (255, 255, 255)
VERMELHO = (150, 30, 30)
VERMELHO_CLARO = (200, 50, 50)
VERDE = (50, 160, 70)

fonte_titulo = pygame.font.Font(None, 70)
fonte_texto = pygame.font.Font(None, 35)
fonte_pequena = pygame.font.Font(None, 28)

ARQUIVO = Path("usuarios.json")

REGEX_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


# ============================================================
# ARMAZENAMENTO
# ============================================================

class ErroDeArmazenamento(Exception):
    pass


def carregar_usuarios():
    if not ARQUIVO.exists():
        return []

    try:
        with ARQUIVO.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except json.JSONDecodeError:
        raise ErroDeArmazenamento(
            "O arquivo usuarios.json está corrompido."
        )

    except OSError as erro:
        raise ErroDeArmazenamento(
            f"Não foi possível ler o arquivo: {erro}"
        )


def salvar_usuarios(usuarios):
    try:
        with ARQUIVO.open("w", encoding="utf-8") as arquivo:
            json.dump(
                usuarios,
                arquivo,
                ensure_ascii=False,
                indent=2
            )

    except OSError as erro:
        raise ErroDeArmazenamento(
            f"Não foi possível salvar os usuários: {erro}"
        )


# ============================================================
# SEGURANÇA DA SENHA
# ============================================================

def gerar_hash(senha):
    salt = os.urandom(16)

    hash_senha = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode(),
        salt,
        100_000
    )

    return {
        "salt": salt.hex(),
        "hash": hash_senha.hex()
    }


# ============================================================
# VALIDAÇÕES
# ============================================================

def validar_nome(nome):
    if len(nome.strip()) < 3:
        return "O nome deve ter pelo menos 3 caracteres."

    return None


def validar_email(email):
    if not REGEX_EMAIL.match(email.strip()):
        return "E-mail inválido. Exemplo: nome@dominio.com"

    return None


def email_ja_cadastrado(email, usuarios):
    email = email.strip().lower()

    if any(usuario["email"] == email for usuario in usuarios):
        return "Já existe um usuário com esse e-mail."

    return None


def validar_senha(senha):
    if len(senha) < 8:
        return "A senha deve ter pelo menos 8 caracteres."

    if not any(caractere.isdigit() for caractere in senha):
        return "A senha deve ter pelo menos um número."

    if not any(caractere.isalpha() for caractere in senha):
        return "A senha deve ter pelo menos uma letra."

    return None


# ============================================================
# CADASTRO
# ============================================================

def cadastrar_usuario(nome, email, senha):

    nome = nome.strip()
    email = email.strip().lower()

    usuarios = carregar_usuarios()

    validacoes = [
        validar_nome(nome),
        validar_email(email),
        email_ja_cadastrado(email, usuarios),
        validar_senha(senha)
    ]

    for erro in validacoes:
        if erro:
            return False, erro

    usuarios.append({
        "nome": nome,
        "email": email,
        "senha": gerar_hash(senha)
    })

    salvar_usuarios(usuarios)

    return True, "Usuário cadastrado com sucesso!"


# ============================================================
# FUNÇÕES DO PYGAME
# ============================================================

def desenhar_texto(texto, fonte, cor, x, y):
    imagem = fonte.render(texto, True, cor)
    tela.blit(imagem, (x, y))


def campo_texto(rotulo, valor, x, y, ativo):
    desenhar_texto(
        rotulo,
        fonte_pequena,
        BRANCO,
        x,
        y
    )

    caixa = pygame.Rect(x, y + 30, 400, 45)

    cor = VERDE if ativo else BRANCO

    pygame.draw.rect(tela, cor, caixa, 2)

    texto = fonte_pequena.render(valor, True, BRANCO)

    tela.blit(texto, (x + 10, y + 40))

    return caixa


# ============================================================
# TELA DE CADASTRO
# ============================================================

def tela_cadastro():

    nome = ""
    email = ""
    senha = ""
    confirmar_senha = ""

    campo_atual = "nome"

    mensagem = ""

    executando = True

    while executando:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:

                # ENTER muda para o próximo campo
                if evento.key == pygame.K_RETURN:

                    if campo_atual == "nome":
                        campo_atual = "email"

                    elif campo_atual == "email":
                        campo_atual = "senha"

                    elif campo_atual == "senha":
                        campo_atual = "confirmar"

                    elif campo_atual == "confirmar":

                        sucesso, mensagem = cadastrar_usuario(
                            nome,
                            email,
                            senha
                        )

                        if sucesso:
                            return

                # BACKSPACE apaga
                elif evento.key == pygame.K_BACKSPACE:

                    if campo_atual == "nome":
                        nome = nome[:-1]

                    elif campo_atual == "email":
                        email = email[:-1]

                    elif campo_atual == "senha":
                        senha = senha[:-1]

                    elif campo_atual == "confirmar":
                        confirmar_senha = confirmar_senha[:-1]

                else:

                    if evento.unicode:

                        if campo_atual == "nome":
                            nome += evento.unicode

                        elif campo_atual == "email":
                            email += evento.unicode

                        elif campo_atual == "senha":
                            senha += evento.unicode

                        elif campo_atual == "confirmar":
                            confirmar_senha += evento.unicode

            # Clique do mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:

                posicao = evento.pos

                caixa_nome = pygame.Rect(250, 160, 400, 45)
                caixa_email = pygame.Rect(250, 240, 400, 45)
                caixa_senha = pygame.Rect(250, 320, 400, 45)
                caixa_confirmar = pygame.Rect(250, 400, 400, 45)

                if caixa_nome.collidepoint(posicao):
                    campo_atual = "nome"

                elif caixa_email.collidepoint(posicao):
                    campo_atual = "email"

                elif caixa_senha.collidepoint(posicao):
                    campo_atual = "senha"

                elif caixa_confirmar.collidepoint(posicao):
                    campo_atual = "confirmar"

        # ====================================================
        # DESENHO
        # ====================================================

        tela.fill(FUNDO)

        titulo = fonte_titulo.render(
            "CRIAR CONTA",
            True,
            BRANCO
        )

        tela.blit(titulo, (315, 60))

        campo_texto(
            "Nome",
            nome,
            250,
            130,
            campo_atual == "nome"
        )

        campo_texto(
            "E-mail",
            email,
            250,
            210,
            campo_atual == "email"
        )

        campo_texto(
            "Senha",
            "*" * len(senha),
            250,
            290,
            campo_atual == "senha"
        )

        campo_texto(
            "Confirmar senha",
            "*" * len(confirmar_senha),
            250,
            370,
            campo_atual == "confirmar"
        )

        if mensagem:
            desenhar_texto(
                mensagem,
                fonte_pequena,
                (255, 100, 100),
                250,
                470
            )

        desenhar_texto(
            "ENTER = próximo campo",
            fonte_pequena,
            BRANCO,
            250,
            520
        )

        pygame.display.update()


# ============================================================
# MENU PRINCIPAL
# ============================================================

botao_cadastro = pygame.Rect(300, 250, 300, 60)
botao_login = pygame.Rect(300, 330, 300, 60)
botao_sair = pygame.Rect(300, 410, 300, 60)

rodando = True

while rodando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:

            if botao_cadastro.collidepoint(evento.pos):

                tela_cadastro()

            if botao_login.collidepoint(evento.pos):

                print("RF2 - Login")

            if botao_sair.collidepoint(evento.pos):

                rodando = False

    tela.fill(FUNDO)

    titulo = fonte_titulo.render(
        "TUPÃ",
        True,
        BRANCO
    )

    tela.blit(titulo, (350, 100))

    mouse = pygame.mouse.get_pos()

    cor = (
        VERMELHO_CLARO
        if botao_cadastro.collidepoint(mouse)
        else VERMELHO
    )

    pygame.draw.rect(
        tela,
        cor,
        botao_cadastro
    )

    texto = fonte_texto.render(
        "CRIAR CONTA",
        True,
        BRANCO
    )

    tela.blit(texto, (365, 265))

    cor = (
        VERMELHO_CLARO
        if botao_login.collidepoint(mouse)
        else VERMELHO
    )

    pygame.draw.rect(
        tela,
        cor,
        botao_login
    )

    texto = fonte_texto.render(
        "LOGIN",
        True,
        BRANCO
    )

    tela.blit(texto, (410, 345))

    cor = (
        VERMELHO_CLARO
        if botao_sair.collidepoint(mouse)
        else VERMELHO
    )

    pygame.draw.rect(
        tela,
        cor,
        botao_sair
    )

    texto = fonte_texto.render(
        "SAIR",
        True,
        BRANCO
    )

    tela.blit(texto, (425, 425))

    pygame.display.update()

pygame.quit()

