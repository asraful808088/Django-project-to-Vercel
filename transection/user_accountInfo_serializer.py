from rest_framework import serializers
from .models import UserAccountInfo
class UserAccountInfoSerializer(serializers.Serializer):
    account_type = serializers.CharField(max_length=255)
    amount = serializers.CharField(max_length=255)
    account_lvl = serializers.DecimalField(max_digits=20, decimal_places=10) #  # decimal_places=0
    create_time = serializers.DateField() 




class GetAccountInfoSerializer(serializers.Serializer):
    user_id = serializers.DecimalField(max_digits=120, decimal_places=0)
    def validate(self, data):
       
        try:
            result  = UserAccountInfo.objects.get(user_id=data.get("user_id"))
            password = False
            if not result.account_pin=='unset':
                password = True
            return {
                
                "account_type":result.account_type,
                "amount":result.amount,
                "account_lvl":result.account_lvl,
                "secure":password
             }
        except Exception as a :
           
            raise serializers.ValidationError({"token":"invalid token"})  

      
        
      