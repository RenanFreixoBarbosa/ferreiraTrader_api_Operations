from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Chamamos o exception handler padrão primeiro para obter a resposta inicial
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        # Personalizando a mensagem para AuthenticationFailed
        return Response(
            {'detail': 'Você não está autorizado a acessar esta parte do sistema.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if isinstance(exc, NotAuthenticated):
        # Personalizando a mensagem para NotAuthenticated
        return Response(
            {'detail': 'Autenticação necessária. Faça o login para continuar.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if isinstance(exc, PermissionDenied):
        # Personalizando a mensagem para PermissionDenied
        return Response(
            {'detail': 'Você não tem permissão para realizar esta ação.'},
            status=status.HTTP_403_FORBIDDEN
        )

    return response
