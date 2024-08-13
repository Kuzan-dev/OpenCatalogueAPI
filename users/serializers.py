from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserRegistrationSerializer(RegisterSerializer):
    """
   Serializador para registro de usuarios.

    Este serializador se utiliza para registrar nuevos usuarios. Valida el usuario
    correo electrónico, nombre, apellido y contraseña. También proporciona métodos para
    limpieza y creación de datos adicionales para el usuario.

    Atributos:
        nombre de usuario: el nombre de usuario del usuario (no utilizado en este serializador).
        first_name: el nombre del usuario.
        last_name: El apellido del usuario.
        correo electrónico: La dirección de correo electrónico del usuario.

    Métodos:
        validar: Valida el correo electrónico y la contraseña del usuario.
        get_cleaned_data_extra: devuelve datos limpios adicionales para el usuario.
        create_extra: Crea datos adicionales para el usuario.
        custom_signup: realiza una lógica de registro personalizada para el usuario.

    """
     # Define los campos del serializador.
    username = None
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all(),
                message=_("A user is already registered with this email."),
            )
        ],
    )

    # Define los campos de contraseña.

    def validate(self, validated_data):
        """
        Valida el email y la contraseña del usuario.

        Args:
            datos_validados: Los datos validados para el serializador.

        Suena:
            serializers.ValidationError: Si falta el email o las
                contraseñas no coinciden.

        Devuelve:
            Los datos validados.
        """
        # Obtiene el email del usuario.
        email = validated_data.get("email")

        # Verifica si el email está presente.
        if not email:
            raise serializers.ValidationError(_("Email is required."))
        # Verifica si las contraseñas coinciden.
        if validated_data["password1"] != validated_data["password2"]:
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )

        return validated_data

       # Define los campos de contraseña.
    def get_cleaned_data_extra(self):
        """
        Devuelve datos extra limpiados para el usuario.

        Devuelve:
            Un diccionario que contiene el nombre y apellidos del usuario.
        """
        # Devuelve los datos limpios adicionales para el usuario.
        return {
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
        }
    # Define los campos de contraseña.

    def create_extra(self, user, validated_data):
        """
        Returns extra data cleared for the user.

        Returns:
            A dictionary containing the user's first and last name.
        """
        # Crea datos adicionales para el usuario.
        user.first_name = self.validated_data.get("first_name")
        user.last_name = self.validated_data.get("last_name")
        user.save()

        # Define el serializador de registro de usuario.

    def custom_signup(self, request, user):
        """
        Realiza la lógica de registro personalizada para el usuario.

        Args:
            request: El objeto de petición HTTP.
            user: El objeto usuario.
        """
        # Crea datos adicionales para el usuario.
        self.create_extra(user, self.get_cleaned_data_extra())