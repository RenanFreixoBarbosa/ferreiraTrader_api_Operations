from rest_framework import serializers

class SerializerService():
    class Meta:
        model = None
    
    @classmethod
    def get_serializer(cls,model):
        class GenericSerializer(serializers.ModelSerializer):
            if model:
                cls.Meta.model = model
            else:
                raise ValueError("Não tem model!!!!!")
            class Meta:
                model = cls.Meta.model
                fields = "__all__"
        return GenericSerializer