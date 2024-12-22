from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta

def default_expiration():
    return now() + timedelta(days=10)

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('team','Team')
    )
    type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    created_at = models.DateTimeField(auto_now_add=True)  # Define a data automaticamente na criação
    expires_at = models.DateTimeField(default= default_expiration)
    id_guru = models.CharField(max_length=100)
    full_name = models.CharField(max_length=150,blank=True)
    
    @classmethod
    def change_password(cls,user_id,new_password):
        user = cls.objects.get(id=user_id)
        # Altera a senha de forma segura
        user.set_password(new_password)
        # Salva o usuário após atualizar a senha
        user.save()
        return "senha atualizada"
    
    def create_user(cls,username,email,type):
        cls.username = username
        cls.email = email
        cls.type=type
        cls.save()
        return "Usuario cadastrado"
