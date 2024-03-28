from django.urls import path

from app.apps import ApplicationConfig
from app.views import index

app_name = ApplicationConfig.name

urlpatterns = [
    path('', index, name='index'),
]