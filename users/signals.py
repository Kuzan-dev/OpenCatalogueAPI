from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Creates a profile for the user when the user is created.

    Args:
        sender: The sender of the signal.
        instance: The instance of the user.
        created: A boolean indicating whether the user was created.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if created:
        Profile.objects.create(user=instance)
        print(f"Profile created for {instance.username}.")

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Saves the profile when the user is saved.

    Args:
        sender: The sender of the signal.
        instance: The instance of the user.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    instance.profile.save()
    print(f"Profile saved for {instance.username}.")