from django.urls import path
from rest_framework.authtoken import views

from users.views import ListCreateUserAPIView

urlpatterns = [
    # URL pattern for user login and obtaining an authentication token
    path('login/', views.obtain_auth_token, name='user_login'),

    # URL pattern for user sign up/registration
    path('signup/', ListCreateUserAPIView.as_view(), name='user_signup'),

    # URL pattern for retrieving the list of users
    path('list/', ListCreateUserAPIView.as_view(), name='user_list'),
]