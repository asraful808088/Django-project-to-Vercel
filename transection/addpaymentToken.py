from rest_framework import serializers
from .models import TransferTempToken
from login_create.models import CustomUser
from bank.utility.hashing import decrypt,encrypt
from django.conf import settings
import  time
import uuid
import json
class AddPaymentTokenClient(serializers.Serializer):
        token = serializers.CharField(max_length=555)
        email = serializers.CharField(max_length=355)
        api_name = serializers.CharField(max_length=355)
        def validate(self, attrs):
                
                try:
                      
                      getTokenData = TransferTempToken.objects.get(token=attrs.get("token"))

                except Exception as e:
                      raise serializers.ValidationError({"token_issue":"not_found_token","client_error":False})
                
                if getTokenData.api_name == attrs.get("api_name") and getTokenData.api_key== attrs.get("api_key"):
                    
                    try:
                         client = CustomUser.objects.get(email=attrs.get("client_email"))
                    except:
                       raise serializers.ValidationError({"client_error":"not_found_client","api_issue":False})
                    if client.email == attrs.get("client_email"):
                        return {
                              "api_key":getTokenData.api_key,
                              "email":client.email,
                              "api_name":getTokenData.api_name
                        }
                    else:
                      raise serializers.ValidationError({"client_error":"not_found_api","api_issue":False})
                else:
                       
                       raise serializers.ValidationError({"api_issue":"not_found_api","client_error":False})


