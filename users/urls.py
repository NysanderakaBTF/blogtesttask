from django.urls import path
from users.views import user_list_template, sing_up_template, user_login_template, user_logout

urlpatterns = [
    path('list/', user_list_template, name='list_t_users'),
    path('signup/', sing_up_template, name='singup_t'),
    path('login/', user_login_template, name='login_t'),
    path('logout/', user_logout, name='logout')
]
