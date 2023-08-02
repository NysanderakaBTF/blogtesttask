from django.db import models
from users.models import User

class Post(models.Model):
    """
    Model class for representing blog posts.

    This model represents blog posts and includes fields for the post's author, title, and body.

    Fields:
    - author: ForeignKey field linking to the User model representing the post's author.
    - title: CharField for the post's title with a maximum length of 255 characters.
    - body: TextField for the post's main content.

    """

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")
    title = models.CharField(max_length=255, null=False)
    body = models.TextField()
