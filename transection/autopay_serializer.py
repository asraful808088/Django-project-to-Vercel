from rest_framework import serializers
from .models import AutoPay
from django.conf import settings
from login_create.models import CustomUser
from bank.utility.hashing import decrypt,encrypt
from .models import PaymentAddress,AutoPay
import time
import json
import re
class CreateAutoPaySerializer(serializers.Serializer):
        token = serializers.CharField(max_length=555)
        name = serializers.CharField(max_length=255)
        amount = serializers.DecimalField(max_digits=150, decimal_places=0)
        id = serializers.DecimalField(max_digits=150, decimal_places=0)
        lvl_order = serializers.IntegerField()
        def validate(self,data):
                try:
                  convertStr = re.sub(r"^b'(.*)'$", r'\1', data.get("token"))
                  getData = json.loads(decrypt(convertStr ,settings.SECRET_KEY))
                  try:
                        CustomUser.objects.get(email=getData['email'],username=getData['username'],id=getData['id'])
                        PaymentAddress.objects.get(token=data.get("token"))
                        new_token_info = {
                               "create_time":time.time(),
                               "amount":str(data.get("amount")),
                               "email":getData['email'],
                               "username":getData['username'],
                               "id":getData['id'],
                               "lvl_order":data.get("lvl_order"),
                               "name":data.get("name")
                        }
                        stringObj  = json.dumps(new_token_info)
                        create_token =encrypt(stringObj ,settings.SECRET_KEY)
                        result  = AutoPay(token=create_token,amount=data.get("amount"),lvl_order=data.get("lvl_order"),author_id=data.get("id"),name=data.get("name") )
                        result.save()
                        getData = AutoPay.objects.get(token=create_token)
                       
                        return {
                              "id":getData.id, 
                              "token":getData.token, 
                              "amount":getData.amount, 
                              "lvl_order":getData.lvl_order, 
                               "name":getData.name
                        }
                  except Exception as a:
                         raise serializers.ValidationError({"invalid":"invalid address"})
                except Exception as a:
                        raise serializers.ValidationError({"invalid":"invalid address"})
              


class UpdateAutoPaySerializer(serializers.Serializer):
       amount = serializers.DecimalField(max_digits=150, decimal_places=0,required=False)
       lvl_order = serializers.IntegerField(required=False) 
       def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
