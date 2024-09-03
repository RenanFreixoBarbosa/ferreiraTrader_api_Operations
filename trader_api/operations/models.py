from django.db import models
from django.conf import settings
# Create your models here.

class Operation(models.Model):
    RESULT_CHOICES = [
        ('lost', 'Lost'),
        ('win', 'Win'),
        ('draw', 'Draw'),
    ]

    FINAL_RESULT_CHOICES =[
        ('profit','profit'),
        ('prejudice','prejudice'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    payout = models.DecimalField(max_digits=10, decimal_places=2)
    final_result = models.CharField(max_length=10, choices=FINAL_RESULT_CHOICES)