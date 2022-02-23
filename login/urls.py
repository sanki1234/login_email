from django.urls import path
from .views import *

urlpatterns=[
    path('',home_page,name="home"),
    path('login/',login_here,name="login"),
    path('register/',register_here,name="register"),
    path('verification/',verification,name="verification"),
    path('success/',success_here,name="success"),
    path('login/forgot/',forgotpass,name="forgot"),
]