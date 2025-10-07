from rest_framework import serializers

class HistorySerializer(serializers.Serializer):
      name = serializers.CharField(max_length=255)
      sender = serializers.CharField(max_length=255)
      receiver = serializers.CharField(max_length=255)
      amount = serializers.CharField(max_length=255)
      reference = serializers.CharField(max_length=255)
      account_type = serializers.CharField(max_length=255)
      timestamp = serializers.DecimalField(max_digits=20, decimal_places=10) #  # decimal_places=0
      create_time = serializers.DateField() 