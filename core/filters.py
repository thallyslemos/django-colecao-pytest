from django_filters import rest_framework as filters
from .models import Livro, Categoria, Autor

# Filtro para o modelo Livro (já existente)
class LivroFilter(filters.FilterSet):
    titulo = filters.CharFilter(lookup_expr='icontains')
    autor = filters.CharFilter(field_name='autor__nome', lookup_expr='icontains')
    categoria = filters.AllValuesFilter(field_name='categoria__nome')

    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'categoria']


# Filtro para o modelo Categoria
class CategoriaFilter(filters.FilterSet):
    nome = filters.CharFilter(lookup_expr='icontains')  # Busca por nome da categoria (case-insensitive)

    class Meta:
        model = Categoria
        fields = ['nome']


# Filtro para o modelo Autor
class AutorFilter(filters.FilterSet):
    nome = filters.CharFilter(lookup_expr='icontains')  # Busca por nome do autor (case-insensitive)

    class Meta:
        model = Autor
        fields = ['nome']
