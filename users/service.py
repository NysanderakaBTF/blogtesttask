from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from users.models import User
from users.serializers import UserCreateSerializer


class UserService:

    @classmethod
    def get_by_id(cls, id):
        return get_object_or_404(User, pk=id)

    @classmethod
    def sing_up(cls, serializer):
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = Token.objects.create(user=user)
            return {'user': user, 'token': token}

    @classmethod
    def get_list(cls):
        return User.objects.all()
