# Tupã

Aplicativo desktop em Python para **conhecer e valorizar os povos originários do Brasil**. O usuário pesquisa informações sobre povos indígenas, responde a um quiz educativo e, depois de criar uma conta, pode **contribuir com novas informações** sobre povos.

> Projeto da área de Educação, desenvolvido em Python com Pygame.

## Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Criar conta | Cadastro com nome, e-mail e senha, com verificação ao vivo dos requisitos de cada campo. Ao concluir, a pessoa já entra na própria conta, sem refazer o login |
| Login | Autenticação por e-mail e senha |
| Pesquisar povos | Busca por nome, com navegação por setas, rodinha do mouse e cliques |
| Favoritar povos | Usuário logado marca povos com uma estrela e pode filtrar só os favoritos. Visitantes pesquisam, mas precisam entrar na conta para favoritar |
| Abas de conteúdo | Cada povo do conteúdo base tem cinco abas: **Sobre**, **Palavras** (vocabulário básico com o significado), **Mitologia** (criação do mundo, divindades e seres), **Narrativas** (histórias, memória e tradições vividas) e **Culinária** (alimentos tradicionais). Todas trazem as fontes consultadas |
| Administração | Contas de administrador (lista em `permissoes.py`) removem povos adicionados por qualquer usuário, com confirmação em dois cliques. Os povos do conteúdo base não podem ser removidos |
| Quiz | Perguntas sobre diversidade e respeito aos povos indígenas, com pontuação |
| Adicionar informações | Usuário logado cadastra, edita e exclui informações sobre povos |
| Deletar conta | Exclui a conta e os favoritos dela, após confirmação com a senha |

## Inovação do projeto

1. **Conteúdo colaborativo com controle de autoria.** Além do conteúdo base, as contas podem adicionar povos. Esses registros aparecem na pesquisa marcados como "adicionado por usuário", cada pessoa só edita e exclui o que ela mesma criou, e os povos do conteúdo base não podem ser sobrescritos.
2. **Incentivo à pesquisa respeitosa.** Cada povo tem o campo "Para pesquisar mais", que orienta o leitor a buscar fontes confiáveis, em linha com o tema do quiz (consultar, quando possível, fontes dos próprios povos).
3. **Painel de requisitos ao vivo.** No cadastro, cada regra (por exemplo, "pelo menos um número") fica verde ou vermelha enquanto a pessoa digita. Ao enviar, **todos** os erros são listados de uma vez, com a contagem (ex.: "Há 3 erros: Nome, E-mail, Senha."), em vez de parar no primeiro.
4. **Privacidade na exclusão da conta.** Ao deletar a conta, nome, e-mail e senha são apagados. O conteúdo que a pessoa adicionou permanece, mas perde o vínculo com o e-mail dela (princípio de minimização de dados).

## Tecnologias e bibliotecas

| Biblioteca | Tipo | Uso no projeto | Por que foi escolhida |
|---|---|---|---|
| `pygame` (2.x) | Externa | Janela, desenho, fontes, eventos de mouse e teclado | Permite construir uma interface gráfica interativa com poucas linhas e sem depender de navegador ou servidor |
| `json` | Padrão | Persistência de contas e de povos adicionados | Um banco de dados seria excessivo para o tamanho do projeto; JSON é legível e fácil de inspecionar |
| `hashlib` | Padrão | Hash de senhas (PBKDF2-HMAC-SHA256) | Evita guardar senhas em texto puro, sem precisar de biblioteca externa |
| `os` | Padrão | Sal aleatório (`os.urandom`) e troca atômica de arquivo (`os.replace`) | Sal seguro por senha e gravação que não corrompe o JSON se o programa fechar no meio |
| `re` | Padrão | Expressão regular para validar e-mail | Validação de formato simples e direta |
| `pathlib` | Padrão | Construção dos caminhos dos arquivos JSON a partir da localização do próprio projeto | Evita depender da pasta de onde o programa foi iniciado e funciona em diferentes sistemas operacionais |
| `math` | Padrão | Apoio a cálculos usados nos componentes gráficos da interface | Faz parte do Python e atende às necessidades matemáticas da interface |
| `copy` | Padrão | Cópia independente dos dados do conteúdo-base dos povos | Evita alterações acidentais nos dados originais durante a montagem das informações exibidas |
| `unittest` | Padrão | Testes automatizados das regras e operações do sistema | Permite verificar o funcionamento sem instalar outra biblioteca |

Só o Pygame precisa ser instalado. Todo o resto vem com o Python.

## Como executar

