"""Leitura e gravação dos arquivos JSON. Não conhece regras de negócio."""
import json
import os
from pathlib import Path

PASTA = Path(__file__).resolve().parent
ARQUIVO = PASTA / "usuarios.json"
ARQUIVO_POVOS = PASTA / "povos_usuarios.json"


class ErroDeArmazenamento(Exception):
    pass


def _ler_lista(caminho):
    if not caminho.exists():
        return []
    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        if not isinstance(dados, list):
            raise ErroDeArmazenamento(f"O arquivo {caminho.name} precisa conter uma lista.")
        return dados
    except (json.JSONDecodeError, OSError) as erro:
        raise ErroDeArmazenamento(f"Não foi possível ler {caminho.name}: {erro}")


def _gravar_lista(caminho, dados):
    """Grava em arquivo temporário e troca no final, para não corromper o JSON se algo falhar."""
    temporario = caminho.with_suffix(".tmp")
    try:
        with temporario.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        os.replace(temporario, caminho)
    except OSError as erro:
        raise ErroDeArmazenamento(f"Não foi possível salvar {caminho.name}: {erro}")


def carregar_usuarios():
    return _ler_lista(ARQUIVO)


def salvar_usuarios(usuarios):
    _gravar_lista(ARQUIVO, usuarios)


def carregar_povos_usuarios():
    return _ler_lista(ARQUIVO_POVOS)


def salvar_povos_usuarios(povos):
    _gravar_lista(ARQUIVO_POVOS, povos)
