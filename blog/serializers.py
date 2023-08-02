from rest_framework import serializers
from users.models import User
from .models import Post
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Post model.

    This serializer is used to convert Post model instances to JSON and vice versa.
    It defines the representation of Post objects and the fields to be included in the serialized output.

    Fields:
    - id: The unique identifier of the post.
    - author: The author of the post represented as a User object.
    - title: The title of the post.
    - body: The main content of the post.

    Usage:
    - Use this serializer in views to serialize Post objects and display them in API responses.
    """

    # Define the 'author' field to use the author pk for author representation
    author = User.objects.all()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'body']
