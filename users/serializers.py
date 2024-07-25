from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserRegistrationSerializer(RegisterSerializer):
    """
    Serializer for user registration.

    This serializer is used for registering new users. It validates the user's
    email, first name, last name, and password. It also provides methods for
    cleaning and creating extra data for the user.

    Attributes:
        username: The username of the user (not used in this serializer).
        first_name: The first name of the user.
        last_name: The last name of the user.
        email: The email address of the user.

    Methods:
        validate: Validates the user's email and password.
        get_cleaned_data_extra: Returns extra cleaned data for the user.
        create_extra: Creates extra data for the user.
        custom_signup: Performs custom signup logic for the user.
    """

    username = None
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all(),
                message=_("A user is already registered with this email."),
            )
        ],
    )

    def validate(self, validated_data):
        """
        Validates the user's email and password.

        Args:
            validated_data: The validated data for the serializer.

        Raises:
            serializers.ValidationError: If the email is missing or the
                passwords don't match.

        Returns:
            The validated data.
        """
        email = validated_data.get("email")

        if not email:
            raise serializers.ValidationError(_("Email is required."))

        if validated_data["password1"] != validated_data["password2"]:
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )

        return validated_data

    def get_cleaned_data_extra(self):
        """
        Returns extra cleaned data for the user.

        Returns:
            A dictionary containing the first name and last name of the user.
        """
        return {
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
        }

    def create_extra(self, user, validated_data):
        """
        Creates extra data for the user.

        Args:
            user: The user object.
            validated_data: The validated data for the serializer.
        """
        user.first_name = self.validated_data.get("first_name")
        user.last_name = self.validated_data.get("last_name")
        user.save()

    def custom_signup(self, request, user):
        """
        Performs custom signup logic for the user.

        Args:
            request: The HTTP request object.
            user: The user object.
        """
        self.create_extra(user, self.get_cleaned_data_extra())