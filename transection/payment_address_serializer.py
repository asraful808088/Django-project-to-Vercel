from rest_framework import serializers
from bank.utility.hashing import encrypt
from django.conf import settings
from .models import PaymentAddress
import json
import time
from login_create.models import CustomUser
class PaymentAddressSerializer(serializers.Serializer):
      token = serializers.CharField(max_length=255)
      create_time = serializers.DateField() 


class PaymentAddressGeneratorSerializer(serializers.Serializer):
      id = serializers.DecimalField(max_digits=150, decimal_places=0)
      email = serializers.CharField(max_length=255)
      username = serializers.CharField(max_length=255)
      def validate(self, data):
            email = data.get("email")
            username = data.get("username")
            id = data.get("id")
            user = CustomUser.objects.get(id=id,email=email,username=username)
            if user == None:
                  raise serializers.ValidationError({"auth":"invalid user"})  
            else:
             create_obj = {
                  "email":email,
                  "username":username,
                  'id':f"{id}",
                  "create_time":time.time()
             }
             token = encrypt(json.dumps(create_obj),settings.SECRET_KEY)
             
             PaymentAddress(token=token,author_id=id).save()
             result  = PaymentAddress.objects.get(token=token)
             return {
                  "token":result.token,
                  "id":result.id
             }
      



