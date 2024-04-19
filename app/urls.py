from django.urls import path

from app.apps import ApplicationConfig
from app.views import PublicationCreateView, PublicationListView, PublicationDetailView, PublicationUpdateView, \
    PublicationDeleteView, SubscriptionCreateView

app_name = ApplicationConfig.name

urlpatterns = [
    path('', PublicationListView.as_view(), name='index'),
    path('create/', PublicationCreateView.as_view(), name='create'),
    path('<slug:slug>/', PublicationDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', PublicationUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', PublicationDeleteView.as_view(), name='delete'),
    path('subs/add/', SubscriptionCreateView.as_view(), name='subs_add')
]