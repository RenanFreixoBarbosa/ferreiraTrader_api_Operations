from django.db import models
from django.conf import settings

# Create your models here.
class Subscription(models.Model):
    PAY_SERVICES_CHOICES = [
        ('guru', 'Guru'),
        ('google_pay', 'GooglePay'),
        ('apple_pay', 'ApplePay'),
    ]
      
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store = models.CharField(max_length=20,choices=PAY_SERVICES_CHOICES,default='guru')
    valid = models.DateField()
    subscription_key = models.CharField(blank=False,max_length=255)
    status_subscription = models.BooleanField(default=True)