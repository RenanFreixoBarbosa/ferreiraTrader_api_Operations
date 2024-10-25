from services.database_service import PostgresServices
from operations.service import OperationService
from django.utils.dateparse import parse_date

from .models import DailyResult
class DailyResultService(PostgresServices):
    def __init__(self):
        super().__init__(DailyResult)
    
    def create(self,user, data):
      operations_list = data.pop('operations')
      daily_result_data = data
      daily_result_data['user'] = user.id
      daily_result = super().create(daily_result_data)

      operation_service = OperationService()
      for operation in operations_list:
          operation["daily_result_id"] = daily_result['id']
          operation["user"] = user.id
          operation_service.create(operation)

      return daily_result
    
    def read(self,user,**kwargs):
      daily_result_list = super().read(user=user.id,date__range=[kwargs['start_date'],kwargs['end_date']])

      total_operations=0
      qtd_total_wins,qtd_total_draws,qtd_total_lost = 0,0,0
      total_arrecadado=0

      daily_result_process=[]
      #get operations per daily results id
      for daily in daily_result_list:
        operation_list = OperationService().read(daily_result_id=daily['id'])   
        daily_dict = {
         'id':daily['id'],
         'value': daily['value'],
         'date' : daily['date'],
         'operations': operation_list
        }
        daily_result_process.append(daily_dict)
        
        operation_results = OperationService().calc_operation_result_day(operation_list)

        total_operations += int(operation_results.get('total_operations'))
        qtd_total_wins += int(operation_results.get('total_wins')) 
        qtd_total_draws += int(operation_results.get('total_lost'))
        qtd_total_lost += int(operation_results.get('total_draw')) 
        total_arrecadado += float(operation_results.get('total_arrecadado'))

      percent_wins_period = (round((qtd_total_wins / total_arrecadado) * 100, 2) if total_operations > 0 else 0)
      
      return {
        "qtd_operations_period": total_operations,
        "total_value_periood": total_arrecadado,
        "total_wins_period": qtd_total_wins,
        "total_lost_period": qtd_total_lost,
        "total_draw_period": qtd_total_draws,
        "percent_wins_period": percent_wins_period,
        "daily_result": daily_result_process
      }