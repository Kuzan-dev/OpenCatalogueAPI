from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    """
    Representa un perfil de usuario.

    Atributos:
        user (Usuario): El usuario asociado al perfil.
        avatar (ImageField): La imagen avatar del usuario.
        name (CharField): El nombre del usuario.
        created_at (DateTimeField): La fecha y hora en que se creó el perfil.
        updated_at (DateTimeField): La fecha y hora en que se actualizó el perfil por última vez.
    """
    # Define los campos del modelo.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     
     # Define el orden en que se mostrarán los perfiles.
    class Meta:
        ordering = ('-created_at',) # Ordena los perfiles por fecha de creación de forma descendente.

    # Define la representación de la clase.
    def __str__(self):
        return self.user.get_full_name() # Retorna el nombre completo del usuario asociado al perfil.