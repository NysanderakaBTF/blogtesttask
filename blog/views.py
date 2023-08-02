from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.forms import PostForm
from blog.models import Post
from blog.permissions import PostPermission
from blog.serializers import PostSerializer
from users.service import UserService


@api_view(['GET'])
def get_post_list(request, user_pk):
    """
    API view to get a list of blog posts for a specific user.

    This view returns a list of blog posts associated with the specified user.

    Method: GET
    URL: /api/posts/user/<int:user_pk>/

    Args:
        request (HttpRequest): The HTTP request object.
        user_pk (int): The primary key of the user whose blog posts are requested.

    Returns:
        Response: JSON response containing the list of blog posts for the specified user.

    """
    res = Post.objects.filter(author_id=user_pk)
    return Response(PostSerializer(res, many=True).data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([PostPermission])
@authentication_classes([TokenAuthentication])
def create_post(request):
    """
    API view to create a new blog post.

    This view allows authenticated users to create a new blog post.
    The request data should contain the title and body of the new post.
    The author of the post is automatically set to the authenticated user.

    Method: POST
    URL: /api/posts/

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: JSON response containing the created blog post details.

    """
    data = request.data
    data.setdefault('author', request.user.pk)
    serializer = PostSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeletePostAPIView(APIView):
    """
    API view to delete a blog post.

    This view allows authenticated users to delete their own blog post.
    The user must have the necessary permissions to perform the delete operation.

    Method: DELETE
    URL: /api/posts/<int:pk>/

    Args:
        permission_classes (list): List of permission classes applied to the view.

    """
    permission_classes = [PostPermission]

    def delete(self, request, pk):
        """
        Handles the DELETE request to delete a blog post.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the blog post to be deleted.

        Returns:
            Response: Empty response with status code 204 (No Content) on successful deletion.

        """
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required()
def post_list_template(request, user_pk):
    """
    View to render a template for displaying a list of blog posts for a specific user.

    This view retrieves the list of blog posts associated with the specified user
    and renders the 'posts/post_list.html' template to display them.

    Args:
        request (HttpRequest): The HTTP request object.
        user_pk (int): The primary key of the user whose blog posts are displayed.

    Returns:
        HttpResponse: The response containing the rendered template.

    """
    user = UserService.get_by_id(user_pk)
    res = Post.objects.filter(author_id=user_pk)
    return render(request, 'posts/post_list.html', {
        'posts': res,
        'user': user
    })


@login_required()
def create_post_template(request):
    """
    View to render a template for creating a new blog post.

    This view renders the 'posts/create.html' template, which contains a form for creating a new blog post.
    If the form data is valid, a new blog post is created with the authenticated user as the author.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The response containing the rendered template or a redirect response.

    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list_template', user_pk=request.user.pk)
    else:
        form = PostForm()
    return render(request, '../templates/posts/create.html', {'form': form})


@login_required()
def delete_post_template(request, pk):
    """
    View to render a template for deleting a blog post.

    This view renders the 'posts/delete.html' template for confirming the deletion of a blog post.
    If the user has the necessary permissions and confirms the deletion, the blog post is deleted.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the blog post to be deleted.

    Returns:
        HttpResponse: The response containing the rendered template.

    """
    try:
        post = get_object_or_404(Post, pk=pk)
    except Exception as e:
        return render(request, '../templates/error.html', {'error': e})
    if request.method == 'POST':
        if request.user == post.author:
            post.delete()
            return redirect('post_list_template', user_pk=request.user.pk)
        else:
            return render(request, '../templates/error.html', {'error': 'Permission denied'})
    return render(request, '../templates/posts/delete.html', {'post': post})
