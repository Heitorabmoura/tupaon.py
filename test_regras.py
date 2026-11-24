"""Testes automatizados da camada de regras (sem pygame, sem abrir janela).

Executar na pasta do projeto:  python -m unittest -v
"""
import pathlib
import tempfile
import unittest

import armazenamento
import favoritos
import permissoes
import povos
import senhas
import usuarios
import validacao
from validacao import LIMITES_CONTEUDO


class BaseComArquivosTemporarios(unittest.TestCase):
    """Redireciona os JSON para uma pasta temporária, sem tocar nos dados reais."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        pasta = pathlib.Path(self._tmp.name)
        self._originais = (armazenamento.ARQUIVO, armazenamento.ARQUIVO_POVOS,
                           armazenamento.ARQUIVO_FAVORITOS)
        armazenamento.ARQUIVO = pasta / "usuarios.json"
        armazenamento.ARQUIVO_POVOS = pasta / "povos_usuarios.json"
        armazenamento.ARQUIVO_FAVORITOS = pasta / "favoritos.json"

    def tearDown(self):
        (armazenamento.ARQUIVO, armazenamento.ARQUIVO_POVOS,
         armazenamento.ARQUIVO_FAVORITOS) = self._originais
        self._tmp.cleanup()


class TestValidacao(unittest.TestCase):
    def test_cadastro_valido_nao_tem_erros(self):
        self.assertEqual(validacao.erros_cadastro("Ana Lima", "ana@x.com", "senha1234", "senha1234"), [])

    def test_varios_erros_sao_listados_de_uma_vez(self):
        erros = validacao.erros_cadastro("Jo", "joao@", "abc", "xyz")
        campos = {campo for campo, _ in erros}
        self.assertEqual(campos, {"Nome", "E-mail", "Senha", "Confirmar senha"})
        self.assertEqual(len(erros), 5)  # a senha "abc" falha em duas regras

    def test_resumo_diz_quando_ha_mais_de_um_erro(self):
        erros = validacao.erros_cadastro("Jo", "joao@", "senha1234")
        self.assertEqual(validacao.resumir_erros(erros), "Há 2 erros: Nome, E-mail.")

    def test_resumo_de_erro_unico_diz_a_regra(self):
        erros = validacao.erros_cadastro("Ana Lima", "ana@x.com", "senhaforte")
        self.assertEqual(validacao.resumir_erros(erros), "Senha: pelo menos um número.")

    def test_confirmacao_vazia_nao_conta_como_igual(self):
        self.assertFalse(validacao.regras_confirmacao("", "")[0][1])

    def test_erros_povo(self):
        erros = validacao.erros_povo("", "ab", "curto", "")
        self.assertEqual([campo for campo, _ in erros], ["Nome", "Região", "Sobre"])


class TestSenhas(unittest.TestCase):
    def test_hash_confere_e_nao_guarda_a_senha(self):
        dados = senhas.gerar_hash("senha1234")
        self.assertTrue(senhas.senha_confere("senha1234", dados))
        self.assertFalse(senhas.senha_confere("outra1234", dados))
        self.assertNotIn("senha1234", str(dados))

    def test_mesmo_texto_gera_hashes_diferentes(self):
        self.assertNotEqual(senhas.gerar_hash("senha1234")["hash"], senhas.gerar_hash("senha1234")["hash"])


class TestUsuarios(BaseComArquivosTemporarios):
    def test_cadastro_e_login(self):
        self.assertTrue(usuarios.cadastrar_usuario("Ana Lima", "ana@x.com", "senha1234")[0])
        ok, dados = usuarios.verificar_login("ANA@x.com", "senha1234")
        self.assertTrue(ok)
        self.assertEqual(dados, {"nome": "Ana Lima", "email": "ana@x.com"})

    def test_email_duplicado_e_senha_errada(self):
        usuarios.cadastrar_usuario("Ana Lima", "ana@x.com", "senha1234")
        self.assertFalse(usuarios.cadastrar_usuario("Outra Ana", "ana@x.com", "senha1234")[0])
        self.assertEqual(usuarios.verificar_login("ana@x.com", "errada123"), (False, "Senha incorreta."))

    def test_excluir_conta_exige_senha_correta(self):
        usuarios.cadastrar_usuario("Ana Lima", "ana@x.com", "senha1234")
        self.assertEqual(usuarios.excluir_usuario("ana@x.com", "errada123"), (False, "Senha incorreta."))
        self.assertTrue(usuarios.verificar_login("ana@x.com", "senha1234")[0])
        self.assertTrue(usuarios.excluir_usuario("ana@x.com", "senha1234")[0])
        self.assertFalse(usuarios.verificar_login("ana@x.com", "senha1234")[0])


class TestPovos(BaseComArquivosTemporarios):
    TEXTO = "Povo de Pesqueira, no agreste de Pernambuco."

    def test_criar_e_listar(self):
        self.assertTrue(povos.salvar_povo("ana@x.com", "Xukuru", "Pernambuco", self.TEXTO, "")[0])
        self.assertEqual([p["nome"] for p in povos.listar_povos_do_usuario("ana@x.com")], ["Xukuru"])
        nomes = [p["nome"] for p in povos.obter_povos()]
        self.assertIn("Xukuru", nomes)
        self.assertIn("Guarani", nomes)  # conteúdo base continua presente

    def test_conteudo_base_nao_pode_ser_sobrescrito(self):
        ok, _ = povos.salvar_povo("ana@x.com", "guarani", "Brasil", self.TEXTO, "")
        self.assertFalse(ok)

    def test_editar_e_renomear_o_proprio_povo(self):
        povos.salvar_povo("ana@x.com", "Xukuru", "Pernambuco", self.TEXTO, "")
        ok, msg = povos.salvar_povo("ana@x.com", "Xukuru do Ororubá", "Pernambuco", self.TEXTO,
                                    "", nome_original="Xukuru")
        self.assertEqual((ok, msg), (True, "Informações atualizadas!"))
        self.assertEqual([p["nome"] for p in povos.listar_povos_do_usuario("ana@x.com")], ["Xukuru do Ororubá"])

    def test_outro_usuario_nao_toma_nem_edita_a_entrada(self):
        povos.salvar_povo("ana@x.com", "Xukuru", "Pernambuco", self.TEXTO, "")
        self.assertFalse(povos.salvar_povo("beto@x.com", "Xukuru", "Pernambuco", self.TEXTO, "")[0])
        self.assertFalse(povos.excluir_povo("beto@x.com", "Xukuru")[0])

    def test_excluir_conta_mantem_povos_sem_vinculo(self):
        usuarios.cadastrar_usuario("Ana Lima", "ana@x.com", "senha1234")
        povos.salvar_povo("ana@x.com", "Xukuru", "Pernambuco", self.TEXTO, "")
        usuarios.excluir_usuario("ana@x.com", "senha1234")
        restantes = armazenamento.carregar_povos_usuarios()
        self.assertEqual([(p["nome"], p["autor"]) for p in restantes], [("Xukuru", None)])


class TestFavoritos(BaseComArquivosTemporarios):
    TEXTO = "Povo de Pesqueira, no agreste de Pernambuco."

    def test_favoritar_e_desfavoritar(self):
        self.assertEqual(favoritos.alternar_favorito("ana@x.com", "Guarani"), (True, "Adicionado aos favoritos!"))
        self.assertEqual(favoritos.listar_favoritos("ana@x.com"), ["Guarani"])
        self.assertEqual(favoritos.alternar_favorito("ana@x.com", "guarani"), (True, "Removido dos favoritos."))
        self.assertEqual(favoritos.listar_favoritos("ana@x.com"), [])

    def test_favoritos_sao_separados_por_usuario(self):
        favoritos.alternar_favorito("ana@x.com", "Guarani")
        favoritos.alternar_favorito("beto@x.com", "Tikuna")
        self.assertEqual(favoritos.listar_favoritos("ana@x.com"), ["Guarani"])
        self.assertEqual(favoritos.listar_favoritos("beto@x.com"), ["Tikuna"])

    def test_nome_vazio_e_recusado(self):
        self.assertFalse(favoritos.alternar_favorito("ana@x.com", "   ")[0])

    def test_renomear_povo_mantem_o_favorito_de_todos(self):
        povos.salvar_povo("ana@x.com", "Xukuru", "Pernambuco", self.TEXTO, "")
        favoritos.alternar_favorito("beto@x.com", "Xukuru")
        povos.salvar_povo("ana@x.com", "Xukuru do Ororubá", "Pernambuco", self.TEXTO, "",
                          nome_original="Xukuru")
        self.assertEqual(favoritos.listar_favoritos("beto@x.com"), ["Xukuru do Ororubá"])

    def test_excluir_povo_remove_dos_favoritos_de_todos(self):
        povos.salvar_povo("ana@x.com", "Xukuru", "Pernambuco", self.TEXTO, "")
        favoritos.alternar_favorito("beto@x.com", "Xukuru")
        favoritos.alternar_favorito("beto@x.com", "Guarani")
        povos.excluir_povo("ana@x.com", "Xukuru")
        self.assertEqual(favoritos.listar_favoritos("beto@x.com"), ["Guarani"])

    def test_excluir_conta_apaga_os_favoritos_da_pessoa(self):
        usuarios.cadastrar_usuario("Ana Lima", "ana@x.com", "senha1234")
        favoritos.alternar_favorito("ana@x.com", "Guarani")
        favoritos.alternar_favorito("beto@x.com", "Guarani")
        usuarios.excluir_usuario("ana@x.com", "senha1234")
        self.assertEqual(favoritos.listar_favoritos("ana@x.com"), [])
        self.assertEqual(favoritos.listar_favoritos("beto@x.com"), ["Guarani"])


class TestConteudoBase(unittest.TestCase):
    """Garante que o conteúdo dos povos base está completo, com fontes, e cabe na tela."""

    def test_cada_povo_base_tem_todas_as_abas(self):
        for povo in povos.POVOS:
            with self.subTest(povo=povo["nome"]):
                self.assertGreaterEqual(len(povo["palavras"]), 5)
                self.assertGreaterEqual(len(povo["culinaria"]), 5)
                self.assertTrue(povo["fonte_palavras"])
                self.assertTrue(povo["fonte_culinaria"])
                for chave in ("mitologia", "narrativa"):
                    self.assertTrue(povo[chave]["titulo"])
                    self.assertTrue(povo[chave]["texto"])
                    self.assertTrue(povo[chave]["fonte"])

    def test_mitologia_e_narrativa_nao_repetem_o_mesmo_texto(self):
        for povo in povos.POVOS:
            with self.subTest(povo=povo["nome"]):
                self.assertNotEqual(povo["mitologia"]["texto"], povo["narrativa"]["texto"])
                self.assertNotEqual(povo["mitologia"]["titulo"], povo["narrativa"]["titulo"])

    def test_tamanhos_cabem_na_tela(self):
        L = LIMITES_CONTEUDO
        for povo in povos.POVOS:
            with self.subTest(povo=povo["nome"]):
                for item in povo["palavras"]:
                    self.assertLessEqual(len(item["palavra"]), L["palavra"])
                    self.assertLessEqual(len(item["significado"]), L["significado"])
                for item in povo["culinaria"]:
                    self.assertLessEqual(len(item["prato"]), L["prato"], item["prato"])
                    self.assertLessEqual(len(item["descricao"]), L["descricao"], item["descricao"])
                for chave in ("observacao_palavras", "observacao_culinaria"):
                    self.assertLessEqual(len(povo[chave]), L["observacao"])
                for chave in ("fonte_palavras", "fonte_culinaria"):
                    self.assertLessEqual(len(povo[chave]), L["fonte"])
                for chave in ("mitologia", "narrativa"):
                    self.assertLessEqual(len(povo[chave]["titulo"]), L["narrativa_titulo"])
                    self.assertLessEqual(len(povo[chave]["texto"]), L["narrativa_texto"])
                    self.assertLessEqual(len(povo[chave]["fonte"]), L["fonte"])

    def test_itens_nao_se_repetem_dentro_do_povo(self):
        for povo in povos.POVOS:
            for chave, campo in (("palavras", "palavra"), ("culinaria", "prato")):
                nomes = [i[campo].casefold() for i in povo[chave]]
                self.assertEqual(len(nomes), len(set(nomes)), f"{povo['nome']} / {chave}")


class TestObterPovosComConteudo(BaseComArquivosTemporarios):
    def test_base_traz_conteudo_e_povo_de_usuario_vem_sem(self):
        povos.salvar_povo("ana@x.com", "Xukuru", "Pernambuco", "Povo de Pesqueira, no agreste de Pernambuco.", "")
        por_nome = {p["nome"]: p for p in povos.obter_povos()}
        self.assertTrue(por_nome["Guarani"]["palavras"])
        self.assertTrue(por_nome["Guarani"]["culinaria"])
        self.assertIsNotNone(por_nome["Guarani"]["mitologia"])
        self.assertIsNotNone(por_nome["Guarani"]["narrativa"])
        self.assertEqual(por_nome["Xukuru"]["palavras"], [])
        self.assertEqual(por_nome["Xukuru"]["culinaria"], [])
        self.assertIsNone(por_nome["Xukuru"]["mitologia"])
        self.assertIsNone(por_nome["Xukuru"]["narrativa"])
        self.assertTrue(por_nome["Xukuru"]["comunidade"])

    def test_obter_povos_nao_altera_o_conteudo_base(self):
        povos.obter_povos()[0]["palavras"].append({"palavra": "x", "significado": "y"})
        self.assertNotIn("x", [i["palavra"] for i in povos.POVOS[0]["palavras"]])


class TestPermissoes(unittest.TestCase):
    def test_lista_de_administradores(self):
        self.assertTrue(permissoes.eh_administrador("heitor.alves@ufrpe.br"))
        self.assertTrue(permissoes.eh_administrador("ivan.guilherme@ufrpe.br"))

    def test_ignora_maiusculas_e_espacos(self):
        self.assertTrue(permissoes.eh_administrador("  Heitor.Alves@UFRPE.br "))

    def test_outros_e_valores_invalidos_nao_sao_administradores(self):
        self.assertFalse(permissoes.eh_administrador("ana@x.com"))
        self.assertFalse(permissoes.eh_administrador("heitor.alves@ufrpe.com"))   # domínio diferente
        self.assertFalse(permissoes.eh_administrador(""))
        self.assertFalse(permissoes.eh_administrador(None))


class TestRemocaoPeloAdministrador(BaseComArquivosTemporarios):
    TEXTO = "Povo de Pesqueira, no agreste de Pernambuco."
    ADM = "heitor.alves@ufrpe.br"

    def setUp(self):
        super().setUp()
        povos.salvar_povo("ana@x.com", "Xukuru", "Pernambuco", self.TEXTO, "")

    def _nomes(self):
        return [p["nome"] for p in povos.obter_povos()]

    def test_usuario_comum_nao_remove_povo_de_outra_pessoa(self):
        ok, _ = povos.excluir_povo_como_admin("beto@x.com", "Xukuru")
        self.assertFalse(ok)
        self.assertIn("Xukuru", self._nomes())

    def test_dono_sem_ser_admin_tambem_nao_usa_a_funcao_de_admin(self):
        self.assertFalse(povos.excluir_povo_como_admin("ana@x.com", "Xukuru")[0])
        self.assertIn("Xukuru", self._nomes())

    def test_admin_remove_povo_de_qualquer_usuario(self):
        self.assertEqual(povos.excluir_povo_como_admin(self.ADM, "xukuru"),
                         (True, "Povo removido pelo administrador."))
        self.assertNotIn("Xukuru", self._nomes())

    def test_admin_remove_povo_de_conta_ja_excluida(self):
        usuarios.cadastrar_usuario("Ana Lima", "ana@x.com", "senha1234")
        usuarios.excluir_usuario("ana@x.com", "senha1234")      # povo fica com autor None
        self.assertTrue(povos.excluir_povo_como_admin(self.ADM, "Xukuru")[0])
        self.assertNotIn("Xukuru", self._nomes())

    def test_admin_nao_remove_povo_do_conteudo_base(self):
        ok, _ = povos.excluir_povo_como_admin(self.ADM, "Guarani")
        self.assertFalse(ok)
        self.assertIn("Guarani", self._nomes())

    def test_povo_inexistente(self):
        self.assertEqual(povos.excluir_povo_como_admin(self.ADM, "Nao existe"), (False, "Povo não encontrado."))

    def test_remocao_tira_o_povo_dos_favoritos_de_todos(self):
        favoritos.alternar_favorito("beto@x.com", "Xukuru")
        favoritos.alternar_favorito("beto@x.com", "Guarani")
        povos.excluir_povo_como_admin(self.ADM, "Xukuru")
        self.assertEqual(favoritos.listar_favoritos("beto@x.com"), ["Guarani"])


if __name__ == "__main__":
    unittest.main()
