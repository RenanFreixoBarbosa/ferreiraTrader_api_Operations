from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('trader', 'Trader'),
        ('viewer', 'Viewer'),
        ('comum','comum')
    )
    type = models.CharField(max_length=10, choices=USER_TYPES, default='comum')
