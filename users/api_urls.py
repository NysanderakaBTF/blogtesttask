from django.urls import path
from rest_framework.authtoken import views

from users.views import sign_up, get_user_list

urlpatterns = [
    path('login/', views.obtain_auth_token , name='user_login'),
    path('signup/', sign_up, name='user_singup'),
    path('list/', get_user_list, name='user_list')
]
