from rest_framework import serializers
from .models import PaymantGateWay, TransferTempToken, UserAccountInfo
from bank.utility.hashing import decrypt
from login_create.models import CustomUser
from django.conf import settings
import re
import json
from datetime import datetime


class APIPaymentServiceSerializer(serializers.Serializer):
    api_name = serializers.CharField(max_length=255, required=True)
    api_key = serializers.CharField(max_length=255, required=True)
    token = serializers.CharField(max_length=755, required=True)
    amount = serializers.DecimalField(max_digits=150, decimal_places=0, required=True)

    def validate(self, data):
        getpaymentInfo = None
        try:
            getpaymentInfo = PaymantGateWay.objects.get(
                api_name=data.get("api_name"), api_key=data.get("api_key")
            )
           
            if getpaymentInfo.api_key and getpaymentInfo.api_name:
                pass
            else:
                raise serializers.ValidationError(
                    {"api_issue": "invalid API", "error_type": "server-side"}
                )
        except Exception:
            raise serializers.ValidationError(
                {"api_issue": "invalid API", "error_type": "server-side"}
            )

        try:
            tempTokenInfo = TransferTempToken.objects.get(token=data.get("token"))
        except Exception as e:
            print(e)
            raise serializers.ValidationError({"token_issue": "Your token is invalid."})

        if not tempTokenInfo.access:
            raise serializers.ValidationError(
                {
                    "access_denied": "Your token is valid but does not have the necessary access permissions"
                }
            )
        current_timestamp = int(datetime.now().timestamp() * 1000)
        if not (tempTokenInfo.create_timespan + tempTokenInfo.exp_date > current_timestamp):
            raise serializers.ValidationError({"date_exp": "token date exp.."})

        if not (tempTokenInfo.limite - tempTokenInfo.used > data.get("amount")):
            raise serializers.ValidationError({"limit_cross": "not available your current amount"})
        
        bank_a = CustomUser.objects.get(email=tempTokenInfo.author)
        userAccountInfo = UserAccountInfo.objects.get(user=bank_a.id)

        if int(userAccountInfo.amount) < data.get("amount"):
            raise serializers.ValidationError({"limit_cross": "not available your current amount"})
        else:
            UserAccountInfo.objects.filter(user=bank_a.id).update(
                amount=f"{int(userAccountInfo.amount) - data.get('amount')}"
            )
            TransferTempToken.objects.filter(token=data.get("token")).update(
                used=tempTokenInfo.used + data.get("amount")
            )

        convertStr = re.sub(r"^b'(.*)'$", r"\1", data.get("token"))
        decodeData = decrypt(convertStr, settings.SECRET_KEY)
        objData = json.loads(decodeData)

        apiServiceHolder = PaymantGateWay.objects.get(api_name=objData["api_name"])
        suserAccountInfo = CustomUser.objects.get(email=apiServiceHolder.user)
        SAccountInfo = UserAccountInfo.objects.get(user=suserAccountInfo.id)

        UserAccountInfo.objects.filter(user=suserAccountInfo.id).update(
            amount=f"{int(SAccountInfo.amount) + data.get('amount')}"
        )
        return {}
