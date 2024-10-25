from .models import DailyResult
from .service import DailyResultService
from core.GenericViews import GenericAPIView
from rest_framework.request import Request  # Importa para o tipo do request
# Create your views here.


class CreateDailyResultView(GenericAPIView):
    queryset = DailyResult.objects.all()
    http_method_names=['post']
    service = DailyResultService()
    
class DailyResultGraphs(GenericAPIView):
    queryset = DailyResult.objects.all()
    http_method_names=['get']
    service = DailyResultService()
