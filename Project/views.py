from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.urls import reverse
from rest_framework.response import Response
from Account.authentication import CookieJWTAuthentication
from Project.permission import HasPermission
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from Project.serializer import ResearchSerializer, ProjectListSerializer
from Project.models import ResearchField, Project


# Create your views here.
class DashboardView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    permission_required = 'Project.view_project'
    authentication_classes = [CookieJWTAuthentication]

    def get_permissions(self):
        return [
            IsAuthenticated(),
            HasPermission(self.permission_required)
        ]
        
    def permission_denied(self, request, message=None, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise PermissionDenied(
                detail={
                    "code": "ERROR",
                    "message": "Bạn chưa đăng nhập hoặc thông tin xác thực không hợp lệ."
                },
                code="authentication_failed"
            )
        raise PermissionDenied(
            detail={
                "code": "ERROR",
                "message": "Bạn không có quyền thực hiện hành động này."
            },
            code="permission_denied"
        )
    
    def get(self, request):
        data = {
        "code":"SUCCESS",
        "status": 200
        }
        return Response(data, status=status.HTTP_200_OK)
    
class ResearchFieldCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]
    queryset = ResearchField.objects.all()
    serializer_class = ResearchSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        breakpoint()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {
            "message":"them thanh cong",
            "code":"SUCCESS",
            "status":201,
            "data":serializer.data
        }
        
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self,serializer):
        serializer.save(
            created_by_id = self.request.user.id
        )

class ProjectAddAPIView(CreateAPIView):
    queryset = Project.objects.all()
    permission_required = "Project.add_project"
    authentication_classes = [CookieJWTAuthentication]
    serializer_class = ProjectListSerializer
    def get_permissions(self):
        return [
            IsAuthenticated(),
            HasPermission(self.permission_required)
        ]
        
    def permission_denied(self, request, message=None, code=None):
        data = {
            "message":"Not have permission",
            "status":403,
            "code":code or "ERROR"
        }
        return Response(data,status=status.HTTP_403_FORBIDDEN)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {
            "message":"Add project successfully",
            "code":"SUCCESS",
            "status":201,
            "data":serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(
            created_by_id = self.request.user.id
        )

class ProjectDeleteAPIView(DestroyAPIView):
    authentication_classes = [CookieJWTAuthentication]
    permission = "Project.delete_project"
    queryset = Project.objects.all()
    
    def get_permissions(self):
        return [
            IsAuthenticated(),
            HasPermission(self.permission)
        ]
    
    def permission_denied(self, request, message=None, code=None):
        data = {
            "message":"Not have permission",
            "status":403,
            "code":"ERROR"
        }
        return Response(data,status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response={
            "message":f"Delete {instance.name} successfully",
            "code":"SUCCESS",
            "status":204,
        }
        return Response(response,status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_deleted = 1
        instance.save()
    
        