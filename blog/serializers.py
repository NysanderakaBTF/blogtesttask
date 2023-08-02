from rest_framework import serializers

from users.models import User
from .models import Post
from users.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    author = User.objects.all()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'body']
