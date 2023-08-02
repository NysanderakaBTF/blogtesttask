from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from rest_framework import views, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer
from users.service import UserService
from users.forms import UserForm


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sign_up(request):
    res = UserService.sing_up(UserCreateSerializer(request.data))
    return Response({'user': UserCreateSerializer(instance=res['user']).data,
                     'token': res['token'].key}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_user_list(request):
    users = User.objects.all()
    return Response(UserSerializer(users, many=True).data, status=200)


def sing_up_template(request):
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
    res = UserService.get_list()
    return render(request, '../templates/users/user_list.html',
                  {'users': res})


def user_login_template(request):
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
    logout(request)
    return redirect('list_t_users')
