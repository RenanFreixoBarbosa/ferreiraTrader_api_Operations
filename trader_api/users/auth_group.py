from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

class UserGroup:
    @staticmethod
    def create_user_and_add_to_group(username, password,email,group_name='student'):
        User = get_user_model()
        
        # Mapeamento de grupos (ou você pode buscar os grupos diretamente)
        group_map = {'student': 1, 'team': 2, 'admin': 3}

        try:
            # Verifica se o grupo existe
            if group_name not in group_map:
                return {"status": "error", "message": f"Grupo '{group_name}' não encontrado."}

            # Inicia a transação atômica
            with transaction.atomic():
                # Cria o usuário
                user = User.objects.create_user(username=username, password=password,email=email)
                # Obtém o grupo
                group = Group.objects.get(id=group_map[group_name])

                # Associa o usuário ao grupo
                user.groups.add(group)

                return user

        except ValidationError as e:
            return {"status": "error", "message": f"Erro de validação: {str(e)}"}
        except Group.DoesNotExist:
            return {"status": "error", "message": f"Grupo '{group_name}' não encontrado."}
        except Exception as e:
            return {"status": "error", "message": f"Ocorreu um erro inesperado: {str(e)}"}

