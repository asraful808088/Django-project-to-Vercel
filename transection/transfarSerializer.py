from rest_framework import serializers 
from .models import UserAccountInfo,PaymentAddress,AutoPay
from login_create.models import CustomUser
from django.contrib.auth.hashers import check_password
from bank.utility.hashing import encrypt,decrypt
import re
import json
from django.conf import settings
class TransfarSysSeaializer(serializers.Serializer):
    address = serializers.CharField(max_length=555)
    amount = serializers.DecimalField(max_digits=150, decimal_places=0) 
    pin = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    send_email = serializers.CharField(max_length=255)
    send_username = serializers.CharField(max_length=255)
    send_id = serializers.CharField(max_length=255)

    def validate(self,data):
        errors=None
        try:
            address = data.get('address')
            paymentData =  PaymentAddress.objects.get(token=address)
            try:
                
                processAddress = re.sub(r"^b'(.*)'$", r'\1', data.get("address")) 
                tokenInfo = json.loads(decrypt(processAddress,settings.SECRET_KEY))
                CustomUser.objects.get(id=paymentData.author_id,email=tokenInfo["email"],username=tokenInfo["username"])
                send_user = CustomUser.objects.get(id=data.get("send_id"),email=data.get("send_email"),username=data.get("send_username"))
                if send_user.username == tokenInfo["username"] and send_user.email == tokenInfo["email"]:
                     errors = {"address":"this address not invalid "}
                     raise serializers.ValidationError({"address":"this address not invalid "}) 
                userPass = check_password(data.get('password'),send_user.password)
                if userPass:
                    try:
                        getuser = UserAccountInfo.objects.get(user=send_user.id)
                  
                        if check_password(data.get('pin'),getuser.account_pin):
                                      vat_rate = 0
                                      if getuser.account_type == 'Personal':
                                          if float(getuser.amount)<=1000:
                                              vat_rate = .05
                                          elif float(getuser.amount)<=5000:
                                               vat_rate = .03
                                          else:
                                                vat_rate = .02
                                      if float(getuser.amount)>float( float(data.get("amount")) + float(data.get("amount"))*vat_rate):
                                             
                                              new_bal_amount = str(float(getuser.amount)-(float(data.get("amount") )+ float(data.get("amount"))*vat_rate))
                                              UserAccountInfo.objects.filter(user=send_user.id).update(
                                                      amount=new_bal_amount,
                                                  )
                                              oposite = UserAccountInfo.objects.get(user=tokenInfo["id"])
                                              UserAccountInfo.objects.filter(user=tokenInfo["id"]).update(
                                                      amount=str( float(oposite.amount) + (float(data.get("amount")))),
                                                  )
                                              
                                              try:
                                                  listOfToken =  AutoPay.objects.all()
                                                  listOfAutopay = []
                                                  for item  in listOfToken:
                                                      if item.author_id==int(tokenInfo["id"]):
                                                          listOfAutopay.append(item)
                                                  listOfAutopay = sorted(listOfAutopay, key=lambda x: x.lvl_order, reverse=True)
                                                  revUser = UserAccountInfo.objects.get(user=tokenInfo["id"])
                                                  revAmo = float(revUser.amount)
                                                  for item in listOfAutopay:
                                                      autoTokenInfo = json.loads(decrypt(re.sub(r"^b'(.*)'$", r'\1', item.token),settings.SECRET_KEY))
                                                      if revAmo>float(autoTokenInfo["amount"]) + float(autoTokenInfo["amount"]) * vat_rate:
                                                          vat_rate = 0
                                                          if revUser.account_type == 'Personal':
                                                              if float(autoTokenInfo["amount"])<=1000:
                                                                  vat_rate = .05
                                                              elif float(autoTokenInfo["amount"])<=5000:
                                                                   vat_rate = .03
                                                              else:
                                                                   vat_rate = .02
                                                          UserAccountInfo.objects.filter(user=revUser.user).update(amount=str(revAmo-float(autoTokenInfo["amount"]) + float(autoTokenInfo["amount"]) * vat_rate))
                                                          new_rev_acc = UserAccountInfo.objects.get(user=autoTokenInfo["id"])
                                                          UserAccountInfo.objects.filter(user=autoTokenInfo["id"]).update(amount=str( float(  new_rev_acc.amount)+float(autoTokenInfo["amount"])))
                                                          auto_pay = AutoPay.objects.get(token=item.token)
                                                          auto_pay.delete()
                                                          
                                                      else:
                                                          break
                                                      pass
          
                                              except Exception as a:
                                                  pass
                                              # another task will be bank profit
          
          
                                              # auto pay
                                              return {"success":True,"new_bal":new_bal_amount}
                                      else:
                                         if  errors == None:
                                          errors ={"amount":"Your account does not have enough balance to complete this transaction"}
                                         raise serializers.ValidationError({"amount":"Your account does not have enough balance to complete this transaction"}) 
                        else:
                             
                          if  errors == None:
                            errors = {"pin":"this pin not invalid "}
                          raise serializers.ValidationError({"pin":"this pin not invalid "}) 
                    except:
                        if  errors == None:
                            errors = {"pin":"this pin not invalid "}
                        raise serializers.ValidationError({"pin":"this pin not invalid "})  
                    
                else:
                    if  errors == None:
                     errors = {"password":"you password invalid"}
                    raise serializers.ValidationError({"password":"this address not invalid "})  
            except Exception as a:
                if  errors == None:
                  errors = {"address":"this address not invalid "}
                raise serializers.ValidationError({"address":"this address not invalid "}) 

        except Exception as a:
            
             if  errors == None: 
                errors = {"address":"this address not invalid "}
             raise serializers.ValidationError(errors) 