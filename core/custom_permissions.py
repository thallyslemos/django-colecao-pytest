from rest_framework.permissions import BasePermission


class IsColecionador(BasePermission):
    def has_object_permission(self, request, view, objeto):
        # Apenas o colecionador pode editar ou excluir
        return objeto.colecionador == request.user
