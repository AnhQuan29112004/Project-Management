

from django.urls import path,include
from decouple import config

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from Account.views import GetUserById, RegisterAPI, LogoutAPI,LoginAPI, CustomTokenRefreshView,GetCrrUser,AddUserAPI,DeleteUserAPI,GetAllUserAPI,UpdateUserAPI
from Project.views import ResearchFieldGetById, ResearchFieldListPaginateAPIView, ResearchFieldUpdateAPIView, ResearchFieldDeleteAPIView, DashboardView, ResearchFieldCreateAPIView, ProjectAddAPIView, ProjectDeleteAPIView, ProjectDetailAPIView, ProjectUpdateAPIView,ResearchFieldListAPIView
version_api = config('VERSION_API')

urlpatterns = [
    path(f'{version_api}/auth/login', LoginAPI.as_view(), name='login'),
    path(f'{version_api}/auth/register', RegisterAPI.as_view(), name='register'),
    path(f'{version_api}/auth/getUser', GetCrrUser.as_view(), name='getUser'),
    path(f'{version_api}/auth/getAccesstoken', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path(f'{version_api}/auth/logout', LogoutAPI.as_view(), name='logout'),
    path(f'{version_api}/project/get', DashboardView.as_view(), name='projectdashboard'),
    path(f'{version_api}/researchfield/create', ResearchFieldCreateAPIView.as_view(), name='createresearchfield'),
    path(f'{version_api}/researchfield/get', ResearchFieldListAPIView.as_view(), name='createresearchfield'),    
    path(f'{version_api}/researchfield/get/<int:pk>', ResearchFieldGetById.as_view(), name='createresearchfield'),            
    path(f'{version_api}/researchfield/get/paginate', ResearchFieldListPaginateAPIView.as_view(), name='createresearchfield'),    
    path(f'{version_api}/researchfield/delete/<int:pk>', ResearchFieldDeleteAPIView.as_view(), name='createresearchfield'),
    path(f'{version_api}/researchfield/update/<int:pk>', ResearchFieldUpdateAPIView.as_view(), name='createresearchfield'),        
    path(f'{version_api}/project/create', ProjectAddAPIView.as_view(), name='createproject'),
    path(f'{version_api}/project/delete/<int:pk>', ProjectDeleteAPIView.as_view(), name='deleteproject'),
    path(f'{version_api}/project/get/<int:pk>', ProjectDetailAPIView.as_view(), name='projectdetail'),
    path(f'{version_api}/project/update/<int:pk>', ProjectUpdateAPIView.as_view(), name='projectupdate'),
    path(f'{version_api}/account/create', AddUserAPI.as_view(), name='projectupdate'),
    path(f'{version_api}/account/get', GetAllUserAPI.as_view(), name='projectupdate'),
    path(f'{version_api}/account/delete/<int:pk>', DeleteUserAPI.as_view(), name='projectupdate'),
    path(f'{version_api}/account/update/<int:pk>', UpdateUserAPI.as_view(), name='projectupdate'),
    path(f'{version_api}/account/get/<int:pk>', GetUserById.as_view(), name='projectupdate'),


]
