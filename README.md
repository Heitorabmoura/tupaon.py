# Tupã — versão modularizada

## Como executar
1. Instale Python 3 e Pygame, se ainda não estiverem instalados: `python -m pip install pygame`
2. Abra esta pasta no VS Code.
3. Execute `main.py` (botão Run Python File ou `python main.py` no terminal).

## Arquivos
- `main.py`: ponto de entrada e menu principal.
- `configuracoes.py`: janela, cores e fontes compartilhadas.
- `interface.py`: funções visuais reutilizáveis e quebra de texto.
- `armazenamento.py`: validação, hash de senhas e arquivo de usuários.
- `cadastro.py`: tela de cadastro.
- `login.py`: tela de login.
- `area_usuario.py`: tela após login.
- `pesquisas.py`: busca e conteúdo sobre povos indígenas.
- `quiz.py`: quiz educativo.
- `usuarios.json`: será criado quando o primeiro usuário for cadastrado.

## Observação
O arquivo `usuarios.json` é criado na mesma pasta deste projeto. Não compartilhe esse arquivo ao publicar o repositório, pois ele pode conter dados pessoais de teste.
