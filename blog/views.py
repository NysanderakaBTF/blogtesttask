from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404, ListAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.generic import CreateView, FormView, ListView, DeleteView, TemplateView

from blog.forms import PostForm
from blog.models import Post
from blog.permissions import PostPermission
from blog.serializers import PostSerializer
from users.service import UserService


class PostListAPIView(ListAPIView):
    serializer_class = PostSerializer
    model = Post
    """
    API view to get a list of blog posts for a specific user.

    This view returns a list of blog posts associated with the specified user.

    Method: GET
    URL: /api/posts/user/<int:user_pk>/

    Args:
        user_pk (int): The primary key of the user whose blog posts are requested.

    Returns:
        Response: JSON response containing the list of blog posts for the specified user.
    """

    def get_queryset(self):
        return self.model.objects.filter(author_id=self.kwargs.get('user_pk'))


class PostCreateDeleteAPIView(CreateModelMixin, DestroyModelMixin, GenericAPIView):
    model = Post
    permission_classes = [PostPermission, IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    """
        View for creating and deleting blog posts.

        This view is a combination of CreateAPIView and DestroyAPIView, allowing both creation and deletion of
        blog posts.
        To create a new post, make a POST request to the endpoint. To delete a post, make a DELETE request 
        to the endpoint with the post ID.

        Method: POST
        URL: /api/posts/
        Body (JSON):
        {
            "title": "Post Title",
            "body": "Post Content"
        }
        Headers:
        Authorization: Token <your_token>

        Method: DELETE
        URL: /api/posts/<int:pk>/
        Headers:
        Authorization: Token <your_token>

    """

    def post(self, request, *args, **kwargs):
        data = request.data
        data.setdefault('author', request.user.pk)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostListView(ListView):
    """
    View to render a template for displaying a list of blog posts for a specific user.

    This view retrieves the list of blog posts associated with the specified user
    and renders the 'posts/post_list.html' template to display them.

    Kwargs:
        user_pk (int): The primary key of the user whose blog posts are displayed.

    Returns:
        HttpResponse: The response containing the rendered template.

    """
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/post_list.html'

    def get_queryset(self):
        return self.model.objects.filter(author_id=self.kwargs.get('user_pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request"] = self.request
        context['user'] = UserService.get_by_id(self.kwargs.get('user_pk'))
        return context


class CreatePostView(LoginRequiredMixin, FormView):
    template_name = 'posts/create.html'
    form_class = PostForm

    """
    View to render a template for creating a new blog post.

    This view renders the 'posts/create.html' template, which contains a form for creating a new blog post.
    If the form data is valid, a new blog post is created with the authenticated user as the author.

    Kwargs:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The response containing the rendered template or a redirect response.

    """

    def get_success_url(self):
        return reverse('post_list_template', kwargs={'user_pk': self.request.user.pk})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


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
