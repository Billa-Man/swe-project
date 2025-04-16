from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('connection/', views.connection_check, name='connection_check'),


]
