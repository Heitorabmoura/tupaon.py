"""RF001 - Cadastro de usuário (versão de terminal).

Fluxo principal: pede nome, e-mail e senha, valida e salva em usuarios.json.

Fluxos alternativos / de erro:
  - Dado inválido (nome, e-mail ou senha): mostra o motivo e pede o dado
    de novo, quantas vezes for preciso, até o usuário corrigir.
  - E-mail já cadastrado: avisa e pede outro e-mail.
  - Senhas diferentes: avisa e pede a senha de novo.
  - Arquivo de dados corrompido ou sem permissão: mostra erro claro
    e encerra sem apagar nada.
  - Ctrl+C: cancela o cadastro com uma mensagem, sem quebrar o programa.
"""

import getpass
import hashlib
import json
import os
import re
from pathlib import Path

ARQUIVO = Path("usuarios.json")
REGEX_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


class ErroDeArmazenamento(Exception):
    """Problema ao ler ou gravar o arquivo de usuários."""


#Persistência
def carregar_usuarios() -> list[dict]:
    if not ARQUIVO.exists():
        return []
    try:
        with ARQUIVO.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ErroDeArmazenamento(
            f"O arquivo {ARQUIVO} está corrompido. "
            "Corrija ou apague o arquivo e tente de novo."
        )
    except OSError as e:
        raise ErroDeArmazenamento(f"Não foi possível ler {ARQUIVO}: {e}")


def salvar_usuarios(usuarios: list[dict]) -> None:
    try:
        with ARQUIVO.open("w", encoding="utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise ErroDeArmazenamento(f"Não foi possível salvar em {ARQUIVO}: {e}")


#Segurança
def gerar_hash(senha: str) -> dict:
    """Nunca guardamos a senha pura: guardamos salt + hash."""
    salt = os.urandom(16)
    hash_senha = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, 100_000)
    return {"salt": salt.hex(), "hash": hash_senha.hex()}


#Validações (cada uma retorna mensagem de erro ou None)
def validar_nome(nome: str) -> str | None:
    if len(nome.strip()) < 3:
        return "O nome deve ter pelo menos 3 caracteres."
    return None


def validar_email(email: str) -> str | None:
    if not REGEX_EMAIL.match(email.strip()):
        return "E-mail em formato inválido (exemplo: nome@dominio.com)."
    return None


def email_ja_cadastrado(email: str, usuarios: list[dict]) -> str | None:
    email = email.strip().lower()
    if any(u["email"] == email for u in usuarios):
        return "Já existe um usuário cadastrado com esse e-mail."
    return None


def validar_senha(senha: str) -> str | None:
    if len(senha) < 8:
        return "A senha deve ter pelo menos 8 caracteres."
    if not any(c.isdigit() for c in senha):
        return "A senha deve ter pelo menos um número."
    if not any(c.isalpha() for c in senha):
        return "A senha deve ter pelo menos uma letra."
    return None


#Regra de negócio
def cadastrar_usuario(nome: str, email: str, senha: str) -> tuple[bool, str]:
    """Valida tudo de novo (última barreira) e grava o usuário."""
    nome, email = nome.strip(), email.strip().lower()
    usuarios = carregar_usuarios()

    for erro in (
        validar_nome(nome),
        validar_email(email),
        email_ja_cadastrado(email, usuarios),
        validar_senha(senha),
    ):
        if erro:
            return False, erro

    usuarios.append({"nome": nome, "email": email, "senha": gerar_hash(senha)})
    salvar_usuarios(usuarios)
    return True, "Usuário cadastrado com sucesso!"


#Interface: pede de novo até o usuário acertar
def pedir_campo(texto: str, validadores: list) -> str:
    """Repete a pergunta até que TODOS os validadores aprovem o valor."""
    while True:
        valor = input(texto)
        for validar in validadores:
            erro = validar(valor)
            if erro:
                print(f"  ✗ {erro} Tente novamente.\n")
                break
        else:
            return valor


def pedir_senha() -> str:
    """Pede a senha e a confirmação, repetindo até ficarem válidas e iguais."""
    while True:
        senha = getpass.getpass("Senha: ")
        erro = validar_senha(senha)
        if erro:
            print(f"  ✗ {erro} Tente novamente.\n")
            continue

        confirmacao = getpass.getpass("Confirme a senha: ")
        if senha != confirmacao:
            print("  ✗ As senhas não conferem. Digite novamente.\n")
            continue

        return senha


def main() -> None:
    print("=== Cadastro de usuário === (Ctrl+C para cancelar)\n")
    try:
        usuarios = carregar_usuarios()

        nome = pedir_campo("Nome: ", [validar_nome])
        email = pedir_campo(
            "E-mail: ",
            [validar_email, lambda e: email_ja_cadastrado(e, usuarios)],
        )
        senha = pedir_senha()

        sucesso, mensagem = cadastrar_usuario(nome, email, senha)
        print(("\nV " if sucesso else "\nX ") + mensagem)

    except ErroDeArmazenamento as e:
        print(f"\nX Erro: {e}")
    except (KeyboardInterrupt, EOFError):
        print("\n\nCadastro cancelado pelo usuário.")


if __name__ == "__main__":
    main()