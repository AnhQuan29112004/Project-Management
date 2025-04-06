from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import RegisterForm
from django.urls import reverse
from .models import CustomUser
from .serializers import CustormToken
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status



# Create your views here.
def home(request):
    
    return render(request, 'home.html',{
        "user": request.user,
    })
def logout(request):
    response = JsonResponse({"message": "Logout successfully", "next":reverse('home')}, status=status.HTTP_200_OK)
    response.delete_cookie('refresh')
    response.delete_cookie('access')
    return response

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
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
            return JsonResponse({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"error": form.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = RegisterForm()
    return render(request, 'register.html',{'form': form})

def loginview(request):
    return render(request, 'login.html', )

class CustormViewToken(TokenObtainPairView):
    serializer_class = CustormToken
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            data = serializer.validated_data
            response = Response({
                    "message": "Login successfully",
                    "data": {
                        "access": data.get("access"),
                    },
                    'Status': 200,
                    'next': reverse('home')
                }, status=status.HTTP_200_OK)
            
            response.set_cookie(
                key='refresh',
                value=data.get("refresh"),
                httponly=True, 
                secure=True,   
                samesite='Lax', 
                max_age=3600*24*14 
            )
            
            response.set_cookie(
                key='access',
                value=data.get("access"),
                httponly=False,  
                secure=True,     
                samesite='Lax',  
                max_age=3600     
            )
            print(response.cookies['refresh'].value)
            print(response.cookies['access'].value)
            return response
        else:
            return Response({
                "message": "Login failed",
                "error": serializer.errors,
                'Status': 400
            },status=status.HTTP_400_BAD_REQUEST)