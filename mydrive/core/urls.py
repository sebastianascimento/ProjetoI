from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib import admin

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('admin/', admin.site.urls), 
    path('logout/', views.logout_view, name='logout'),

    path('reset_password/', views.reset_password_request, name='reset_password_request'),
    path('reset_password_confirm/<str:username>/', views.reset_password_confirm, name='reset_password_confirm'),
]
