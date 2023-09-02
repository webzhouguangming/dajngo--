
from .views import *

from django.urls import path
from .views import home_view, signup_view, login_view, logout_view

urlpatterns = [
    path('', home_view, name='home'),
    path('user-center/', user_center_view, name='user_center'),
    path('signup/', signup_view2, name='signup'),
    path('login/', login_view2, name='login'),
    # path('login_test/', login_view2, name='login_test'),
    # path('register_test/', signup_view2, name='register_test'),
    path('forget_password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('reset_password/', ResetPassword.as_view(), name='reset_password'),
    path('logout/', logout_view, name='logout'),
    path('send_code/', send_code, name='send_code')
]

