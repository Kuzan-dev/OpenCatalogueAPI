from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
# Obtiene el modelo de usuario.
User = get_user_model()

# Define el backend de autenticación personalizado.
class EmailAuthBackend(ModelBackend):
    """
    Backend de autenticación personalizado que autentica a los usuarios en función de su dirección de correo electrónico.
    """
    # Define el método de autenticación.
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica a un usuario basándose en su dirección de correo electrónico y contraseña.

        Args:
            request (HttpRequest): El objeto de petición actual.
            username (str): La dirección de correo electrónico del usuario.
            password (str): La contraseña del usuario.

        Devuelve:
            Usuario: El usuario autenticado si el email y la contraseña son correctos, Ninguno en caso contrario.
        """
        # Verifica si se proporcionó un nombre de usuario y contraseña.
        try:
            # Obtiene el usuario basado en la dirección de correo electrónico.
            user = User.objects.get(email=username)
            # Verifica la contraseña del usuario.
            if user.check_password(password):
                # Devuelve el usuario si la contraseña es correcta.
                return user
            # Devuelve Ninguno si la contraseña es incorrecta.
        except User.DoesNotExist:
            return None
           
    # Define el método para obtener un usuario.
    def get_user(self, user_id):
        """
        Recupera un usuario basándose en su ID de usuario.

        Args:
            user_id (str): El ID del usuario.

        Devuelve:
            Usuario: El usuario con el ID especificado si se encuentra, Ninguno en caso contrario.
        """
        # Obtiene el modelo de usuario.
        UserModel = get_user_model()
        # Verifica si se proporcionó un ID de usuario.
        try:
            # Obtiene el usuario basado en el ID de usuario.
            return UserModel.objects.get(pk=user_id)
        # Devuelve Ninguno si el usuario no se encuentra.
        except UserModel.DoesNotExist:
            return None