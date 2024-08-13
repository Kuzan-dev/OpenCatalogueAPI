from django.urls import include, path
from .views import UserRegistrationView

# Define el espacio de nombres de la aplicación.
app_name = "users"

# Define las rutas de la aplicación.
urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user_register"), # Ruta para el registro de usuario.
]