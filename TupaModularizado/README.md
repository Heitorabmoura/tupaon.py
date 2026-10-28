# Tupã — versão modularizada

## Como executar
1. Instale Python 3 e Pygame, se ainda não estiverem instalados: `python -m pip install pygame`
2. Abra esta pasta no VS Code.
3. Execute `main.py` (botão Run Python File ou `python main.py` no terminal).

## Organização em camadas
Cada arquivo tem uma responsabilidade. As telas só chamam a camada de regras, e só `armazenamento.py` mexe em arquivos.

**Telas (pygame)**
- `main.py`: ponto de entrada e menu principal.
- `cadastro.py`: tela de cadastro, com o painel de requisitos ao vivo.
- `login.py`: tela de login.
- `area_usuario.py`: tela após o login (Meus povos, Excluir conta, Voltar).
- `meus_povos.py`: lista dos povos que o usuário adicionou (adicionar, editar, excluir).
- `formulario_povo.py`: formulário de adicionar/editar um povo.
- `conta.py`: exclusão da própria conta (pede a senha).
- `pesquisas.py`: busca e exibição dos povos.
- `quiz.py`: quiz educativo.

**Visual compartilhado**
- `configuracoes.py`: janela, cores e fontes.
- `interface.py`: botões, campos de texto, marcadores de requisito e quebra de texto.

**Regras (sem pygame)**
- `validacao.py`: regras dos campos e geração da lista de erros.
- `senhas.py`: hash e conferência de senhas.
- `usuarios.py`: criar conta, entrar e excluir conta.
- `povos.py`: conteúdo base sobre os povos + adicionar, editar e excluir os povos dos usuários.

**Arquivos**
- `armazenamento.py`: leitura e gravação dos JSON.
- `usuarios.json`: criado quando o primeiro usuário for cadastrado.
- `povos_usuarios.json`: criado quando alguém adicionar o primeiro povo.

Dependências entre as camadas: telas → regras → armazenamento. (`usuarios` → `povos` → `armazenamento`; `validacao` e `senhas` não dependem de ninguém.)

## Observação
Os arquivos `usuarios.json` e `povos_usuarios.json` são criados na mesma pasta deste projeto. Não compartilhe esses arquivos ao publicar o repositório, pois eles podem conter dados pessoais de teste.

## Regras do CRUD
- **Update (povos):** cada usuário só edita e exclui o que ele mesmo adicionou. Povos do conteúdo base não podem ser sobrescritos.
- **Delete (conta):** exige a senha. O usuário é removido; os povos que ele adicionou continuam, sem vínculo com o e-mail.

## Validação dos campos
- No cadastro, o painel **REQUISITOS** mostra ao vivo, para cada campo, quais regras já foram cumpridas (verde) e quais não (vermelho). Campos vazios ficam cinza até a pessoa tentar criar a conta.
- Ao tentar criar a conta (ou salvar um povo), **todos** os erros são conferidos de uma vez. Com mais de um, a mensagem diz quantos são e quais campos (ex.: "Há 3 erros: Nome, E-mail, Senha.").
- No formulário de povos, o contador de cada campo fica verde quando atinge o mínimo e vermelho quando falta.
- As regras ficam em `validacao.py`, então a tela e a validação usam a mesma fonte.
