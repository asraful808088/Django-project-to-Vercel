from django.db import models
from login_create.models import CustomUser 
class Saving_Account(models.Model):
    name = models.CharField(max_length=255,unique=True)
    init_amount = models.DecimalField(max_digits=20, decimal_places=10) 
    num_of_year =  models.IntegerField()
    rate_rate = models.FloatField()
    current_amount = models.DecimalField(max_digits=20, decimal_places=10) 
    create_time = models.DateField(auto_now_add=True) 
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)