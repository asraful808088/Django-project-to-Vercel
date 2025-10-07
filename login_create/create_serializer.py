from rest_framework import serializers
from .models import CustomUser
from transection.models import UserAccountInfo
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

class CreateUser(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    co_password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = CustomUser
        fields = ['username', "email", "phone", "first_name", "last_name", "account_type","password","co_password"]

    def validate(self, attrs):
        if 'first_name' in attrs and not attrs['first_name'].replace(' ', '').isalpha():
            raise serializers.ValidationError({'first_name': 'First name should contain only English alphabetic characters.'})
        if 'last_name' in attrs and not attrs['last_name'].replace(' ', '').isalpha():
            raise serializers.ValidationError({'last_name': 'Last name should contain only English alphabetic characters.'})
        if 'username' in attrs and CustomUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({'username': 'this username already exists.'})
        if 'email' in attrs and CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email': 'this email already exists.'})
        if 'phone' in attrs and CustomUser.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError({'phone': ' this phone already exists.'})
        if 'phone' in attrs:
            phone_number = attrs['phone']
            if not phone_number.isdigit():
                raise serializers.ValidationError({'phone': 'Phone number should contain only numeric characters.'})
        if attrs.get('password') != attrs.get('co_password'):
            raise serializers.ValidationError({'co_password': 'Passwords do not match. with Co_password'})
        return attrs
    

    
    def create(self, validated_data):
        validated_data.pop('co_password', None)
        time_threshold = timezone.now() - timedelta(minutes=30)

        CustomUser.objects.filter(
            create_time__lt=time_threshold,
            is_superuser=False
        ).filter(
            Q(is_active=True) | Q(is_staff=False)
        ).delete()
        user = CustomUser.objects.create_user(**validated_data)
        
        bankAcountInfo =  UserAccountInfo(user_id=user.id,account_type=user.account_type,amount=10000000000000,account_pin=user.password,account_lvl=0)
        bankAcountInfo.save()
        return user