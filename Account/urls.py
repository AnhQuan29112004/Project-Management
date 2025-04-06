from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from Account.views import CustormViewToken
from decouple import config
version_api = config('VERSION_API')
from .views import register, loginview, home, logout, GetUserView
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', loginview, name='loginview'),
    path('logout/', logout, name='logoutview'),
    path('home/', home, name='home'),
]