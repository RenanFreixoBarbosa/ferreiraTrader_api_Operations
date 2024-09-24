from rest_framework import serializers
from .models import Operation

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['amount', 'date', 'result', 'payout', 'name', 'profit_operation', 'daily_result_id','user']
    def create(self, validated_data):
        daily_result = validated_data['daily_result_id']
        validated_data['daily_result_id'] = daily_result
        return super().create(validated_data)
