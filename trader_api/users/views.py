from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Importa para utilizar códigos de status HTTP
from rest_framework.request import Request  # Importa para o tipo do request
from .service import UserService
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from core.permissions import IsAdminOrEditorPermission

from .models import User

class UserCreateView(APIView):
    def post(self, request):
        user_data = request.data
        user_service = UserService()
        user = user_service.insert_user(user_data)
        return Response(user)

class GetUserView(APIView):
    permission_classes = [IsAdminOrEditorPermission]

    def get(self,request):
        users = UserService().get_users()
        return Response(users)
    
class SuportLogin(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Verifica se ambos os parâmetros foram enviados
        if not username or not password:
            return Response({"error": "Username e senha são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        # Tenta autenticar o usuário
        user = authenticate(username=username, password=password)

        # Se o usuário não for encontrado ou a senha for errada
        if user is None:
            return Response({"error": "Credenciais inválidas."}, status=status.HTTP_401_UNAUTHORIZED)

        # Verifica o tipo do usuário
        if user.type not in ['team', 'admin']:
            return Response({"error": "Usuário não autorizado."}, status=status.HTTP_403_FORBIDDEN)

        # Gera o Refresh Token (JWT)
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Retorna o JWT (access token)
        return Response({
            "access_token": str(access_token),
            "refresh_token": str(refresh),
        }, status=status.HTTP_200_OK)