import secrets
from django.utils import timezone
from datetime import timedelta
from .models import Token_Pass
from django.contrib.auth import get_user_model


class GenericPasswordToken():
    def generate_password_reset_token(user):
        # Gera um token seguro aleatório
        token = secrets.token_urlsafe(64)  # Tamanho do token pode ser ajustado conforme necessário
    
        # Define a data de expiração para 2 horas a partir de agora
        expires_at = timezone.now() + timedelta(hours=2)
    
        # Cria e salva o token no banco de dados
        Token_Pass.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
    
        return token
    
    def verify_autencity_token(token):
        try:
            # Localiza o token no banco de dados
            token_object = Token_Pass.objects.get(token=token)
        except Token_Pass.DoesNotExist:
            return {'result':False,"message":"Não foi possivel validar o token"}
       
        # Verifica se o token já expirou
        if timezone.now() > token_object.expires_at:
            return {"result":"False","message":"Token expirado."}
        
        if token_object.consum == True:
            return {"result":False,"message":"Este token já foi utilizado anteriormente"}
        
        #updated token
        token_object.consum=True
        token_object.save()
        
        return {'result':True,'user_id':token_object.user_id,"message":"Token Válido"}
    