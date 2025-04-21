from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from Account.models import CustomUser, UserProfile


class CustormToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['role'] = user.role  
        token['email'] = user.email

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        return {
            "access": data["access"],
            "refresh": data["refresh"],
        }

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'birth', 'mssv', 'role']

class InforUser(serializers.ModelSerializer):
    class Meta:
        model = UserProfile 
        fields = ['address', 'bio']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for i,j in AccountSerializer(instance.user).data.items():
            representation[i] = j
        return representation
    
        
