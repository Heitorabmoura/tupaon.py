"""Hash e conferência de senhas (PBKDF2-SHA256 com sal)."""
import hashlib
import os

ITERACOES = 100_000


def _calcular(senha, salt):
    return hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, ITERACOES)


def gerar_hash(senha, salt=None):
    if salt is None:
        salt = os.urandom(16)
    return {"salt": salt.hex(), "hash": _calcular(senha, salt).hex()}


def senha_confere(senha, dados_senha):
    salt = bytes.fromhex(dados_senha["salt"])
    return _calcular(senha, salt).hex() == dados_senha["hash"]
