from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Importa para utilizar códigos de status HTTP
from rest_framework.request import Request  # Importa para o tipo do request
from .serializers import DailyResultSerializer
from .models import DailyResult
from django.utils.dateparse import parse_date
from operations.models import Operation
# Create your views here.


class CreateDailyResultView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request) -> Response:
        serializer = DailyResultSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DailyResultGraphs(APIView):
    def get(self,request,start_date,end_date=None):
        # Converte as strings para objetos de data
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        daily_results = DailyResult.objects.filter(date__range=[start_date, end_date])
        data_serialized= []
        for result in daily_results:
            serializer = DailyResultSerializer(result)
            data_serialize = serializer.data
            operation_details = Operation.calc_operations_graphs(data_serialize.get("id"))
            data_result={
                "id" : data_serialize.get("id"),
                "date" : data_serialize.get("date"),
                "value": data_serialize.get("daily_result")
            }
            
            data_serialized.append(data_result)
        graph_dict = {
            "qtd_operations_period": 0,
            "total_value_daily_periood": 0,
            "total_wins_period":0,
            "total_lost_period":0,
            "percent_wins_period":0,
            "daily_result" : data_serialized
        }
        return Response(graph_dict,status=status.HTTP_200_OK)