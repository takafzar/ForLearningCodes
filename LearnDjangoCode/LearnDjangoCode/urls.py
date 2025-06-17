"""
URL configuration for LearnDjangoCode project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# LearnDjangoCode/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from familyloanclub import views as club_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('familyloanclub.urls')),
    path('logout/', club_views.custom_logout_view, name='logout'),
    path('profile/', club_views.profile_view, name='profile'),
    # اضافه کردن مسیر
]
