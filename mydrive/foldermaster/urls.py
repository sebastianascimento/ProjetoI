from django.urls import path
from . import views

app_name = 'foldermaster'

urlpatterns = [
    path('', views.index, name='index'),
    path('foldermanagement/', views.foldermanagement, name='foldermanagement'),
    path('foldermanagement/<int:folder_id>/', views.foldermanagement, name='foldermanagement'), 
    path('download/<int:file_id>/', views.download_file, name='download_file'),
]
