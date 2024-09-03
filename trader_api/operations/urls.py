from django.urls import path
from .views import ListAllOperations,OperationCreate,OperationByUser

urlpatterns = [
    path('operations/', ListAllOperations.as_view(), name='operations-list'),
    path('create-operations/', OperationCreate.as_view(), name='operation-create'),
    path('operations-user/', OperationByUser.as_view(), name='operation-user'),
]