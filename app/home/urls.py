
from django.urls import path, include, re_path
from .views import *

urlpatterns = [

    re_path('^$', Index.as_view(), name='home'),
    re_path('^test/$', Test.as_view(), name='test')

]