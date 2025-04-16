"""
URL configuration for phishlearn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main.views import login_view
from core.views import login_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login_dashboard/', login_dashboard, name='login_dashboard'),
    path('accounts/login/', login_view, name='login_view'),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls')),
    path('', include('main.urls'))
]

admin.site.site_header = "PhishLearn Admin"  
admin.site.site_title = "PhishLearn Admin Portal"  
admin.site.index_title = "Welcome, PhishLearn Administrator!"  