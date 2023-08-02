from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for the User model.

    This serializer is used to transform User model instances into JSON representation.
    It includes the fields 'id', 'email', and 'name' of the User model.

    Usage:
    - When serializing a User instance, initialize the serializer with the User object as the data argument.

    """

    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class UserCreateSerializer(serializers.Serializer):
    """
    Serializer class for creating a new User instance.

    This serializer handles the validation and creation of a new User object.
    It includes fields for 'email', 'password', and 'name'.
    The 'email' field is validated to ensure it is unique.

    Usage:
    - When creating a new User instance, initialize the serializer with the data to be validated and saved.

    """

    email = serializers.EmailField()
    password = serializers.CharField()
    name = serializers.CharField()

    def validate_email(self, value):
        """
        Validate that the email is not already registered in the database.

        Arguments:
        - value: Email value to be validated.

        Returns:
        - Email value if validation is successful.

        Raises:
        - ValidationError: If the email is already registered.

        """
        if User.objects.filter(email=value).exists():
            raise ValidationError('User with this email exists')
        return value

    def create(self, validated_data):
        """
        Create and save a new User instance.

        Arguments:
        - validated_data: A dictionary containing the validated data for creating the new User.

        Returns:
        - The created User instance.

        """
        user = get_user_model().objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
