
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users.views import GoogleLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    path('user/login/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/', include('products.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)