from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Importa para utilizar códigos de status HTTP
from rest_framework.request import Request  # Importa para o tipo do request
from .serializers import DailyResultSerializer
from .models import DailyResult
from django.utils.dateparse import parse_date
from operations.models import Operation
from operations.serializers import OperationSerializer
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
        qtd_op_wins,qtd_op_lost,qtd_op_draw,total_op,value_total = 0,0,0,0,0
        for result in daily_results:
            serializer = DailyResultSerializer(result)
            data_serialize = serializer.data
            operation_details = Operation.calc_operations_graphs(data_serialize.get("id"))

            qtd_op_wins += operation_details.get("total_wins")
            qtd_op_draw += operation_details.get("total_draw")
            qtd_op_lost += operation_details.get("total_lost")
            total_op += operation_details.get("total_operations")
            value_total += round(float(data_serialize.get("daily_result")),2)
            operations = Operation.get_operations_by_daily_result(data_serialize.get("id"))
            operations_serialized = OperationSerializer(operations,many=True)
            data_result={
                "id" : data_serialize.get("id"),
                "date" : data_serialize.get("date"),
                "value": data_serialize.get("daily_result"),
                "operations":operations_serialized.data
            }
            
            data_serialized.append(data_result)
        percent_wins_period = (round((qtd_op_wins / total_op) * 100, 2) if total_op > 0 else 0)
        graph_dict = {
            "qtd_operations_period": total_op,
            "total_value_periood": value_total,
            "total_wins_period":qtd_op_wins,
            "total_lost_period":qtd_op_lost,
            "total_draw_period":qtd_op_draw,
            "percent_wins_period":percent_wins_period,
            "daily_result" : data_serialized
        }
        return Response(graph_dict,status=status.HTTP_200_OK)