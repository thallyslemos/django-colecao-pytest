from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from core.models import Colecao, Livro, Categoria, Autor


class ColecaoTestCase(APITestCase):
    def setUp(self):
        # Criação de usuários
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

        # Criação de autores
        self.autor1 = Autor.objects.create(nome="Autor 1")
        self.autor2 = Autor.objects.create(nome="Autor 2")

        # Configuração do cliente autenticado
        self.client = APIClient()

        # Criação de categorias e livros
        self.categoria1 = Categoria.objects.create(nome="Ficção")
        self.categoria2 = Categoria.objects.create(nome="Não-Ficção")
        self.livro1 = Livro.objects.create(
            titulo="Livro 1",
            publicado_em="2024-01-01",
            autor=self.autor1,
            categoria=self.categoria1
        )
        self.livro2 = Livro.objects.create(
            titulo="Livro 2",
            publicado_em="2024-02-01",
            autor=self.autor2,
            categoria=self.categoria2
        )

    def test_criacao_colecao(self):
        """Testa se uma nova coleção é criada e associada ao usuário autenticado."""
        self.client.force_authenticate(user=self.user1)
        data = {
            "nome": "Minha Coleção",
            "descricao": "Descrição da coleção",
            "livros": [self.livro1.id, self.livro2.id],
        }
        response = self.client.post("/api/colecoes/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["colecionador"], self.user1.id)

    def test_listagem_colecoes(self):
        """Testa se a listagem de coleções é visível para usuários autenticados."""
        # Criar coleções associadas ao user1
        Colecao.objects.create(nome="Coleção 1", descricao="Descrição", colecionador=self.user1)
        Colecao.objects.create(nome="Coleção 2", descricao="Outra Descrição", colecionador=self.user1)

        # Listar como user1
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/colecoes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

        # Listar sem autenticação
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/colecoes/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permissoes_edicao_colecao(self):
        """Testa se apenas o colecionador pode editar sua coleção."""
        # Criar uma coleção associada ao user1
        colecao = Colecao.objects.create(
            nome="Coleção Teste", descricao="Descrição", colecionador=self.user1
        )
        colecao.livros.add(self.livro1)

        # Tentar editar como user2
        self.client.force_authenticate(user=self.user2)
        data = {"nome": "Tentativa de Edição"}
        response = self.client.patch(f"/api/colecoes/{colecao.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Editar como user1
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(f"/api/colecoes/{colecao.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome"], "Tentativa de Edição")

    def test_permissoes_acesso_nao_autenticado(self):
        """Testa se usuários não autenticados não podem criar, atualizar ou deletar coleções."""
        # Tentativa de criar coleção sem autenticação
        data = {
            "nome": "Coleção Sem Autenticação",
            "descricao": "Descrição",
            "livros": [self.livro1.id],
        }
        response = self.client.post("/api/colecoes/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delecao_colecao(self):
        """Testa se somente o colecionador pode deletar sua coleção."""
        # Criar uma coleção associada ao user1
        colecao = Colecao.objects.create(
            nome="Coleção Deletável", descricao="Descrição", colecionador=self.user1
        )
        colecao.livros.add(self.livro1)

        # Tentar deletar como user2
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f"/api/colecoes/{colecao.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Deletar como user1
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f"/api/colecoes/{colecao.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Colecao.objects.filter(id=colecao.id).exists())
