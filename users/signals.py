from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile

# Obtiene el modelo de usuario.
User = get_user_model()

# Define la señal para crear un perfil cuando se crea un usuario.
@receiver(post_save, sender=User)
# Define la señal para guardar el perfil cuando se guarda un usuario.
def create_profile(sender, instance, created, **kwargs):
    """
   Crea un perfil para el usuario cuando se cree este.

    Argumentos:
        sender: el remitente de la señal.
        Instancia: la instancia del usuario.
        Creado: un booleano que indica si el usuario fue creado.
        kwargs: argumentos adicionales de palabra clave.

    Devuelve:
        Ninguno.
    """
    # Verifica si el usuario fue creado.
    if created:
        Profile.objects.create(user=instance)
        print(f"Profile created for {instance.username}.")

# Define la señal para guardar el perfil cuando se guarda un usuario.
@receiver(post_save, sender=User)
# Define la señal para guardar el perfil cuando se guarda un usuario.
def save_profile(sender, instance, **kwargs):
    """
   Guarda el perfil cuando se guarda el usuario.

    Args:
        sender: El remitente de la señal.
        instancia: La instancia del usuario.
        **kwargs: Argumentos adicionales de palabra clave.

    Devuelve:
        Ninguno
    """
    # Guarda el perfil del usuario.
    instance.profile.save()
    print(f"Profile saved for {instance.username}.")