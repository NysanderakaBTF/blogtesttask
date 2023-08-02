from django.urls import path
from blog.views import delete_post_template, CreatePostView, PostListView

urlpatterns = [
    path('user/<int:user_pk>/', PostListView.as_view(), name='post_list_template'),
    path('create/', CreatePostView.as_view(), name='post_create_template'),
    path('delete/<int:pk>/', delete_post_template, name='delete_post_template')
]
