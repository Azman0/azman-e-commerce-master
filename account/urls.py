from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('myaccount', views.myaccount, name='myaccount'),
    path('myorders', views.myorders, name='myorders'),
    path('orderdetails/<cart_no>', views.orderdetails, name='orderdetails'),
    path('logout', views.logout, name='logout'),
    path('confirmorder', views.confirmorder, name='confirmorder'),
]