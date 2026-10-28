"""Regras de validação dos campos. Só confere valores: não lê nem grava arquivos."""
import re

REGEX_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")

# Limites dos campos de um povo (a tela de pesquisa foi desenhada para caber nisso).
LIMITES_POVO = {"nome": 40, "regiao": 120, "sobre": 280, "cuidado": 160}
MINIMOS_POVO = {"nome": 2, "regiao": 3, "sobre": 20, "cuidado": 0}
ROTULOS_POVO = {"nome": "Nome", "regiao": "Região", "sobre": "Sobre", "cuidado": "Para pesquisar mais"}


# Cada regra_* devolve uma lista de (descrição, cumpre?), usada tanto pelo painel ao vivo quanto pelos erros.

def regras_nome(nome):
    return [("Pelo menos 3 caracteres", len(nome.strip()) >= 3)]


def regras_email(email):
    return [("Formato nome@dominio.com", bool(REGEX_EMAIL.match(email.strip().lower())))]


def regras_senha(senha):
    return [
        ("Pelo menos 8 caracteres", len(senha) >= 8),
        ("Pelo menos um número", any(c.isdigit() for c in senha)),
        ("Pelo menos uma letra", any(c.isalpha() for c in senha)),
    ]


def regras_confirmacao(senha, confirmar):
    return [("Igual à senha", confirmar != "" and confirmar == senha)]


def erros_cadastro(nome, email, senha, confirmar=None):
    """Lista TODOS os erros como (campo, motivo). Sem confirmar, não checa a confirmação."""
    secoes = [("Nome", regras_nome(nome)), ("E-mail", regras_email(email)),
              ("Senha", regras_senha(senha))]
    if confirmar is not None:
        secoes.append(("Confirmar senha", regras_confirmacao(senha, confirmar)))
    return [(campo, rotulo[0].lower() + rotulo[1:])
            for campo, regras in secoes for rotulo, ok in regras if not ok]


def erros_povo(nome, regiao, sobre, cuidado):
    """Todos os erros dos campos de um povo, como (campo, motivo)."""
    valores = {"nome": nome.strip(), "regiao": regiao.strip(),
               "sobre": sobre.strip(), "cuidado": cuidado.strip()}
    erros = []
    for chave, valor in valores.items():
        if len(valor) < MINIMOS_POVO[chave]:
            erros.append((ROTULOS_POVO[chave], f"mínimo de {MINIMOS_POVO[chave]} caracteres"))
        elif len(valor) > LIMITES_POVO[chave]:
            erros.append((ROTULOS_POVO[chave], f"máximo de {LIMITES_POVO[chave]} caracteres"))
    return erros


def resumir_erros(erros):
    """Transforma [(campo, motivo), ...] em uma frase curta; deixa claro quando há mais de um erro."""
    if not erros:
        return ""
    if len(erros) == 1:
        campo, motivo = erros[0]
        return f"{campo}: {motivo}."
    campos = list(dict.fromkeys(campo for campo, _ in erros))
    return f"Há {len(erros)} erros: " + ", ".join(campos) + "."
