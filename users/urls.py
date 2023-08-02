from django.urls import path
from users.views import user_logout, UserSignUp, UserListView, UserLoginView

urlpatterns = [
    path('list/', UserListView.as_view(), name='list_t_users'),
    path('signup/', UserSignUp.as_view(), name='singup_t'),
    path('login/', UserLoginView.as_view(), name='login_t'),
    path('logout/', user_logout, name='logout')
]
