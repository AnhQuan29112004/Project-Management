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
from rest_framework import status, exceptions
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView
from Project.serializer import ResearchSerializer, ProjectListSerializer
from Project.models import ResearchField, Project
from django.template.response import ContentNotRenderedError
from core.response.get_or_404 import Base_get_or_404
from core.shared.pagination_project import Pagination
from rest_framework.filters import SearchFilter, OrderingFilter
from .searchbase import CustomSearchFilter

# Create your views here.
class DashboardView(ListAPIView):
    queryset = Project.objects.filter(is_deleted=0).order_by('-created_at')
    serializer_class = ProjectListSerializer
    permission_required = 'Project.view_project'
    authentication_classes = [JWTAuthentication]
    pagination_class = Pagination
    filter_backends = [CustomSearchFilter]
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
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response = {
            "message":"Get project successfully",
            "code":"SUCCESS",
            "status":200,
            "data":serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    
class ResearchFieldCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = ResearchField.objects.all()
    serializer_class = ResearchSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
    
class ResearchFieldGetById(RetrieveAPIView):
    permission_required = "Project.view_researchfield"
    authentication_classes = [JWTAuthentication]
    queryset = ResearchField.objects.filter(is_deleted=0)
    serializer_class = ResearchSerializer
    
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
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = {
            "code":"SUCCESS",
            "status":200,
            "data":serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
class ResearchFieldListPaginateAPIView(ListAPIView):
    permission_required = "Project.view_researchfield"
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = Pagination
    queryset = ResearchField.objects.filter(is_deleted=0)
    serializer_class = ResearchSerializer
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
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        response = {
            "message":"Get research field successfully",
            "code":"SUCCESS",
            "status":200,
            "data":serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)

class ResearchFieldListAPIView(ListAPIView):
    permission_required = "Project.view_researchfield"
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = ResearchField.objects.filter(is_deleted=0)
    serializer_class = ResearchSerializer
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
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        response = {
            "message":"Get research field successfully",
            "code":"SUCCESS",
            "status":200,
            "data":serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)
    
class ResearchFieldUpdateAPIView(UpdateAPIView):
    queryset=ResearchField.objects.filter(is_deleted=False)
    serializer_class=ResearchSerializer
    authentication_classes = [JWTAuthentication]
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        response={
            "code":"SUCCESS",
            "status":200,
            "data":serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()
    
class ResearchFieldDeleteAPIView(DestroyAPIView):
    queryset=ResearchField.objects.filter(is_deleted=False)
    serializer_class=ResearchSerializer
    authentication_classes = [JWTAuthentication]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response={
            "code":"SUCCESS",
            "status":200,
            "data":""
        }
        return Response(response,status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class ProjectAddAPIView(CreateAPIView):
    queryset = Project.objects.all()
    permission_required = "Project.add_project"
    authentication_classes = [JWTAuthentication]
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
        serializer = self.get_serializer(data=request.data,context={'request': request})
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
    authentication_classes = [JWTAuthentication]
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
    
class ProjectDetailAPIView(RetrieveAPIView):
    permission = "Project.view_project"
    authentication_classes = [JWTAuthentication]
    queryset = Project.objects.filter(is_deleted=0)
    serializer_class = ProjectListSerializer
    def get_permissions(self):
        return [IsAuthenticated(),
            HasPermission(self.permission)]
        
    def permission_denied(self, request, message=None, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        return exceptions.PermissionDenied({
            "message":"Not have permission",
            "code":"ERROR",
            "status":401})
    
    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = Base_get_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            response = {
                "message":f"Get detail project {instance.name} successfully",
                "code":"SUCCESS",
                "status":200,
                "data":serializer.data
            }
        else:
            response = {
                "message":f"Object doesn't exist",
                "code":"ERROR",
                "status":400,
            }
            
        return Response(response, status=status.HTTP_200_OK if response.get("status") == 200 else status.HTTP_400_BAD_REQUEST) 
        
class ProjectUpdateAPIView(UpdateAPIView):
    queryset = Project.objects.filter(is_deleted=0)
    serializer_class = ProjectListSerializer
    permission_required = "Project.change_project"
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        return [
            IsAuthenticated(),
            HasPermission(self.permission_required)
        ]
        
    def permission_denied(self, request, message=None, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        return exceptions.PermissionDenied({
            "message":"Not have permission",
            "code":"ERROR",
            "status":401})
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial,context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            response = {
                "status":200,
                "code":"SUCCESS",
                "message":f"Update project {instance.id} successfully",
                "data":serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except exceptions.ValidationError as e:
            response = {
                "status":400,
                "code":"ERROR",
                "message":"Update project failed",
                "error":str(e.detail)
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save(
            updated_by_id = self.request.user.id
        )