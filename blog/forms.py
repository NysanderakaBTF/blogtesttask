from django import forms
from blog.models import Post


class PostForm(forms.ModelForm):
    """
    Form class for creating and updating blog posts.

    This form is used for creating and updating blog posts based on the Post model.
    It includes the fields 'title' and 'body' from the Post model.

    Usage:
    - Use this form in views to create and update blog posts.
    """

    class Meta:
        model = Post
        fields = ['title', 'body']
