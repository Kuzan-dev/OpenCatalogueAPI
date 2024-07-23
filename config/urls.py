
from django.contrib import admin
from django.urls import path, include
from users.views import GoogleLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    path('user/login/google/', GoogleLogin.as_view(), name='google_login'),
]
