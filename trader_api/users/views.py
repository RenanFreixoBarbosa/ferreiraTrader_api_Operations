from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Importa para utilizar códigos de status HTTP
from rest_framework.request import Request  # Importa para o tipo do request
from .serilalizers import UserSerializer
from .auth_group import UserGroup

class UserCreateView(APIView):
    permission_classes = []
    def post(self, request):
        user_data = request.data
        try:
            user = UserGroup.create_user_and_add_to_group(user_data['username'],user_data['password'],user['email'],user_data["type"])
        except BaseException as e :
            return Response({'message':e})
        return Response({'id': user.id, 'username': user.username, 'type': user.type}, status=status.HTTP_201_CREATED)
