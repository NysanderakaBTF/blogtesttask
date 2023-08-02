from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, ListView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView

from users.forms import UserForm
from users.models import User
from users.permissions.mixins import PermissionPolicyMixin
from users.permissions.permissions import IsNotAuthenticated
from users.serializers import UserSerializer, UserCreateSerializer
from users.service import UserService


class ListCreateUserAPIView(PermissionPolicyMixin, ListModelMixin, CreateModelMixin, GenericAPIView):
    """
        View for listing and creating users.

        This view allows listing all users and creating a new user. For listing users, make a GET request to the endpoint.
        For creating a new user, make a POST request with the user data in JSON format.
    """
    model = User
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes_per_method = {
        'list': (AllowAny,),
        'post': (IsNotAuthenticated,)
    }

    def get_serializer_class(self):
        """
               Get the serializer class based on the request method.

               If the request method is POST, use the UserCreateSerializer for creating a new user.
               Otherwise, use the UserSerializer for listing users.

        """
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request):
        res = UserService.sing_up(UserCreateSerializer(data=request.data))
        return Response({'user': UserCreateSerializer(instance=res['user']).data,
                         'token': res['token'].key}, status=status.HTTP_201_CREATED)


class UserSignUp(FormView):
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = 'list_t_users'

    """
       View to handle user signup through a template form.

       This view renders the user signup template containing a form for user registration.
       If the form data is valid, a new user is created, and the user is logged in automatically.

    """

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.data.get('password'))
        user.save()
        login(self.request, user)
        return redirect('list_t_users')


class UserListView(ListView):
    """
    View to render the user list template.

    This view fetches the list of users from the API and renders the user list template.
    The template shows a list of all users available in the database.

    """
    template_name = 'users/user_list.html'
    model = User
    context_object_name = 'users'


class UserLoginView(FormView):
    """
      View to handle user login through a template form.

      This view renders the user login template containing a form for user authentication.
      If the form data is valid, the user is logged in, and they are redirected to the user list page.

    """
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = '/users/list/'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


def user_logout(request):
    """
    View to handle user logout.

    This view logs out the authenticated user and redirects to the user list page.
    """
    logout(request)
    return redirect('list_t_users')