**Requisitos:** Python 3.10 ou superior (os testes automatizados foram executados na versão 3.12) e Pygame 2.x. O Pygame 2 é necessário por causa do evento de rodinha do mouse.

```bash
# 1. clonar o repositório
git clone <URL-DO-REPOSITORIO>
cd <PASTA-DO-REPOSITORIO>

# 2. instalar a única dependência externa
python -m pip install -r requirements.txt     # ou: python -m pip install pygame

# 3. executar
python main.py
```

### Importações necessárias

As importações utilizadas no código estão divididas em três grupos:

- **Biblioteca externa:** `pygame`, importada com `import pygame`. É a única dependência que precisa ser instalada manualmente.
- **Bibliotecas nativas do Python:** `json` e `os` (leitura, gravação e substituição segura dos arquivos); `pathlib` (caminhos); `hashlib` (proteção das senhas); `re` (validação de e-mail); `math` (operações matemáticas da interface); `copy` (cópia independente dos dados); `unittest`, `tempfile` e `pathlib` (testes automatizados). Essas bibliotecas já acompanham o Python.
- **Módulos internos:** arquivos do próprio projeto, importados diretamente, como `from povos import obter_povos`, `from usuarios import cadastrar_usuario` e `from favoritos import alternar_favorito`. Eles devem permanecer na mesma pasta para que as importações funcionem corretamente.

Não é necessário instalar `json`, `os`, `pathlib`, `hashlib`, `re`, `math`, `copy` ou `unittest`: todos fazem parte da biblioteca padrão do Python. A lista de dependências externas está no arquivo `requirements.txt` e contém somente o Pygame.

Os arquivos `usuarios.json`, `povos_usuarios.json` e `favoritos.json` são criados automaticamente, na pasta do projeto, quando houver o primeiro cadastro, a primeira informação adicionada e o primeiro favorito.

## Organização dos módulos

O projeto é dividido em camadas. As telas só desenham e tratam eventos, as regras ficam sem Pygame, e somente `armazenamento.py` lê e grava arquivos.

```
Telas (pygame)            Regras (sem pygame)          Arquivos
─────────────────         ───────────────────          ─────────────────
main.py (menu)            validacao.py                 armazenamento.py
cadastro.py               senhas.py                      ├─ usuarios.json
login.py                  usuarios.py                    ├─ povos_usuarios.json
area_usuario.py           povos.py                       └─ favoritos.json
meus_povos.py             favoritos.py, permissoes.py
formulario_povo.py        Visual compartilhado
conta.py                  ────────────────────
pesquisas.py              configuracoes.py  (janela, cores, fontes)
painel_povo.py            interface.py      (botões, campos, marcadores, quebra de texto)
quiz.py
```

| Módulo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada e menu principal |
| `configuracoes.py` | Inicializa o Pygame; define janela (900x600), cores e fontes |
| `interface.py` | Componentes reutilizáveis de tela: botão, campo de texto, campo multilinha, marcador de requisito, estrela de favorito, texto cortado, quebra de texto |
| `cadastro.py` | Tela de criação de conta com painel de requisitos ao vivo e login automático ao concluir |
| `login.py` | Tela de login |
| `area_usuario.py` | Tela exibida após o login (Pesquisar e favoritar, Meus favoritos, Adicionar informações, Deletar conta, Voltar) |
| `meus_povos.py` | Lista dos povos adicionados pelo usuário, com adicionar, editar e excluir |
| `formulario_povo.py` | Formulário de criação e edição de um povo |
| `conta.py` | Tela de exclusão de conta com confirmação por senha |
| `pesquisas.py` | Busca e exibição dos povos, com estrela de favoritar e filtro de favoritos |
| `painel_povo.py` | Painel de detalhes do povo, com as abas Sobre, Palavras, Mitologia, Narrativas e Culinária |
| `quiz.py` | Quiz educativo |
| `validacao.py` | Regras dos campos e geração da lista de erros |
| `senhas.py` | Geração e conferência de hash de senha |
| `usuarios.py` | Criar conta, autenticar e excluir conta |
| `favoritos.py` | Favoritar e desfavoritar povos por usuário; mantém os favoritos coerentes ao renomear ou excluir um povo e ao excluir a conta |
| `permissoes.py` | Lista de administradores e a função `eh_administrador` |
| `povos.py` | Conteúdo base sobre os povos (informações, palavras, mitologia, narrativas, culinária e fontes), CRUD dos povos dos usuários e remoção pelo administrador |
| `armazenamento.py` | Leitura e gravação dos arquivos JSON |
| `test_regras.py` | Testes automatizados das regras |

