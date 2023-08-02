from django.urls import path
from blog.views import PostListAPIView, PostCreateDeleteAPIView

urlpatterns = [
    # URL pattern to get a list of posts for a specific user
    # path('user/<int:user_pk>/', get_post_list, name="user_post_list"),
    path('user/<int:user_pk>/', PostListAPIView.as_view(), name="user_post_list"),

    # URL pattern to create a new post
    path('', PostCreateDeleteAPIView.as_view(), name="create_post"),

    # URL pattern to delete a post using APIView
    path('<int:pk>/', PostCreateDeleteAPIView.as_view(), name="delete_post"),
]
