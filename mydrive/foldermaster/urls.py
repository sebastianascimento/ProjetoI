from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import user_passes_test


app_name = 'foldermaster'

urlpatterns = [
    path('', views.index, name='index'),
    path('foldermanagement/',views.foldermanagement, name='foldermanagement'),
    path('foldermanagement/<int:folder_id>/', views.foldermanagement, name='foldermanagement_with_folder'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('folder/<int:folder_id>/', views.folder_view, name='folder_view'),
    path('folder/create/', views.create_folder, name='create_folder_root'),
    path('folder/create/<int:folder_id>/', views.create_folder, name='create_subfolder'),
    path('upload/', views.upload_file, name='upload_file_root'),
    path('upload/<int:folder_id>/', views.upload_file, name='upload_file_with_folder'),
    path('upload-folder/', views.upload_folder, name='upload_folder'),
    path('upload-folder/<int:folder_id>/', views.upload_folder, name='upload_folder_with_parent'),
    path('delete-folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
