from rest_framework import serializers
from .models import PaymantGateWay,TransferTempToken
from login_create.models import CustomUser
from bank.utility.hashing import decrypt,encrypt
from django.conf import settings
import  time
import uuid
import json
from datetime import datetime

class PaymentTokenGenerateSerializer(serializers.Serializer):
        api_name = serializers.CharField(max_length=255)
        client_email = serializers.CharField(max_length=255)
        api_key = serializers.CharField(max_length=255)
        def validate(self, attrs):
                try:
                      getTokenData = PaymantGateWay.objects.get(api_name=attrs.get("api_name"))
                except:
                      raise serializers.ValidationError({"api_issue":"not_found_api","client_error":False})
                
                if getTokenData.api_name == attrs.get("api_name") and getTokenData.api_key== attrs.get("api_key"):
                    
                    # try:
                    #      client = CustomUser.objects.get(email=attrs.get("client_email"))
                    # except:
                    #    raise serializers.ValidationError({"client_error":"not_found_client","api_issue":False})
                    # if client.email == attrs.get("client_email"):
                        return {
                              "api_key":getTokenData.api_key,
                              "email":attrs.get("client_email"),
                              "api_name":getTokenData.api_name
                        }
                   
                else:
                       
                       raise serializers.ValidationError({"api_issue":"not_found_api","client_error":False})





class AccountPaymentTokenGeneratorSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=555)
    exp_date = serializers.DecimalField(max_digits=190, decimal_places=0)
    limite = serializers.CharField(max_length=555)
    email = serializers.EmailField(max_length=555)

    def validate(self, data):
      
        if not data.get('token'):
            raise serializers.ValidationError({"token":"Token is required."})
        if not data.get('exp_date'):
            raise serializers.ValidationError({"exp_date":"Expiration date is required."})
        if not data.get('limite'):
            raise serializers.ValidationError({"limite":"Limite is required."})
        if not data.get('email'):
            raise serializers.ValidationError({"email":"email is required."})
       
        try:
            token = decrypt(data.get('token'),settings.SECRET_KEY)
            token = json.loads(token)
            try:    
                  PaymantGateWay.objects.get(api_name=token["api_name"])
                  
                  try:  
                        
                        user = CustomUser.objects.get(email=data.get('email'))

                        current_timestamp = int(datetime.now().timestamp() * 1000)
                        makeToken = json.dumps({    
                             "client_email":token["email"],
                             "api_name":token["api_name"],
                             "q_account_email":data.get('email'),
                             "exp_date":  str(data.get('exp_date')),
                             "limite":data.get('limite'),
                             "create_time":current_timestamp
                        })
                        
                        create_token = encrypt(makeToken,settings.SECRET_KEY)
                        
                        result  = TransferTempToken(
                             token = create_token,
                             token_user = token["email"],
                             limite = data.get('limite'),
                             access = True,
                             exp_date = data.get('exp_date'),
                             used = 0,
                             exp_date_used =0,
                             api_name = token["api_name"],
                             author_id = user.id, 
                             create_timespan = current_timestamp
                        )
                        result.save()
                        return {
                             "info":TransferTempToken.objects.get(token=create_token),
                             "token":None
                        }
                  except  Exception as a:
                      
                       
                       raise serializers.ValidationError({"token":"Client not found !!"})  
            except Exception as a:
           
              
              raise serializers.ValidationError({"token":"Api not found !!"})  
        except Exception as a:
              raise serializers.ValidationError({"token":"invalid token"})  
        

        raise serializers.ValidationError({"token":"invalid token"})  

        


