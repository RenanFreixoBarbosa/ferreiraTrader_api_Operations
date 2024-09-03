from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Importa para utilizar códigos de status HTTP
from rest_framework.request import Request  # Importa para o tipo do request
from .serilalizers import UserSerializer

class ReceiveOperationsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        # Aqui você processa os dados enviados no corpo da requisição
        data = request.data  # Aqui você acessa os dados do corpo da requisição
        # Processar os resultados das operações binárias...
        
        return Response({"message": "Dados recebidos com sucesso!"}, status=status.HTTP_200_OK)


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'id': user.id, 'username': user.username, 'type': user.type}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)