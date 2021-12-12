from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Account(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    email=models.CharField(max_length=150, unique=True)
    password=models.CharField(max_length=100)
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=15, unique=True)

#Registration model
class Registration(models.Model):
    VEHCICLE_TYPE = (
        ('T', 'Two Wheeler'),
        ('F', 'Four Wheeler'),
        ('S', 'SUV'),
    )
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField() 
    ranged = models.DecimalField(decimal_places=1,max_digits=3)
    vehicle = models.CharField(max_length=1, choices=VEHCICLE_TYPE)
    payment = models.BooleanField(default=False)