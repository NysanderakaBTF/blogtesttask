from django.urls import path
from blog.views import create_post, get_post_list, DeletePostAPIView

urlpatterns = [
    path('user/<int:user_pk>/', get_post_list, name="user_post_list"),
    path('', create_post, name="create_post"),
    path('<int:pk>/', DeletePostAPIView.as_view(), name="delete_post"),
]
