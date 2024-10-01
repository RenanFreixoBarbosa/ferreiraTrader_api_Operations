from rest_framework import serializers
from .models import DailyResult
from operations.serializers import OperationSerializer

class DailyResultSerializer(serializers.ModelSerializer):
    operations = serializers.ListField(child=serializers.DictField(), write_only=True)
    
    class Meta:
        model = DailyResult
        fields = ['id', 'date', 'daily_result', 'operations']
    
    def create(self, validated_data):
        operations_data = validated_data.pop('operations', [])
        user = self.context['request'].user
        validated_data['user'] = user
        daily_result = DailyResult.objects.create(**validated_data)
        
        # Processar e criar as operações associadas
        for op_data in operations_data:
            op_data['user'] = user.id
            op_data['daily_result_id'] = daily_result.id
            operation_serializer = OperationSerializer(data={**op_data, 'daily_result': daily_result}, context=self.context)
            if operation_serializer.is_valid():
                operation_serializer.save()
            else:
                # Log the errors if needed
                print(operation_serializer.errors)
            
        return daily_result