**Sentido das dependências:** telas → regras → armazenamento. Nenhum módulo de regras importa algo de tela, então a lógica pode ser testada sem abrir a janela.

```
main ─┬─ cadastro ─┬─► usuarios ─► povos ─► armazenamento
      │            └─► area_usuario (login automático após o cadastro)
      ├─ login ─► area_usuario ┬─ meus_povos ─► formulario_povo ─► povos
      │                        ├─ conta ─► usuarios
      │                        └─ pesquisas ─► povos, favoritos
      ├─ pesquisas ─► povos, favoritos
      └─ quiz
(povos e usuarios também chamam favoritos para manter os favoritos coerentes; favoritos só depende de armazenamento; povos usa permissoes, que não depende de ninguém)
(validacao e senhas não dependem de nenhum outro módulo do projeto)
```

## Persistência de dados

O projeto utiliza três arquivos JSON, todos armazenados localmente e organizados como listas de objetos:

```jsonc
// usuarios.json
[{ "nome": "Ana Lima", "email": "ana@exemplo.com",
   "senha": { "salt": "<hex 16 bytes>", "hash": "<hex PBKDF2>" } }]

// povos_usuarios.json   ("autor" vira null quando a conta do autor é excluída)
[{ "nome": "Xukuru", "regiao": "Pernambuco", "sobre": "...",
   "cuidado": "...", "autor": "ana@exemplo.com" }]

// favoritos.json   (um registro por par pessoa/povo; o povo é identificado pelo nome)
[{ "email": "ana@exemplo.com", "povo": "Guarani" }]
```

A gravação é feita em arquivo temporário seguido de `os.replace`, para não corromper o arquivo caso algo falhe no meio.

## Decisões técnicas de segurança

- Senhas nunca são guardadas em texto puro: PBKDF2-HMAC-SHA256, 100.000 iterações e sal aleatório de 16 bytes por senha.
- E-mails são normalizados (minúsculas, sem espaços) antes de comparar.
- Excluir a conta exige a senha atual.
- Cada operação sobre povos confere o autor: só o dono edita ou exclui a própria entrada.
- Cada pessoa só lê e altera os próprios favoritos (filtrados pelo e-mail da conta logada), e eles são apagados junto com a conta.
- Só administradores removem povos de outras pessoas. A checagem fica na camada de regras (`povos.excluir_povo_como_admin`), não só na tela, então vale mesmo que outra tela chame a função.
- Tamanhos máximos dos campos são validados antes de gravar.
- Os JSON estão no `.gitignore`, para dados de teste não irem para o repositório.

## Testes

```bash
python -m unittest -v
```

São 38 testes das camadas de validação, senhas, usuários, povos, favoritos e permissões. Eles também conferem que o conteúdo das cinco abas está completo, tem fontes e cabe na tela, e que a remoção pelo administrador respeita as regras. Eles usam uma pasta temporária e não alteram os dados reais. As telas em Pygame são conferidas manualmente.

## Limitações conhecidas

- Os dados ficam em arquivos locais. As "contribuições" são compartilhadas entre as contas **da mesma instalação**, não entre computadores diferentes. Para isso seria preciso um servidor e um banco de dados.
- As mensagens de login diferenciam "e-mail não encontrado" de "senha incorreta", o que facilita descobrir quais e-mails têm conta. Isso é aceitável para um projeto acadêmico local, mas não para produção.
- O conteúdo adicionado pelos usuários não passa por moderação. Povos adicionados por usuários só têm a aba Sobre (palavras, mitologia, narrativas e culinária existem apenas no conteúdo base).
- Palavras, mitologia, narrativas e culinária dos povos base são resumos feitos a partir de fontes acadêmicas e do ISA (listadas na própria tela). Não foram revisados por falantes ou lideranças dos povos, e as tradições variam entre comunidades. Para uso além do trabalho acadêmico, vale pedir essa revisão.
- O vocabulário é curto (6 a 8 palavras por povo) e prioriza termos centrais de cada cultura; uma lista maior exigiria um dicionário de referência de cada língua.
- A interface tem tamanho fixo (900x600).
- A lista de administradores é fixa no código (`permissoes.py`) e o app não confirma que o e-mail pertence a quem o digitou: qualquer pessoa pode criar uma conta com um e-mail da lista na própria instalação e virar administradora ali. Como os dados são locais, o poder vale só nessa instalação; num sistema online o e-mail precisaria ser confirmado. Os e-mails dos administradores ficam visíveis no repositório.

## Autores

Heitor Alves Bezerra Moura e Ivan Guilherme.
