from rest_framework import serializers

class  PaymantGateWaySerializer(serializers.Serializer):
         api_name = serializers.CharField(max_length=255)
         api_key = serializers.CharField(max_length=255)
         domain =  serializers.CharField(max_length=255)
         create_time = serializers.DateField() 