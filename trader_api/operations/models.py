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
            