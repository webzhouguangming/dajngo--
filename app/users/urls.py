
from .views import *

from django.urls import path
from .views import home_view, FoodListView, FoodDetailView, signup_view, login_view, logout_view

urlpatterns = [
    path('', home_view, name='home'),
    path('user_center/', UserProfileView.as_view(), name='user_center'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('list1/', FoodListView.as_view(), name='list'),
    path('detail1/<int:pk>/', FoodDetailView.as_view(), name='detail'),
]

