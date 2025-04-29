from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import RegisterForm
from django.urls import reverse
from .models import CustomUser, UserProfile
from .serializers import CustormToken
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status, exceptions
from .authentication import CookieJWTAuthentication
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import generics
from Account.serializers import InforUser, AccountSerializer
from core.response.get_or_404 import Base_get_or_404


# Create your views here.
def home(request):
    
    return render(request, 'home.html',{
        "user": request.user,
    })
def register(request):  
    form = RegisterForm()
    return render(request, 'register.html', {
        'form': form,   })
    
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            response = Response({
                "message": "Logout successfully", 
                "code": "SUCCESS",
                "next": reverse("loginview")
            }, status=status.HTTP_200_OK)
            
            response.delete_cookie('refresh')
            response.delete_cookie('access')
            return response
            
        except Exception as e:
            return Response({"error": str(e),"code":"ERROR"}, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = RegisterForm(data=request.data)
        if form.is_valid():
            user = CustomUser.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['passWord'],
                username=form.cleaned_data['username'],
                last_name=form.cleaned_data['last_name'],
                first_name=form.cleaned_data['first_name'],
                phone_number=form.cleaned_data['phone_number'],
                birth=form.cleaned_data['birth']
            )
            user.save()
            return Response({"message": "User registered successfully", 'next':reverse("loginview"), 'code':"SUCCESS", 'status':201}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": form.errors,'code':"ERROR", 'status':400}, status=status.HTTP_400_BAD_REQUEST)


def loginview(request):
    return render(request, 'login.html', )


class LoginAPI(TokenObtainPairView):
    serializer_class = CustormToken

    def post(self, request, *args, **kwargs):
        print("DATA :",request.data)
        user = CustomUser.objects.get(email=request.data.get('email'))
        serializer = self.get_serializer(data=request.data)
        next = request.data.get('next', reverse("home"))
        if (serializer.is_valid()):
            data = serializer.validated_data
            response = Response({
                    "message": "Login successfully",
                    "data": {
                        "accessToken": data.get("access"),
                        "refreshToken": data.get("refresh"),
                    },
                    'status': 200,
                    'next': next,
                    'role': user.role,
                    'code':"SUCCESS"
                }, status=status.HTTP_200_OK)
            
            return response
        else:
            return Response({
                "message": "Login failed",
                "error": serializer.errors,
                'status': 400,
                'code':"ERROR",
                
            },status=status.HTTP_400_BAD_REQUEST)
            
class CustomTokenRefreshView(TokenRefreshView):
    def get(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh')
            if not refresh_token:
                raise ValueError("No refresh token found in cookies")
            
            serializer = self.get_serializer(data={'refresh': refresh_token})

            try:
                serializer.is_valid(raise_exception=True)
            except TokenError as e:
                raise ValueError("Invalid refresh token")

            response_data = serializer.validated_data

            data = {
                "status": 200,
                "message": "Token refreshed successfully",
                "access": response_data.get("access"),
                "code": "SUCCESS",
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {
                "status": 400,
                "message": f"Failed to refresh token: {str(e)}",
                "details": "Invalid or expired refresh token",
                "code": "ERROR",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
class AccountUpdateAPI(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = InforUser
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user


class GetCrrUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            user = request.user
            inforUser = UserProfile.objects.get(user=user)
            serializer = InforUser(inforUser)
            return Response({
                "message": "Get user successfully",
                "code":"SUCCESS",
                "status":200,
                "data":serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e),'code':"ERROR","status":400}, status=status.HTTP_400_BAD_REQUEST)


class GetAllUserAPI(generics.ListAPIView):

    serializer_class = InforUser
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return UserProfile.objects.filter(is_deleted=False)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        breakpoint()
        serializer = self.get_serializer(queryset, many=True)
        response = {
            "message": "Get all users successfully",
            "status": 200,
            "code":"SUCCESS",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

class AddUserAPI(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = {
            "message": "User created successfully",
            "status": 201,
            "code":"SUCCESS",
            "data": serializer.validated_data,
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
class UpdateUserAPI(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = InforUser
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "message": "User updated successfully",
            "status": 200,
            "code":"SUCCESS",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
    
class DeleteUserAPI(generics.DestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = InforUser
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
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
        breakpoint()

        self.check_object_permissions(self.request, obj)

        return obj
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted'])
        response = {
            "message": "User deleted successfully",
            "status": 200,
            "code":"SUCCESS",
        }
        return Response(response, status=status.HTTP_200_OK)