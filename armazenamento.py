"""Cadastro, validação e armazenamento local dos usuários."""
import hashlib
import json
import os
import re
from pathlib import Path

ARQUIVO = Path(__file__).resolve().parent / "usuarios.json"
REGEX_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")

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
