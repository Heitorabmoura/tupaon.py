# Tupã — Cultura e Conhecimento dos Povos Originários

## Sobre o projeto

O Tupã é um aplicativo desenvolvido em Python com o objetivo de promover o conhecimento e dar visibilidade à diversidade dos povos originários. A proposta é reunir informações culturais em uma interface simples e oferecer recursos interativos para apoiar o aprendizado.

## Objetivo

Utilizar a tecnologia para facilitar o acesso a informações sobre os povos originários, contribuindo para o reconhecimento e a valorização de suas histórias, culturas e tradições.

## Funcionalidades atuais — Release 1.0

- **Menu inicial:** acesso às funcionalidades principais do aplicativo.
- **Cadastro de usuário:** criação de conta com validação dos campos preenchidos.
- **Login:** verificação das credenciais de um usuário cadastrado.
- **Mostrar/ocultar senha:** opção para visualizar ou esconder a senha durante o preenchimento.
- **Navegação entre telas:** botões para voltar ao menu e sair do aplicativo.
- **Pesquisa de povos:** busca de informações iniciais sobre povos como Guarani, Yanomami, Tikuna e Pataxó.
- **Quiz educativo:** perguntas de múltipla escolha com contagem de pontos.

> Observação: a pesquisa e o quiz estão em uma versão inicial e podem ser ampliados nas próximas etapas do projeto.

## Tecnologias e bibliotecas

- **Python:** linguagem utilizada no desenvolvimento.
- **Pygame:** criação da janela, interface gráfica, textos, botões e tratamento de eventos.
- **JSON (`json`):** armazenamento dos dados de cadastro no arquivo `usuarios.json`.
- **`hashlib`:** geração de hashes de senha.
- **`os`:** geração de dados aleatórios usados no processo de proteção das senhas.
- **`re`:** validação do formato do e-mail por expressão regular.
- **`pathlib`:** manipulação do caminho do arquivo de dados.

## Como executar

### Requisitos

- Python 3 instalado.
- Biblioteca Pygame instalada.

### Instalação

1. Baixe ou clone o repositório do projeto.
2. Abra um terminal na pasta do projeto.
3. Instale o Pygame:

   ```bash
   python -m pip install pygame
   ```

4. Execute o aplicativo:

   ```bash
   python tupa_corrigido.py
   ```

   Se o comando `python` não funcionar no Windows, tente:

   ```bash
   py tupa_corrigido.py
   ```

> Se o arquivo principal tiver outro nome no repositório, substitua `tupa_corrigido.py` pelo nome correto.

## Armazenamento de usuários

Os dados das contas são armazenados localmente em `usuarios.json`, criado ou atualizado pelo aplicativo. Mantenha esse arquivo na pasta esperada pelo programa para que as contas cadastradas continuem disponíveis entre execuções.

## Próximas melhorias

- Ampliar e revisar as informações culturais com fontes confiáveis, incluindo materiais produzidos pelos próprios povos indígenas.
- Adicionar novas perguntas ao quiz.
- Melhorar a organização e a navegação do conteúdo.
- Realizar testes e corrigir problemas encontrados durante o desenvolvimento.

## Público-alvo

Estudantes, professores e pessoas interessadas em conhecer mais sobre os povos originários e a diversidade de suas culturas.

## Integrantes

- Ivan Guilherme
- Heitor Alves

## Status

Em desenvolvimento.
