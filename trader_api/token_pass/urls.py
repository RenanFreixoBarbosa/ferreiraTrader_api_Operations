from django.urls import path
from . import views

urlpatterns=[
    path('change-password/', views.RequestResetPassword.as_view(), name='change-password'),
]
