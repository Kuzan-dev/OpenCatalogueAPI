from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, RegisterView
from dj_rest_auth.views import LoginView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _ 
from rest_framework import permissions, status
from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    
)
from rest_framework.response import Response
from allauth.account.utils import send_email_confirmation
from rest_framework.viewsets import ReadOnlyModelViewSet
from users.models import  Profile
from users.serializers import (
    UserRegistrationSerializer,
   
)
from django.conf import settings

# Create your views here.

# Obtiene el modelo de usuario.
User = get_user_model()
# Define la vista para el registro de usuario.
class UserRegistrationView(RegisterView):
    """
    Clase de visualización para el registro de usuarios.
    """
    # Define el serializador para el registro de usuario.
    serializer_class = UserRegistrationSerializer
    
    # Define los permisos para el registro de usuario.
    def create(self, request, *args, **kwargs):
        # Obtiene el serializador de la solicitud.
        serializer = self.get_serializer(data=request.data)
        # Valida el serializador.
        serializer.is_valid(raise_exception=True)
        # Crea el usuario.
        user = self.perform_create(serializer)
        # Obtiene los encabezados de éxito.
        headers = self.get_success_headers(serializer.data)
        # Obtiene los datos de respuesta.
        response_data = ''
        # Verifica si se requiere verificación de correo electrónico.
        email = request.data.get('email', None)
        # Verifica si se requiere verificación de correo electrónico.
        if email:
            response_data = {
                'email': email,
                'message': 'Please verify your email to continue registration.'
            }
       
        # Devuelve la respuesta.
        return Response(response_data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)
   


    
    









class GoogleLogin(SocialLoginView):
    """
    View class for handling Google login.
    """
    adapter_class = GoogleOAuth2Adapter   # Adapter class for Google OAuth2
    client_class = OAuth2Client          # OAuth2 client class
    callback_url = "http://localhost:3000/login" # Callback URL for Google OAuth2
   