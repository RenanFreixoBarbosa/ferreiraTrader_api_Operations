from services.database_service import PostgresServices
from .models import Operation

class OperationService(PostgresServices):
    def __init__(self):
        super().__init__(Operation)
    
    def calc_operation_result_day(self,operation_list):
        qtd_wins, qtd_lost,qtd_draw,arrecadado = 0, 0, 0,0
        qtd_op = len(operation_list)  # Melhor usar count() do que len() em um QuerySet
        for operation in operation_list:
            if operation['result'] == "win":
                qtd_wins += 1
                arrecadado += float(operation['price'])
            elif operation['result'] == "lost":  # Use `elif` para melhorar a eficiência
                qtd_lost += 1
            else:
                qtd_draw +=1
        
        # Verificação para evitar divisão por zero
        percent_arrecadado = (round((qtd_wins / qtd_op) * 100, 2) if qtd_op > 0 else 0)
        
        return {
            'total_operations': qtd_op,
            'total_wins': qtd_wins,
            'total_lost': qtd_lost,
            "total_draw" : qtd_draw,
            'total_arrecadado': arrecadado,
            'percent_arrecadado': percent_arrecadado,
        }
    