from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailAuthBackend(BaseBackend):
    """
    Custom authentication backend that authenticates users based on their email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticates a user based on their email address and password.

        Args:
            request (HttpRequest): The current request object.
            username (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            User: The authenticated user if the email and password are correct, None otherwise.
        """
        try:
            # Attempt to retrieve the user using the email address
            user = User.objects.get(email=username)
            # Verify if the password is correct
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Retrieves a user based on their user ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            User: The user with the specified ID if found, None otherwise.
        """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None