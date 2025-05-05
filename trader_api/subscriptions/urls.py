from django.urls import path
from .views import ListAllSubscription,CreateSubscription,GetGoogleToken

urlpatterns = [
    path('subscriptions/', ListAllSubscription.as_view(), name='subscription-list'),
    path('subscription/', CreateSubscription.as_view(), name='subscription-create'),
    path('get-token/', GetGoogleToken.as_view(), name='get-google-token'),
]