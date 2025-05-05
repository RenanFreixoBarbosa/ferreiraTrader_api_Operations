from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Importa para utilizar códigos de status HTTP
from rest_framework.request import Request  # Importa para o tipo do request
from .models import Subscription
from .serializers import SubscriptionSerializer
from .services import SubscriptionService
from services.google_services import GooglePlayServices

class ListAllSubscription(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        subscriptions = list(Subscription.objects.all())
        serializer = SubscriptionSerializer(subscriptions, many=True) 
        return Response({"message": "Dados recebidos com sucesso!","data":serializer.data}, status=status.HTTP_200_OK)
    

class CreateSubscription(APIView):
    permission_classes = [IsAuthenticated]
    service = SubscriptionService()
    def post(self, request):
        data = self.service.create_subscription(request.data)
        return Response({"message": "Dados recebidos com sucesso!", "data": data}, status=status.HTTP_200_OK)


class GetGoogleToken(APIView):
    # permission_classes = [IsAuthenticated]
    service = SubscriptionService()
    def post(self, request):
        package_name = "com.gestao.binarias"
        g_service = GooglePlayServices(package_name=package_name,product_id="plano_anual_gestao_alpha")
        token = g_service.get_credentials()
        return Response({"data":token})

        

