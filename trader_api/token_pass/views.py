from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from users.models import User 
from .models import Token_Pass
import os
from .genericPasswordToken import GenericPasswordToken
# Create your views here.

class RequestResetPassword(APIView):
    def post(self,request):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message':"Usuário não existe",'data':[]})
         
        # Gera o token de recuperação de senha
        token = GenericPasswordToken.generate_password_reset_token(user)
        print(os.getenv('EMAIL'))
        # Envia o e-mail com o link para recuperação
        send_mail(
                'Recuperação de Senha',
                f'Cole o token no aplicativo para resetar sua senha: {token}',
                os.getenv('EMAIL'),
                [user.email],
                fail_silently=False,
                )
        return Response({'message':"Email enviado com Sucesso"})

    def patch(self,request):
        new_password = request.data['password']
        token = request.data ['token']
        token_result = GenericPasswordToken.verify_autencity_token(token)
        if token_result['result'] == True:
            User.change_password(token_result['user_id'],new_password)
            return Response({"message":"Senha alterada com Sucesso"})
        else:
            return Response({'message':token_result['message']})
            