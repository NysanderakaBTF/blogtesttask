from django.contrib import admin
from django.urls import path, include

'''
urls with /api are used by Rest Framework and returns JSON
urls without them are used for HTML rendering
'''
urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/users/', include('users.api_urls')),
    path('api/posts/', include('blog.api_urls')),

    path('users/', include('users.urls')),
    path('posts/', include('blog.urls')),
]
