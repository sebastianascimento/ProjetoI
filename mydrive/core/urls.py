from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'core'


urlpatterns = [
    path('' , views.index , name='index'),
    path('contact/' , views.contact, name='contact'),
    path('signup/' , views.signup , name='signup'),
    path('login/', views.login_view , name='login'),
    path('yourdrive/', views.yourdrive, name='yourdrive'),
    path('logout/', views.logout_view, name='logout'),
]