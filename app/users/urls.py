
from .views import *

from django.urls import path
from .views import home_view, FoodListView, FoodDetailView, signup_view, login_view, logout_view

urlpatterns = [
    path('', home_view, name='home'),
    path('user_center/', UserProfileView.as_view(), name='user_center'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('login_test/', login_view2, name='login_test'),
    path('register_test/', signup_view2, name='register_test'),
    path('forget_password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('reset_password/', ResetPassword.as_view(), name='reset_password'),
    path('logout/', logout_view, name='logout'),
    path('list1/', FoodListView.as_view(), name='list'),
    path('detail1/<int:pk>/', FoodDetailView.as_view(), name='detail'),
    path('send_code/', send_code, name='send_code')
]

