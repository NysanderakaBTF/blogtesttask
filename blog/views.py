from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from blog.forms import PostForm
from blog.models import Post
from blog.permissions import PostPermission
from blog.serializers import PostSerializer
from users.service import UserService


@api_view(['GET'])
def get_post_list(request, user_pk):
    res = Post.objects.filter(author_id=user_pk)
    return Response(PostSerializer(res, many=True).data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([PostPermission])
@authentication_classes([TokenAuthentication])
def create_post(request):
    data = request.data
    data.setdefault('author', request.user.pk)
    serializer = PostSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeletePostAPIView(APIView):
    permission_classes = [PostPermission]

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def post_list_template(request, user_pk):
    user = UserService.get_by_id(user_pk)
    res = Post.objects.filter(author_id=user_pk)
    return render(request, 'posts/post_list.html', {
        'posts': res,
        'user': user
    })


@login_required()
def create_post_template(request):
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
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        if request.user == post.author:
            post.delete()
            return redirect('post_list_template', user_pk=request.user.pk)
        else:
            return render(request, '../templates/error.html', {'error':'Permission denied'})
    return render(request, '../templates/posts/delete.html', {'post': post})