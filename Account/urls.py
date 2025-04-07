from django.urls import path

from .views import loginview, home, register
urlpatterns = [
    path('login/', loginview, name='loginview'),
    path('home/', home, name='home'),
    path('register/', register, name='registerview'),
]