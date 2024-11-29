from .models import User
from .serilalizers import UserSerializer
from django.contrib.auth.models import Group
from .serilalizers import UserSerializer

class UserService():
    
    def insert_user(self,user_data):
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            self.insert_user_auth_group(user)
            return {"id":user.id,"username":user.username,"type":user.type,"email":user.email,'name':user.first_name,'id_guru':user.id_guru}
        
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
        
    def get_users(self):
        users = User.objects.filter().order_by('first_name')
        serialized_users = UserSerializer(users, many=True)
        return serialized_users.data
    
    def set_status_user(self,user_id,status=True):
        user = User.objects.get(pk=user_id)
        if not user.is_active and not status:
            return "Usuário já está inativo."
        elif user.is_active and status:
            return "Usuário já está ativado"
        else:
            user.is_active = False if not status else True
            user.save()
            message = "Usuário inativado com sucesso." if not status else "Usuário ativado com sucesso."
            return message

    def delete_user(self,user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return "usuario deletado com sucesso"
        except User.DoesNotExist:
            return "Usuário não encontrado"
    
    def update_user(self,user_id,data):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return {'message':"Usuário não encontrado.",'data':[]}

        serializer = UserSerializer(user, data=data, partial=True)  # Atualização parcial
        if serializer.is_valid():
            serializer.save()
            return {'message':'Usuario atualizado com sucesso','data':serializer.data}
        else:
            return {'message': serializer.errors, 'data': []}

    def manager_user(self,json_request):
        user_data = json_request.get("subscriber") 
        id_guru = user_data.get("id") 
        try:
            user_exist = User.objects.get(id_guru=id_guru)
            if user_exist.email != user_data['email']:
                user_exist.email = user_data['email']
                user_exist.username=user_data['email']
                user_exist.save()
            function_map = {
                "active": lambda: self.set_status_user(user_exist.id, True),
                "canceled": lambda: self.set_status_user(user_exist.id, False),
                "expired": lambda: self.set_status_user(user_exist.id, False),
                "inactive": lambda: self.set_status_user(user_exist.id, False),
            }

            last_status = json_request.get("last_status").lower()
            if last_status in function_map:
                return function_map[last_status]()
            else:
                return "Tipo de Status não mapeado"

        except User.DoesNotExist:
            user_data = {"username":user_data.get("email"),
                         "email":user_data.get("email"),
                         "password":user_data.get("phone_number"),
                         "id_guru":id_guru,
                         "type":"student"}
            
            created = self.insert_user(user_data)
            return created
        