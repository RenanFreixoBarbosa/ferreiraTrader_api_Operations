from django.db import models
from django.conf import settings

# Create your models here.
class Token_Pass(models.Model):
    token = models.CharField(max_length=5000,null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    consum = models.BooleanField(default=False)