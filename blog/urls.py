from django.urls import path
from blog.views import post_list_template, create_post_template, delete_post_template

urlpatterns = [
    path('user/<int:user_pk>/', post_list_template, name='post_list_template'),
    path('create/', create_post_template, name='post_create_template'),
    path('delete/<int:pk>/', delete_post_template, name='delete_post_template')
]
