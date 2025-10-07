

from rest_framework import serializers

class PaymentTokenSerializer(serializers.Serializer):
    id = serializers.DecimalField(max_digits=150, decimal_places=0, required=False)
    token = serializers.CharField(max_length=255, required=False)
    token_user = serializers.CharField(max_length=255, required=False)
    limite = serializers.DecimalField(max_digits=150, decimal_places=0, required=False)
    access = serializers.BooleanField(required=False)
    exp_date = serializers.DecimalField(max_digits=150, decimal_places=0, required=False)
    used = serializers.DecimalField(max_digits=150, decimal_places=0, required=False)
    exp_date_used = serializers.DecimalField(max_digits=150, decimal_places=0, required=False)
    api_name = serializers.CharField(max_length=255, required=False)
    create_timespan = serializers.DecimalField(max_digits=150, decimal_places=0, required=False)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        setattr(instance,"used",0)
        instance.save()
        return instance
