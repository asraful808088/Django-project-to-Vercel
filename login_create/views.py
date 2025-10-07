from django.shortcuts import render
from .models import CustomUser
from rest_framework.views import APIView,Response,status
from django.http import HttpResponse
from .create_serializer import CreateUser
from .login_serializer import LoginAuth
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from .models import CustomUser
class CreateUsers(APIView):
    def post(self, request, *args, **kwargs):
        formData = request.data
        result  = CreateUser(data=formData)
        if  result.is_valid():
            result.save()
            return Response({"success":True}, status=status.HTTP_200_OK)
        errors = {}
        for field, messages in result.errors.items():
                errors[field] = messages[0]
       
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)



class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        result = LoginAuth(data= request.data)
        if result.is_valid():
             tokens = result.validated_data
             response = Response({
                 
                 'login': tokens['login'],
                 'access':tokens['access'],
                 'refresh':tokens['refresh'],
                 "username":tokens['username'],
                 "email":tokens['email'],
                 "id":tokens['id'],
             }, status=status.HTTP_200_OK)
             return response
        return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetUserInfo(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        access_token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        try:
            result = AccessToken(access_token)
            user = result.payload['user_id']
            userInfo = CustomUser.objects.get(id=user)
            user_info = {
                'user_id': userInfo.id,
                'username': userInfo.username,
                'email':userInfo.email,
            }
            return Response(user_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    




class RefreshInfo(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token is missing'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh_token = RefreshToken(refresh_token)
            access_token = str(refresh_token.access_token)
            return Response({'access': access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)



