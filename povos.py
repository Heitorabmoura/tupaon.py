"""Povos indígenas: conteúdo base do Tupã e as informações adicionadas pelos usuários."""
import copy

from armazenamento import (
    ErroDeArmazenamento, carregar_povos_usuarios, salvar_povos_usuarios
)
from favoritos import remover_povo, renomear_povo
from permissoes import eh_administrador
from validacao import erros_povo, resumir_erros

# Conteúdo base. Cada povo tem: informações gerais, "palavras" (vocabulário básico), "mitologia"
# (criação do mundo, divindades e seres), "narrativa" (histórias, memória e tradições vividas),
# "culinaria" (alimentos tradicionais) e as fontes de cada parte.
# O texto é um resumo; as tradições variam entre comunidades. Tamanhos máximos: validacao.LIMITES_CONTEUDO.
POVOS = [
    {
        "nome": "Guarani",
        "regiao": "Diferentes áreas do Brasil, além de países vizinhos.",
        "sobre": "Guarani é o nome de povos indígenas com línguas e identidades próprias. Há diferentes grupos Guarani.",
        "cuidado": "Evite tratar todos os povos indígenas como se tivessem a mesma cultura.",
        "palavras": [
            {"palavra": "Tekoa", "significado": "Aldeia"},
            {"palavra": "Opy", "significado": "Casa de reza (casa cerimonial)"},
            {"palavra": "Nhanderu", "significado": "Divindade criadora"},
            {"palavra": "Yvy", "significado": "Terra"},
            {"palavra": "Aguyje", "significado": "Plenitude, perfeição espiritual"},
            {"palavra": "Avati", "significado": "Milho"},
            {"palavra": "Juruá", "significado": "Pessoa não indígena"},
            {"palavra": "Mborai", "significado": "Canto sagrado"},
        ],
        "observacao_palavras": "Palavras do Guarani Mbya; outras parcialidades Guarani podem falar de forma diferente.",
        "fonte_palavras": "Glossário de termos indígenas (UFRGS) e artigos das revistas Espaço Ameríndio (UFRGS), Amazônica (UFPA) e Travessia.",
        "mitologia": {
            "titulo": "Nhanderu, o primeiro sol e a primeira terra",
            "texto": "Para os Guarani Mbya, antes da primeira terra existia Nhanderu, o Pai primeiro, numa noite originária iluminada pelo reflexo do próprio coração do criador, que deu origem ao primeiro sol, Nhamandu. Nhamandu criou a primeira terra, Yvy, sobre o oceano primitivo, e seus filhos criaram os primeiros humanos, dando-lhes o canto sagrado e as belas palavras. Na história dos irmãos Kuaray (Sol) e Jaxy (Lua), essa primeira terra foi destruída por um dilúvio.",
            "fonte": "Anuário Antropológico (UnB, 2018); Outras Palavras (Ayvu Rapyta); Espaço Ameríndio (UFRGS, 2009).",
        },
        "narrativa": {
            "titulo": "Yvy Marã Ey, a terra sem males",
            "texto": "Para os Guarani Mbya, Yvy Marã Ey, a 'terra sem males', é o lugar onde não existem dor, medo, fome nem frio. Por muito tempo, grupos Guarani caminharam em busca dela, guiados pelos sonhos e pelas rezas de seus líderes religiosos. Muitos hoje a entendem como uma terra espiritual, para onde vão os que alcançam a plenitude (aguyje) por meio das rezas e do bom comportamento.",
            "fonte": "Cadernos da Escola da Cidade; tese de Almires Machado (UFPA, 2015); revista Travessia.",
        },
        "culinaria": [
            {"prato": "Avati etei", "descricao": "O 'milho verdadeiro', milho tradicional"},
            {"prato": "Mbojape", "descricao": "Bolo de milho assado nas cinzas"},
            {"prato": "Kaguijy", "descricao": "Bebida de milho, alimento sagrado"},
            {"prato": "Rora", "descricao": "Farofa de milho"},
            {"prato": "Jety", "descricao": "Batata-doce, plantada em muitas variedades"},
            {"prato": "Mandi'ó", "descricao": "Mandioca, cultivada nas roças"},
        ],
        "observacao_culinaria": "O milho é sagrado: a cerimônia Nhemongarai celebra o milho e é um ritual importante dos Mbya.",
        "fonte_culinaria": "FAO Brasil (2020); Arca do Gosto (Slow Food); Comissão Pró-Índio de SP; Cadernos de Agroecologia (ABA).",
    },
    {
        "nome": "Yanomami",
        "regiao": "Territórios na região amazônica do Brasil e da Venezuela.",
        "sobre": "Os Yanomami são um povo indígena da região amazônica, com línguas, conhecimentos e modos de vida próprios.",
        "cuidado": "A proteção territorial e o respeito às comunidades são temas importantes.",
        "palavras": [
            {"palavra": "Urihi a", "significado": "Terra-floresta, onde a vida se sustenta"},
            {"palavra": "Xapiri", "significado": "Espíritos auxiliares dos xamãs"},
            {"palavra": "Napë", "significado": "Pessoa não Yanomami (não indígena)"},
            {"palavra": "Xawara", "significado": "Epidemia, a 'fumaça' que traz doenças"},
            {"palavra": "Hutukara", "significado": "Nome da Associação Yanomami; palavra da cosmologia"},
            {"palavra": "Omama", "significado": "Criador (demiurgo) do mundo yanomami"},
            {"palavra": "Yoasi", "significado": "Irmão de Omama; origem da morte e das doenças"},
            {"palavra": "Mari hi", "significado": "Árvore dos sonhos"},
        ],
        "observacao_palavras": "",
        "fonte_palavras": "ISA (Povos Indígenas no Brasil); Revista da UFMG (Gomes e Kopenawa, 2016); revista PRACS (UNIFAP).",
        "mitologia": {
            "titulo": "Omama e Yoasi",
            "texto": "Na tradição Yanomami, Omama, o criador, fez a terra, a floresta e os Yanomami, e criou a árvore dos sonhos. Seu irmão Yoasi trouxe a morte e as doenças. Por isso os não indígenas, os napë, às vezes são chamados de 'gente de Yoasi'. Omama também criou os xapiri, espíritos que protegem os Yanomami e que só os xamãs conseguem fazer descer e dançar.",
            "fonte": "ISA (Povos Indígenas no Brasil); revista PRACS (UNIFAP); revista Anansi (UNEB).",
        },
        "narrativa": {
            "titulo": "A queda do céu",
            "texto": "Para os Yanomami, o céu pode desabar, e sustentá-lo é tarefa dos xamãs. Omama fixou os pés do céu com peças de metal, e hoje os xamãs fazem os xapiri descerem e dançarem para reforçá-lo. Davi Kopenawa, xamã e liderança Yanomami, conta essa história no livro 'A queda do céu', escrito com o antropólogo Bruce Albert, e alerta que a floresta só morre se for destruída pelos brancos, os napë.",
            "fonte": "Kopenawa e Albert, A queda do céu (2015); Cadernos da Escola da Cidade; ISA (Povos Indígenas no Brasil).",
        },
        "culinaria": [
            {"prato": "Banana", "descricao": "Muitas variedades; também assada verde"},
            {"prato": "Beiju", "descricao": "Pão fino feito de mandioca"},
            {"prato": "Pupunha", "descricao": "Fruto das roças, em várias variedades"},
            {"prato": "Cogumelos", "descricao": "Colhidos na floresta; têm uma enciclopédia"},
            {"prato": "Caça moqueada", "descricao": "Carne defumada no moquém, para conservar"},
            {"prato": "Cupins e larvas", "descricao": "Assados na folha de taioba (Sanöma)"},
        ],
        "observacao_culinaria": "Nas roças yanomami há em média cerca de 100 variedades de 40 espécies cultivadas.",
        "fonte_culinaria": "ISA (acervo e notícias); Revista de Estudios Brasileños (Univ. de Salamanca); nota técnica do COE-Yanomami (2023).",
    },
    {
        "nome": "Tikuna",
        "regiao": "Principalmente na região do Alto Solimões, no Amazonas.",
        "sobre": "Os Tikuna possuem língua e práticas culturais próprias, além de expressões artísticas e conhecimentos tradicionais.",
        "cuidado": "As tradições e experiências podem variar entre comunidades e gerações.",
        "palavras": [
            {"palavra": "Magüta", "significado": "Como os Tikuna chamam a si mesmos"},
            {"palavra": "Magü", "significado": "Pescar com vara"},
            {"palavra": "Yo'i", "significado": "Herói cultural que pescou o povo Magüta"},
            {"palavra": "Ipi", "significado": "Irmão de Yo'i, também herói cultural"},
            {"palavra": "Eware", "significado": "Igarapé onde Yo'i pescou o primeiro povo"},
            {"palavra": "Worecü", "significado": "Moça nova; festa de iniciação feminina"},
        ],
        "observacao_palavras": "Magüta vem de 'magü' (pescar com vara) e 'ta' (coletivo): gente pescada com vara.",
        "fonte_palavras": "ISA (Povos Indígenas no Brasil); revista Interethnica (UnB); Revista de Antropologia da UFSCar.",
        "mitologia": {
            "titulo": "Yo'i, Ipi e o povo pescado no Eware",
            "texto": "Segundo a tradição oral Tikuna, o herói cultural Yo'i pescou o primeiro povo Tikuna, com vara, nas águas do igarapé Eware. Os peixes se transformaram em gente: o povo Magüta. Em outra versão contada, Yo'i e seu irmão Ipi derrubaram a samaúma gigante para que o dia clareasse e o sol, o céu e as estrelas pudessem ser vistos.",
            "fonte": "ISA (Povos Indígenas no Brasil); revista Iluminuras (UFRGS); revista Interethnica (UnB).",
        },
        "narrativa": {
            "titulo": "Worecü, a Festa da Moça Nova",
            "texto": "Quando uma moça Tikuna tem a primeira menstruação, a família organiza a Festa da Moça Nova (Worecü), que dura três dias. A moça fica reclusa e recebe ensinamentos das mulheres da família. Durante a festa, as flautas cantam com a voz dos encantados e as máscaras representam entidades e forças da natureza. É um dos rituais mais importantes do povo e foi preservado apesar das pressões externas.",
            "fonte": "Agência FAPESP (2020); Revista de Antropologia (USP); Jornada de Iniciação Científica (UFFS).",
        },
        "culinaria": [
            {"prato": "Macaxeira", "descricao": "Uma das principais plantas das roças"},
            {"prato": "Farinha de mandioca", "descricao": "Feita com a mandioca das roças"},
            {"prato": "Pajuaru", "descricao": "Bebida fermentada de mandioca da Moça Nova"},
            {"prato": "Peixe moqueado", "descricao": "Peixe seco e defumado em grelha no fogo"},
            {"prato": "Caça moqueada", "descricao": "Preparada com antecedência para as festas"},
            {"prato": "Frutas", "descricao": "Açaí, buriti, pupunha e banana"},
        ],
        "observacao_culinaria": "Mandioca e peixe são preparados com antecedência para a Festa da Moça Nova, que dura três dias.",
        "fonte_culinaria": "Jornada de Iniciação Científica (UFFS); Revista de Antropologia (USP); Agência FAPESP (2020); Portal Amazônia.",
    },
    {
        "nome": "Pataxó",
        "regiao": "Principalmente no sul da Bahia e em Minas Gerais.",
        "sobre": "O povo Pataxó mantém ações de fortalecimento cultural, memória, língua e defesa de seus territórios.",
        "cuidado": "Consulte fontes indígenas e instituições confiáveis para aprofundar a pesquisa.",
        "palavras": [
            {"palavra": "Patxôhã", "significado": "Língua de guerreiro (a língua pataxó)"},
            {"palavra": "Txihi", "significado": "Gente; os indígenas Pataxó"},
            {"palavra": "Taputary", "significado": "Parentes"},
            {"palavra": "Awê", "significado": "Ritual de cantos e danças pataxó"},
            {"palavra": "Awãkã", "significado": "Narrativa, o 'causo' contado pelos mais velhos"},
            {"palavra": "Makiami", "significado": "Anciãos e anciãs"},
            {"palavra": "Kijetxawê", "significado": "Escola"},
        ],
        "observacao_palavras": "O Patxôhã está em retomada desde os anos 1990 e já reúne cerca de 2.500 palavras.",
        "fonte_palavras": "Revistas Tellus (UCDB), Nanduty (UFGD), Tempus (UnB) e Aprender (UESB).",
        "mitologia": {
            "titulo": "Os Naôs, encantados da mata",
            "texto": "A espiritualidade Pataxó é marcada pelos encantados, os Naôs, manifestações da força da natureza. Eles se relacionam com as pessoas por meio dos pajés e ensinam a cuidar da natureza, a se curar e a viver em equilíbrio. Entre os seres espirituais está Naô Katumbayá, o espírito da Mãe da Mata. Eles moram em lugares sagrados, como a mata e o Monte Pascoal: os encantados cuidam dos Pataxó e os Pataxó cuidam da mata, a casa deles.",
            "fonte": "TCC da UFMG (Txonãg, 2023); revista Argumentos (Unimontes, 2024).",
        },
        "narrativa": {
            "titulo": "O Monte Pascoal e as histórias dos mais velhos",
            "texto": "Para os Pataxó, o Monte Pascoal, chamado por eles de 'Pé de Pedra', é terra indígena, memória e altar dos antepassados. Os mais velhos, os makiami, passam as histórias (awãkã) de geração em geração, e muitas começam com 'Assim contam os mais velhos'. Os Pataxó também explicam o próprio nome como a água da chuva que bate na terra e nas pedras e segue para o rio e o mar.",
            "fonte": "ISA (Povos Indígenas no Brasil); revistas Kiri-kerê (UFES), Nanduty (UFGD) e Espaço Ameríndio (UFRGS).",
        },
        "culinaria": [
            {"prato": "Peixe na patioba", "descricao": "Peixe assado na folha de uma palmeira"},
            {"prato": "Beiju", "descricao": "Feito de mandioca, em vários tipos"},
            {"prato": "Farinha de puba", "descricao": "Também chamada de 'farinha do índio'"},
            {"prato": "Cauim", "descricao": "Bebida fermentada de mandioca"},
            {"prato": "Quibebo", "descricao": "Preparado de abóbora"},
            {"prato": "Banana-da-terra", "descricao": "Assada no fogão de barro, a lenha"},
        ],
        "observacao_culinaria": "A diversidade de mandiocas e o calendário lunar orientam os plantios e as colheitas.",
        "fonte_culinaria": "Cadernos de Agroecologia (ABA, UFSB); reportagem do jornal Correio sobre vivência em aldeia Pataxó.",
    },
]


