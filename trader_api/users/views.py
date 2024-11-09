from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Importa para utilizar códigos de status HTTP
from rest_framework.request import Request  # Importa para o tipo do request
from .service import UserService

class UserCreateView(APIView):
    def post(self, request):
        user_data = request.data
        user_service = UserService()
        user = user_service.insert_user(user_data)
        return Response(user)