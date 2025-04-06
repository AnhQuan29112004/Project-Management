from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from Account.views import CustormViewToken
from decouple import config
version_api = config('VERSION_API')
from .views import register, loginview, home, logout
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', loginview, name='loginview'),
    path('logout/', logout, name='logoutview'),
    path('home/', home, name='home'),
    path(f'{version_api}/api/auth/', CustormViewToken.as_view(), name='login'),
    path(f'{version_api}/api/auth/refresh/get', TokenRefreshView.as_view(), name='token_refresh'),
]