def _sem_extras():
    """Valores padrão (sempre novos, nunca compartilhados): povos de usuários só têm as informações gerais."""
    return {"palavras": [], "observacao_palavras": "", "fonte_palavras": "",
            "mitologia": None, "narrativa": None,
            "culinaria": [], "observacao_culinaria": "", "fonte_culinaria": ""}


def _melhor_esforco(acao, *args):
    """Favoritos sem povo correspondente não aparecem para ninguém, então uma falha ao limpá-los
    não deve desfazer a operação principal (que já foi gravada)."""
    try:
        acao(*args)
    except ErroDeArmazenamento:
        pass


def obter_povos():
    """Conteúdo base + povos dos usuários (estes marcados com comunidade=True)."""
    povos = [dict(_sem_extras(), **copy.deepcopy(p), comunidade=False) for p in POVOS]
    try:
        extras = carregar_povos_usuarios()
    except ErroDeArmazenamento:
        return povos
    validos = [e for e in extras if isinstance(e, dict) and e.get("nome")]
    for e in sorted(validos, key=lambda p: p["nome"].casefold()):
        povos.append(dict(_sem_extras(), **{
            "nome": e["nome"],
            "regiao": e.get("regiao", ""),
            "sobre": e.get("sobre", ""),
            "cuidado": e.get("cuidado", ""),
            "comunidade": True,
        }))
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
        nome_antigo = None
        if alvo is None:
            povos.append(registro)
            mensagem = "Informações adicionadas!"
        else:
            nome_antigo = povos[alvo].get("nome", "")
            povos[alvo] = registro
            mensagem = "Informações atualizadas!"
        salvar_povos_usuarios(povos)
        if nome_antigo and nome_antigo.casefold() != chave:
            _melhor_esforco(renomear_povo, nome_antigo, nome)
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
        _melhor_esforco(remover_povo, nome)
        return True, "Entrada excluída."
    except (ErroDeArmazenamento, TypeError, AttributeError) as erro:
        return False, str(erro)


def excluir_povo_como_admin(email_admin, nome):
    """Remove um povo adicionado por qualquer usuário (inclusive de contas já excluídas).

    Só administradores podem; os povos do conteúdo base nunca podem ser removidos.
    A checagem fica aqui (e não só na tela) para valer mesmo que outra tela chame esta função.
    """
    if not eh_administrador(email_admin):
        return False, "Apenas administradores podem remover povos de outras pessoas."
    nome = nome.strip()
    if nome.casefold() in {p["nome"].casefold() for p in POVOS}:
        return False, "Os povos do conteúdo base não podem ser removidos."
    try:
        povos = carregar_povos_usuarios()
        restantes = [p for p in povos
                     if not (isinstance(p, dict) and p.get("nome", "").casefold() == nome.casefold())]
        if len(restantes) == len(povos):
            return False, "Povo não encontrado."
        salvar_povos_usuarios(restantes)
        _melhor_esforco(remover_povo, nome)
        return True, "Povo removido pelo administrador."
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
