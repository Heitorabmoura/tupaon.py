"""Povos indígenas: conteúdo base do Tupã e as informações adicionadas pelos usuários."""
from armazenamento import (
    ErroDeArmazenamento, carregar_povos_usuarios, salvar_povos_usuarios
)
from validacao import erros_povo, resumir_erros

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


def obter_povos():
    """Conteúdo base + povos dos usuários (estes marcados com comunidade=True)."""
    povos = [dict(p, comunidade=False) for p in POVOS]
    try:
        extras = carregar_povos_usuarios()
    except ErroDeArmazenamento:
        return povos
    validos = [e for e in extras if isinstance(e, dict) and e.get("nome")]
    for e in sorted(validos, key=lambda p: p["nome"].casefold()):
        povos.append({
            "nome": e["nome"],
            "regiao": e.get("regiao", ""),
            "sobre": e.get("sobre", ""),
            "cuidado": e.get("cuidado", ""),
            "comunidade": True,
        })
    return povos


def listar_povos_do_usuario(email):
    email = email.strip().lower()
    povos = [p for p in carregar_povos_usuarios()
             if isinstance(p, dict) and p.get("autor") == email]
    return sorted(povos, key=lambda p: p.get("nome", "").casefold())


def salvar_povo(email, nome, regiao, sobre, cuidado, nome_original=None):
    """Cria um povo novo ou atualiza um que o próprio usuário já cadastrou.

    nome_original: nome atual da entrada que está sendo editada (permite renomear).
    Os povos do conteúdo base não podem ser sobrescritos.
    """
    email = email.strip().lower()
    nome, regiao, sobre, cuidado = (t.strip() for t in (nome, regiao, sobre, cuidado))

    erros = erros_povo(nome, regiao, sobre, cuidado)
    if erros:
        return False, resumir_erros(erros)

    chave = nome.casefold()
    if chave in {p["nome"].casefold() for p in POVOS}:
        return False, "Esse povo já faz parte do conteúdo base do Tupã."

    try:
        povos = carregar_povos_usuarios()
        original = (nome_original or nome).casefold()
        alvo = None
        for i, p in enumerate(povos):
            if p.get("nome", "").casefold() == original and p.get("autor") == email:
                alvo = i
        for i, p in enumerate(povos):
            if i != alvo and p.get("nome", "").casefold() == chave:
                return False, "Já existe um povo cadastrado com esse nome."

        registro = {"nome": nome, "regiao": regiao, "sobre": sobre,
                    "cuidado": cuidado, "autor": email}
        if alvo is None:
            povos.append(registro)
            mensagem = "Informações adicionadas!"
        else:
            povos[alvo] = registro
            mensagem = "Informações atualizadas!"
        salvar_povos_usuarios(povos)
        return True, mensagem
    except (ErroDeArmazenamento, TypeError, AttributeError) as erro:
        return False, str(erro)


def excluir_povo(email, nome):
    email = email.strip().lower()
    try:
        povos = carregar_povos_usuarios()
        restantes = [p for p in povos
                     if not (isinstance(p, dict) and p.get("autor") == email
                             and p.get("nome", "").casefold() == nome.casefold())]
        if len(restantes) == len(povos):
            return False, "Entrada não encontrada."
        salvar_povos_usuarios(restantes)
        return True, "Entrada excluída."
    except (ErroDeArmazenamento, TypeError, AttributeError) as erro:
        return False, str(erro)


def desvincular_autor(email):
    """Remove o e-mail dos povos que a pessoa adicionou (usado quando a conta é excluída)."""
    povos = carregar_povos_usuarios()
    mudou = False
    for povo in povos:
        if isinstance(povo, dict) and povo.get("autor") == email:
            povo["autor"] = None
            mudou = True
    if mudou:
        salvar_povos_usuarios(povos)
