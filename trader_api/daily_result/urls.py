from django.urls import path 
from .views import CreateDailyResultView

urlpatterns = [
    path('create-daily-result/', CreateDailyResultView.as_view(), name='create-daily-result'),
]