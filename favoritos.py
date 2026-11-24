"""Povos favoritados por cada usuário. Cada favorito é um par (e-mail da pessoa, nome do povo)."""
from armazenamento import ErroDeArmazenamento, carregar_favoritos, salvar_favoritos


def _chave(texto):
    return texto.strip().casefold()


def _e_da_pessoa(favorito, email):
    return isinstance(favorito, dict) and favorito.get("email") == email


def listar_favoritos(email):
    """Nomes dos povos que a pessoa favoritou, na ordem em que favoritou."""
    email = email.strip().lower()
    return [f["povo"] for f in carregar_favoritos()
            if _e_da_pessoa(f, email) and f.get("povo")]


def alternar_favorito(email, nome):
    """Favorita o povo se ainda não for favorito; se já for, remove. Retorna (sucesso, mensagem)."""
    email = email.strip().lower()
    nome = nome.strip()
    if not nome:
        return False, "Povo inválido."
    try:
        favoritos = carregar_favoritos()
        restantes = [f for f in favoritos
                     if not (_e_da_pessoa(f, email) and _chave(f.get("povo", "")) == _chave(nome))]
        if len(restantes) < len(favoritos):
            salvar_favoritos(restantes)
            return True, "Removido dos favoritos."
        restantes.append({"email": email, "povo": nome})
        salvar_favoritos(restantes)
        return True, "Adicionado aos favoritos!"
    except (ErroDeArmazenamento, TypeError, AttributeError) as erro:
        return False, str(erro)


# As funções abaixo mantêm os favoritos coerentes quando algo muda em outro lugar.

def renomear_povo(nome_antigo, nome_novo):
    """Quando o autor renomeia um povo, os favoritos de todos continuam apontando para ele."""
    favoritos = carregar_favoritos()
    mudou = False
    for f in favoritos:
        if isinstance(f, dict) and _chave(f.get("povo", "")) == _chave(nome_antigo):
            f["povo"] = nome_novo
            mudou = True
    if mudou:
        salvar_favoritos(favoritos)


def remover_povo(nome):
    """Quando um povo é excluído, ele sai dos favoritos de todos."""
    favoritos = carregar_favoritos()
    restantes = [f for f in favoritos
                 if not (isinstance(f, dict) and _chave(f.get("povo", "")) == _chave(nome))]
    if len(restantes) < len(favoritos):
        salvar_favoritos(restantes)


def remover_favoritos_do_usuario(email):
    """Apaga os favoritos de uma pessoa (usado quando a conta é excluída)."""
    email = email.strip().lower()
    favoritos = carregar_favoritos()
    restantes = [f for f in favoritos if not _e_da_pessoa(f, email)]
    if len(restantes) < len(favoritos):
        salvar_favoritos(restantes)
