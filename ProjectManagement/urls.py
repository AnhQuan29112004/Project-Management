"""
URL configuration for ProjectManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from decouple import config

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
version_api = config('VERSION_API')
from Account.views import RegisterAPI, LogoutAPI, GetUserView,LoginAPI
version_api = config('VERSION_API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{version_api}/api/auth/login/', LoginAPI.as_view(), name='login'),
    path(f'{version_api}/api/auth/register/', RegisterAPI.as_view(), name='register'),
    path(f'{version_api}/api/auth/getUser/', GetUserView.as_view(), name='getUser'),
    path(f'{version_api}/api/auth/getAccesstoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path(f'{version_api}/api/auth/logout/', LogoutAPI.as_view(), name='logout'),
    path('account/', include('Account.urls')),
]
