"""
This module defines the URL patterns for the OpenCatalogueAPI application.

The urlpatterns list contains the following URL patterns:
- '/admin/': The URL pattern for the Django admin site.
- '/auth/': The URL pattern for the dj_rest_auth endpoints.
- '/api-auth/': The URL pattern for the rest_framework authentication endpoints.
- '/user/login/google/': The URL pattern for the Google login view.
- '/account-confirm-email/<key>/': The URL pattern for the email verification view.
- '/resend-email-verification/': The URL pattern for the email verification view.
- '/account-email-verification-sent/': The URL pattern for the email verification view. 

These URL patterns are used to map the specified URLs to their corresponding views.
"""


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from users.views import GoogleLogin
from django.views.generic import TemplateView
from dj_rest_auth.registration.views import VerifyEmailView , ResendEmailVerificationView, RegisterView

urlpatterns = [
        
    path('admin/', admin.site.urls), # URL pattern for the Django admin site
    
    path('api-auth/', include('rest_framework.urls',namespace='rest_framework')), # URL pattern for the rest_framework authentication endpoints
   
    path('user/login/google/', GoogleLogin.as_view(), name='google_login'), # URL pattern for the Google login view
    path('api/user/', include('users.urls', namespace="users")), # URL pattern for the users app
    path('api/', include('products.urls')),
    
    # URL pattern for the email verification view
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    path('resend-email-verification/', ResendEmailVerificationView.as_view(), name='resend_email_verification'),
    path('account-email-verification-sent/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)