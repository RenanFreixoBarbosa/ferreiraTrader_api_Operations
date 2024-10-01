from django.db import models
from django.conf import settings

# Create your models here.
class DailyResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    daily_result = models.DecimalField(max_digits=10, decimal_places=2,null=False)
