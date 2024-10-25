from rest_framework.views import APIView, Request, Response, status
""" Authentications' DRF and/or JWT """
from rest_framework.permissions import DjangoModelPermissions

class GenericAPIView(APIView):
    permission_classes = [DjangoModelPermissions]
    def get(self, request, *args, **kwargs) -> Response:
        user = request.user  # Corrigido para usar request.user
        data = self.service.read(user=user, **kwargs)  # Passando o usuário como argumento
        return Response({'message': "Dado encontrado com sucesso", 'data': data})


    def patch(self, request: Request, *_,**kwargs) -> Response:
        data = self.service.update(request.data,**kwargs)
        return Response({"message": "Dado atualizado com Sucesso.", "data": data})

    def delete(self, request: Request, *_,**kwargs) -> Response:
        self.service.delete(**kwargs)
        return Response({"message": "Dado deletado com Sucesso", "data": []})
    
    def post(self, request: Request) -> Response:
        user = request.user
        data = self.service.create(user,request.data)
        return Response({"message": "Dado cadastrado com sucesso.", "data": data}, status=status.HTTP_201_CREATED)
