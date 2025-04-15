from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access')
        print("Access token:", access_token)
        if not access_token:
            return None 

        try:
            validated_token = self.get_validated_token(access_token)
            user = self.get_user(validated_token)
            print("USER: ",user)
            return (user, validated_token)
        except (InvalidToken, TokenError) as e:
            raise AuthenticationFailed({"error": "Invalid or expire token", "code":"ERROR", "status":401})