from rest_framework.permissions import BasePermission

class IsInAnyGroupPermission(BasePermission):
    """
    Permissão que verifica se o usuário pertence a pelo menos um dos grupos permitidos.
    """
    allowed_groups = []  # Lista de grupos permitidos, definida como variável de classe

    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado e pertence a pelo menos um dos grupos permitidos
        return request.user and request.user.is_authenticated and request.user.groups.filter(name__in=self.allowed_groups).exists()

class IsAdminOrEditorPermission(IsInAnyGroupPermission):
    allowed_groups = ['admin', 'team']

class IsViewerPermission(IsInAnyGroupPermission):
    allowed_groups = ['student']