from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from users.models import User


class UserService:
    """
    Service class to handle operations related to User model.

    This class provides methods to retrieve, create, and get a list of users.

    Usage:
    - Use the methods of this class to perform user-related operations.

    """

    @classmethod
    def get_by_id(cls, id):
        """
        Get a user by its primary key (ID).

        Arguments:
        - id: The primary key of the user to retrieve.

        Returns:
        - User instance if found.

        Raises:
        - Http404: If the user with the given ID does not exist.

        """
        return get_object_or_404(User, pk=id)

    @classmethod
    def sing_up(cls, serializer):
        """
        Sign up a new user and create an authentication token.

        Arguments:
        - serializer: An instance of the UserCreateSerializer.

        Returns:
        - A dictionary containing the created user instance and the associated authentication token.

        Raises:
        - ValidationError: If the serializer data is invalid.

        """
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = Token.objects.create(user=user)
            return {'user': user, 'token': token}

    @classmethod
    def get_list(cls):
        """
        Get a list of all users.

        Returns:
        - A queryset containing all user instances.

        """
        return User.objects.all()
