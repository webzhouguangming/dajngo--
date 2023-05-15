
from django.urls import path

from .views import OrderDetailView, Pay

# app_name = 'orders'

urlpatterns = [
    path('pay/', Pay.as_view(), name='pay'),
    path('<str:pk>/', OrderDetailView.as_view(), name='detail'),

]
