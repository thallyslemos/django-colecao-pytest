from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    LivroList, LivroDetail, CategoriaList, CategoriaDetail,
    AutorList, AutorDetail, ColecaoListCreate, ColecaoDetail
)

urlpatterns = [
    # URLs para Livros
    path('livros/', LivroList.as_view(), name='livros-list'),
    path('livros/<int:pk>/', LivroDetail.as_view(), name='livro-detail'),
    
    # URLs para Categorias
    path('categorias/', CategoriaList.as_view(), name='categorias-list'),
    path('categorias/<int:pk>/', CategoriaDetail.as_view(), name='categoria-detail'),
    
    # URLs para Autores
    path('autores/', AutorList.as_view(), name='autores-list'),
    path('autores/<int:pk>/', AutorDetail.as_view(), name='autor-detail'),
    
    # URLs para Coleções
    path('colecoes/', ColecaoListCreate.as_view(), name='colecao-list-create'),
    path('colecoes/<int:pk>/', ColecaoDetail.as_view(), name='colecao-detail'),
    
    # Endpoint de autenticação por token
    path('api/token-auth/', obtain_auth_token, name='api-token-auth'),
]
