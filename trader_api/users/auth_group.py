from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

class UserGroup:
    @staticmethod
    def insert_user_in_group(username, group_id=1):
        User = get_user_model()
        try:
            # Verifica se o usuário existe
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return f"Usuário com username '{username}' não encontrado."

        try:
            # Verifica se o grupo existe
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return f"Grupo com ID '{group_id}' não encontrado."

        # Associa o usuário ao grupo
        user.groups.add(group)
        return f"Usuário '{username}' inserido no grupo '{group.name}' com sucesso."
