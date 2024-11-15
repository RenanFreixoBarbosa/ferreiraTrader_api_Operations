from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from . import views

urlpatterns=[
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('suporte-login/',views.SuportLogin.as_view(),name='login_suport_app'),
    path('get-user/',views.GetUserView.as_view(),name='retrieve_update_user'),
]
