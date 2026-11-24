"""Quem tem poder de administrador no Tupã.

A lista fica aqui, em um só lugar. Administradores podem remover povos adicionados por qualquer usuário.
Observação: o app não confirma que o e-mail pertence a quem o digitou; isso serve para uso local/acadêmico.
"""

ADMINISTRADORES = frozenset({
    "heitor.alves@ufrpe.br",
    "ivan.guilherme@ufrpe.br",
})


def eh_administrador(email):
    """True se o e-mail (sem diferenciar maiúsculas) estiver na lista de administradores."""
    return isinstance(email, str) and email.strip().lower() in ADMINISTRADORES
