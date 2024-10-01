from django.urls import path 
from .views import CreateDailyResultView,DailyResultGraphs

urlpatterns = [
    path('create-daily-result/', CreateDailyResultView.as_view(), name='create-daily-result'),
    path('daily-result-graph/<str:start_date>/<str:end_date>/', DailyResultGraphs.as_view(), name='get-daily-result_graph'),
]