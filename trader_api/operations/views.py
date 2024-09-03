from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Importa para utilizar códigos de status HTTP
from rest_framework.request import Request  # Importa para o tipo do request
from .serializers import OperationSerializer
from .models import Operation

class ListAllOperations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        operations = list(Operation.objects.all())
        serializer = OperationSerializer(operations, many=True) 
        return Response({"message": "Dados recebidos com sucesso!","data":serializer.data}, status=status.HTTP_200_OK)
    
class OperationCreate(APIView):
    def post(self, request):
        serializer = OperationSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OperationByUser(APIView):
    def get(self, request):
        user = request.user
        operations = Operation.objects.filter(user=user)
        serializer = OperationSerializer(operations, many=True)
        return Response({"message": "Dados recebidos com sucesso!", "data": serializer.data}, status=status.HTTP_200_OK)
