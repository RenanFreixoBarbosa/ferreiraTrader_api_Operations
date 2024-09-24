from django.urls import path
from .views import ListAllOperations,OperationByUser

urlpatterns = [
    path('operations/', ListAllOperations.as_view(), name='operations-list'),
    path('operations-user/', OperationByUser.as_view(), name='operation-user'),
]