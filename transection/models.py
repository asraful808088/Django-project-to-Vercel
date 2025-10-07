from django.db import models
from login_create.models import CustomUser



class UserAccountInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='account_info')
    account_type = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    account_pin = models.CharField(max_length=255,null=True)
    account_lvl = models.DecimalField(max_digits=20, decimal_places=10) 
    create_time = models.DateField(auto_now_add=True) 













class PaymantGateWay(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='payment_gateway')
    api_name = models.CharField(max_length=255,unique=True)
    api_key = models.CharField(max_length=255,unique=True)
    domain =  models.CharField(max_length=255,unique=True)
    create_time = models.DateField(auto_now_add=True) 








class History(models.Model):
    name = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    reference = models.CharField(max_length=255)
    account_type = models.CharField(max_length=255)
    timestamp = models.DecimalField(max_digits=20, decimal_places=10) #  # decimal_places=0
    create_time = models.DateField(auto_now_add=True) 
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    




class TransferTempToken(models.Model):
    token = models.CharField(max_length=555,unique=True)
    token_user = models.CharField(max_length=255)
    limite  = models.DecimalField(max_digits=150, decimal_places=0)
    access = models.BooleanField()
    exp_date = models.DecimalField(max_digits=150, decimal_places=0) 
    used = models.DecimalField(max_digits=150, decimal_places=0) 
    exp_date_used = models.DecimalField(max_digits=150, decimal_places=0) 
    api_name = models.CharField(max_length=255)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    create_timespan = models.DecimalField(max_digits=150, decimal_places=0)
    create_time = models.DateField(auto_now_add=True) 
    



class AutoPay(models.Model):
    token = models.CharField(max_length=555)
    amount = models.DecimalField(max_digits=150, decimal_places=0) 
    lvl_order = models.IntegerField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    create_time = models.DateField(auto_now_add=True) 


class PaymentAddress(models.Model):
    token = models.CharField(max_length=555,unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    create_time = models.DateField(auto_now_add=True) 


class CardRequestBoard(models.Model):
    CARD_TYPES = [
        ( 'request_to_cradit','CRADIT-CARD REQUEST'),
        ( 'request_to_ACCEPT','CRADIT-CARD ACCEPT'),
        ( 'request_DEINE','CRADIT-CARD DEINE'),
    ]
    stage = models.CharField(choices=CARD_TYPES)
    card_lvl = models.CharField(max_length=555)
    card_stap_type = models.CharField(max_length=555)
    card_num = models.CharField(max_length=555)
    cvv = models.CharField(max_length=555)
    exp_date = models.CharField(max_length=555)
    card_type = models.CharField(max_length=555)
    used_value = models.IntegerField()
    total_aspect_value = models.IntegerField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    create_time = models.DateField(auto_now_add=True) 
