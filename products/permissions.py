from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsAdmin(BasePermission):
    """
    Permiso personalizado que permite a los administradores
    realizar ciertas acciones.
    """

    def has_permission(self, request, view):
      # Permitir acceso solo a administradores
      if request.method in SAFE_METHODS:
        return True
      
      return request.user.is_authenticated and request.user.is_admin
