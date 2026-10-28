"""Contas de usuário: criar, entrar e excluir."""
from armazenamento import ErroDeArmazenamento, carregar_usuarios, salvar_usuarios
from povos import desvincular_autor
from senhas import gerar_hash, senha_confere
from validacao import REGEX_EMAIL, erros_cadastro, resumir_erros


def cadastrar_usuario(nome, email, senha):
    nome = nome.strip()
    email = email.strip().lower()

    erros = erros_cadastro(nome, email, senha)
    if erros:
        return False, resumir_erros(erros)
    try:
        usuarios = carregar_usuarios()
        if any(u.get("email", "").lower() == email for u in usuarios):
            return False, "Já existe uma conta com esse e-mail."
        usuarios.append({
            "nome": nome,
            "email": email,
            "senha": gerar_hash(senha)
        })
        salvar_usuarios(usuarios)
        return True, "Conta criada com sucesso!"
    except (ErroDeArmazenamento, KeyError, TypeError) as erro:
        return False, str(erro)


def verificar_login(email, senha):
    """Retorna (True, {"nome": ..., "email": ...}) ou (False, mensagem de erro)."""
    email = email.strip().lower()
    if not REGEX_EMAIL.match(email):
        return False, "Digite um e-mail válido."
    try:
        usuarios = carregar_usuarios()
        for usuario in usuarios:
            if not isinstance(usuario, dict):
                continue
            if usuario.get("email", "").lower() == email:
                if senha_confere(senha, usuario["senha"]):
                    return True, {"nome": usuario.get("nome", "Usuário"), "email": email}
                return False, "Senha incorreta."
        return False, "Não existe conta com esse e-mail."
    except (ErroDeArmazenamento, KeyError, TypeError, ValueError) as erro:
        return False, str(erro)


def excluir_usuario(email, senha):
    """Apaga a conta (exige a senha). Os povos adicionados continuam, mas sem o vínculo com o e-mail."""
    email = email.strip().lower()
    try:
        usuarios = carregar_usuarios()
        for i, usuario in enumerate(usuarios):
            if isinstance(usuario, dict) and usuario.get("email", "").lower() == email:
                if not senha_confere(senha, usuario["senha"]):
                    return False, "Senha incorreta."
                desvincular_autor(email)
                del usuarios[i]
                salvar_usuarios(usuarios)
                return True, "Conta excluída."
        return False, "Conta não encontrada."
    except (ErroDeArmazenamento, KeyError, TypeError, ValueError) as erro:
        return False, str(erro)
