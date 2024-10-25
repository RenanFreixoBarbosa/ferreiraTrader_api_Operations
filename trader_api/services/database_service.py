from .serializer_service import SerializerService
class PostgresServices(SerializerService):
        def __init__(self,model):
             super().__init__()
             self.model=model
             self.serializer_class = self.get_serializer(self.model)
             
        def read(self,**kwargs):
            data = self.model.objects.filter(**kwargs) if kwargs else self.model.objects.all()
            serializer =self.serializer_class(data,many=True)
            # serializer.is_valid(raise_exception=True)
            return serializer.data
        
        def create(self,data):
              serializer =self.serializer_class(data=data)
              serializer.is_valid(raise_exception=True)
              serializer.save()
              return serializer.data
        
        def delete(self,**kwargs): 
            self.model.objects.filter(**kwargs).delete()
            return {'detail':f"deletado elementos"}
        
        def update(self,data,id):
            instance = self.model.objects.get(id=id)
            serializer = self.serializer_class(instance, data=data, partial=True)
            if serializer.is_valid():
                instance = serializer.save()
                return self.serializer_class(instance).data
            else:
                return serializer.errors 