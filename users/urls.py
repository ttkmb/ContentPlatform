from django.urls import path

from users.apps import UsersConfig
from users.views import UserRegisterView, UserLoginView, UserProfileView, UserLogoutView, UserVerifyView

app_name = UsersConfig.name

urlpatterns = [
    path('reg/', UserRegisterView.as_view(), name='register'),
    path('log/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify/', UserVerifyView.as_view(), name='verify'),
]