from rest_framework import serializers
from utils.random_num import getRandom16,getcvv
from login_create.models import CustomUser
from .models import CardRequestBoard
from datetime import datetime; 
from dateutil.relativedelta import relativedelta;
class  CardRequestSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    card_lvl = serializers.CharField(max_length=555)
    def validate(self, data):
        
        card_num = getRandom16()
        cvv = getcvv()
        request_stage = "request_to_cradit" 
        card_stap_type = "card_type"
        card_lvl =  data["card_lvl"]
        card_type = "VISA"  ## const 
        formatted_date = (datetime.now() + relativedelta(months=1)).strftime("%d/%m")
        exp_date = formatted_date
        used_value = 0
        total_aspect_value = 100000
        
        return{ "total_aspect_value":total_aspect_value,"used_value":used_value,"exp_date":exp_date,"card_type":card_type,"card_lvl":card_lvl,"card_stap_type":card_stap_type,"stage":request_stage,"cvv":cvv,"card_num":card_num,"author_id": data["email"] }
    def create(self, validated_data):
        try:
             author = CustomUser.objects.get(email=validated_data["author_id"])
             user_with_id = validated_data
             user_with_id["author_id"] = author.id
             CardRequestBoard.objects.create(**user_with_id)
             validated_data["failed_status"] = False
             return validated_data
        except:
            return {"failed_status":True}
        
