from .models import User
from .serilalizers import UserSerializer
from django.contrib.auth.models import Group

class UserService():
    
    def insert_user(self,user_data):
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            self.insert_user_auth_group(user)
            return {"id":user.id,"username":user.username,"type":user.type,"email":user.email}
        
        # Se o serializer não for válido, retorna os erros
        return {"error": serializer.errors}
    
    def insert_user_auth_group(self,user):
        type_map = {'student':1,'team':2,'admin':3}

        # Verifica se o tipo de usuário é válido
        if user.type not in type_map:
            return {"error": f"Tipo de usuário '{user.type}' não é válido."}
        
        try:
            # Obtém o grupo pelo ID
            group = Group.objects.get(id=type_map[user.type])
            user.groups.add(group)  # Adiciona o usuário ao grupo
            return {"message": f"Usuário {user.username} inserido no grupo {user.type}."}
        except Group.DoesNotExist:
            return {"error": f"Grupo '{user.type}' não encontrado."}


        
