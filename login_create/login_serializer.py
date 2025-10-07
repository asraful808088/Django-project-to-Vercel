from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
# from django.core.mail import send_mail
class LoginAuth(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', "email", "password",]
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        username = attrs.get('username')
        
        user = authenticate( password=password,username = username)
        if user and user.is_active and user.email == email:
            refresh = RefreshToken.for_user(user)
            return {
                "login": True,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "username":user.username,
                "email":user.email,
                "id":user.id
            }
        else:
             raise serializers.ValidationError('Invalid email or password')


