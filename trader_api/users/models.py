from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('team','Team')
    )
    type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    
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