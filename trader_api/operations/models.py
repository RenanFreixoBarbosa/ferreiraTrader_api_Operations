from django.db import models
from django.conf import settings

# Create your models here.

class Operation(models.Model):
    RESULT_CHOICES = [
        ('lost', 'Lost'),
        ('win', 'Win'),
        ('draw', 'Draw'),
    ]

    daily_result_id = models.ForeignKey('daily_result.DailyResult', on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    payout = models.DecimalField(max_digits=10, decimal_places=2)
    name =  models.CharField(max_length=100)
    profit_operation = models.DecimalField(max_digits=10, decimal_places=2)

    @classmethod
    def created_operations_by_daily_result(cls,daily_result,operations_list):
        for operation in operations_list:
            cls.objects.create(
                daily_result=daily_result,
                user=operation.get('user'),
                amount=operation.get('amount'),
                date=operation.get('date'),
                result=operation.get('result'),
                payout=operation.get('payout'),
                name=operation.get('name'),
                profit_operation=operation.get('profit_operation')
            )
        return "All operation as created"
    
    @classmethod
    def calc_operations_graphs(cls, daily_result_id):
        operations = cls.objects.filter(daily_result_id=daily_result_id)
        
        qtd_wins, qtd_lost,qtd_draw,arrecadado = 0, 0, 0,0
        
        qtd_op = operations.count()  # Melhor usar count() do que len() em um QuerySet
        for operation in operations:
            if operation.result == "win":
                qtd_wins += 1
                arrecadado += operation.amount
            elif operation.result == "lost":  # Use `elif` para melhorar a eficiência
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
            'percent_arrecadado': percent_arrecadado
        }
    
    @classmethod
    def get_operations_by_daily_result(cls,daily_result_id):
        operations = cls.objects.filter(daily_result_id=daily_result_id)
        return operations