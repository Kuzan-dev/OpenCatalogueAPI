from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings

# Create your views here.


class GoogleLogin(SocialLoginView):
    
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "call_back_url"
    # callback_url = "http://localhost:8000"