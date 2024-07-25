from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
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
from rest_framework.viewsets import ReadOnlyModelViewSet
from users.models import  Profile
from users.serializers import (
    UserRegistrationSerializer,
   
)
from django.conf import settings

# Create your views here.

User = get_user_model()

class UserRegistrationView(GenericAPIView):
    """
    View class for user registration.
    """
    serializer_class = UserRegistrationSerializer
    

    def create(self, request, *args, **kwargs):
        """
        Creates a new user.
        """
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request)  # Modificado para pasar request como argumento
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, request):
        serializer.save(request=request)  # Modificado para incluir request como argumento

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[User.USERNAME_FIELD])}
        except (TypeError, KeyError):
            return {}








class GoogleLogin(SocialLoginView):
    """
    View class for handling Google login.
    """
    adapter_class = GoogleOAuth2Adapter   # Adapter class for Google OAuth2
    client_class = OAuth2Client          # OAuth2 client class
    callback_url = "http://localhost:3000/login" # Callback URL for Google OAuth2
   