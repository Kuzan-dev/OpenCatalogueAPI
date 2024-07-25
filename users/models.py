from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    """
    Represents a user profile.

    Attributes:
        user (User): The user associated with the profile.
        avatar (ImageField): The avatar image of the user.
        name (CharField): The name of the user.
        created_at (DateTimeField): The date and time when the profile was created.
        updated_at (DateTimeField): The date and time when the profile was last updated.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',) # Orders the profiles by the date and time they were created in descending order.

    
    def __str__(self):
        return self.user.get_full_name() # Returns the full name of the user associated with the profile.