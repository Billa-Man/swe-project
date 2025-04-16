from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('connection/', views.connection_check, name='connection_check'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('change-password/', views.change_password, name='change_password'),
]
