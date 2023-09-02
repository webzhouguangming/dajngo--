from django.urls import path, re_path, include
from .views import *
urlpatterns = [

    path('messages/', message_view, name='messages'),
    path('create_message/', create_message_view, name='create_message'),



]