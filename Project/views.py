from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.urls import reverse
from rest_framework.response import Response
from Account.authentication import CookieJWTAuthentication
from Project.permission import HasPermission
from rest_framework import status


# Create your views here.
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    permission_required = 'project.add_project'
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