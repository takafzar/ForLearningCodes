# familyloanclub/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.custom_login_view, name='login'),
    path('request-access/', views.request_access_view, name='request_access'),
    path('verify-access-code/', views.verify_access_code_view,
         name='verify_access_code'),
    path('complete-profile/', views.complete_profile_view, name='complete_profile'),
    path('manage-access', views.manage_access_requests,
         name='manage_access_requests'),
    path('admin-create-user/', views.admin_create_user_view,
         name='admin_create_user'),
]
