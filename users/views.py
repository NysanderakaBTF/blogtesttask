from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from rest_framework import permissions, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response

from users.forms import UserForm
from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer
from users.service import UserService


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sign_up(request):
    """
    API endpoint for user signup.

    This view handles user signup through the API.
    It allows any user (unauthenticated) to access this endpoint.
    When a new user is successfully signed up, it returns the user data and an authentication token.

    Method: POST
    URL: /api/users/signup/

    Request data (JSON):
    {
        "name": "User's name",
        "email": "user@example.com",
        "password": "user_password"
    }

    Response (JSON):
    {
        "user": {
            "id": 1,
            "email": "user@example.com",
            "name": "User's name"
        },
        "token": "your_auth_token"
    }

    """
    res = UserService.sing_up(UserCreateSerializer(data=request.data))
    return Response({'user': UserCreateSerializer(instance=res['user']).data,
                     'token': res['token'].key}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_user_list(request):
    """
    API endpoint to get a list of all users.

    This view returns a list of all users available in the database.
    It allows any user (unauthenticated) to access this endpoint.

    Method: GET
    URL: /api/users/list/

    Response (JSON):
    [
        {
            "id": 1,
            "email": "user1@example.com",
            "name": "User1"
        },
        {
            "id": 2,
            "email": "user2@example.com",
            "name": "User2"
        },
        ...
    ]

    """
    users = User.objects.all()
    return Response(UserSerializer(users, many=True).data, status=200)


def sing_up_template(request):
    """
    View to handle user signup through a template form.

    This view renders the user signup template containing a form for user registration.
    If the form data is valid, a new user is created, and the user is logged in automatically.

    Method: POST
    URL: /users/signup/

    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.data.get('password'))
            user.save()
            login(request, user)
            return redirect('list_t_users')
    else:
        form = UserForm()
    return render(request, '../templates/users/create.html', {'form': form})


def user_list_template(request):
    """
    View to render the user list template.

    This view fetches the list of users from the API and renders the user list template.
    The template shows a list of all users available in the database.

    Method: GET
    URL: /users/list/

    """
    res = UserService.get_list()
    return render(request, '../templates/users/user_list.html',
                  {'users': res})


def user_login_template(request):
    """
    View to handle user login through a template form.

    This view renders the user login template containing a form for user authentication.
    If the form data is valid, the user is logged in, and they are redirected to the user list page.

    Method: POST
    URL: /users/login/

    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_t_users')
    else:
        form = AuthenticationForm()
    return render(request, '../templates/users/login.html', {'form': form})


def user_logout(request):
    """
    View to handle user logout.

    This view logs out the authenticated user and redirects to the user list page.

    Method: GET
    URL: /users/logout/

    """
    logout(request)
    return redirect('list_t_users')
