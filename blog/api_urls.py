from django.urls import path
from blog.views import create_post, get_post_list, DeletePostAPIView

urlpatterns = [
    # URL pattern to get a list of posts for a specific user
    path('user/<int:user_pk>/', get_post_list, name="user_post_list"),

    # URL pattern to create a new post
    path('', create_post, name="create_post"),

    # URL pattern to delete a post using APIView
    path('<int:pk>/', DeletePostAPIView.as_view(), name="delete_post"),
]
