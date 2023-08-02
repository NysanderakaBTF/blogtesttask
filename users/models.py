from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom User Manager for the User model.

    This manager provides methods to create regular users and superusers.
    It also includes validation to ensure that required fields (name, email, and password) are set.

    Usage:
    - When creating a new user, call `create_user()` method.
    - When creating a superuser, call `create_superuser()` method.

    """

    use_in_migrations = True

    def _create_user(self, name, email, password, **extra_fields):
        """
        Creates and saves a new User with the given email, name, and password.

        Arguments:
        - name: User's name.
        - email: User's email address.
        - password: User's password.
        - extra_fields: Additional fields to be saved in the User model.

        Returns:
        - User instance.

        Raises:
        - ValueError: If any of the required fields (name, email, password) are not provided.

        """
        values = [email, name, password]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email, name, and password.

        Arguments:
        - name: User's name.
        - email: User's email address.
        - password: User's password.
        - extra_fields: Additional fields to be saved in the User model.

        Returns:
        - User instance.

        """
        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(self, name, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email, name, and password.

        Arguments:
        - name: User's name.
        - email: User's email address.
        - password: User's password.
        - extra_fields: Additional fields to be saved in the User model.

        Returns:
        - User instance.

        """
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with email-based authentication.

    This model represents a user with unique email as the username.
    It includes fields for user's name, email, and permissions.
    The last_login field is disabled, as this user model doesn't track last login.

    Attributes:
    - name: CharField for the user's name with a maximum length of 30 characters.
    - email: EmailField for the user's email address, and it must be unique.

    """

    name = models.CharField(max_length=30, verbose_name="User's name")
    email = models.EmailField(unique=True)
    last_login = None  # Disable last_login field.

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']
