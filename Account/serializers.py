from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from Account.models import CustomUser, UserProfile
from django.utils.timezone import now, localtime
from datetime import datetime, timedelta



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
        user = self.user
        user.last_login = localtime(now() + timedelta(hours=7))
        user.save(update_fields=['last_login'])
        print("User last login updated: ", user.last_login)
        return {
            "access": data["access"],
            "refresh": data["refresh"],
        }

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'birth', 'mssv', 'role']
    def create(self, validated_data):
        request = self.context.get('request')
        password = request.data.get('password', None)
        validated_data['password'] = password
        print(validated_data)
        print(password)
        return CustomUser.objects.create_user(**validated_data)
class InforUser(serializers.ModelSerializer):
    class Meta:
        model = UserProfile 
        fields = ['id','address', 'bio']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        userAccount = AccountSerializer(instance.user).data
        representation = {**representation, **userAccount}
        for i,j in AccountSerializer(instance.user).data.items():
            representation[i] = j
        return representation
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        instance.save()
        return instance
    
        
