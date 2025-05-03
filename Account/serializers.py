from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from Account.models import CustomUser, UserProfile
from django.utils.timezone import now, localtime
from datetime import datetime, timedelta, date



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
        data = self.context['request'].data
        date_obj = datetime.strptime(data["birth"], "%d/%m/%Y").date()
        for key, value in data.items():
            if hasattr(instance.user, key):
                if key == "birth":
                    setattr(instance.user, key, date_obj)
                else:
                    setattr(instance.user, key, value)
        instance.user.save()
        return instance
    
        
