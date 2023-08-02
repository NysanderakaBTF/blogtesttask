from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    name = serializers.CharField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('User with this email exists')
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create(email=validated_data['email'],
                                               password=validated_data['password'],
                                               name=validated_data['name'])
        user.set_password(validated_data['password'])
        user.save()

        return user
