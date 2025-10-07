from rest_framework import serializers
from django.contrib.auth.hashers import check_password,make_password
from .models import UserAccountInfo


class CheckValidPinSerializar(serializers.Serializer):
      pin = serializers.CharField(max_length=255)
      id = serializers.DecimalField(max_digits=150, decimal_places=0) 

      def validate(self, attrs):
           account_info = UserAccountInfo.objects.get(user_id=attrs.get("id"))
           password = check_password(attrs.get("pin"),account_info.account_pin) 
           if password==True:
                return  {
                     "success":True
                }
           raise serializers.ValidationError({"invalid":"invalid pin"})