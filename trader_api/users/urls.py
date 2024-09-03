from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from . import views

urlpatterns=[
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('register/', views.UserCreateView.as_view(), name='register'),
]
